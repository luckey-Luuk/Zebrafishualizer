import numpy as np
import tifffile
import pyvista

# data = tifffile.imread('Data/20190701--2/20190701--20119.tif') #path name to tiff file goes here
data = tifffile.imread('/Users/robertgijsbers/Desktop/Repository_github/Zebrafishualizer/Data/20190701--2/20190701--20119.tif')

imarray = np.array(data)
num_layers, height, width = imarray.shape[0], imarray.shape[1], imarray.shape[2] # initialize number of layers, height and width
grayscale_threshold = 200

point_clouds = []

for z in range(num_layers):
    layer = imarray[z, :, :]
    matching_pixels = np.where(layer >= grayscale_threshold)
    point_cloud = np.column_stack(matching_pixels)
    point_cloud = point_cloud.astype(float)  # Convert to float to handle non-integer coordinates
    point_cloud[:, 0] -= height / 2
    point_cloud[:, 1] -= width / 2
    point_cloud = np.hstack((point_cloud, np.full((point_cloud.shape[0], 1), z)))  # Add z-coordinate
    point_clouds.append(point_cloud)

combined_point_cloud = np.concatenate(point_clouds)

# points is a 3D numpy array (n_points, 3) coordinates of a sphere
cloud = pyvista.PolyData(combined_point_cloud)

# here the mesh is made from the point cloud. 
volume = cloud.delaunay_3d(alpha=3) # The alpha variable dictates how close the ponts have to be to get connedted
shell = volume.extract_geometry()
shell.save('mesh.stl')
# shell.plot() # uncomment this line to see the mesh in python