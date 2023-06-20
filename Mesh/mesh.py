import os
import numpy as np
import tifffile
import pyvista as pv
import vtk
# import pymeshfix # won't work, when it "fixes" it gets rid of more than half of the points
# import trimesh # won't work, runtime error when it "fixes" when it does show something it does not appear altered
# from trimesh import repair


source = "Data/convertedToImagej/20190701--2_inter_29layers_mask_imagej" # folder containing labeled tif files
target_folder = "Data/meshes/20190701--2_meshes" # folder to save mesh files

for filename in os.listdir(source):
    target_file = target_folder + '/' + os.path.splitext(filename)[0].split('_')[0] + "_mesh.stl"

   # Read tif file
    f = os.path.join(source, filename) # get file path
    if not f.endswith(".tif"): # check if file is a tif file
        print("Not a tif file: " + f)
        #TODO: check if tifs have the same shape
    else:
        imarray = np.array(tifffile.imread(f)) # read tif file
        num_layers, height, width = imarray.shape[0], imarray.shape[1], imarray.shape[2] # initialize number of layers, height and width
        num_cells = imarray.max() # get number of cells in tif

       # Create point cloud
        point_clouds = [[]] * num_cells # initialize list of point clouds
        for z in range(num_layers):
            layer = imarray[z, :, :] # select layer

            for c in range(1, num_cells):
                matching_pixels = np.where(layer == c) # find pixels with current cell label
                point_cloud = np.column_stack(matching_pixels) # add pixels to point cloud

                point_cloud = point_cloud.astype(float)  # convert to float to handle non-integer coordinates
                point_cloud[:, 0] -= height / 2
                point_cloud[:, 1] -= width / 2
                point_cloud = np.hstack((point_cloud, np.full((point_cloud.shape[0], 1), z)))  # Add z-coordinate
                
                point_clouds[c-1].append(point_cloud)
        
        clouds = [None] * num_cells
        for c in range(1, num_cells):
            clouds[c-1] = pv.PolyData(np.concatenate(point_clouds[c-1])) # combine layers into one and convert to polydata

       # Create mesh
        mesh = clouds[0].delaunay_3d(alpha=3, tol=0.1, offset=2.5).extract_geometry() # use delaunay to create mesh, alpha variable dictates how close the points have to be to get connected
        # mesh = pv.wrap(combined_point_cloud).reconstruct_surface() # use (poisson?) surface reconstruction to create mesh (not working)
        mesh.plot()
        # mesh.save(target_file)


    #     # Perform mesh smoothing
    #     smoother = vtk.vtkSmoothPolyDataFilter()
    #     smoother.SetInputData(mesh)
    #     smoother.SetNumberOfIterations(500)
    #     smoother.Update()
    #     smoothed_mesh = smoother.GetOutput() # get the smoothed mesh
    #     smoothed_mesh_pv = pv.wrap(smoothed_mesh) # convert the VTK data to a PyVista mesh

    #     # plotter = pv.Plotter() # create PyVista plotter
    #     # plotter.add_mesh(smoothed_mesh_pv) # add smoothed mesh to plotter
    #     # plotter.show()

    #     smooth = mesh.smooth(n_iter=5000)
    #     # smooth.plot()
    #     smooth_taubin = mesh.smooth_taubin(n_iter=5000, pass_band=0.5)
    #     # smooth_taubin.plot()


    #     conn = smoothed_mesh_pv.connectivity(largest=False) # get connectivity of mesh
    #     # conn.plot()
    #     # conn.save(target_folder + '/connectivities/' + os.path.splitext(filename)[0].split('_')[0] + '_conn.stl')

    #     bodies = conn.split_bodies() # seperate cells
    #     bodiesPolyData = bodies.as_polydata_blocks()
    #     for body in bodiesPolyData:
    #         if body.n_cells > 1: # filter degenerate bodies

    #             body.plot()
    #             vtk.vtkFillHolesFilter(body)
    #             body.plot()

    #             enclosed_body = body.select_enclosed_points(body, check_surface=False)
    #             # print(enclosed_body['SelectedPoints'])
    #             # print(body)
    #             print(enclosed_body)
    #             enclosed_body.plot()
    #     #         body.plot()
    #     #         if not os.path.exists(target_folder + '/bodies/' + os.path.splitext(filename)[0].split('_')[0]):
    #     #             os.mkdir(target_folder + '/bodies/' + os.path.splitext(filename)[0].split('_')[0])
    #     #         body.save(target_folder + '/bodies/' + os.path.splitext(filename)[0].split('_')[0] + '/body'+str(bodiesPolyData.index(body))+'.stl')
    #     # bodies.plot()
    
        break # uncomment to create only 1 mesh
