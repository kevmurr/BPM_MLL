import config as cf
import numpy as np
def wedged_mll_x(n_layer,focallength,z,wavelength=cf.wavelength):
    x_val=np.sqrt(n_layer*focallength*wavelength+n_layer**2*wavelength**2/4)*(1-z/(2*focallength))
    return(x_val)
def mk_wedged_mll(z_val,N_px=cf.N_px,offset_x=0,f=cf.f,pxsize=cf.pxsize):
    #this function creates a slice along x of a wedged mll
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
def mk_grating(N_layers,period,N_px=cf.N_px,offset_x=0,pxsize=cf.pxsize):
    result_arr=np.zeros((N_px)).astype("complex")
    N_px_layer=int(0.5*period/pxsize)
    if N_px<N_px_layer*N_layers:
        print("Warning: Not enough pixels chosen. Need at least %s"%(N_px_layer*N_layers))
    else:
        for i in range (0,N_layers,1):
            if i%2==0:
                result_arr[i*N_px_layer:(i+1)*N_px_layer]=cf.delta_1+1j*cf.beta_1
            else:
                result_arr[i*N_px_layer:(i+1)*N_px_layer]=cf.delta_2+1j*cf.beta_2
    return(result_arr)
def mk_plane_wave(N_px=cf.N_px,Amp=1,theta=0,wavelength=cf.wavelength,pxsize=cf.pxsize):
    #theta in rad
    kx=2*np.pi/wavelength*np.sin(theta)
    x_arr=np.linspace(0,N_px*pxsize,N_px)
    phase=(kx*x_arr)%(2*np.pi)
    plane_wave=Amp*np.exp(1j*phase)
    return(plane_wave)
    
def mk_bulk(delta_1=0,beta_1=0,N_px=cf.N_px):
    opt_const=delta_1*np.ones((N_px))+1j*beta_1*np.ones((N_px))
    return(opt_const)

def mk_slit(size=cf.slits_size,delta=cf.slits_delta,beta=cf.slits_beta,offset=cf.slit_offset,N_px=cf.N_px,pxsize=cf.pxsize):
    size_px=int(size/pxsize)
    offset_px=int(offset/pxsize)
    slit=np.ones((N_px)).astype("complex")
    slit=slit*delta+1j*beta
    if offset_px+size_px>N_px:
        slit[offset_px:]=np.zeros((N_px-offset_px))
    else:
        slit[offset_px:(offset_px+size_px)]=np.zeros((size_px))
    return(slit)
