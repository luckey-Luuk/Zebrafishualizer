"""
This script creates point clouds and meshes of the cells and frame in the first number of tif files (frames) in a specific folder 
and plots and/or saves the meshes to a specific location.
"""

# import sys #TODO: run from command line
import os # file handling
import numpy as np # arrays
import tifffile # reading tif files
import pyvista as pv # generating meshes
import pymeshfix as mf # improving meshes
# from trimesh import repair #TODO: check if this library is useful


def plot_mesh(mesh, clouds=[], plot_cloud=False, text="description not provided"):
    """
    Plot a mesh and its associated point clouds.

    Parameters
    ----------
    mesh : pyvista.PolyData
        mesh to plot
    clouds : list
        point clouds belonging to mesh
    plot_cloud : bool (optional)
        whether to plot point clouds
    text : str (optional)
        description of plot
    
    Returns
    -------
    None
    """
    pl = pv.Plotter()
    pl.add_text(text)
    pl.add_mesh(mesh)
    if plot_cloud:
        for points in clouds:
            if points:
                pl.add_points(points.points, color='red', point_size=3, style='points_gaussian', emissive=False)
    pl.show()


def save_mesh(mesh, foldername, filename, overwrite=False):
    """
    Save mesh to a file in a specific location.

    Parameters
    ----------
    mesh : pyvista.PolyData
        mesh to save
    foldername : str
        folder to save mesh to
    filename : str
        name of file
    overwrite : bool (optional)
        whether to overwrite existing file

    Returns
    -------
    None
    """
    if not os.path.exists(foldername): # create folder if it doesn't exist
        os.makedirs(foldername)
    elif os.path.exists(foldername + '/' + filename + '.stl'): # check if file needs to be overwritten
        if overwrite:
            os.remove(foldername + '/' + filename + '.stl')
        else:
            return
    mesh.save(foldername + '/' + filename + '.stl') # save mesh


def create_pointclouds(tif):
    """
    Read a tif file and create point clouds of each cell in the tif file (1 frame).

    Parameters
    ----------
    tif : str
        path to tif file
        
    Returns
    -------
    clouds : list
        list of point clouds
    min_cell : int
        lowest cell label
    max_cell : int
        highest cell label
    """
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


def create_frame_meshes(pointclouds, min_cell, max_cell, save_folder, save_name, plot_cells=False, plot_frames=False, plot_points=False, overwrite=False):
    """
    Create meshes of each cell in a list of point clouds and combine them into one mesh for the whole frame (1 tif file),
    then plot and/or save them to a specific location.

    Parameters
    ----------
    pointclouds : list
        list of point clouds belonging to the same frame
    min_cell : int
        lowest cell label
    max_cell : int
        highest cell label
    save_folder : str
        folder to save meshes to
    save_name : str
        base name for saving mesh
    plot_cells : bool (optional)
        whether to plot each cell
    plot_frames : bool (optional)
        whether to plot the frame
    plot_points : bool (optional)
        whether to plot point clouds belonging to the meshes
    overwrite : bool (optional)
        whether to overwrite existing files

    Returns
    -------
    None
    """
    frame = pv.PolyData() # initialize mesh with all cells

    #create mesh of each cell
    for c in range(min_cell, max_cell+1):
        if pointclouds[c]:
            # cell = clouds[c].delaunay_3d(alpha=3, tol=0.1, offset=2.5).extract_geometry() # use delaunay to create mesh
            cell = pointclouds[c].reconstruct_surface(sample_spacing=1) # use surface reconstruction to create mesh
            # cell = cell.delaunay_3d(alpha=3, tol=0.1, offset=2.5).extract_geometry() # use delaunay on mesh

            #Fix mesh TODO: check if this is necessary
            meshfix = mf.MeshFix(cell)
            meshfix.repair()
            cell = meshfix.mesh

            smoothed_cell = cell.smooth_taubin(n_iter=50, pass_band=0.1) # smooth mesh

            #Save and plot cell mesh
            if plot_cells:
                plot_mesh(smoothed_cell, [pointclouds[c]], plot_points, save_name + '-' + str(c))

            save_mesh(smoothed_cell, save_folder + '/' + save_name, save_name + '-' + str(c), overwrite)

            frame = frame.merge(smoothed_cell) # add cell mesh to frame mesh

    #Save and plot frame mesh
    if plot_frames:
        plot_mesh(frame, pointclouds, plot_points, save_name)

    save_mesh(frame, save_folder, save_name, overwrite)


def create_meshes(source, save_folder, plot_cells=False, plot_frames=False, plot_points=False, overwrite=False, n_frames=np.inf):
    """
    Create point clouds and meshes of the cells and frame in the first number of tif files (frames) in a specific folder 
    and plot and/or save the meshes to a specific location.

    Parameters
    ----------
    source : str
        folder with tif files
    save_folder : str
        folder to save meshes to
    plot_cells : bool (optional)
        whether to plot each cell
    plot_frames : bool (optional)
        whether to plot each frame
    plot_points : bool (optional)
        whether to plot point clouds belonging to the meshes
    overwrite : bool (optional)
        whether to overwrite existing files
    n_frames : int (optional)
        maximum number of frames to create meshes of
    """
    for filename in os.listdir(source):
        tif = os.path.join(source, filename) # get file path
        if not tif.endswith(".tif"): # check if file is a tif file
            print("Not a tif file: " + tif)
            return
            #TODO: check if tifs have the same dimensions
        else:
            shortened_filename = os.path.splitext(filename)[0].split('_')[0] # shorten filename for saving

            pointclouds, min_cell, max_cell = create_pointclouds(tif) # create point clouds from tif
            create_frame_meshes(pointclouds, min_cell, max_cell, save_folder, shortened_filename, plot_cells, plot_frames, plot_points, overwrite) # create meshes from point clouds

        n_frames -= 1
        if n_frames <= 0: # stop if maximum number of frames is reached
            break


if __name__ == "__main__":
    # source = sys.argv[1]
    # save_folder = sys.argv[2]
    source      = "./Data/convertedToImagej/20190701--2_inter_29layers_mask_imagej" #folder with labeled imagej tif files
    save_folder = "./Data/meshes/20190701--2" #folder to save mesh files
    plot_cells  = True #plot each individual cell
    plot_frames = True #plot whole frames
    plot_points = False #plot point clouds
    overwrite   = False #overwrite existing files
    n_frames    = 2 #np.inf #maximum number of frames to create meshes of

    create_meshes(source, save_folder, plot_cells, plot_frames, plot_points, overwrite, n_frames)

    # python3 mesh.py Data/convertedToImagej/20190701--2_inter_29layers_mask_imagej Data/meshes/20190701--2
