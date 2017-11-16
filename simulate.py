#This script is to simulate wedged MLLs according to Andrejczuks paper
#"Influence of imperfections in a wedged MLL ..."
#This is the main script to execute
import config as cf
import mk_sample as mks
import propagators as pr
import numpy as np
import matplotlib.pyplot as plt
from math import ceil
#------------------------------
print("Making the samples...")
#make the incident wave

#--------------------------------------------------------------------------
#..........................................................................
#samples
opt_const_vac=mks.mk_bulk()
N_steps_grat=int(cf.mll_depth/cf.stepsize_z)

#N_steps_grat=int(cf.grating_depth/cf.stepsize_z)
#grating=mks.mk_grating(N_layers=cf.grating_layers,period=cf.grating_period)
#Insert MLL
grating=mks.mk_wedged_mll(z_val=0,offset_x=cf.mll_offset)
slits=mks.mk_slit()
print("Done.")
#------------------------------------------------------------------------
wave0=mks.mk_plane_wave(theta=cf.theta)
#now introducing a slit
stepslit=cf.slits_depth/cf.slits_steps
for i in range(0,cf.slits_steps,1):
    wave0=pr.split_operator(wave0,opt_const=slits,step_size=stepslit)
    print("Propagating through slit: %s/%s" %(i,cf.slits_steps))
#propagate in free space 
stepvac=cf.stepvac #stepsize of free space propagator in meters
wave1=pr.split_operator(wave0,opt_const=opt_const_vac,step_size=stepvac)
#---------------------------------------------------------------------------
wave=wave1
if cf.save_intensity==True:
    modulo_img=int(N_steps_grat/cf.size_intensity_arr[1])
    if modulo_img==0:
        modulo_img=1
    if cf.size_intensity_arr[1]<N_steps_grat:
        intensity_plot=np.zeros((cf.size_intensity_arr[0],cf.size_intensity_arr[1]))
    else:
        intensity_plot=np.zeros((cf.size_intensity_arr[0],N_steps_grat))
    i2=0
    for i1 in range(N_steps_grat):
        wave=pr.split_operator(wave,opt_const=grating)
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
        print("Sample slice %s of %s completed"%(i1,N_steps_grat))

    
else:
    for i in range(N_steps_grat):
        wave=pr.split_operator(wave,opt_const=grating)
        print("iteration %s of %s completed"%(i,N_steps_grat))
#............................................................................
#---------------------------------------------------------------------------
#now freespace propagation
N_slices_vac=cf.N_slices_ff
wave3=wave
modulo_img=int(N_steps_grat/cf.size_ff_arr[1])
if modulo_img==0:
    modulo_img=1
if cf.size_ff_arr[1]<N_slices_vac:
    intensity_ff=np.zeros((cf.size_ff_arr[0],cf.size_ff_arr[1]))
else:
    intensity_ff=np.zeros((cf.size_ff_arr[1],N_slices_vac))
i2=0
for i in range(N_slices_vac):
    wave3=pr.split_operator(wave3,opt_const=opt_const_vac,step_size=cf.slicevac)
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
    print("Farfield slice %s of %s completed"%(i,N_slices_vac))
size_obj=cf.N_px*cf.pxsize
max_recom_zstep=size_obj**2/cf.wavelength
#stepsize_vec=(cf.grating_depth/N_steps_grat,cf.mll_depth/N_steps_grat,cf.slits_depth/cf.slits_steps)
#namestep_vec=["sample (grating)","sample (mll)","slit"]
#maxstepsize_i=np.argmax(stepsize_vec)
#maxstepsize=np.amax(stepsize_vec)
#if maxstepsize>max_recom_zstep:
#   print("WARNING: the chosen stepsize for %s might be too big! It should be smaller than %s."%(string(namestep_vec[maxstepsize_i]))))
print("")
print("The nearfield propagation in the sample is saved as intensity_plot")
print("The farfield propagation in the sample is saved as intensity_ff")
print("Finished run.")