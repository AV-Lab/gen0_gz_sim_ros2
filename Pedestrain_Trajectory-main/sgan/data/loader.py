from numpy.core.fromnumeric import size
from torch.utils.data import DataLoader

from sgan.data.trajectories import TrajectoryDataset, seq_collate


def data_loader(args, path,data_passed):
    dset = TrajectoryDataset(data_passed,
        path,
        obs_len=args.obs_len,
        pred_len=args.pred_len,
        skip=args.skip,  
        delim=args.delim)
    #print(dset)
    # print("dset from dataloader _real: ",dset.__getitem__(0))
    #print("dset from dataloader: _normal",dset.__getitem__(17)[0])
    #print("num_of_seq: ",dset.__len__())

    loader = DataLoader(
        dset,
        batch_size=1000, #args.batch_size
        shuffle=True,
        num_workers=args.loader_num_workers,
        collate_fn=seq_collate)    
    #print("args.batch_size: ",args.batch_size)
    #dadad=iter(loader)
    #print("data: ",len(dadad))


    return dset, loader
