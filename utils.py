import numpy as np
import cmath
import config as cf
import h5py as h5
##############################################
##GENERAL UTILS
def get_phase(arr):
    phase=np.zeros_like(arr)
    for i in range(0,arr.shape[0],1):
        phase[i]=cmath.phase(arr[i])
    phase=np.real(phase)
    return(phase)
##############################################
#CHECK STUFF
def check_directory(path):
    import os
    val=os.path.exists(str(path))
    if val==True:
        print("Directory exists!")
    else:
        return IOError("Given save_directory doesn't exist! Please choose another one")

def check_lenstype():
    if cf.mll_type!="flat" or cf.mll_type!="wedged":
        return IOError("Lens type not understood! Has to be flat or wedged")
################################################
#FOCUS FINDER
def get_maxval(wave,i,f=cf.f,search_rad=cf.search_rad,stepsize=cf.slicevac):
    i_f=int(cf.f/stepsize)
    i_min=i_f-int(search_rad*i_f)
    i_max=i_f+int(search_rad*i_f)
    maxval=0
    first_look=False
    if i==i_min:
        first_look=True
    if i>i_min and i<i_max:
        print("Looking for focus...")
        wave=wave.astype("complex")
        maxval=np.amax(np.abs(wave))
    return(maxval,first_look)
        
    #This first version of the focus finder takes as an estimation the input focal lenght. After that, it looks around it with the radius search_rad(unitless: 0.1=10% of focal length value is the search zone).
    #The slice with the highest peak intensity is the focal plane.This works good for a focus with high efficiency. If tilt angle is wrong, the focus might be mistaken
    
def post_process_focus(wave_focus):
    px_max=np.argmax(np.abs(wave_focus))
    central_pixel=round(wave_focus.shape[0]/2)
    shift=int(central_pixel-px_max)
    processed_wave=np.roll(wave_focus,shift)
    return(processed_wave)
####################################################
#SAVE DATA
def save_data(data_int_in_lens,data_int_after_lens,data_pupil,data_end,data_focus,int_before_lens,i_scan):
    if i_scan==0:
        print("Creating h5 file...")
        f=h5.File(cf.save_directory,"w")
        data=f.create_group("data")
        if cf.save_ot_inlens==True:
            data.create_dataset("int_in_lens",data=data_int_in_lens)
        if cf.save_ot_afterlens==True:
            data.create_dataset("int_after_lens",data=data_int_after_lens)
        if cf.save_ot_afterlens_lastcol==True:
            data.create_dataset("int_after_lens_lastcol",data=data_int_after_lens[:,-1])
        if cf.save_ot_wave==True:
            data.create_dataset("pupil",data=data_pupil)
        if cf.save_ot_wave_end==True:
            data.create_dataset("data_end",data=data_end)
        if cf.save_ot_focus==True:
            data.create_dataset("data_focus",data=data_focus)
        if cf.save_ot_beforelens==True:
            data.create_dataset("int_before_lens",data=int_before_lens)
        #writing the log
        log=f.create_group("log")
        general=log.create_group("general")
        general.create_dataset("wavelength",data=cf.wavelength)
        general.create_dataset("amplitude",data=cf.amplitude)
        general.create_dataset("N_px",data=cf.N_px)
        general.create_dataset("px_size",data=cf.pxsize)
        
        if cf.scanmode=="omegatheta":
            thetaarr=np.linspace(cf.theta_start,cf.theta_end,cf.N_theta)
            general.create_dataset("theta_arr",data=thetaarr)
        else:
            general.create_dataset("theta",data=cf.theta)
        mll=log.create_group("mll")
        if cf.scanmode=="efficiency":
            deptharr=np.linspace(cf.depth_start,cf.depth_end,cf.N_depth)
            mll.create_dataset("depth_arr",data=deptharr)
        else:
            mll.create_dataset("mll_depth",data=cf.mll_depth)
        mll.create_dataset("mll_offset",data=cf.mll_offset)
        mll.create_dataset("mll_type",data=str(cf.mll_type))
        if cf.mll_type=="flat":
            mll.create_dataset("sigma",data=cf.sigma_flat)
        if cf.mll_type=="wedged":
            if cf.sigma_wedge!=None:
                mll.create_dataset("sigma",data=cf.sigma_wedge)
        mll.create_dataset("n_start",data=cf.n_begin)
        mll.create_dataset("n_end",data=cf.n_end)
        mll.create_dataset("delta1",data=cf.delta_1)
        mll.create_dataset("delta2",data=cf.delta_2)
        mll.create_dataset("beta1",data=cf.beta_1)
        mll.create_dataset("beta2",data=cf.beta_2)
        mll.create_dataset("stepsize_z",data=cf.stepsize_z)
        mll.create_dataset("f",data=cf.f)
        if cf.shifted_energy!=None:
            mll.create_dataset("shifted_wavelength",data=cf.shifted_wavelength)
        slits=log.create_group("slits")
        slits.create_dataset("mk_slit",data=cf.mk_slit)
        slits.create_dataset("slits_size",data=cf.slits_size)
        slits.create_dataset("slits_offset",data=cf.slit_offset)
        slits.create_dataset("slits_depth",data=cf.slits_depth)
        slits.create_dataset("slits_steps",data=cf.slits_steps)
        slits.create_dataset("slits_delta",data=cf.slits_delta)
        slits.create_dataset("slits_beta",data=cf.slits_beta)
        vac=log.create_group("vacuum")
        vac.create_dataset("slicevac",data=cf.slicevac)
        vac.create_dataset("N",data=cf.N_slices_ff)
        f.close()
    else:
        print("Updating h5 file...")
        f=h5.File(cf.save_directory,"a")
        if cf.save_ot_inlens==True:
            folder=f["data"]
            data=f["data/int_in_lens"][:]
            if i_scan==1:
                small_data=data.reshape((1,data.shape[0],data.shape[1]))
            else:
                small_data=data
            big_data=np.zeros((small_data.shape[0]+1,small_data.shape[1],small_data.shape[2]))
            big_data[:-1,:,:]=small_data
            big_data[-1,:,:]=data_int_in_lens
            del f["/data/int_in_lens"]
            folder.create_dataset("int_in_lens",data=big_data)
        if cf.save_ot_afterlens==True:
            folder=f["data"]
            data=f["data/int_after_lens"][:]
            if i_scan==1:
                small_data=data.reshape((1,data.shape[0],data.shape[1]))
            else:
                small_data=data
            big_data=np.zeros((small_data.shape[0]+1,small_data.shape[1],small_data.shape[2]))
            big_data[:-1,:,:]=small_data
            big_data[-1,:,:]=data_int_after_lens
            del f["/data/int_after_lens"]
            folder.create_dataset("int_after_lens",data=big_data)
        if cf.save_ot_afterlens_lastcol==True:
            folder=f["data"]
            data=f["data/int_after_lens_lastcol"][:]
            if i_scan==1:
                small_data=data.reshape((1,data.shape[0]))
            else:
                small_data=data
            big_data=np.zeros((small_data.shape[0]+1,small_data.shape[1])).astype("float")
            big_data[:-1,:]=small_data
            big_data[-1,:]=data_int_after_lens[:,-1]
            del f["/data/int_after_lens_lastcol"]
            folder.create_dataset("int_after_lens_lastcol",data=big_data)
        if cf.save_ot_wave==True:
            folder=f["data"]
            data=f["data/pupil"][:]
            if i_scan==1:
                small_data=data.reshape((1,data.shape[0]))
            else:
                small_data=data
            big_data=np.zeros((small_data.shape[0]+1,small_data.shape[1]))
            big_data[:-1,:]=small_data
            big_data[-1,:]=data_pupil
            del f["/data/pupil"]
            folder.create_dataset("pupil",data=big_data)
        if cf.save_ot_wave_end==True:
            folder=f["data"]
            data=f["data/data_end"][:]
            if i_scan==1:
                small_data=data.reshape((1,data.shape[0]))
            else:
                small_data=data
            big_data=np.zeros((small_data.shape[0]+1,small_data.shape[1]))
            big_data[:-1,:]=small_data
            big_data[-1,:]=data_end
            del f["/data/data_end"]
            folder.create_dataset("data_end",data=big_data)
        if cf.save_ot_focus==True:
            folder=f["data"]
            data=f["data/data_focus"][:]
            if i_scan==1:
                small_data=data.reshape((1,data.shape[0]))
            else:
                small_data=data
            big_data=np.zeros((small_data.shape[0]+1,small_data.shape[1]))
            big_data[:-1,:]=small_data
            big_data[-1,:]=data_focus
            del f["/data/data_focus"]
            folder.create_dataset("data_focus",data=big_data)
        if cf.save_ot_beforelens==True:
            folder=f["data"]
            data=f["data/int_before_lens"][:]
            if i_scan==1:
                small_data=data.reshape((1,data.shape[0],data.shape[1]))
            else:
                small_data=data
            big_data=np.zeros((small_data.shape[0]+1,small_data.shape[1],small_data.shape[2]))
            big_data[:-1,:,:]=small_data
            big_data[-1,:,:]=int_before_lens
            del f["/data/int_before_lens"]
            folder.create_dataset("int_before_lens",data=big_data)
        f.close()
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