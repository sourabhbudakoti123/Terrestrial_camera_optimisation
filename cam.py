from principal_point import principal_point as pp
from rotation_matrix import R as rm
def cam(cam_location,img_size,view_direction,F):
    import math 
    import numpy as np

    if(len(img_size)<2):
        print('Kharab ya galat hai ye image')
        return
    else :
        dir = []
        for i in view_direction:
            dir.append((i * math.pi)/180)
        vd= np.array(dir)
        
        c = pp(cam_location)

        k=np.array([0,0,0,0,0,0])
        p=np.array([0,0])

        R=rm(vd)

        full_model = [cam_location,img_size,view_direction,F,c,k,p]
        return {'camera location': cam_location, 'image size': img_size, 'view direction': view_direction, 'f':F, 'c':c, 'Rcoeff':k, 'Tcoeff': p, 'Rotational matrix':R,'Full Model': full_model}