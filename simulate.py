#This script is to simulate wedged MLLs according to Andrejczuks paper
#"Influence of imperfections in a wedged MLL ..."
#This is the main script to execute
import config as cf
import matplotlib.pyplot as plt
import build_setup as bs
from shutil import copyfile
import utils as ut
################################################
#SINGLE SCAN
################################################
if cf.scanmode=="single" or cf.scanmode=="Single" or cf.scanmode=="s":
    #---------------------------------------------------------------------
    ###################################
    #Preparations
    ###################################
    ut.check_directory(cf.save_directory)
    ut.check_lenstype()
    print("Making the samples...")
    #Making the samples
    if cf.mk_slit==True:
        print("Making slit...")
        slits_pre_result=bs.b_slit()#make the slit sample
        slits=slits_pre_result[0]
        stepslit=slits_pre_result[1]
    #Making vacuum
    print("Making vacuum...")
    opt_const_vac=bs.b_vac()
    #Now making the mll if flat mll
    if cf. mll_type=="flat":
        print("Making flat mll...")
        mll_pre_result=bs.b_mll()
        grating=mll_pre_result[0]
        N_steps_grat=mll_pre_result[1]
    if cf.mll_type=="wedged":
            N_steps_grat=int(cf.mll_depth/cf.stepsize_z)
    
    #------------------------------------------------------------------------
    #####################################
    #The Propagation
    #####################################
    #INCIDENT WAVE
    print("Making incident wave...")
    wave00=bs.mk_incident_wave(theta=cf.theta)
    #--------------------------------------------------------------------------
    #SLIT
    wave0=wave00
    if cf.mk_slit==True:
        wave1=bs.prop_slit(wave0,stepslit=stepslit,opt_const=slits) 
    else:
        wave1=wave0
    #--------------------------------------------------------------------------
    #FREESPACE
    wave1=bs.prop_single(wave1,opt_const=opt_const_vac)
    #---------------------------------------------------------------------------
    #MLL
    wave=wave1
    if cf.mll_type=="flat":
        mll_prop_result=bs.prop_mll_flat(wave,N_steps_grat=N_steps_grat,opt_const=grating)
    if cf.mll_type=="wedged":
        mll_prop_result=bs.prop_mll_wedge(wave,N_steps_grat=N_steps_grat)
    wave=mll_prop_result[0]
    intensity_in_mll=mll_prop_result[1]
    #---------------------------------------------------------------------------
    #FREESPACE
    freespace_prop_result=bs.prop_bulk(wave,opt_const=opt_const_vac)
    wave_end=freespace_prop_result[0]
    intensity_after_mll=freespace_prop_result[1]
    print("")
    print("The incident wave is ""wave00""")
    print("Wave at entry of lens is ""wave1""")
    print("Wave at the exit pupil of lens is ""wave""")
    print("Wave at the end of simulation is ""wave_end""")
    print("The nearfield propagation in the sample is saved as ""intensity_in_mll""")
    print("The farfield propagation in the sample is saved as ""intensity_after_mll""")
    print("Finished run.")
##################################################
#EFFICIENCY SCAN
##################################################
if cf.scanmode=="efficiency" or cf.scanmode=="Efficiency" or cf.scanmode=="e":
    #This is where i will put the stuff to do an efficiency scan
    #check the save directory:
    ut.check_directory(cf.save_directory)
    ut.check_lenstype()
    import numpy as np
    deptharr=np.linspace(cf.depth_start,cf.depth_end,cf.N_depth)
    for i_depth in range(0,cf.N_depth,1):
        ###################################
        #Preparations
        ###################################
        print("Making the samples...")
        #Making the samples
        if cf.mk_slit==True:
            print("Making slit...")
            slits_pre_result=bs.b_slit()#make the slit sample
            slits=slits_pre_result[0]
            stepslit=slits_pre_result[1]
        #Making vacuum
        print("Making vacuum...")
        opt_const_vac=bs.b_vac()
        #Now making the mll if flat mll
        if cf. mll_type=="flat":
            print("Making flat mll...")
            mll_pre_result=bs.b_mll()
            grating=mll_pre_result[0]
            N_steps_grat=int(deptharr[i_depth]/cf.stepsize_z)
        if cf.mll_type=="wedged":
            N_steps_grat=int(deptharr[i_depth]/cf.stepsize_z)
        #------------------------------------------------------------------------
        #####################################
        #The Propagation
        #####################################
        #INCIDENT WAVE
        print("Making incident wave...")
        wave00=bs.mk_incident_wave(theta=cf.theta)
        #--------------------------------------------------------------------------
        #SLIT
        wave0=wave00
        if cf.mk_slit==True:
            wave1=bs.prop_slit(wave0,stepslit=stepslit,opt_const=slits) 
        else:
            wave1=wave0
        #--------------------------------------------------------------------------
        #FREESPACE
        wave1=bs.prop_single(wave1,opt_const=opt_const_vac)
        #---------------------------------------------------------------------------
        #MLL
        
        wave=wave1
        if cf.mll_type=="flat":
            mll_prop_result=bs.prop_mll_flat(wave,N_steps_grat=N_steps_grat,opt_const=grating,i_img=i_depth,N_img=cf.N_depth)
        if cf.mll_type=="wedged":
            mll_prop_result=bs.prop_mll_wedge(wave,N_steps_grat=N_steps_grat,i_img=i_depth,N_img=cf.N_depth)
        wave=mll_prop_result[0]
        intensity_in_mll=mll_prop_result[1]

        #---------------------------------------------------------------------------
        #FREESPACE
        freespace_prop_result=bs.prop_bulk(wave,opt_const=opt_const_vac,i_img=i_depth,N_img=cf.N_depth)
        wave_end=freespace_prop_result[0]
        intensity_after_mll=freespace_prop_result[1]
        #Saving stuff
        print("Saving...")
        if cf.save_ot_inlens==True:
            print("Saving...intensity in lens")
            np.save("%sdepth_%s_int_in_lens.npy"%(str(cf.save_directory),i_depth),intensity_in_mll)
        if cf.save_ot_afterlens==True:
            print("Saving...intensity after lens")
            np.save("%sdepth_%s_int_after_lens.npy"%(str(cf.save_directory),i_depth),intensity_after_mll)
        if cf.save_ot_wave==True:
            print("Saving...complex wave vector at exit pupil of lens")
            np.save("%sdepth_%s_pupil_wave.npy"%(str(cf.save_directory),i_depth),wave)
        if cf.save_ot_wave_end==True:
            print("Saving...complex wave vector at end of simulation")
            np.save("%sdepth_%s_pupil_end.npy"%(str(cf.save_directory),i_depth),wave_end)
    print("Saving...copy of config for logging")
    copyfile("config.py", str(cf.save_directory)+"config.py")
    print("Finished run.")
    
##################################################
#OMEGATHETA SCAN
##################################################
if cf.scanmode=="omegatheta" or cf.scanmode=="Omegatheta" or cf.scanmode=="o":
    #check the save directory:
    ut.check_directory(cf.save_directory)
    ut.check_lenstype()
    import numpy as np
    thetaarr=np.linspace(cf.theta_start,cf.theta_end,cf.N_theta)
    for i_theta in range(0,cf.N_theta,1):
        #This is where i will put the stuff to do an efficiency scan
            #---------------------------------------------------------------------
        ###################################
        #Preparations
        ###################################
        print("Making the samples...")
        #Making the samples
        if cf.mk_slit==True:
            print("Making slit...")
            slits_pre_result=bs.b_slit()#make the slit sample
            slits=slits_pre_result[0]
            stepslit=slits_pre_result[1]
        #Making vacuum
        print("Making vacuum...")
        opt_const_vac=bs.b_vac()
        #Now making the mll if flat mll
        if cf. mll_type=="flat":
            print("Making flat mll...")
            mll_pre_result=bs.b_mll()
            grating=mll_pre_result[0]
            N_steps_grat=mll_pre_result[1]
        if cf.mll_type=="wedged":
            N_steps_grat=int(cf.mll_depth/cf.stepsize_z)
        #------------------------------------------------------------------------
        #####################################
        #The Propagation
        #####################################
        #INCIDENT WAVE
        print("Making incident wave...")
        wave00=bs.mk_incident_wave(theta=thetaarr[i_theta])
        #--------------------------------------------------------------------------
        #SLIT
        wave0=wave00
        if cf.mk_slit==True:
            wave1=bs.prop_slit(wave0,stepslit=stepslit,opt_const=slits) 
        else:
            wave1=wave0
        #--------------------------------------------------------------------------
        #FREESPACE
        wave1=bs.prop_single(wave1,opt_const=opt_const_vac)
        #---------------------------------------------------------------------------
        #MLL
        
        wave=wave1
        if cf.mll_type=="flat":
            mll_prop_result=bs.prop_mll_flat(wave,N_steps_grat=N_steps_grat,opt_const=grating,i_img=i_theta,N_img=cf.N_theta)
        if cf.mll_type=="wedged":
            mll_prop_result=bs.prop_mll_wedge(wave,N_steps_grat=N_steps_grat,i_img=i_theta,N_img=cf.N_theta)
        wave=mll_prop_result[0]
        intensity_in_mll=mll_prop_result[1]

        #---------------------------------------------------------------------------
        #FREESPACE
        freespace_prop_result=bs.prop_bulk(wave,opt_const=opt_const_vac,i_img=i_theta,N_img=cf.N_theta)
        wave_end=freespace_prop_result[0]
        intensity_after_mll=freespace_prop_result[1]
        #Saving stuff
        print("Saving...")
        if cf.save_ot_inlens==True:
            print("Saving...intensity in lens")
            np.save("%stheta_%s_int_in_lens.npy"%(str(cf.save_directory),i_theta),intensity_in_mll)
        if cf.save_ot_afterlens==True:
            print("Saving...intensity after lens")
            np.save("%stheta_%s_int_after_lens.npy"%(str(cf.save_directory),i_theta),intensity_after_mll)
        if cf.save_ot_wave==True:
            print("Saving...complex wave vector at exit pupil of lens")
            np.save("%stheta_%s_pupil_wave.npy"%(str(cf.save_directory),i_theta),wave)
        if cf.save_ot_wave_end==True:
            print("Saving...complex wave vector at end of simulation")
            np.save("%stheta_%s_pupil_end.npy"%(str(cf.save_directory),i_theta),wave_end)
    print("Saving...copy of config for logging")
    copyfile("config.py", str(cf.save_directory)+"config.py")
    print("Finished run.")