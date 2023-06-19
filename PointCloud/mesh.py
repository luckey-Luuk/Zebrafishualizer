import numpy as np
import tifffile
import pyvista as pv
import vtk
import pymeshfix # won't work, when it "fixes" it gets rid of more than half of the points
import trimesh # won't work, runtime error when it "fixes" when it does show something it does not appear altered
from trimesh import repair


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
mesh = cloud.delaunay_3d(alpha=3, tol=0.1, offset=2.5, progress_bar=True).extract_geometry() # use delaunay to create mesh, alpha variable dictates how close the points have to be to get connedted
# mesh = pv.wrap(combined_point_cloud).reconstruct_surface() # use (poisson?) surface reconstruction to create mesh (not working)
# mesh.save('mesh.stl')
mesh.plot()

smoother = vtk.vtkSmoothPolyDataFilter()
smoother.SetInputData(mesh)
smoother.SetNumberOfIterations(500)
# Perform mesh smoothing
smoother.Update()
# Get the smoothed mesh
smoothed_mesh = smoother.GetOutput()
# Convert the VTK data to a PyVista mesh
smoothed_mesh_pv = pv.wrap(smoothed_mesh)

# Create a PyVista plotter
plotter = pv.Plotter()
# Add the smoothed mesh to the plotter
plotter.add_mesh(smoothed_mesh_pv)
# Set up the plotter and display the window
plotter.show()


smooth = mesh.smooth(n_iter=5000)
# smooth.plot()
smooth_taubin = mesh.smooth_taubin(n_iter=5000, pass_band=0.5)
# smooth_taubin.plot()

conn = smoothed_mesh_pv.connectivity(largest=False) # get connectivity of mesh
# conn.plot()
# conn.save('conn.stl')

bodies = conn.split_bodies() # seperate cells
bodiesPolyData = bodies.as_polydata_blocks()
for body in bodiesPolyData:
    if body.n_cells > 1: # filter degenerate bodies

        body.plot()
        # vtk.vtkFillHolesFilter(body)
        # body.plot()

        # enclosed_body = body.select_enclosed_points(body, check_surface=False)
        # # print(enclosed_body['SelectedPoints'])
        # # print(body)
        # print(enclosed_body)
        # enclosed_body.plot()
        # body.plot()
        # body.save('body'+str(bodiesPolyData.index(body))+'.stl')
# bodies.plot()
