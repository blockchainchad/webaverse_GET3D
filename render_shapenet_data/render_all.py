# Copyright (c) 2022, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# NVIDIA CORPORATION & AFFILIATES and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION & AFFILIATES is strictly prohibited.

import os
import argparse

parser = argparse.ArgumentParser(description='Renders given obj file by rotation a camera around it.')
parser.add_argument(
    '--save_folder', type=str, default='./out',
    help='path for saving rendered image')
parser.add_argument(
    '--dataset_folder', type=str, default='./shapenet',
    help='path for downloaded 3d dataset folder')

args = parser.parse_args()

save_folder = args.save_folder
dataset_folder = args.dataset_folder
blender_root = 'blender'

synset_list = [
    # '02958343',  # Car
    # '03001627',  # Chair
    '03790512'  # Motorbike
]
scale_list = [
    # 0.9,
    # 0.7,
    0.9
]

# check if save folder exists
# if not, create it
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# for shapenet v2, we normalize the model location
for synset, obj_scale in zip(synset_list, scale_list):
    file_list = sorted(os.listdir(os.path.join(dataset_folder, synset)))
    for file in file_list:
        # check if file_list+'/models' exists
        if os.path.exists(os.path.join(dataset_folder, synset, file, 'models')):
            # move all files in file_list+'/models' to file_list
            os.system('mv ' + os.path.join(dataset_folder, synset, file, 'models/*') + ' ' + os.path.join(dataset_folder, synset, file))
            # remove file_list+'/models' if it exists
            os.system('rm -rf ' + os.path.join(dataset_folder, synset, file, 'models'))


for synset, obj_scale in zip(synset_list, scale_list):
    file_list = sorted(os.listdir(os.path.join(dataset_folder, synset)))
    for idx, file in enumerate(file_list):
        render_cmd = '%s -b -P render_shapenet.py -- --output %s %s  --scale %f --views 24' % (
            blender_root, save_folder, os.path.join(dataset_folder, synset, file, 'model_normalized.obj'), obj_scale
        )
        os.system(render_cmd)