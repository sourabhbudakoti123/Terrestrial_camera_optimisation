def principal_point(img_size):
    import numpy as np
    c=[]
    for i in img_size:
        c.append((i+1)/2)
    C=np.array(c)
    return C