import numpy as np
import tifffile
import pyvista as pv
from PIL import Image
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os
from mpl_toolkits.mplot3d import Axes3D

# data = tifffile.imread('Data/20190701--2/20190701--20119.tif') #8 layers
# data = tifffile.imread('Data/3D tracking data to visualize/20190701--2_inter_29layers_green/20190701--20000.tif') #29 layers
# data = tifffile.imread('Data/3D tracking data to visualize/20190701--2_inter_29layers_mask_3a/20190701--20000_M3a_Step92.tif') #29 layers labeled

# data = tifffile.imread("/Users/robertgijsbers/Desktop/Repository_github/Zebrafishualizer/Data/3D tracking data to visualize/20190701--2_inter_29layers_green/20190701--20000.tif")


frames = []
i = [f"{i:03}" for i in range(30)] # the number in the range() function has to be 120 to get every timestep

for element in i:
    # image_path = f"/Users/robertgijsbers/Desktop/Repository_github/Zebrafishualizer/Data/3D tracking data to visualize/20190701--2_inter_29layers_green/20190701--20{element}.tif"
    image_path = f"Data/3D tracking data to visualize/20190701--2_inter_29layers_green/20190701--20{element}.tif"
    image = Image.open(image_path)
    frames.append(image)


with imageio.get_writer('output.mp4', mode='I', fps=30) as writer:
    frame_counter = 0
    for frame in frames:
        # Render the frame
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.imshow(frame)

        file_number = i[frame_counter]
        # data = tifffile.imread(f"/Users/robertgijsbers/Desktop/Repository_github/Zebrafishualizer/Data/3D tracking data to visualize/20190701--2_inter_29layers_green/20190701--20{file_number}.tif")
        data = tifffile.imread(f"Data/3D tracking data to visualize/20190701--2_inter_29layers_green/20190701--20{element}.tif")

        imarray = np.array(data)
        num_layers, height, width = imarray.shape[0], imarray.shape[1], imarray.shape[2] # initialize number of layers, height and width
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

        cloud = pv.PolyData(np.concatenate(point_clouds))

        # Create the 3D mesh
        mesh = cloud.delaunay_3d(alpha=2).extract_geometry() # The alpha variable dictates how close the ponts have to be to get connedted

        # mesh_alpha = 2  # Adjust the alpha value to control the mesh connectivity
        # Extract the vertices and connectivity arrays
        vertices = mesh.points
        connectivity = mesh.connectivity(largest=False) # get connectivity of mesh
        # connectivity = mesh.delaunay_3d(alpha=mesh_alpha).extract_geometry().faces
        # Render the 3D mesh
        ax.plot_trisurf(vertices[:, 0], vertices[:, 1], vertices[:, 2], triangles=connectivity, cmap='viridis')


        # Save the figure to an image file
        fig.savefig('temp.png')

        # Append the image to the video
        writer.append_data(imageio.imread('temp.png'))

        # Close and delete the temporary image file
        plt.close(fig)
        os.remove('temp.png')
        frame_counter += 1

# imarray = np.array(data)
# # print(imarray.shape)
# num_layers, height, width = imarray.shape[0], imarray.shape[1], imarray.shape[2] # initialize number of layers, height and width
# # num_layers, height, width, id = imarray.shape[0], imarray.shape[1], imarray.shape[2], imarray.shape[3] # initialize number of layers, height and width
# # height, width = imarray.shape[0], imarray.shape[1] # initialize number of layers, height and width
# grayscale_threshold = 0

# point_clouds = []

# for z in range(num_layers):
#     layer = imarray[z, :, :]
#     matching_pixels = np.where(layer > grayscale_threshold)
#     point_cloud = np.column_stack(matching_pixels)
#     point_cloud = point_cloud.astype(float)  # Convert to float to handle non-integer coordinates
#     point_cloud[:, 0] -= height / 2
#     point_cloud[:, 1] -= width / 2
#     point_cloud = np.hstack((point_cloud, np.full((point_cloud.shape[0], 1), z)))  # Add z-coordinate
#     point_clouds.append(point_cloud)

# combined_point_cloud = np.concatenate(point_clouds)

# # points is a 3D numpy array (n_points, 3) coordinates of a sphere
# cloud = pv.PolyData(combined_point_cloud)

# # here the mesh is made from the point cloud. 
# mesh = cloud.delaunay_3d(alpha=2).extract_geometry() # The alpha variable dictates how close the ponts have to be to get connedted
# # mesh = pv.wrap(combined_point_cloud).reconstruct_surface()
# # mesh.save('mesh.stl')
# # mesh.plot() # uncomment this line to see the mesh in python

# conn = mesh.connectivity(largest=False) # get connectivity of mesh
# # conn.plot()
# conn.save('conn.stl')

# # sized = conn.compute_cell_sizes()
# # cell_volumes = sized.cell_data['Volume']
# # print(cell_volumes)

# # surface = conn.extract_surface()
# # surface.plot()

# bodies = conn.split_bodies()
# bodiesPolyData = bodies.as_polydata_blocks()
# for body in bodiesPolyData:
#     # print(body)
#     if body.n_cells > 1:
#         # body.plot()
#         body.save('body'+str(bodiesPolyData.index(body))+'.stl')
# # bodies.plot()

