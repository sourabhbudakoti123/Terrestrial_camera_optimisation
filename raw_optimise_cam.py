def optimize_cam(cam,xyz,uv,freeparams,img_path,optmethod='trf',show = False):
    import numpy as np
    from scipy import optimize
    from PIL import Image
    from plot_residual import plotResiduals
    from plot_residual import readImg

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
    params= []
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


    if len(params) != 0:
      # acha sa optimiser chaiye abhi!!
        out = optimize.least_squares(ResidualUV, params, method=optmethod, 
                            verbose=2, max_nfev=10000, 
                            args=(stable, paramix, xyz,uv)) 
        if out.success is True:

            print('\noptimization is successfull')

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
            cam_optimized = {'camera location': fullmodel0[0], 'image size': fullmodel0[1], 'view direction': fullmodel0[2], 'f':fullmodel0[3], 'c':fullmodel0[4], 'Rcoeff':fullmodel0[5], 'Tcoeff': fullmodel0[6], 'Full Model': fullmodel0}
            final_cam = const_cam_sec(cam_optimized['camera location'], cam_optimized['image size'], cam_optimized['view direction'], cam_optimized['f'],cam_optimized['c'],cam_optimized['Rcoeff'],cam_optimized['Tcoeff'])
            
            GCPxyz_proj1, depth, inframe = project(final_cam,xyz)


    



    


    

