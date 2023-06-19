import os
import imagej
ij = imagej.init()

source = "Data/3D tracking data to visualize/20190701--2_inter_29layers_mask_3a"
target = "Data/20190701--2_inter_29layers_mask_imagej"

for filename in os.listdir(source):
    f = os.path.join(source, filename)
    imp = ij.io().open(f)
    ij.io().save(imp, target + '/' + os.path.splitext(filename)[0] + "_imagej.tif")
