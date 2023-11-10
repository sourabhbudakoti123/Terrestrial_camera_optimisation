import numpy as np
from rotation_matrix import R as R
def project(cam, xyz):
    #orientation shi krne ke liye
    if(xyz.shape[1]>3):
        xyz=xyz.T
    temp_xyz = xyz
    #shifting of orgin to camera center
    xyz= xyz-cam['camera location']
    r = R(cam['view direction'])
    #xyz.transpose(r)
    xyz=np.dot(xyz,r.T)
    #x aur y ko z se divide kr rhe hai aur error aa rha tha reshape ke karan
    xy = xyz[:,0:2]/xyz[:,2].reshape(-1,1)
    print(xy)
    #idhar hoga distortion wali maths isliye rcoeff aur tcoeff dekh rhe hai hum
    if np.any(cam['Rcoeff'] != 0) or np.any(cam['Tcoeff'] != 0):
        r2 = np.sum(xy**2,axis=1)
        r2[r2>4] = 4

        if np.any(cam['Rcoeff'][2:6] != 0):
             a = (1 + cam['Rcoeff'][0] * r2 + cam['Rcoeff'][1] * r2**2 + cam['Rcoeff'][2] * r2**3) / (1 + cam['Rcoeff'][3] * r2 + cam['Rcoeff'][4] * r2**2 + cam['Rcoeff'][5] * r2**3)
             
        else:
            a = 1 + cam['Rcoeff'][0] * r2 + cam['Rcoeff'][1] * r2**2 + cam['Rcoeff'][2] * r2**3

        #sare x ko sare y se multpily kr diya h
        xty = xy[:,0] * xy[:,1]

        #again maths from notes!!!
        xy = np.column_stack([
            a * xy[:, 0] + 2 * cam['Tcoeff'][0] * xty + cam['Tcoeff'][1] * (r2 + 2 * xy[:, 0]**2),
            a * xy[:, 1] + 2 * cam['Tcoeff'][0] * xty + cam['Tcoeff'][1] * (r2 + 2 * xy[:, 1]**2)
        ])




    #yahan pe kuch modifcations on xy aur depth aur inframe aayenge
    #some mathematics to calculate uv from xy
    uv = np.column_stack([
        cam['f'][0] * xy[:, 0] + cam['c'][0],
        cam['f'][1] * xy[:, 1] + cam['c'][1]
    ])

    #koi bhi z agar zero ho to use null krdo lekin kyun???
    uv[temp_xyz[:, 2] <= 0, :] = np.nan

          #ye to chap diye samajhne hai abhi!!
    depth = xyz[:, 2] if len(xyz.shape) > 1 else None
    inframe = (depth > 0) & (uv[:, 0] >= 1) & (uv[:, 1] >= 1) & (uv[:, 0] <= cam['image size'][1]) & (uv[:, 1] <= cam['image size'][0]) if len(xyz.shape) > 1 else None

    return uv,depth,inframe
