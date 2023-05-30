import numpy as np
import tifffile
import pyvista as pv

# data = tifffile.imread('Data/20190701--2/20190701--20119.tif') #8 layers
data = tifffile.imread('Data/3D tracking data to visualize/20190701--2_inter_29layers_green/20190701--20000.tif') #29 layers
# data = tifffile.imread('Data/3D tracking data to visualize/20190701--2_inter_29layers_mask_3a/20190701--20000_M3a_Step92.tif') #29 layers labeled

imarray = np.array(data)
# print(imarray.shape)
num_layers, height, width = imarray.shape[0], imarray.shape[1], imarray.shape[2] # initialize number of layers, height and width
# num_layers, height, width, id = imarray.shape[0], imarray.shape[1], imarray.shape[2], imarray.shape[3] # initialize number of layers, height and width
# height, width = imarray.shape[0], imarray.shape[1] # initialize number of layers, height and width
grayscale_threshold = 0

point_clouds = []

for z in range(num_layers):
    layer = imarray[z, :, :]
    matching_pixels = np.where(layer > grayscale_threshold)
    point_cloud = np.column_stack(matching_pixels)
    point_cloud = point_cloud.astype(float)  # Convert to float to handle non-integer coordinates
    point_cloud[:, 0] -= height / 2
    point_cloud[:, 1] -= width / 2
    point_cloud = np.hstack((point_cloud, np.full((point_cloud.shape[0], 1), z)))  # Add z-coordinate
    point_clouds.append(point_cloud)

combined_point_cloud = np.concatenate(point_clouds)

# points is a 3D numpy array (n_points, 3) coordinates of a sphere
cloud = pv.PolyData(combined_point_cloud)

# here the mesh is made from the point cloud. 
mesh = cloud.delaunay_3d(alpha=10).extract_geometry() # The alpha variable dictates how close the ponts have to be to get connedted
# mesh = pv.wrap(combined_point_cloud).reconstruct_surface()
# mesh.save('mesh.stl')
# mesh.plot() # uncomment this line to see the mesh in python

conn = mesh.connectivity(largest=False) # get connectivity of mesh
conn.plot()
conn.save('conn.stl')