def R(view_direction):
    import numpy as np
    S=np.sin(view_direction)
    C=np.cos(view_direction)
    mat = np.array([(S[2]*S[1]*C[0]) -(C[2]*S[0]), (S[2]*S[1]*S[0]) +(C[2]*C[0]), S[2]*C[1], (C[2]*S[1]*C[0])+(S[2]*S[0]), (C[2]*S[1]*S[0])-(S[1]*C[0]), C[2]*C[1], C[1]*C[0], C[1]*S[0], -1*S[1]]).reshape(3,3)
    mat[:2, :] = -mat[:2, :]

    return mat