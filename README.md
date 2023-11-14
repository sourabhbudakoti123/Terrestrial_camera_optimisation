# Terrestrial_camera_optimisation
camera.py: This is the main file where all functions and operations related to cameras are executed.

cam.py: This file contains 20 critical parameters and information such as 'camera location,' 'image size,' 'view direction,' 'f' ( focal length), 'c' (principal point), 'Rcoeff' (rotation coefficient), 'Tcoeff' (translation coefficient), 'Rotational matrix,' and the 'Full Model.' 

focal.py: This file converts the real-world focal length to pixel units.

principal_point.py: It provides the 'c' value, indicating the center of the image. 

rotation_matrix.py: This file computes and provides the rotation matrix ('R') using mathematical formulae. 

gcp_txt_to_matrix.py: It processes text files containing Ground Control Points (GCPs) and converts them into a matrix format. 
project.py: This fike utilizes information from the cameras (derived from Photogrammetry cam.py) to transform the 3D information captured by the cameras into a 2D representation.

raw_optimise_cam.py: It is not completed but its work is to return optimised parameters
