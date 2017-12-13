import config as cf
import numpy as np
import mk_sample as mks
import propagators as pr
from math import ceil
#mk incidend wave
def mk_incident_wave(theta,wave_type=cf.incident_type):
    if wave_type=="plane":
        incident_wave=mks.mk_plane_wave(theta=theta,N_px=cf.N_px,Amp=1,wavelength=cf.wavelength,pxsize=cf.pxsize)
    return(incident_wave)    
def b_vac():
    opt_const_vac=mks.mk_bulk()
    return(opt_const_vac)
def b_slit():
    if cf.mk_slit==True:
        slits=mks.mk_slit()
        stepslit=cf.slits_depth/cf.slits_steps
    return(slits,stepslit)

def b_mll(z=0,mll_type=cf.mll_type):
#if mll is flat the optical constants are already made here. If not then they will be made every step when calculating bpm
    if mll_type=="flat":
        grating=mks.mk_wedged_mll(z=0,sigma=cf.sigma_flat,N_px=cf.N_px,pxsize=cf.pxsize,f=cf.f,wavelength=cf.wavelength,n_begin=cf.n_begin,n_end=cf.n_end,delta_1=cf.delta_1,delta_2=cf.delta_2,beta_1=cf.beta_1,beta_2=cf.beta_2)
    N_steps_grat=int(cf.mll_depth/cf.stepsize_z)
    return(grating,N_steps_grat)
    if mll_type=="wedged":
        grating=mks.mk_wedged_mll(z,N_px=cf.N_px,sigma=cf.sigma_wedge,pxsize=cf.pxsize,f=cf.f,wavelength=cf.wavelength,n_begin=cf.n_begin,n_end=cf.n_end,delta_1=cf.delta_1,delta_2=cf.delta_2,beta_1=cf.beta_1,beta_2=cf.beta_2)
def prop_slit(input_wave,stepslit,opt_const):
    wave0=input_wave
    for i in range(0,cf.slits_steps,1):
        wave0=pr.split_operator(wave0,opt_const=opt_const,step_size=stepslit)
        print("Propagating through slit: %s/%s" %(i,cf.slits_steps))
    output_wave=wave0
    return(output_wave)

def prop_mll_flat(input_wave,opt_const,N_steps_grat,step_size=cf.stepsize_z,i_img=1,N_img=1):
    mll_type=cf.mll_type
    wave=input_wave
    grating=opt_const
    if mll_type=="flat":
        modulo_img=int(N_steps_grat/cf.size_intensity_arr[1])
        if modulo_img==0:
            modulo_img=1
        if cf.size_intensity_arr[1]<N_steps_grat:
            intensity_plot=np.zeros((cf.size_intensity_arr[0],cf.size_intensity_arr[1]))
        else:
            intensity_plot=np.zeros((cf.size_intensity_arr[0],N_steps_grat))
        i2=0
        for i1 in range(N_steps_grat):
            wave=pr.split_operator(wave,opt_const=grating,step_size=step_size)
            if i1%modulo_img==0:
                wave_now=np.abs(wave)
                modulo_bin=ceil(wave_now.shape[0]/cf.size_intensity_arr[0])
                #now binning down
                i3=0
                wave_bin=np.zeros((cf.size_intensity_arr[0]))
                for i in range(0,wave_now.shape[0],1):
                    if i%modulo_bin==0:
                        wave_bin[i3]=wave_now[i]
                        i3+=1   
                intensity_plot[:,i2]=wave_bin
                i2+=1
                print("Img(%s/%s) MLL slice %s of %s completed"%(i_img,N_img,i1,N_steps_grat))
    output_wave=wave
    return(output_wave,intensity_plot)
def prop_mll_wedge(input_wave,N_steps_grat,step_size=cf.stepsize_z,i_img=1,N_img=1):
    mll_type=cf.mll_type
    wave=input_wave
    if mll_type=="wedged":
        modulo_img=int(N_steps_grat/cf.size_intensity_arr[1])
        if modulo_img==0:
            modulo_img=1
        if cf.size_intensity_arr[1]<N_steps_grat:
            intensity_plot=np.zeros((cf.size_intensity_arr[0],cf.size_intensity_arr[1]))
        else:
            intensity_plot=np.zeros((cf.size_intensity_arr[0],N_steps_grat))
        i2=0
        z=0
        for i1 in range(N_steps_grat):
            grating=mks.mk_wedged_mll(z=z)
            z=z+step_size
            #print("z value is currently %s m" %z)
            wave=pr.split_operator(wave,opt_const=grating,step_size=step_size)
            if i1%modulo_img==0:
                wave_now=np.abs(wave)
                modulo_bin=ceil(wave_now.shape[0]/cf.size_intensity_arr[0])
                #now binning down
                i3=0
                wave_bin=np.zeros((cf.size_intensity_arr[0]))
                for i in range(0,wave_now.shape[0],1):
                    if i%modulo_bin==0:
                        wave_bin[i3]=wave_now[i]
                        i3+=1   
                intensity_plot[:,i2]=wave_bin
                i2+=1
                print("Img(%s/%s) MLL slice %s of %s completed"%(i_img,N_img,i1,N_steps_grat))
    output_wave=wave
    return(output_wave,intensity_plot)
def prop_single(input_wave,opt_const,stepvac=cf.stepvac):
     #stepsize of free space propagator in meters
     output_wave=pr.split_operator(input_wave,opt_const=opt_const,step_size=stepvac)
     return(output_wave)

def prop_bulk(input_wave,opt_const,N_slices_vac=cf.N_slices_ff,step_size=cf.slicevac,i_img=1,N_img=1):
    wave3=input_wave
    modulo_img=round(N_slices_vac/cf.size_ff_arr[1])
    if modulo_img==0:
        modulo_img=1
    if cf.size_ff_arr[1]<N_slices_vac:
        intensity_ff=np.zeros((cf.size_ff_arr[0],cf.size_ff_arr[1]))
    else:
        intensity_ff=np.zeros((cf.size_ff_arr[1],N_slices_vac))
    i2=0
    for i in range(N_slices_vac):
        wave3=pr.split_operator(wave3,opt_const=opt_const,step_size=step_size)
        if i%modulo_img==0:
            wave_now=np.abs(wave3)
            modulo_bin=ceil(wave_now.shape[0]/cf.size_ff_arr[0])
            #now binning down
            i3=0
            wave_bin=np.zeros((cf.size_ff_arr[0]))
            for i1 in range(0,wave_now.shape[0],1):
                if i1%modulo_bin==0:
                    wave_bin[i3]=wave_now[i1]
                    i3+=1   
            intensity_ff[:,i2]=wave_bin
            i2+=1
        print("Img (%s/%s) Farfield slice %s of %s completed"%(i_img,N_img,i,N_slices_vac))
    output_wave=wave3
    return(output_wave,intensity_ff)