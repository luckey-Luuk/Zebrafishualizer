import numpy as np
import tifffile
import pyvista as pv


#Read tiff file
# data = tifffile.imread('Data/20190701--2/20190701--20119.tif') #8 layers
data = tifffile.imread('Data/3D tracking data to visualize/20190701--2_inter_29layers_green/20190701--20000.tif') #29 layers
# data = tifffile.imread('Data/3D tracking data to visualize/20190701--2_inter_29layers_mask_3a/20190701--20000_M3a_Step92.tif') #29 layers labeled

imarray = np.array(data) # convert tiff file to numpy array
num_layers, height, width = imarray.shape[0], imarray.shape[1], imarray.shape[2] # initialize number of layers, height and width


#Create point cloud
point_clouds = []
grayscale_threshold = 0
for z in range(num_layers):
    layer = imarray[z, :, :] # select layer
    matching_pixels = np.where(layer > grayscale_threshold) # find pixels that are not black
    point_cloud = np.column_stack(matching_pixels) # add pixels to point cloud
    point_cloud = point_cloud.astype(float)  # Convert to float to handle non-integer coordinates
    point_cloud[:, 0] -= height / 2
    point_cloud[:, 1] -= width / 2
    point_cloud = np.hstack((point_cloud, np.full((point_cloud.shape[0], 1), z)))  # Add z-coordinate
    point_clouds.append(point_cloud)

cloud = pv.PolyData(np.concatenate(point_clouds)) # combine layers into one and convert to polydata


#Create mesh
mesh = cloud.delaunay_3d(alpha=2).extract_geometry() # use delaunay to create mesh, alpha variable dictates how close the points have to be to get connedted
# mesh = pv.wrap(combined_point_cloud).reconstruct_surface() # use (poisson?) surface reconstruction to create mesh (not working)
# mesh.save('mesh.stl')
# mesh.plot()

conn = mesh.connectivity(largest=False) # get connectivity of mesh
# conn.plot()
# conn.save('conn.stl')

# surface = conn.extract_surface() # use (poisson?) surface reconstruction on connectivity (has no effect)
# surface.save('surface.stl')
# surface.plot()

bodies = conn.split_bodies() # seperate cells
bodiesPolyData = bodies.as_polydata_blocks()
for body in bodiesPolyData:
    if body.n_cells > 1: # filter degenerate bodies
        # body.plot()
        # body.save('body'+str(bodiesPolyData.index(body))+'.stl')
# bodies.plot()
