# import sys #TODO: run from command line
import os # file handling
import numpy as np # arrays
import tifffile # reading tif files
import pyvista as pv # generating meshes
import pymeshfix as mf # improving meshes
# from trimesh import repair #TODO: check if this library is useful


def plot_mesh(mesh, clouds, plot_cloud=False, text="description not provided"):
    pl = pv.Plotter()
    pl.add_text(text)
    pl.add_mesh(mesh)
    if plot_cloud:
        for points in clouds:
            if points:
                pl.add_points(points.points, color='red', point_size=3, style='points')#_gaussian', emissive=True, point_size=5)
    pl.show()


def save_mesh(mesh, foldername, filename, overwrite=False):
    if not os.path.exists(foldername): # create folder if it doesn't exist
        os.makedirs(foldername)
    elif os.path.exists(foldername + '/' + filename + '.stl'): # check if file needs to be overwritten
        if overwrite:
            os.remove(foldername + '/' + filename + '.stl')
        else:
            return
    mesh.save(foldername + '/' + filename + '.stl') # save mesh


def create_mesh(save_name, save_folder, plot_cells=False, plot_frames=False, plot_points=False, overwrite=False):
    shortened_filename = os.path.splitext(save_name)[0].split('_')[0]

    #Read tif file
    f = os.path.join(source, save_name) # get file path
    if not f.endswith(".tif"): # check if file is a tif file
        print("Not a tif file: " + f)
        return
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
                meshfix = mf.MeshFix(cell)
                meshfix.repair()
                cell = meshfix.mesh

                smoothed_cell = cell.smooth_taubin(n_iter=50, pass_band=0.1) # smooth mesh

                #Save and plot cell mesh
                if plot_cells:
                    plot_mesh(smoothed_cell, [clouds[c]], plot_points, shortened_filename + '-' + str(c))

                save_mesh(smoothed_cell, save_folder + '/' + shortened_filename, shortened_filename + '-' + str(c), overwrite)

                frame = frame.merge(smoothed_cell) # add cell mesh to frame mesh

        #Save and plot frame mesh
        if plot_frames:
            plot_mesh(frame, clouds, plot_points, shortened_filename)

        save_mesh(frame, save_folder, shortened_filename, overwrite)


def create_meshes(source, save_folder, plot_cells=False, plot_frames=False, plot_points=False, overwrite=False, n_meshes=np.inf):
    for filename in os.listdir(source):
        create_mesh(filename, save_folder, plot_cells, plot_frames, plot_points, overwrite)

        n_meshes -= 1
        if n_meshes <= 0:
            break


if __name__ == "__main__":
    # source = sys.argv[1]
    # save_folder = sys.argv[2]
    source      = "Data/convertedToImagej/20190701--2_inter_29layers_mask_imagej" # folder containing labeled tif files
    save_folder = "Data/meshes/20190701--2" # folder to save mesh files
    plot_cells  = False # plot each individual cell
    plot_frames = True # plot whole frames
    plot_points = True # plot point clouds
    overwrite   = False # overwrite existing files
    n_meshes    = np.inf # maximum number of meshes to create

    create_meshes(source, save_folder, plot_cells, plot_frames, plot_points, overwrite, n_meshes)

    # python3 mesh.py Data/convertedToImagej/20190701--2_inter_29layers_mask_imagej Data/meshes/20190701--2
