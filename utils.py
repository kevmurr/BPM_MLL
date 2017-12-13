import numpy as np
import cmath
import config as cf
def get_phase(arr):
    phase=np.zeros_like(arr)
    for i in range(0,arr.shape[0],1):
        phase[i]=cmath.phase(arr[i])
    phase=np.real(phase)
    return(phase)
def check_directory(path):
    import os
    val=os.path.exists(str(path))
    if val==True:
        print("Directory exists!")
    else:
        return IOError("Given save_directory doesn't exist! Please choose another one")
    
    
######################################
#OLD FUNCTIONS
def mk_wedged_mll_andr(z,sigma=1,N_px=cf.N_px,pxsize=cf.pxsize,f=cf.f,wavelength=cf.wavelength,n_begin=cf.n_begin,n_end=cf.n_end,delta_1=cf.delta_1,delta_2=cf.delta_2,beta_1=cf.beta_1,beta_2=cf.beta_2):
    #THIS IS THE FIRST BETA OF A WEDGED MLL IN THIS PROGRAM. TESTING IS NEEDED
    #sigma controls the sharpness of the edges. 0 means step function, 1 means sine
    #This function makes a wedged mll with possible smoothing of interfaces between layers
    conv=2*np.pi/wavelength
    z=z*conv
    x=conv*np.linspace(0,N_px*pxsize,N_px)
    #drmin=wedged_mll_x(n_layer=n_begin+1,focallength=f,z=z,wavelength=cf.wavelength)-wedged_mll_x(n_layer=n_begin,focallength=f,z=z,wavelength=cf.wavelength)
    #drmax=wedged_mll_x(n_layer=n_begin+1,focallength=f,z=z,wavelength=cf.wavelength)-wedged_mll_x(n_layer=n_begin,focallength=f,z=z,wavelength=cf.wavelength)
    xmin=wedged_mll_x(n_layer=n_begin,focallength=f,z=z,wavelength=cf.wavelength)*conv
    xmax=wedged_mll_x(n_layer=n_end,focallength=f,z=z,wavelength=cf.wavelength)*conv
    #log_x=(x)<xmax and (x)>xmin
    log_x=np.bitwise_and(x<xmax,x>xmin).astype("int")
    #log_x=np.ones_like(log_x)
    a=1-z*1/(2*f*(1+n_end*wavelength/8/f))#shrinkage factor
    L=np.sqrt(np.square(x)/a**2+f**2)-f
    eps1=delta_1+1j*beta_1
    eps2=delta_2+1j*beta_2
    modeps=1/np.pi*((np.arctan(1/sigma*np.sin(L))+np.pi/2)*eps1+(-np.arctan(1/sigma*np.sin(L))+np.pi/2)*eps2)
    eps=np.multiply(modeps,log_x)
    return(eps)
def mk_flat_mll(z_val,N_px=cf.N_px,offset_x=0,f=cf.f,pxsize=cf.pxsize):
    #this function creates a slice along x of a wedged mll (better used for a flat mll!)
    #offset_x is the offset of the coordinate system
    x_arr=np.linspace(0,N_px*pxsize,N_px)
    #initial check of input sizes
    #----
    x_end=wedged_mll_x(n_layer=cf.n_end,focallength=f,z=z_val)
    #x_begin=wedged_mll_x(n_layer=cf.n_begin,focallength=f,z=z_val)
    sugg_px=int(x_end/pxsize)
    if x_end>x_arr[-1]:
        print("WARNING:  the input pixelsize/ number of pixel is too small for the simulated MLL. Please increase the size. You need at least %s pixels" %sugg_px)
    #i_begin=np.argmin(np.abs(x_begin-x_arr))
    #i_end=x_arr.shape[0]
    result_arr=np.zeros_like(x_arr)+1j*np.zeros_like(x_arr) #this writes a vacuum array
    for i_layer in range(cf.n_begin,cf.n_end,1):
        x_now=wedged_mll_x(n_layer=i_layer,focallength=f,z=z_val)
        i_px_bot=np.argmin(np.abs(np.subtract(x_arr,x_now)))
        x_next=wedged_mll_x(n_layer=i_layer+1,focallength=f,z=z_val)
        i_px_top=np.argmin(np.abs(np.subtract(x_arr,x_next)))
        if i_layer%2==0:
            result_arr[i_px_bot:i_px_top]=np.ones((i_px_top-i_px_bot))*cf.delta_1+1j*cf.beta_1
        else:
            result_arr[i_px_bot:i_px_top]=np.ones((i_px_top-i_px_bot))*cf.delta_2+1j*cf.beta_2
        #now apply offset
    offset_px=round(offset_x/pxsize)
    sample_arr=result_arr[:i_px_top]
    if i_px_top+offset_px>N_px:
        result_arr=np.zeros_like(x_arr)+1j*np.zeros_like(x_arr)
        modlength=N_px-offset_px
        sample_arr_mod=sample_arr[:modlength]
        result_arr[offset_px:]=sample_arr_mod
    else:
        result_arr=np.zeros_like(x_arr)+1j*np.zeros_like(x_arr)
        result_arr[offset_px:offset_px+i_px_top]=sample_arr
    return(result_arr)