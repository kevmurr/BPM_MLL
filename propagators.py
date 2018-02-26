import numpy as np
import config as cf
wavelength=cf.wavelength
def split_operator(input_wave,opt_const,step_size,wavelength=cf.wavelength,px_size=cf.pxsize):
    #this is a split operator beam propagation method according to robert r mcleod
    k0=2*np.pi/(wavelength)
    #for now i will normaize the fft of the sample and multiply with k0 to get kx
    input_wave=input_wave.astype("complex")
    opt_const=opt_const.astype("complex")
    kx=np.fft.fftfreq(input_wave.size)/(px_size)
    kz=np.sqrt(np.subtract(np.square(k0),np.square(kx)))
    refr=np.fft.fft(np.multiply(input_wave,np.exp(1j*(np.real(opt_const)+1j*2*np.imag(opt_const))*k0*step_size )))
    output_wave=np.fft.ifft(np.multiply(refr,np.exp(-1j*np.pi*wavelength*step_size*np.square(kz))))
    #output_wave=np.fft.ifft(np.multiply(refr,np.exp(-1j*kz*step_size)))
    return(output_wave)
def split_operator_andr(input_wave,opt_const,step_size,px_size=cf.pxsize):
    #this is not fully operational yet! However, except some rescaling it should be quite similar to split_operator
    Mx=input_wave.shape[0]
    dx=px_size*2*np.pi/cf.wavelength
    dkx= 2*np.pi/(Mx*dx)
    kx=((np.arange(0,Mx,1))-Mx/2)*dkx
    log_p=kx**2<1
    p=(np.sqrt(1-kx**2)*log_p)
    G1=np.multiply(np.fft.fftshift(np.fft.fft(input_wave)),np.exp(1j*p*dx))
    U1=np.multiply(np.fft.ifft(np.fft.ifftshift(G1)),np.exp(1j*dx*opt_const/2))
    return(U1)
