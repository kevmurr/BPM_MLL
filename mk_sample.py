import config as cf
import numpy as np
from scipy.signal import square
from scipy.ndimage.filters import gaussian_filter
def wedged_mll_x(n_layer,focallength,z,wavelength=cf.wavelength):
    #this is the function to make the x value of a certain layer in an MLL
    x_val=np.sqrt(n_layer*focallength*wavelength+n_layer**2*wavelength**2/4)*(1-z/(2*focallength))
    return(x_val)

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
def mk_plane_wave(theta,wavelength,N_px=cf.N_px,Amp=cf.amplitude,pxsize=cf.pxsize):
    #theta in rad
    kx=np.sin(theta)/wavelength
    x_arr=np.linspace(0,N_px*pxsize,N_px)
    phase=2*np.pi*kx*x_arr
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


def mk_wedged_mll(z=0,sigma=cf.sigma_wedge,N_px=cf.N_px,pxsize=cf.pxsize,f=cf.f,offset=cf.mll_offset,wavelength=cf.wavelength,n_begin=cf.n_begin,n_end=cf.n_end,delta_1=cf.delta_1,delta_2=cf.delta_2,beta_1=cf.beta_1,beta_2=cf.beta_2,flip_mll=False,gamma=cf.gamma):
    if flip_mll==True:
        z=cf.mll_depth-z
    r=np.arange(0,N_px*pxsize,pxsize)
    t_array=np.pi*4*f*np.square(r)/(wavelength*(2*f-z)**2)
    rect=square(t_array,duty=gamma+0.05)
    if sigma!=None:
        print("Using sigma",sigma)
        rect=gaussian_filter(rect,sigma=sigma)
    xmin=wedged_mll_x(n_layer=n_begin,focallength=f,z=z,wavelength=cf.wavelength)
    xmax=wedged_mll_x(n_layer=n_end,focallength=f,z=z,wavelength=cf.wavelength)
    mask=np.bitwise_and(r<xmax,r>xmin).astype("int")
    rect=(rect+1)
    diff_delta=delta_1-delta_2
    diff_beta=beta_1-beta_2
    complex_array=(rect*diff_delta/2+delta_2)+1j*(rect*diff_beta/2+beta_2)
    complex_array=np.multiply(mask,complex_array)
    #now applying an offset
    if offset!=0:
        shift_px=int(offset/pxsize)
        complex_array=np.roll(complex_array,shift_px)
    return(complex_array)

