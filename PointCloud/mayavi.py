import numpy as np
import tifffile
# from pywavefront import Wavefront
import matplotlib.pyplot as plt
# from skimage import io, color
# from sklearn.cluster import KMeans
# from mpl_toolkits.mplot3d import Axes3D
# from pyntcloud import PyntCloud
# import pandas as pd
import trimesh

data = tifffile.imread('Data/20190701--2/20190701--20119.tif') #path name to tiff file goes here
# volume = np.array(data)
# im = Image.open('Data/20190701--2/20190701--20119.tif)

num_layers, height, width = 8, 512, 512 #initialize number of layers, height and width

imarray = np.array(data)
# print(imarray.shape)
grayscale_threshold = 200


point_clouds = []
colors = []  # List to store RGB colors

for z in range(num_layers):
    layer = imarray[z, :, :]
    matching_pixels = np.where(layer >= grayscale_threshold)
    point_cloud = np.column_stack(matching_pixels)
    point_cloud = point_cloud.astype(float)  # Convert to float to handle non-integer coordinates
    point_cloud[:, 0] -= height / 2
    point_cloud[:, 1] -= width / 2
    point_cloud = np.hstack((point_cloud, np.full((point_cloud.shape[0], 1), z)))  # Add z-coordinate
    point_clouds.append(point_cloud)

    color_values = data[z, matching_pixels[0], matching_pixels[1]]
    colors.append(color_values)

combined_point_cloud = np.concatenate(point_clouds)
colors = np.concatenate(colors)

# print(combined_point_cloud)
z_coords = np.zeros(combined_point_cloud.shape[0])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(combined_point_cloud[:, 0], combined_point_cloud[:, 1], z_coords, s=1, c=colors / 255.0)
plt.show()

#till here it works only the points are at a single z-axis.


# Create a trimesh object
mesh = trimesh.Trimesh(vertices=combined_point_cloud)

# Save the mesh as an OBJ file
output_file = "point_cloud.obj"
mesh.export(output_file)
