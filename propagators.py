import numpy as np
import config as cf
wavelength=cf.wavelength
def fine_propagator(input_wave,deltaz,opt_const):
    exponent1=np.exp(1j/2*deltaz)
    exponent2=np.exp(-1j/2*opt_const*deltaz)
    exponent=np.multiply(exponent1,exponent2)
    output_wave=np.multiply(input_wave,exponent)
    return(output_wave)
def split_operator(input_wave,opt_const,px_size=cf.pxsize,step_size=cf.stepsize_z):
    #this is a split operator beam propagation method according to robert r mcleod
    k0=2*np.pi/(wavelength)
    #for now i will normaize the fft of the sample and multiply with k0 to get kx
    input_wave=input_wave.astype("complex")
    opt_const=opt_const.astype("complex")
    #kx=k0*kx_unnorm/(np.amax(np.abs(kx_unnorm)))
    #min_freq=1/(input_wave.shape[0]*px_size)
    #nyq_freq=1/(2*px_size)
    kx=np.fft.fftfreq(input_wave.size)/px_size
    kz=np.sqrt(np.subtract(np.square(k0),np.square(kx)))
    refr=np.fft.fft(np.multiply(input_wave,np.exp(1j*opt_const*k0*step_size)))
    output_wave=np.fft.ifft(np.multiply(refr,np.exp(-1j*kz*step_size)))
    
    #diffr=np.multiply(np.fft.fft(input_wave),np.exp(-1j*step_size*kz))
    #output_wave=np.fft.ifft(diffr)*np.exp(-1j*k0*step_size*opt_const)
    return(output_wave)