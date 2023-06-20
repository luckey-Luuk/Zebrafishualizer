# open tif files in imagej and save to usable format

import os
import imagej
ij = imagej.init()

overwrite = False # change to True to overwrite existing files

source = "Data/original/3D tracking data to visualize/20190701--2_inter_29layers_mask_3a" # folder containing original files
target_folder = "Data/convertedToImagej/20190701--2_inter_29layers_mask_imagej" # folder to save converted files

for filename in os.listdir(source):
    target_file = target_folder + '/' + os.path.splitext(filename)[0] + "_imagej.tif"
    
    if os.path.exists(target_file):
        if overwrite:
            os.remove(target_file)
        else:
            continue

    f = os.path.join(source, filename)
    imp = ij.io().open(f) # open tif in imagej
    ij.io().save(imp, target_file) # save tif
