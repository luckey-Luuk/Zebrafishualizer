import numpy as np
import tifffile
from pywavefront import Wavefront
import matplotlib.pyplot as plt
from skimage import io, color
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from pyntcloud import PyntCloud
import pandas as pd

data = tifffile.imread('Data/20190701--2/20190701--20119.tif') #path name to tiff file goes here
# volume = np.array(data)
# im = Image.open('Data/20190701--2/20190701--20119.tif)

num_layers, height, width = 8, 512, 512 #initialize number of layers, height and width

imarray = np.array(data)
# print(imarray.shape)
grayscale_threshold = 200


point_clouds = []
for z in range(num_layers):
    layer = imarray[z,:,:]
    matching_pixels = np.where(layer >= grayscale_threshold)
    point_cloud = np.column_stack(matching_pixels)
    point_clouds.append(point_cloud)
combined_point_cloud = np.concatenate(point_clouds)

# print(combined_point_cloud)
z_coords = np.zeros(combined_point_cloud.shape[0])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(combined_point_cloud[:,0], combined_point_cloud[:,1], z_coords, s=1, cmap='viridis')
plt.show()

#till here it works only the points are at a single z-axis.

# output_file = "output.obj"
# with open(output_file, 'w') as f:
#     pass

# obj = Wavefront(output_file)

# output_file = "point_cloud.obj"
# output_file = "point_cloud.obj"
# with open(output_file, "w") as f:
#     for point in combined_point_cloud:
#         f.write(f"v {point[0]} {point[1]} {point[2]}\n")
#     f.write(f"f {' '.join(str(i + 1) for i in range(1, combined_point_cloud.shape[0] + 1))}\n")
