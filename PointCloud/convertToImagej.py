import imagej
ij = imagej.init()

directory = "C:/Users/Eigenaar/Documents/universiteit/jaar 3/Bachelor eindproject/git/Zebrafishualizer/Data/20190701--2_inter_29layers_mask/"

imp = ij.io().open("C:/Users/Eigenaar/Documents/universiteit/jaar 3/Bachelor eindproject/git/Zebrafishualizer/Data/3D tracking data to visualize/20190701--2_inter_29layers_mask_3a/20190701--20000_M3a_Step92.tif")
ij.io().save(imp, "C:/Users/Eigenaar/Documents/universiteit/jaar 3/Bachelor eindproject/git/Zebrafishualizer/Data/20190701--2_inter_29layers_mask_imagej/20190701--20000_M3a_Step92_imagej.tif")
