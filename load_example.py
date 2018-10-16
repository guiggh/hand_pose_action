import argparse
import os
import numpy as np
import trimesh
from matplotlib import pyplot as plt
from PIL import Image


# Loading utilities
def load_objects(obj_root):
    object_names = ['juice_bottle', 'liquid_soap', 'milk', 'salt']
    all_models = {}
    for obj_name in object_names:
        obj_path = os.path.join(obj_root, '{}_model'.format(obj_name),
                                '{}_model.ply'.format(obj_name))
        mesh = trimesh.load(obj_path)
        all_models[obj_name] = {
            'verts': np.array(mesh.vertices),
            'faces': np.array(mesh.faces)
        }
    return all_models


def get_skeleton(sample, skel_root):
    skeleton_path = os.path.join(skel_root, sample['subject'],
                                 sample['action_name'], sample['seq_idx'],
                                 'skeleton.txt')
    print('Loading skeleton from {}'.format(skeleton_path))
    skeleton_vals = np.loadtxt(skeleton_path)
    skeleton = skeleton_vals[:, 1:].reshape(skeleton_vals.shape[0], 21,
                                            -1)[sample['frame_idx']]
    return skeleton


def get_obj_transform(sample, obj_root):
    seq_path = os.path.join(obj_root, sample['subject'], sample['action_name'],
                            sample['seq_idx'], 'object_pose.txt')
    with open(seq_path, 'r') as seq_f:
        raw_lines = seq_f.readlines()
    raw_line = raw_lines[sample['frame_idx']]
    line = raw_line.strip().split(' ')
    trans_matrix = np.array(line[1:]).astype(np.float32)
    trans_matrix = trans_matrix.reshape(4, 4).transpose()
    print('Loading obj transform from {}'.format(seq_path))
    return trans_matrix


# Display utilities
def visualize_joints_2d(ax, joints, joint_idxs=True, links=None, alpha=1):
    """Draw 2d skeleton on matplotlib axis"""
    if links is None:
        links = [(0, 1, 2, 3, 4), (0, 5, 6, 7, 8), (0, 9, 10, 11, 12),
                 (0, 13, 14, 15, 16), (0, 17, 18, 19, 20)]
    # Scatter hand joints on image
    x = joints[:, 0]
    y = joints[:, 1]
    ax.scatter(x, y, 1, 'r')

    # Add idx labels to joints
    for row_idx, row in enumerate(joints):
        if joint_idxs:
            plt.annotate(str(row_idx), (row[0], row[1]))
    _draw2djoints(ax, joints, links, alpha=alpha)


def _draw2djoints(ax, annots, links, alpha=1):
    """Draw segments, one color per link"""
    colors = ['r', 'm', 'b', 'c', 'g']

    for finger_idx, finger_links in enumerate(links):
        for idx in range(len(finger_links) - 1):
            _draw2dseg(
                ax,
                annots,
                finger_links[idx],
                finger_links[idx + 1],
                c=colors[finger_idx],
                alpha=alpha)


def _draw2dseg(ax, annot, idx1, idx2, c='r', alpha=1):
    """Draw segment of given color"""
    ax.plot(
        [annot[idx1, 0], annot[idx2, 0]], [annot[idx1, 1], annot[idx2, 1]],
        c=c,
        alpha=alpha)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True, help='Path to dataset install')
    parser.add_argument('--subject', required=True, default='Subject_1')
    parser.add_argument('--action_name', required=True, default='open_liquid_soap')
    parser.add_argument('--seq_idx', required=True, default='1')
    parser.add_argument('--frame_idx', required=True, default=0, type=int)
    parser.add_argument(
        '--obj', required=True, choices=['liquid_soap', 'juice_bottle', 'milk', 'salt'])
    args = parser.parse_args()
    reorder_idx = np.array([
        0, 1, 6, 7, 8, 2, 9, 10, 11, 3, 12, 13, 14, 4, 15, 16, 17, 5, 18, 19,
        20
    ])

    sample = {
        'subject': args.subject,
        'action_name': args.action_name,
        'seq_idx': args.seq_idx,
        'frame_idx': args.frame_idx,
        'object': args.obj
    }

    print('Loading sample {}'.format(sample))
    cam_extr = np.array(
        [[0.999988496304, -0.00468848412856, 0.000982563360594,
          25.7], [0.00469115935266, 0.999985218048, -0.00273845880292, 1.22],
         [-0.000969709653873, 0.00274303671904, 0.99999576807,
          3.902], [0, 0, 0, 1]])
    cam_intr = np.array([[1395.749023, 0, 935.732544],
                         [0, 1395.749268, 540.681030], [0, 0, 1]])
    skeleton_root = os.path.join(args.root, 'Hand_pose_annotation_v1')
    obj_root = os.path.join(args.root, 'Object_models')
    obj_trans_root = os.path.join(args.root, 'Object_6D_pose_annotation_v1')
    skel = get_skeleton(sample, skeleton_root)[reorder_idx]
    if args.obj is not None:
        # Load object mesh
        object_infos = load_objects(obj_root)

        # Load object transform
        obj_trans = get_obj_transform(sample, obj_trans_root)

        # Get object vertices
        verts = object_infos[sample['object']]['verts'] * 1000

        # Apply transform to object
        hom_verts = np.concatenate(
            [verts, np.ones([verts.shape[0], 1])], axis=1)
        verts_trans = obj_trans.dot(hom_verts.T).T

        # Apply camera extrinsic to objec
        verts_camcoords = cam_extr.dot(
            verts_trans.transpose()).transpose()[:, :3]
        # Project and object skeleton using camera intrinsics
        verts_hom2d = np.array(cam_intr).dot(
            verts_camcoords.transpose()).transpose()
        verts_proj = (verts_hom2d / verts_hom2d[:, 2:])[:, :2]

    # Apply camera extrinsic to hand skeleton
    skel_hom = np.concatenate([skel, np.ones([skel.shape[0], 1])], 1)
    skel_camcoords = cam_extr.dot(
        skel_hom.transpose()).transpose()[:, :3].astype(np.float32)

    skel_hom2d = np.array(cam_intr).dot(skel_camcoords.transpose()).transpose()
    skel_proj = (skel_hom2d / skel_hom2d[:, 2:])[:, :2]

    # Plot everything
    fig = plt.figure()
    # Load image and display
    ax = fig.add_subplot(221)
    img_path = os.path.join(args.root, 'Video_files', sample['subject'],
                            sample['action_name'], sample['seq_idx'], 'color',
                            'color_{:04d}.jpeg'.format(sample['frame_idx']))
    print('Loading image from {}'.format(img_path))
    img = Image.open(img_path)
    ax.imshow(img)
    visualize_joints_2d(ax, skel_proj, joint_idxs=False)
    if args.obj is not None:
        ax.scatter(verts_proj[:, 0], verts_proj[:, 1], alpha=0.01, c='r')
    for proj_idx, (proj_1, proj_2) in enumerate([[0, 1], [1, 2], [0, 2]]):
        ax = fig.add_subplot(2, 2, 2 + proj_idx)
        if proj_idx == 0:
            # Invert y axes to align with image in camera projection
            ax.invert_yaxis()
        ax.set_aspect('equal')
        if args.obj is not None:
            ax.scatter(
                verts_camcoords[:, proj_1], verts_camcoords[:, proj_2], s=1)
        visualize_joints_2d(
            ax,
            np.stack(
                [skel_camcoords[:, proj_1], skel_camcoords[:, proj_2]],
                axis=1),
            joint_idxs=False)
    plt.show()
