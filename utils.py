import numpy as np
import cmath
def get_phase(arr):
    phase=np.zeros_like(arr)
    for i in range(0,arr.shape[0],1):
        phase[i]=cmath.phase(arr[i])
    phase=np.real(phase)
    return(phase)