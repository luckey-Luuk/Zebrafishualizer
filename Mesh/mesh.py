import os
import numpy as np
import tifffile
import pyvista as pv
import pymeshfix as mf
import vtk
# import pymeshfix # won't work, when it "fixes" it gets rid of more than half of the points
# import trimesh # won't work, runtime error when it "fixes" when it does show something it does not appear altered
# from trimesh import repair

def save_mesh(mesh, foldername, filename, overwrite=False):
    if not os.path.exists(foldername): # create folder if it doesn't exist
        os.makedirs(foldername)
    elif os.path.exists(foldername + '/' + filename + '.stl'): # check if file needs to be overwritten
        if overwrite:
            os.remove(foldername + '/' + filename + '.stl')
        else:
            return
    mesh.save(foldername + '/' + filename + '.stl') # save mesh

source = "Data/convertedToImagej/20190701--2_inter_29layers_mask_imagej" # folder containing labeled tif files
target_folder = "Data/meshes/20190701--2" # folder to save mesh files


for filename in os.listdir(source):
    shortened_filename = os.path.splitext(filename)[0].split('_')[0]

   # Read tif file
    f = os.path.join(source, filename) # get file path
    if not f.endswith(".tif"): # check if file is a tif file
        print("Not a tif file: " + f)
        continue
        #TODO: check if tifs have the same shape
    else:
        imarray = np.array(tifffile.imread(f)) # read tif file
        num_layers, height, width = imarray.shape[0], imarray.shape[1], imarray.shape[2] # initialize number of layers, height and width
        min_cell = sorted(set(imarray.flatten()))[1] # get lowest cell label (exclude empty space)
        max_cell = imarray.max() # get highest cell label


       # Create point cloud
        # point_clouds = [ [] for _ in range(num_cells) ]
        point_clouds = [ [] for _ in range(max_cell+1) ]
        for z in range(num_layers):
            layer = imarray[z, :, :] # select layer

            for c in range(min_cell, max_cell+1):
                matching_pixels = np.where(layer == c) # find pixels with current cell label
                point_cloud = np.column_stack(matching_pixels).astype(float) # add pixels to point cloud and convert to float to handle non-integer coordinates
                point_cloud[:, 0] -= height / 2
                point_cloud[:, 1] -= width / 2
                point_cloud = np.hstack((point_cloud, np.full((point_cloud.shape[0], 1), z)))  # Add z-coordinate)
                
                point_clouds[c].append(point_cloud)

        clouds = [None] * (max_cell+1)
        for c in range(min_cell, max_cell+1):
            if point_clouds[c]:
                clouds[c] = pv.PolyData(np.concatenate(point_clouds[c])) # combine layers into one and convert to polydata


       # Create mesh
        frame = pv.PolyData() # initialize mesh with all cells

       # create mesh of each cell
        for c in range(min_cell, max_cell+1):
            if clouds[c]:
                # cell = clouds[c].delaunay_3d(alpha=3, tol=0.1, offset=2.5).extract_geometry() # use delaunay to create mesh, alpha variable dictates how close the points have to be to get connected
                cell = clouds[c].reconstruct_surface(sample_spacing=1) # use surface reconstruction to create mesh
                # cell = cell.delaunay_3d(alpha=3, tol=0.1, offset=2.5).extract_geometry() # use delaunay on mesh

               # Fix mesh
                meshfix = mf.MeshFix(cell)
                meshfix.repair()
                repaired = meshfix.mesh

               # Perform mesh smoothing
                smoother = vtk.vtkSmoothPolyDataFilter()
                smoother.SetInputData(repaired)
                smoother.SetNumberOfIterations(500)
                smoother.Update()
                smoothed_cell = smoother.GetOutput() # get the smoothed mesh
                smoothed_cell_pv = pv.wrap(smoothed_cell) # convert the VTK data to a PyVista mesh

                # plotter = pv.Plotter() # create PyVista plotter
                # plotter.add_mesh(smoothed_cell_pv) # add smoothed mesh to plotter
                # plotter.show()

                # smooth = repaired.smooth(n_iter=5000)
                # smooth.plot()
                # smooth_taubin = repaired.smooth_taubin(n_iter=5000, pass_band=0.5)
                # smooth_taubin.plot()

               # Save cell mesh
                save_mesh(smoothed_cell_pv, target_folder + '/' + shortened_filename, shortened_filename + '-' + str(c))

                frame = frame.merge(smoothed_cell_pv) # add cell mesh to frame mesh
        
        # frame.plot()
        save_mesh(frame, target_folder, shortened_filename)

        break # uncomment to create only meshes of first tif file


    #     conn = smoothed_cell_pv.connectivity(largest=False) # get connectivity of mesh
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
