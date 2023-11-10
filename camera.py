import numpy as np
from PIL import Image
from gcp_txt_to_matrix import save_txt_to_matrix as mtx
from focal import focal as fp
from cam import cam as cam
from project import project as project_from_3d_to_2d
# input de rhe hai 
focal_length = 30
sensor_size = np.array([22.0,14.7])
image_path = 'Camera_Optimization_Final-master/work/KR2_2014_11.JPG'# iska use hoga size 
                                                                    #nikalne mai 
img = Image.open(image_path)
image_size = np.array(img.size)
cam_loc = np.array([447948.820, 8759457.100, 407.092])

view_direction = [275.5354, 3.3047059, 8.5451739]

# provided the gcp data and corresponding u,v pixels 
gcp = 'Camera_Optimization_Final-master/work/KR2_2014.txt'
gcp_val=[]
gcp_val=mtx(gcp)
xyz = gcp_val[:,:3]
uv = gcp_val[:,3:]

f=fp(focal_length,image_size,sensor_size)
print("Focal length in pixels ->" ,f)


camA = {}
camA = cam(cam_loc,image_size,view_direction,f)
print("..........................")
uv,depth,inframe=project_from_3d_to_2d(camA,xyz)
print("..........................")
for key, value in camA.items():
    print(key, value)
    print('\n')
print(xyz)
print("ye hai xyz real world coordinates")
print('\n')
print(uv)
print("ye hai pixels coordinates")