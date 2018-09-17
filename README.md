## First-Person Hand Action Benchmark with RGB-D Videos and 3D Hand Pose Annotations
This repository contains instructions on getting the data, code and models of the work` First-Person Hand Action Benchmark with RGB-D Videos and 3D Hand Pose Annotations` presented at CVPR 2018. For more information on the benchmark check out [[1]](#refs).

### Getting the data
TODO

### Dataset structure:
The dataset is organized as the following example:

- File `Video_files/Subject_3/high_five/3/color/color_0013.jpeg`
Consists of frame number 13 of the color stream of the 3rd repetition of 
action class "high five" by subject number 3.

- File `Video_files/Subject_3/high_five/3/depth/depth_0013.png`
Consists of frame number 13 of the depth stream of the 3rd repetition of
 action class "high five" by subject number 3.

- File `Hand_pose_annotation_v1/Subject_3/high_five/3/skeleton.txt`
Contains the hand pose (in world coordinates) for the sequence: repetition 
3 of action class "high five" by subject number 3. 

Note: Check Figure 3 and 4 of the paper to learn about action categories. We used a slight different nomenclature for some actions compared to the paper. These are: "dish soap -> liquid soap"; "read paper -> read letter"; "use spray -> use flash". 
Note: Check ‘Subjects_info’ folder for details on number of sequences, frames, etc. for each subject. 

TODO: 6D object pose

### Hand pose data:
Format of each line of skeleton.txt:
`t x_1 y_1 z_1 x_2 y_2 z_2 ... x_21 y_21 z_21`

where `t` is the frame number and `x_i y_i z_i` are the world coordinates of joint `i` at frame `t`.

Hand joints are organised as follows:
`[Wrist, TMCP, IMCP, MMCP, RMCP, PMCP, TPIP, TDIP, TTIP, IPIP, IDIP, ITIP, MPIP, MDIP, MTIP, RPIP, RDIP, RTIP, PPIP, PDIP, PTIP]`, where ’T’, ’I’, ’M’, ’R’, ’P’ denote ’Thumb’, ’Index’, ’Middle’, ’Ring’, ’Pinky’ fingers.  

### Image data details
* Camera: Intel RealSense SR300.
* Color data: 1920x1080 32bit, jpeg format.
* Depth data: 640x480 16bit, png format.

### Camera parameters:
Image center:
* u0= 315.944855;
* v0= 245.287079;
Focal Lengths:
* fx = 475.065948;
* fy = 475.065857;

TODO: add RGB sensor

### Benchmark tasks 
#### Action recognition
data_split_action_recognition.txt contains the 1:1 split reported on the paper. These are the files you should use for training and testing if you want to compare with the results reported in the paper.

#### Hand pose estimation
TODO

### Terms and conditions
The download and use of the dataset is released for academic research only and it is free to researchers from educational or research institutes for non-commercial purposes. When downloading the dataset you agree to (unless with expressed permission of the authors): not redistribute, modificate, or commercial usage of this dataset in any way or form, either partially or entirely.

If using this dataset, please cite the following paper:

```
@inproceedings{FirstPersonAction_CVPR2018,
  title={First-Person Hand Action Benchmark with RGB-D Videos and 3D Hand Pose Annotations},
  author={Garcia-Hernando, Guillermo and Yuan, Shanxin and Baek, Seungryul and Kim, Tae-Kyun}
  booktitle = {Proceedings of Computer Vision and Pattern Recognition ({CVPR})},
  year = {2018}
}
```

### Acknowledgment
This dataset is part of Imperial College London-Samsung Research project, supported by Samsung Electronics.

### References
<a name="refs"></a>

[1] *First-Person Hand Action Benchmark with RGB-D Videos and 3D Hand Pose Annotations*, Guillermo Garcia-Hernando, Shanxin Yuan, Seungryul Baek and Tae-Kyun Kim, CVPR 2018.
