def focal(focal_length,img_size,sensor_size):
    import numpy as np
    f=[]#defining list 
    #hum ab focal length ko pixels mai nikalenge

    for i in range(len(img_size)):
        f.append(img_size[i]*(focal_length/sensor_size[i]))
    
    F=np.array(f)
    return F
