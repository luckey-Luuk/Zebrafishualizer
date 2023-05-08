import numpy as np
import tifffile
import matplotlib.pyplot as plt
import trimesh

data = tifffile.imread('Data/20190701--2/20190701--20119.tif') #path name to tiff file goes here

imarray = np.array(data)
num_layers, height, width = imarray.shape[0], imarray.shape[1], imarray.shape[2] # initialize number of layers, height and width
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

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(combined_point_cloud[:, 0], combined_point_cloud[:, 1], combined_point_cloud[:, 2],
           s=1, c=colors / 255.0)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()

# Create a trimesh object
mesh = trimesh.Trimesh(vertices=combined_point_cloud)

# Save the mesh as an OBJ file
output_file = "point_cloud.obj"
mesh.export(output_file)
