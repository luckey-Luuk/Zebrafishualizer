import tifffile
import numpy as np
import matplotlib.pyplot as plt
# import pywavefront
from pywavefront import Wavefront
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image


data = tifffile.imread('/Users/robertgijsbers/Desktop/20190701--2/20190701--20119.tif') #path name to tiff file goes here
# volume = np.array(data)
im = Image.open('/Users/robertgijsbers/Desktop/20190701--2/20190701--20119.tif')

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
# plt.show()

output_file = "output.obj"
with open(output_file, 'w') as f:
    pass



obj = Wavefront(output_file)

# Add the point cloud vertices to the object
for layer in range(8): # assuming 8 layers in the Z direction
    for point in range(len(point_clouds[layer])):
        rows, cols = np.where(point_clouds[layer][point] == 1)
        z = layer
        if rows.size > 0 and cols.size > 0:
            for x, y in zip(rows, cols):
                obj.vertices.append((x, y, z))

# Save the object to a file
with open(output_file, "w") as f:
    f.write(str(obj))
