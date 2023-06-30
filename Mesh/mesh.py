import os # file handling
import numpy as np # arrays
import tifffile # reading tif files
import pyvista as pv # generating meshes
import pymeshfix as mf # improving meshes
# from trimesh import repair #TODO: check if this library is useful


def save_mesh(mesh, foldername, filename, overwrite=False):
    if not os.path.exists(foldername): # create folder if it doesn't exist
        os.makedirs(foldername)
    elif os.path.exists(foldername + '/' + filename + '.stl'): # check if file needs to be overwritten
        if overwrite:
            os.remove(foldername + '/' + filename + '.stl')
        else:
            return
    mesh.save(foldername + '/' + filename + '.stl') # save mesh


#Define folders
source = "Data/convertedToImagej/20190701--2_inter_29layers_mask_imagej" # folder containing labeled tif files
target_folder = "Data/meshes/20190701--2" # folder to save mesh files


for filename in os.listdir(source):
    shortened_filename = os.path.splitext(filename)[0].split('_')[0]

   #Read tif file
    f = os.path.join(source, filename) # get file path
    if not f.endswith(".tif"): # check if file is a tif file
        print("Not a tif file: " + f)
        continue
        #TODO: check if tifs have the same dimensions
    else:
        imarray = np.array(tifffile.imread(f)) # read tif file
        num_layers, height, width = imarray.shape[0], imarray.shape[1], imarray.shape[2] # initialize number of layers, height and width
        min_cell = sorted(set(imarray.flatten()))[1] # get lowest cell label (exclude empty space)
        max_cell = imarray.max() # get highest cell label


       #Create point clouds
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


       #Create mesh
        frame = pv.PolyData() # initialize mesh with all cells

       #create mesh of each cell
        for c in range(min_cell, max_cell+1):
            if clouds[c]:
                # cell = clouds[c].delaunay_3d(alpha=3, tol=0.1, offset=2.5).extract_geometry() # use delaunay to create mesh
                cell = clouds[c].reconstruct_surface(sample_spacing=1) # use surface reconstruction to create mesh
                # cell = cell.delaunay_3d(alpha=3, tol=0.1, offset=2.5).extract_geometry() # use delaunay on mesh

               #Fix mesh TODO: check if this is necessary
                # meshfix = mf.MeshFix(cell)
                # meshfix.repair()
                # cell = meshfix.mesh

                smoothed_cell = cell.smooth_taubin(n_iter=50, pass_band=0.1) # smooth mesh

               #Save and plot cell mesh
                # smoothed_cell.plot()
                save_mesh(smoothed_cell, target_folder + '/' + shortened_filename, shortened_filename + '-' + str(c))

                frame = frame.merge(smoothed_cell) # add cell mesh to frame mesh
        
       #Save and plot frame mesh
        frame.plot()
        save_mesh(frame, target_folder, shortened_filename)

        break #uncomment to create only meshes of first tif file
