import argparse
import os
import torch
from copy import deepcopy
from attrdict import AttrDict
import os
# from Plot import plotem

os.environ['KMP_DUPLICATE_LIB_OK']='True'

from sgan.data.loader import data_loader
from sgan.models import TrajectoryGenerator
from sgan.losses import displacement_error, final_displacement_error
from sgan.utils import relative_to_abs, get_dset_path

import numpy as np 
parser = argparse.ArgumentParser()
parser.add_argument('--model_path',default='models/sgan-models/zara1_8_model.pt', type=str)
parser.add_argument('--num_samples', default=1, type=int)
parser.add_argument('--dset_type', default='test', type=str)

pub=None

def get_generator(checkpoint):
    args = AttrDict(checkpoint['args'])
    generator = TrajectoryGenerator(
        obs_len=args.obs_len,
        pred_len=args.pred_len,
        embedding_dim=args.embedding_dim,
        encoder_h_dim=args.encoder_h_dim_g,
        decoder_h_dim=args.decoder_h_dim_g,
        mlp_dim=args.mlp_dim,
        num_layers=args.num_layers,
        noise_dim=args.noise_dim,
        noise_type=args.noise_type,
        noise_mix_type=args.noise_mix_type,
        pooling_type=args.pooling_type,
        pool_every_timestep=args.pool_every_timestep,
        dropout=args.dropout,
        bottleneck_dim=args.bottleneck_dim,
        neighborhood_size=args.neighborhood_size,
        grid_size=args.grid_size,
        batch_norm=args.batch_norm)
    generator.load_state_dict(checkpoint['g_state'])
    generator.cuda()
    generator.train()
    return generator


def evaluate_helper(error, seq_start_end):
    sum_ = 0
    error = torch.stack(error, dim=1)

    for (start, end) in seq_start_end:
        start = start.item()
        end = end.item()
        _error = error[start:end]
        _error = torch.sum(_error, dim=0)
        _error = torch.min(_error)
        sum_ += _error
    return sum_


def evaluate(args, loader, generator, num_samples):
    ade_outer, fde_outer = [], []
    total_traj = 0

    with torch.no_grad():
        for batch in loader:
            batch = [tensor.cuda() for tensor in batch]
            (obs_traj, pred_traj_gt, obs_traj_rel, pred_traj_gt_rel,
                non_linear_ped, loss_mask, seq_start_end) = batch

            ade, fde = [], []
            total_traj += pred_traj_gt.size(1)
            obs_traj_changed=torch.swapaxes(obs_traj, 0, 1)
            pred_traj_gt_changed=torch.swapaxes(pred_traj_gt, 1, 0)
                
            pred_traj_fake_rel_1 = generator(
                obs_traj, obs_traj_rel, seq_start_end
            )

            pred_traj_fake_1 = relative_to_abs(
                pred_traj_fake_rel_1, obs_traj[-1]
            )
            
            pred_traj_fake_rel_2 = generator(
                obs_traj, obs_traj_rel, seq_start_end
            )

            pred_traj_fake_2 = relative_to_abs(
                pred_traj_fake_rel_2, obs_traj[-1]
            )
            

            pred_traj_fake_changed_1=torch.swapaxes(pred_traj_fake_1, 0, 1)
            pred_traj_fake_changed_2=torch.swapaxes(pred_traj_fake_2, 0, 1)
            prediction_1=(pred_traj_fake_changed_1.cpu().numpy())
            prediction_2=(pred_traj_fake_changed_2.cpu().numpy())
            prediction=np.concatenate((prediction_1, prediction_2), axis=0)
            obs_traj_changed=(obs_traj_changed.cpu().numpy())

            # print(pred_traj_fake_rel_1)
            
            # print(pred_traj_fake_1)
            # print("*********")
            # print(prediction_1)

            pointsArray=PoseArray()
            points=Pose()

            for prediction in prediction_1:
                for positions in prediction:
                    points.position.x=positions[0]
                    points.position.y=positions[1]
                    pointsArray.poses.append(deepcopy(points))
            print(prediction_1)
            print("*********")
            print("inputs----------",obs_traj_changed)
            pub.publish(pointsArray)

            # print("observation------------: ",obs_traj_changed)
            # print("prediction------------: ",pred_traj_fake_changed_1)
            # print("prediction------------: ",(prediction))

           # show_marker(obs_traj_changed,prediction)
path='models/sgan-models/zara1_8_model.pt'
args = parser.parse_args()
checkpoint = torch.load(path,map_location=torch.device('cpu'))
# print("Paths: ",path)
generator = get_generator(checkpoint)
_args = AttrDict(checkpoint['args'])
path = get_dset_path(_args.dataset_name, args.dset_type)
def main(args,data_passed):
    #'models/sgan-models/eth_8_model.pt'
    #'/home/mustofa/tra_ws/src/tra1_viz/src/models/sgan-models/zara1_8_model.pt'
    #For GPUS
    #checkpoint = torch.load(path)
    # checkpoint = torch.load(path,map_location=torch.device('cpu'))
    # # print("Paths: ",path)
    # generator = get_generator(checkpoint)
    # _args = AttrDict(checkpoint['args'])
    # path = get_dset_path(_args.dataset_name, args.dset_type)
    cc, loader = data_loader(_args, path,data_passed)
    #print("loader: ",cc)
    evaluate(_args, loader, generator, args.num_samples)


###########################################
import rospy
from std_msgs.msg import String
import numpy as np
import math
#the output of trajectories for visual will be at "/path" topic
import rospy
from std_msgs.msg import String
import sys
#from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped, Point, PoseArray, Pose
# from zed_interfaces.msg import ObjectsStamped
from visualization_msgs.msg import Marker,MarkerArray
from nav_msgs.msg import Odometry, Path


frame=0
num_of_frames=0
dataset=[]
###################################################################


def show_marker(observation,prediction,num_obs=1):
    pub_line_min_dist = rospy.Publisher('/line_marker', MarkerArray, queue_size=4)
   # rospy.loginfo('Publishing example line')
    marked=MarkerArray()
    #while not rospy.is_shutdown():
    
    marker = Marker()
    marker.header.frame_id = "map"
    marker.id=1
    # marker.ns = "linear_constraints"
    marker.type = marker.LINE_STRIP
    marker.action = marker.ADD



    # marker scale
    marker.scale.x = 0.03
    marker.scale.y = 0.03
    marker.scale.z = 0.03


    # marker color
    marker.color.a = 1.0
    marker.color.r = 1.0
    marker.color.g = 1.0
    marker.color.b = 0.0


    # marker orientaiton
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0

    for j in observation:
        marker.points = []
        for i in range (len(j)):
            
            line_list = Point()
            line_list.x = j[i][0]
            line_list.y = j[i][1]
            line_list.z = 0
            marker.points.append(line_list)
        marked.markers.append(marker)
    

    for i in range(num_obs):
        marker_obs = Marker()
        marker_obs.id=2+i
        # # marker_obs.ns = "linear_constraints"
        marker_obs .header.frame_id = "map"
        marker_obs .type = marker_obs.LINE_STRIP
        marker_obs .action = marker_obs.ADD

        marker_obs.scale.x = 0.05
        marker_obs.scale.y = 0.05
        marker_obs.scale.z = 0.03
        marker_obs.color.a = 1.0
        marker_obs.color.r = 1.0
        if i>0:
         marker_obs.color.g = 1.0
         marker_obs.color.b = 0.6
        marker_obs.pose.orientation.x = 0.0
        marker_obs.pose.orientation.y = 0.0
        marker_obs.pose.orientation.z = 0.0
        marker_obs.pose.orientation.w = 1.0

        pred=prediction[i]
        marker_obs.points = []
        for k in range (len(j)):
            line_list_obs = Point()
            line_list_obs.x = pred[k][0]
            line_list_obs.y = pred[k][1]
            line_list_obs.z = 0
            marker_obs.points.append(line_list_obs)

                
        marked.markers.append(marker_obs)
    pub_line_min_dist.publish(marked)
    


####################################################################

def callback_odom(odom_data):
    global  camera_position
    camera_position = odom_data.pose.pose.position.x
    #cal_coordinate(odom_position)
    #print ("Odometry Position:",camera_position)


###################################################################

def callback(data):
    global frame,num_of_frames
    global dataset
    frame=frame+1
    # #print('frame: ',frame)
    # if (frame!=0):
    #     for obj in object.objects:
    #         coordinate=[]
    #         coordinate.append(int(frame))
    #         coordinate.append(obj.label_id)
    #         coordinate.append(obj.position[0])
    #         coordinate.append(obj.position[2])
    #         if(not (math.isnan(obj.position[0])) and not (math.isnan(obj.position[2]))):
    #             dataset.append(coordinate)
    
    # if (len(dataset)>=1):
    #   a=np.array(dataset)
    #   all_frames=a[:,0]
    #   num_of_frames=len(all_frames)
    # uni,count=np.unique(a[:,1],return_counts=True)
    # # print("Frames: ",all_frames)
    # # print("IDs: ",a[:,1])
    # #dataset=np.array(dataset)
    # # print(len(dataset))
    # if (len(dataset)>=1):
    #     dataset=a[a[:,0]!=((frame)-8)]
    #     # print("Frames---: ",dataset[:,0])
    #     # print("IDs----: ",dataset[:,1])
    #     dataset=dataset.tolist()

    # #  print("B aaaaaaaaaall frames: ",allb_frames)

    # # Calling prediction 
    # if (num_of_frames>7):
    #     # print("Frames: ",np.array(dataset)[:,0])
    #     print("IDs: ",np.array(dataset)[:,1])
    #     main(args,dataset)
    frame=int(data.header.frame_id)
    for sample in data.poses:
        coordinate=[]
        coordinate.append(frame)
        coordinate.append(int(sample.position.z)) # z is used for pedestrian ID
        coordinate.append(sample.position.x)
        coordinate.append(sample.position.y)
        dataset.append(coordinate)
        #print(dataset)
    a=np.array(dataset)
    if (len(dataset)>=1):
        dataset=a[a[:,0]!=((frame)-8)]
        print("Frames---: ",dataset[:,0])
        # print("IDs----: ",dataset[:,1])
        dataset=dataset.tolist()
    
    # Calling prediction 
    frames,count=np.unique((np.array(dataset)[:,0]),return_counts=True)
    if (len(frames)>7):
        # print("Frames: ",np.array(dataset)[:,0])
        # print("IDs: ",np.array(dataset)[:,1])
        main(args,dataset)

################################################################################

def listener():
    rospy.init_node('pedestrian_listener', anonymous=True)

    global pub
    pub = rospy.Publisher('pedestrian_predicted_position', PoseArray, queue_size=10)

    rospy.Subscriber('pedestrian_past_position', PoseArray, callback)
    #rospy.Subscriber('/zed2/zed_node/odom',Odometry,callback_odom)

    # spin() simply keeps python from exiting until this node is stopped
    
    rospy.spin()


##################################################################################

if __name__ == '__main__':
    args = parser.parse_args()
    listener()
    
