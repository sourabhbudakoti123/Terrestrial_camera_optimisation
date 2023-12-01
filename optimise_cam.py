from rotation_matrix import R as rotation_mtx
from project import project as project
from cam import cam as cam1

def ResidualUV(params,stable,paramix,xyz,uv):
    import numpy as np

    #various cases according to the optimising conditions 
    #1 only optimizing the all parameters
    # if all(x in paramix for x in [2,5,6]):
        
    #     view_direction = params[0:3]
    #     k = params[3:9]
    #     p = params[9:]
    #     cam_loc = stable[0:3]
    #     imgsz = stable[3:5]
    #     f = stable[5:7]
    #     c = stable[7:] 
        
    #     # print("\n\n----3")

    #     #2 optimising f,c,rotation and translation coeff
    # elif all(x in paramix for x in [2,5]):
    #     view_direction = params[0:3]
    #     k = params[3:]
    #     cam_loc = stable[0:3]
    #     imgsz = stable[3:5]
    #     f = stable[5:7]
    #     c = stable[7:9]  
    #     p = stable[9:]
        
    #     # print("\n\n----2")

    #     #3 optimizing only view direction and camera location
    # elif all(x in paramix for x in [2,6]):
    #     view_direction = params[0:3]
    #     p = params[3:]
    #     cam_loc = stable[0:3]
    #     imgsz = stable[3:5]
    #     f = stable[5:7]
    #     c = stable[7:9]
    #     k = stable[9:]
        
    #     # print("\n\n----1")
    
    # elif all(x in paramix for x in [5,6]):
    #     k = params[0:6]
    #     p = params[6:]
    #     cam_loc = stable[0:3]
    #     imgsz = stable[3:5]
    #     view_direction = stable[5:8]
    #     f = stable[8:10]
    #     c = stable[10:]
        

    # #4 optimizing only view direction 
    # elif 2 in paramix:
    #     view_direction = params
    #     cam_loc = stable[0:3]
    #     imgsz = stable[3:5]
    #     f = stable[5:7]
    #     c = stable[7:9]
    #     k = stable[9:15]
    #     p = stable[15:]
    #     # print("\n\n----4")

    # elif 5 in paramix:
    #     k = params
    #     cam_loc = stable[0:3]
    #     imgsz = stable[3:5]
    #     view_direction = stable[5:8]
    #     f = stable[8:10]
    #     c = stable[10:12]
    #     p = stable[12:]

    # elif 6 in paramix:
    #     p = params
    #     cam_loc = stable[0:3]
    #     imgsz = stable[3:5]
    #     view_direction = stable[5:8]
    #     f = stable[8:10]
    #     c = stable[10:12]
    #     k = stable[12:]
    
    # else: 
    #     return 0
         
        # print("\n\n----5")

    # cam = cam_constructor(cam_loc, imgsz, view_direction, f)
    # print("\n\n camloc = ",cam_loc)
    # print("\n\n imgsz = ",imgsz)
    # print("\n\n viewdir= ",view_direction)
    # print("\n\n f = ",f)
    # print("\n\n c = ",c)
    # print("\n\n k = ",k)
    # print("\n\n p = ",p)


    if all(x in paramix for x in [0,2,3,4,5,6]):
        
        cam_loc = params[0:3]
        view_direction = params[3:6]
        f = params[6:8]
        c = params[8:10]
        k = params[10:16]
        p = params[16:]
        
        imgsz = stable
        
        # print("\n\n----3")

        #2 optimising f,c,rotation and translation coeff
    elif all(x in paramix for x in [3,4,5,6]):
        f = params[0:2]
        c = params[2:4]
        k = params[4:10]
        p = params[10:]
        
        cam_loc = stable[0:3]
        imgsz = stable[3:5]
        view_direction = stable[5:] 
        
        
        # print("\n\n----2")

        #3 optimizing only view direction and camera location
    elif all(x in paramix for x in [0,2]):
        cam_loc = params[0:3]
        view_direction = params[3:]
        
        
        imgsz = stable[0:2]
        f = stable[2:4]
        c = stable[4:6]
        k = stable[6:12]
        p = params[12:]
        
        # print("\n\n----1")
        

    #4 optimizing only view direction 
    elif 2 in paramix:
        view_direction = params

        cam_loc = stable[0:3]
        imgsz = stable[3:5]
        f = stable[5:7]
        c = stable[7:9]
        k = stable[9:15]
        p = stable[15:]
        # print("\n\n----4")
    
    else: 
        return 0

    
    #With the internal and external parameetrs from above form a camera object which will be the 
    # input for the project fuction
    cam = cam1(cam_loc, imgsz, view_direction, f)
    
    # print("\n\n\ncam in secondary ", cam)


    # cam_constructor(cam_loc, imgsz, view_direction, f):

    # calling the project function for the camera object described above 
    uv_projected,depth,inframe  = project(cam,xyz)
    #print('\n\n\n uv_projected  = ',uv_projected)

    #a list to store the squared difference between the project and actual 2d coordinates
    residual = []

    error = 0

    for i in range(len(uv_projected)):
        residual.append(np.sqrt((uv_projected[i][0]-uv[i][0])**2 + 
                                (uv_projected[i][1]-uv[i][1])**2))

        error += np.sqrt((uv_projected[i][0]-uv[i][0])**2 + 
                                (uv_projected[i][1]-uv[i][1])**2) 
        

    #converting list to array 
    #some iterations randomly to calibrate
    residual = np.array(residual)
    print("ERROR->")
    print(error)
    # print(params)
    print('\n\n\nresidual = ',residual)

    return residual
        



def optimize_cam(cam,xyz,uv,freeparams,img_path,optmethod='trf',show = False):
    import numpy as np
    from scipy import optimize
    from PIL import Image

    #checking whether the matrix xyz or uv contains any NAN values
    nanrows1 = np.array([np.any(np.isnan(row)) for row in xyz])
    nanrows2 = np.array([np.any(np.isnan(row)) for row in uv])


    #from xyz and uv delete those rows where nan values are there 
    xyz = np.delete(xyz, np.where(nanrows1), axis=0)
    uv = np.delete(uv, np.where(nanrows2), axis=0)

    GCPxyz_proj0,depth,inframe = project(cam, xyz)

    

    #extract the full model data from the cam dictionary using the key
    fullmodel0 = cam['Full Model']

    #create a boolean array in which True is when the freeparams value is 1
    freeparams = [True if value == 1 else False for value in freeparams]
 
    paramix = np.where(freeparams)[0]  # Find indices of True elements

    print("\n\n freeparams = ", freeparams)
    print("\n\n paramix = ", paramix)

    #defining two lists to store the variable and stable parameter accroding to the optimization criteria
    params = []
    stable = []

    for i in paramix:
        params.append(fullmodel0[i]) # appending those values in fullmodel0 whose indices are there in paramix

    if len(params) != 0:
        params = np.concatenate(params)   #making it  to a single array of individual numbers 
    
    # appending those values in fullmodel0 whose indices are not in paramix
    for i in range(len(fullmodel0)):
        if i in paramix:
            continue
        else:
            stable.append(fullmodel0[i])

    #making it  to a single array of individual numbers 
    stable = np.concatenate(stable)
    

    print("\n\n params =" , params)
    print("\n\n stable =" , stable)

    print("\n\n\n")


    #optimizing function
    if len(params) != 0:
        out = optimize.least_squares(ResidualUV, params, method=optmethod, 
                            verbose=2, max_nfev=10000, 
                            args=(stable, paramix, xyz, uv)) 
        print("^_^_^_^_^_^_^__^_^")
        # print(RMSE)
        print(out)

        #  ,options={'maxiter':5000},tol = 1e-4,

        # out = optimize.minimize(ResidualUV, params, 
        #                     args=(stable, paramix, xyz,uv))
        
        if out.success is True:

            print('\noptimization is successfull')
            # print("\n\n out = ", out)

            #based on the conditions update the optimized values the fullmodel0 list
            # if all(x in paramix for x in [2,5,6]):
            #     fullmodel0[2] = out.x[0:3]
            #     fullmodel0[5] = out.x[3:9]
            #     fullmodel0[6] = out.x[9:]
            

            # elif all(x in paramix for x in [2,5]):
            #     fullmodel0[2] = out.x[0:3]
            #     fullmodel0[5] = out.x[3:]

            # elif all(x in paramix for x in [2,6]):
            #     fullmodel0[2] = out.x[0:3]
            #     fullmodel0[6] = out.x[3:]
        
            # elif all(x in paramix for x in [5,6]):
            #     fullmodel0[5] = out.x[0:6]
            #     fullmodel0[6] = out.x[6:]

            # elif 2 in paramix:
            #     fullmodel0[2] = out.x

            # elif 5 in paramix:
            #     fullmodel0[5] = out.x
            # else:
            #     fullmodel0[6] = out.x


            if all(x in paramix for x in [0,2,3,4,5,6]):
                fullmodel0[0] = out.x[0:3]
                fullmodel0[2] = out.x[3:6]
                fullmodel0[3] = out.x[6:8]
                fullmodel0[4] = out.x[8:10]
                fullmodel0[5] = out.x[10:16]
                fullmodel0[6] = out.x[16:]
            

            elif all(x in paramix for x in [3,4,5,6]):
                fullmodel0[3] = out.x[0:2]
                fullmodel0[4] = out.x[2:4]
                fullmodel0[5] = out.x[4:10]
                fullmodel0[6] = out.x[10:]

            elif all(x in paramix for x in [0,2]):
                fullmodel0[0] = out.x[0:3]
                fullmodel0[2] = out.x[3:]
        
            else:
                fullmodel0[2] = out.x

            # print("\n\n full model after optimization  = ", fullmodel0)

            #defining a dictionary to store the new optimizd parametrs with their key
            cam_optimized = {'camera location': fullmodel0[0], 'image size': fullmodel0[1], 'view direction': fullmodel0[2], 'f':fullmodel0[3], 'c':fullmodel0[4], 'Rcoeff':fullmodel0[5], 'Tcoeff': fullmodel0[6], 'Full Model': fullmodel0}
        
            #Creating the optimized cam_object
            final_cam = cam1(cam_optimized['camera location'], cam_optimized['image size'], cam_optimized['view direction'], cam_optimized['f'])
            
            GCPxyz_proj1, depth, inframe = project(final_cam,xyz)

            print("\n\n GCPxyz_proj0 = ", GCPxyz_proj0)
            print("\n\n GCPxyz_proj1 = ", GCPxyz_proj1)
            print("\n\n uv = ", uv)

            return final_cam
        
        elif out == 0:
            print("\n\nThe specified optimiation is not supported")
        
        else: 
            print('\n\nOptimization not done due to max iteration')
            return 
    else:
        print("\n\nNo optimization is specified")
        return 
