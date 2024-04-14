
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import flowpy

import torch
from core.raft import RAFT
from core.utils.utils import InputPadder
import argparse

import os 

os
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

color = np.random.randint(0, 255, (100, 3))
weightedGrey = lambda rgb: np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])
RMS = lambda x, y: np.sqrt(np.mean((x-y)**2))

avg_mean = lambda flow, gt: np.nanmean(np.sqrt(np.sum((flow-gt)**2,axis=2)))

def write_flo_file(flow, filename):
    """
    Write optical flow in Middlebury .flo format
    
    :param flow: optical flow map
    :param filename: optical flow file path to be saved
    :return: None
    
    from https://github.com/liruoteng/OpticalFlowToolkit/
    
    """
    # forcing conversion to float32 precision
    flow = flow.astype(np.float32)
    f = open(filename+'.flo', 'wb')
    magic = np.array([202021.25], dtype=np.float32)
    (height, width) = flow.shape[0:2]
    w = np.array([width], dtype=np.int32)
    h = np.array([height], dtype=np.int32)
    magic.tofile(f)
    w.tofile(f)
    h.tofile(f)
    flow.tofile(f)
    f.close()

 
DEVICE = 'cpu'
def load_image(imfile):
    img = np.array(cv.imread(imfile)).astype(np.uint8)
    img = torch.from_numpy(img).permute(2, 0, 1).float()
    return img[None].to('cpu')

def computeOpticalFlow(initial_frame_path, final_frame_path,flow_map_path='./flows/', model_dir_path='models/raft-things.pth'):
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', nargs='?', help="restore checkpoint")
    parser.add_argument('--path', help="dataset for evaluation")
    parser.add_argument('--small', action='store_true', help='use small model')
    parser.add_argument('--mixed_precision', action='store_true', help='use mixed precision')
    parser.add_argument('--alternate_corr', action='store_true', help='use efficent correlation implementation')
    args, unknown= parser.parse_known_args()
    args.model = model_dir_path
    
    model = torch.nn.DataParallel(RAFT(args))
    model.load_state_dict(torch.load(args.model, map_location=torch.device('cpu')))

    model = model.module
    model.to('cpu')
    model.eval()
    with torch.no_grad():
        image1 = load_image(initial_frame_path)
        image2 = load_image(final_frame_path)

        padder = InputPadder(image1.shape)
        image1, image2 = padder.pad(image1, image2)
        flow_low, flow_up = model(image1, image2, iters=20, test_mode=True)
        _res = padder.unpad(flow_up)
        _res = _res.detach().cpu().numpy()[0]
        _res = np.transpose(_res, (1, 2, 0))
        write_flo_file(_res, flow_map_path+'result')
        return _res

if __name__=='__main__':

    initial_frame_path, final_frame_path =  './data/RubberWhale/frame10.png', './data/RubberWhale/frame11.png'
    flow = computeOpticalFlow(initial_frame_path, final_frame_path, flow_map_path='./flows/', model_dir_path='models/raft-things.pth')
    print(flow.shape)