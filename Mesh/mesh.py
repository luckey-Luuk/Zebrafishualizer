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
                pl.add_points(points.points, color='red', point_size=3, style='points_gaussian', emissive=False)
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


def create_pointclouds(tif):
    #TODO: get coordinates of cells if not saved already
    imarray = np.array(tifffile.imread(tif)) # read tif file
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

    return clouds, min_cell, max_cell


def create_cell_meshes(pointclouds, c, shortened_filename, save_folder, plot_cells=False, plot_frames=False, plot_points=False, overwrite=False):
    # cell_mesh = clouds[c].delaunay_3d(alpha=3, tol=0.1, offset=2.5).extract_geometry() # use delaunay to create mesh
    cell_mesh = pointclouds[c].reconstruct_surface(sample_spacing=1) # use surface reconstruction to create mesh
    # cell_mesh = cell_mesh.delaunay_3d(alpha=3, tol=0.1, offset=2.5).extract_geometry() # use delaunay on mesh

    #Fix mesh TODO: check if this is necessary
    meshfix = mf.MeshFix(cell_mesh)
    meshfix.repair()
    cell_mesh = meshfix.mesh

    smoothed_mesh = cell_mesh.smooth_taubin(n_iter=50, pass_band=0.1) # smooth mesh

    #Save and plot mesh
    if plot_cells:
        plot_mesh(smoothed_mesh, [pointclouds[c]], plot_points, shortened_filename + '-' + str(c))

    save_mesh(smoothed_mesh, save_folder + '/' + shortened_filename, shortened_filename + '-' + str(c), overwrite)


def create_frame_meshes(source, save_folder, plot_cells=False, plot_frames=False, plot_points=False, overwrite=False, n_frames=np.inf):
    for filename in os.listdir(source):
        tif = os.path.join(source, filename) # get file path
        if not tif.endswith(".tif"): # check if file is a tif file
            print("Not a tif file: " + tif)
            return
            #TODO: check if tifs have the same dimensions
        else:
            shortened_filename = os.path.splitext(filename)[0].split('_')[0] # shorten filename for saving

            pointclouds, min_cell, max_cell = create_pointclouds(tif) # create pointclouds from tif

            for cell in range(min_cell, max_cell+1): #create meshes for each cell
                if pointclouds[cell]:
                    create_cell_meshes(pointclouds, cell, shortened_filename, save_folder, plot_cells, plot_frames, plot_points, overwrite)

        n_frames -= 1
        if n_frames <= 0: # stop if maximum number of frames is reached
            break


if __name__ == "__main__":
    # source = sys.argv[1]
    # save_folder = sys.argv[2]
    source      = "./Data/convertedToImagej/20190701--2_inter_29layers_mask_imagej" #folder with labeled imagej tif files
    save_folder = "./Data/meshes/20190701--2" #folder to save mesh files
    plot_cells  = True #plot each individual cell
    plot_frames = False #plot whole frames
    plot_points = False #plot point clouds
    overwrite   = False #overwrite existing files
    n_frames    = 2 #np.inf #maximum number of frames to create meshes of

    create_frame_meshes(source, save_folder, plot_cells, plot_frames, plot_points, overwrite, n_frames)

    # python3 mesh.py Data/convertedToImagej/20190701--2_inter_29layers_mask_imagej Data/meshes/20190701--2
