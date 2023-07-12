import argparse
import os
import torch

from attrdict import AttrDict
import os
from Plot import plotem

os.environ['KMP_DUPLICATE_LIB_OK']='True'

from sgan.data.loader import data_loader
from sgan.models import TrajectoryGenerator
from sgan.losses import displacement_error, final_displacement_error
from sgan.utils import relative_to_abs, get_dset_path

import numpy as np 
parser = argparse.ArgumentParser()
parser.add_argument('--model_path',default='models/sgan-models', type=str)
parser.add_argument('--num_samples', default=1, type=int)
parser.add_argument('--dset_type', default='test', type=str)


def get_generator(checkpoint):
    args = AttrDict(checkpoint['args'])
    #print("args: ",args)
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
  while True:  
    with torch.no_grad():
        
      
        k=0

        
        for batch in loader:
            k+=1
            print("batch: ",k)
            batch = [tensor.cuda() for tensor in batch]
            (obs_traj, pred_traj_gt, obs_traj_rel, pred_traj_gt_rel,
             non_linear_ped, loss_mask, seq_start_end) = batch

            print("batch: ",len(batch)," : ",len(batch[0])," : ",len(batch[0][0]))

            ade, fde = [], []
            total_traj += pred_traj_gt.size(1)
            print("obs_traj_len: ",len(obs_traj))
            print("obs_traj_type: ",(obs_traj.shape))
            print("seq_start_end: ",(seq_start_end.shape))
            obs_traj_changed=torch.swapaxes(obs_traj, 0, 1)
            pred_traj_gt_changed=torch.swapaxes(pred_traj_gt, 1, 0)
            pred_faked_all=[]
            
            #for c in range(30): #num_samples
              
            pred_traj_fake_rel = generator(
                    obs_traj, obs_traj_rel, seq_start_end
                )
                #[:,0,:]
                #print("pred_traj_fake_rel: ",pred_traj_fake_rel.size())
            pred_traj_fake = relative_to_abs(
                    pred_traj_fake_rel, obs_traj[-1]
                )
                
            pred_traj_fake_changed=torch.swapaxes(pred_traj_fake, 0, 1)

            print("obs_traj_changed------------: ",obs_traj_changed[0])
            print("pred_traj_fake------------: ",pred_traj_fake_changed[0])
            print("pred_traj_gt++++++++++++++ ",pred_traj_gt_changed[0])
    
            pred_faked_all.append(pred_traj_fake_changed)                

            '''     ade.append(displacement_error(
                    pred_traj_fake, pred_traj_gt, mode='raw'
                ))
                fde.append(final_displacement_error(
                    pred_traj_fake[-1], pred_traj_gt[-1], mode='raw'
                ))
            #plotem(obs_traj_changed,pred_faked_all,pred_traj_gt_changed,5)
       ade_sum = evaluate_helper(ade, seq_start_end)
            fde_sum = evaluate_helper(fde, seq_start_end)

            ade_outer.append(ade_sum)
            fde_outer.append(fde_sum)
        ade = sum(ade_outer) / (total_traj * args.pred_len)
        fde = sum(fde_outer) / (total_traj)'''
        #return ade, fde


def main(args):
    # for path in paths:
        path="models/sgan-models/zara1_12_model.pt"
        checkpoint = torch.load("models/sgan-models/eth_12_model.pt")
        # print("Paths: ",path)
        generator = get_generator(checkpoint)
        _args = AttrDict(checkpoint['args'])
        #path = get_dset_path(_args.dataset_name, args.dset_type)
        cc, loader = data_loader(_args, path)
        print("loader: ",cc)
        evaluate(_args, loader, generator, args.num_samples)
        #print('Dataset: {}, Pred Len: {}, ADE: {:.2f}, FDE: {:.2f}'.format(
         #   _args.dataset_name, _args.pred_len, ade, fde))


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
