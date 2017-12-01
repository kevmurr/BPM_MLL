#This script is to simulate wedged MLLs according to Andrejczuks paper
#"Influence of imperfections in a wedged MLL ..."
#This is the main script to execute
import config as cf
import matplotlib.pyplot as plt
import build_setup as bs
#---------------------------------------------------------------------
###################################
#Making some samples
print("Making the samples...")
#Making the samples
if cf.mk_slit==True:
    slits_pre_result=bs.b_slit()#make the slit sample
    slits=slits_pre_result[0]
    stepslit=slits_pre_result[1]
#Making vacuum
opt_const_vac=bs.b_vac()
#Now making the mll if flat mll
if cf. mll_type=="flat":
    mll_pre_result=bs.b_mll()
    grating=mll_pre_result[0]
    N_steps_grat=mll_pre_result[1]

#------------------------------------------------------------------------
#####################################
#THE PROPAGATION
#####################################
#INCIDENT WAVE
print("Making incident wave")
wave00=bs.mk_incident_wave()
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
mll_prop_result=bs.prop_mll(wave,N_steps_grat=N_steps_grat,opt_const=grating)
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