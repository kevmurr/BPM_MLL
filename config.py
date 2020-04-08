import optical_constants as oc
import scipy.constants as sc
#General experimental parameters
energy=17.5 #energy in kev,if shifted_energy is NOne, this is the incident energy AND the energy that the lens is designed for. IF shifted_energy has a value, the incident beam has the energy shifted_energy
f=0.0015 #geometrical focal length in meters
scanmode="efficiency" #This is very important. If "single" is chosen only a single shot is taken. "efficiency" does a scan of mll depth and measures the efficiency (not implemented yet) ."omegatheta" does an omegathetascan (not implemented yet). 
save_directory="/gpfs/cfel/cxi/labs/MLL-Sigray/Simulations/S200408A.h5"
#simulation parameters
pxsize=0.05*10**-9 #px size in x direction in m
stepsize_z=20*10**-9#stepsize in mll
N_px=2*10**6


#---------------------------------------------
#Incident wave
incident_type="plane"#shape of the incident wave (right now only plane wave supported. For this enter "plane")
amplitude=1
theta=0 #angle of the incident wave in rad (for omegatheta the theta array is being defined below)
shifted_energy=None # If this is None, the incident wavelength is calculacted with the energy. If this has a value, the incident energy is shifted_energy and the lens design is for energy.

#---------------------------------------------


#optical constants of multilayer materials
delta_1=oc.delta_WC_17_5bulk
beta_1=oc.beta_WC_17_5bulk
delta_2=oc.delta_SiC_17_5bulk
beta_2=oc.beta_SiC_17_5bulk
#--------------------------


#MLL
#number of layers in MLL
mll_type="wedged" #choose "flat" or wedged
n_begin=952 #first layer
n_end= n_begin+11400 #last layer
mll_depth=7*10**-6
mll_offset=0 #offset in meters
gamma=0.5
sigma_flat=None # this is the sigma of the layers (in meters). None means the optical constants are like a rect function-> faster calculation!
sigma_wedge=0.8*10**-9
flip_mll=False# should the mll be flipped ? rotation axis orthogonal to optical axis. This is needed for full field simulation
alter_thickness=False #this specifies if a layer correction should be employed


#Alter thickness/ Correction
fnam_corr="../Corrections/2018_10_phase_defect/applied_correction.npy" #additive layer correction in nanometers. First entries are thin layers, Last entries are thick layers

#--------------------------
#SLITS
mk_slit=True #True if slit should be used
slits_size=35*10**-6 #size in meters
slits_depth=100*10**-6
slit_offset=7*10**-6
slits_delta=delta_1
slits_beta=beta_1
slits_steps=10 #number of steps in slit
#.............................................


#Vacuum
stepvac=2*10**-6#1 # distance if step is a single distance propagation
N_slices_ff=50 #farfield slices after lens.
N_slices_bf=0 #slices before lens (possibly 0 if no special data is needed there)
slicevac=60*10**-6 #distance of a single slice in vac in ff or before the mll
#---------------------
#..................................................



#######################################
#SCANNING PARAMETERS. please jump to the respective section to choose your scanning parameters
#######################################
#GENERAL (These settings are also true for omegatheta, efficiency etc)
#--------------------------------------
#FOCUS FINDER
search_rad=0.05 #search radius in percent (10%=0.1). This specifies where the focus finder looks for the focal plane around the estimated focus
#nf image (intensity in the lens)
size_intensity_arr=(2000,2000)
#ff image (intensity after lens of the focus etc)
size_ff_arr=(4000,4000) #this is the size for the far field arr and for the arr before the lens
#The next lines specify what should be saved in the h5 file
save_ot_beforelens=False #This specifies if the intensity before the lens and after slitting should be saved.
save_ot_inlens=False #This specifies if the intensity image inside the lens should be saved 
save_ot_afterlens=True #This specifies if the intensity image after the lens should be saved 
save_ot_afterlens_lastcol=False #This specifies if the last row of the intensity image after the lens should be saved 
save_ot_wave=False #This specifies if the complex valued wave array at the exit pupil should be saved
save_ot_wave_end=True #This specifies if the complex valued wave array at the end of the simulation
save_ot_focus=True #This specifies if the focal plane wavefront should be saved
#######################################


#EFFICIENCY 
#-------------------------------------
#General parameters
N_depth=50 #number of images taken (number of lens thickness values)
depth_start=0.1*10**-6 #start of efficiency scan in m
depth_end=30*10**-6 #end of efficiency scan in m
#######################################


#OMEGATHETA
#--------------------------------------
#General parameters
N_theta=11 #number of images taken (number of theta values)
theta_start=-0.02 #start of the theta scan in rad
theta_end=0.02 #end of the theta scan in rad
###############################################


#PRE CALCULATION
###############################################
wavelength=sc.h*sc.c/(energy*1000*sc.e)#wavelength in meters.
if shifted_energy!=None:
    print("Applying shifted energy...")
    shifted_wavelength=sc.h*sc.c/(shifted_energy*1000*sc.e)
N_px=int(N_px)

if sigma_flat!=None:
    sigma_flat=sigma_flat/pxsize
if sigma_wedge!=None:
    sigma_wedge=sigma_wedge/pxsize
