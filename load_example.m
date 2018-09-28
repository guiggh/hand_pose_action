clc
clear all
close all

person_id = 'Subject_1';
action_id = 'put_salt';
rep  = '1';
frame_num = 15;

% depth sensor intrinsic parameters
fx_d = 475.065948;
fy_d = 475.065857;
u0_d = 315.944855;
v0_d = 245.287079;

% rgb sensor intrinsic parameters
fx_c = 1395.749023;
fy_c = 1395.749268;
u0_c = 935.732544;
v0_c = 540.681030;

% extrinsic parameters
R = [0.999988496304, -0.00468848412856, 0.000982563360594;
     0.00469115935266, 0.999985218048, -0.00273845880292;
    -0.000969709653873, 0.00274303671904, 0.99999576807;
     0,0,0];
 
t = [25.7; 1.22; 3.902; 1];

M = [R,t];

% data loading
folder_frame = ['Video_files/', person_id,'/',action_id,'/',rep,'/'];
folder_pose =  ['Hand_pose_annotation_v1/', person_id,'/',action_id,'/',rep,'/'];

hand_pose = textread([folder_pose 'skeleton.txt']);
hand_pose = hand_pose(:,2:end);

file_rgb = [folder_frame,'color/','color_',num2str(frame_num-1,'%04d'),'.jpeg'];
rgb_image = imread(file_rgb);

file_depth = [folder_frame,'depth/','depth_',num2str(frame_num-1,'%04d'),'.png'];
depth_image = imread(file_depth);

jointLocations = reshape(hand_pose(frame_num,:),[3,21])';

% depth
u_d = u0_d + fx_d*jointLocations(:,1)./jointLocations(:,3);
v_d = v0_d + fy_d*jointLocations(:,2)./jointLocations(:,3);

% color
jointLocations_tf = (M * [jointLocations,ones(21,1)]')';

u_c = u0_c + fx_c*jointLocations_tf(:,1)./jointLocations_tf(:,3);
v_c = v0_c + fy_c*jointLocations_tf(:,2)./jointLocations_tf(:,3);

dotsize = 5;
linesize = 2.5;

% plot depth image + hand pose

imagesc(depth_image);
hold on;

%draw wrist
plot(u_d(1),v_d(1), 'o','MarkerEdgeColor','w','MarkerFaceColor','w', 'MarkerSize',dotsize); hold on;
% draw thumb
ind = [2 7 8 9];
plot(u_d(ind),v_d(ind), 'o','MarkerEdgeColor','m','MarkerFaceColor','m', 'MarkerSize',dotsize); hold on;
plot(u_d([1,ind]),v_d([1,ind]), 'm','LineWidth',linesize)
% draw index
ind = [3 10 11 12];
plot(u_d(ind),v_d(ind), 'o','MarkerEdgeColor','b','MarkerFaceColor','b', 'MarkerSize',dotsize); hold on;
plot(u_d([1,ind]),v_d([1,ind]), 'b','LineWidth',linesize)
% etc.
ind = [4 13 14 15];
plot(u_d(ind),v_d(ind), 'o','MarkerEdgeColor','g','MarkerFaceColor','g', 'MarkerSize',dotsize); hold on;
plot(u_d([1,ind]),v_d([1,ind]), 'g','LineWidth',linesize)
ind = [5 16 17 18];
plot(u_d(ind),v_d(ind), 'o','MarkerEdgeColor','y','MarkerFaceColor','y', 'MarkerSize',dotsize); hold on;
plot(u_d([1,ind]),v_d([1,ind]), 'y','LineWidth',linesize)
ind = [6 19 20 21];
plot(u_d(ind),v_d(ind), 'o','MarkerEdgeColor','r','MarkerFaceColor','r', 'MarkerSize',dotsize); hold on;
plot(u_d([1,ind]),v_d([1,ind]), 'r','LineWidth',linesize)

% plot color image + hand pose

figure(2);
imshow(rgb_image);
hold on

plot(u_c(1),v_c(1), 'o','MarkerEdgeColor','w','MarkerFaceColor','w', 'MarkerSize',dotsize); hold on;
ind = [2 7 8 9];
plot(u_c(ind),v_c(ind), 'o','MarkerEdgeColor','m','MarkerFaceColor','m', 'MarkerSize',dotsize); hold on;
plot(u_c([1,ind]),v_c([1,ind]), 'm','LineWidth',linesize)
ind = [3 10 11 12];
plot(u_c(ind),v_c(ind), 'o','MarkerEdgeColor','b','MarkerFaceColor','b', 'MarkerSize',dotsize); hold on;
plot(u_c([1,ind]),v_c([1,ind]), 'b','LineWidth',linesize)
ind = [4 13 14 15];
plot(u_c(ind),v_c(ind), 'o','MarkerEdgeColor','g','MarkerFaceColor','g', 'MarkerSize',dotsize); hold on;
plot(u_c([1,ind]),v_c([1,ind]), 'g','LineWidth',linesize)
ind = [5 16 17 18];
plot(u_c(ind),v_c(ind), 'o','MarkerEdgeColor','y','MarkerFaceColor','y', 'MarkerSize',dotsize); hold on;
plot(u_c([1,ind]),v_c([1,ind]), 'y','LineWidth',linesize)
ind = [6 19 20 21];
plot(u_c(ind),v_c(ind), 'o','MarkerEdgeColor','r','MarkerFaceColor','r', 'MarkerSize',dotsize); hold on;
plot(u_c([1,ind]),v_c([1,ind]), 'r','LineWidth',linesize)
