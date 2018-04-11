#This script is to simulate wedged MLLs according to Andrejczuks paper
#"Influence of imperfections in a wedged MLL ..."
#This is the main script to execute
import config as cf
import matplotlib.pyplot as plt
import build_setup as bs
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
    before_prop_result=bs.prop_bf(input_wave=wave1,opt_const=opt_const_vac,N_slices_vac=cf.N_slices_bf,step_size=cf.slicevac,i_img=1,N_img=1)
    wave1=before_prop_result[0]
    intensity_before=before_prop_result[1]
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
    freespace_prop_result=bs.prop_ff(wave,opt_const=opt_const_vac)
    wave_end=freespace_prop_result[0]
    intensity_after_mll=freespace_prop_result[1]
    wave_focus=freespace_prop_result[2]
    if cf.save_directory!=None:
        print("Saving...")
        ut.save_data(data_int_in_lens=intensity_in_mll,data_int_after_lens=intensity_after_mll,data_pupil=wave,data_end=wave_end,data_focus=wave_focus,int_before_lens=intensity_before,i_scan=0)
    print("")
    print("The incident wave is ""wave00""")
    print("Wave at entry of lens is ""wave1""")
    print("Wave at the exit pupil of lens is ""wave""")
    print("Wave at the end of simulation is ""wave_end""")
    print("The nearfield propagation in the sample is saved as ""intensity_in_mll""")
    print("The farfield propagation in the sample is saved as ""intensity_after_mll""")
    print("The farfield propagation in the sample is saved as ""wave_focus""")
    print("The detected focal plane is in slice %s which is %s mm from the MLL."%(freespace_prop_result[3],1000*freespace_prop_result[3]*cf.slicevac))
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
        before_prop_result=bs.prop_bf(input_wave=wave1,opt_const=opt_const_vac,N_slices_vac=cf.N_slices_bf,step_size=cf.slicevac,i_img=1,N_img=1)
        wave1=before_prop_result[0]
        intensity_before=before_prop_result[1]
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
        freespace_prop_result=bs.prop_ff(wave,opt_const=opt_const_vac,i_img=i_depth,N_img=cf.N_depth)
        wave_end=freespace_prop_result[0]
        intensity_after_mll=freespace_prop_result[1]
        wave_focus=freespace_prop_result[2]
        #Saving stuff
        print("The detected focal plane is in slice %s which is %s mm from the MLL."%(freespace_prop_result[3],1000*freespace_prop_result[3]*cf.slicevac))
        if cf.save_directory!=None:
            print("Saving...")
            ut.save_data(data_int_in_lens=intensity_in_mll,data_int_after_lens=intensity_after_mll,data_pupil=wave,data_end=wave_end,data_focus=wave_focus,int_before_lens=intensity_before,i_scan=i_depth)
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
        before_prop_result=bs.prop_bf(input_wave=wave1,opt_const=opt_const_vac,N_slices_vac=cf.N_slices_bf,step_size=cf.slicevac,i_img=1,N_img=1)
        wave1=before_prop_result[0]
        intensity_before=before_prop_result[1]
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
        freespace_prop_result=bs.prop_ff(wave,opt_const=opt_const_vac,i_img=i_theta,N_img=cf.N_theta)
        wave_end=freespace_prop_result[0]
        intensity_after_mll=freespace_prop_result[1]
        wave_focus=freespace_prop_result[2]
        #Saving stuff
        print("The detected focal plane is in slice %s which is %s mm from the MLL."%(freespace_prop_result[3],1000*freespace_prop_result[3]*cf.slicevac))    
        if cf.save_directory!=None:
            print("Saving...")
            ut.save_data(data_int_in_lens=intensity_in_mll,data_int_after_lens=intensity_after_mll,data_pupil=wave,data_end=wave_end,data_focus=wave_focus,int_before_lens=intensity_before,i_scan=i_theta)
    print("Finished run.")