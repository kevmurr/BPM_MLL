import optical_constants as oc
import scipy.constants as sc
#General experimental parameters
energy=17.3 #energy in kev,if shifted_energy is NOne, this is the incident energy AND the energy that the lens is designed for. IF shifted_energy has a value, the incident beam has the energy shifted_energy

f=0.0025 #geometrical focal length in meters
scanmode="single" #This is very important. If "single" is chosen only a single shot is taken. "efficiency" does a scan of mll depth and measures the efficiency (not implemented yet) ."omegatheta" does an omegathetascan (not implemented yet). 
save_directory="F:/Simulations/BPM_MLL/single/test_focfinder_omegatheta4.h5"#This is the filename how the data should be saved
#simulation parameters
pxsize=0.2*10**-9 #px size in x direction in m
stepsize_z=10*10**-9#stepsize in mll
N_px=5*10**5
#---------------------------------------------
#Incident wave
incident_type="plane"#shape of the incident wave (right now only plane wave supported. For this enter "plane")
amplitude=1
theta=0 #angle of the incident wave in rad (for omegatheta the theta array is being defined below)
shifted_energy=None # If this is None, the incident wavelength is calculacted with the energy. If this has a value, the incident energy is shifted_energy and the lens design is for energy.

#---------------------------------------------
#optical constants of multilayer materials
delta_1=oc.delta_W_17_3
beta_1=oc.beta_W_17_3
delta_2=oc.delta_Si_17_3
beta_2=oc.beta_Si_17_3
#--------------------------

#MLL
#number of layers in MLL
mll_type="wedged" #choose "flat" or wedged
n_begin=322 #first layer
n_end=5822 #last layer
mll_depth=6*10**-6
mll_offset=6*10**-6#0.0001-0.77*10**-5 #offset in meters
sigma_flat=None # this is the sigma of the layers. None means the optical constants are like a rect function-> faster calculation!
sigma_wedge=1

#--------------------------
#SLITS
mk_slit=True #True if slit should be used
slits_size=30*10**-6 #size in meters
slits_depth=100*10**-6
slit_offset=17.5*10**-6
slits_delta=oc.delta_W_17_3
slits_beta=oc.beta_W_17_3
slits_steps=100 #number of steps in slit
#.............................................
#Vacuum
stepvac=1*10**-6#1 # distance if step is a single distance propagation
N_slices_ff=1000 #farfield slices
slicevac=0.5*10**-5 #distance of a single slice in vac if multiple slices are calculated
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
size_ff_arr=(4000,4000)
save_ot_inlens=False #This specifies if the intensity image inside the lens should be saved (both as npy file and as png)
save_ot_afterlens=True #This specifies if the intensity image after the lens should be saved (both as npy file and as png)
save_ot_wave=True #This specifies if the complex valued wave array at the exit pupil should be saved
save_ot_wave_end=False #This specifies if the complex valued wave array at the end of the simulation
save_ot_focus=True #This specifies if the focal plane wavefront should be saved
#######################################
#EFFICIENCY 
#-------------------------------------
#General parameters
N_depth=30 #number of images taken (number of lens thickness values)
depth_start=1*10**-6 #start of efficiency scan in m
depth_end=20*10**-6 #end of efficiency scan in m

#######################################
#OMEGATHETA
#--------------------------------------
#General parameters
N_theta=30 #number of images taken (number of theta values)
theta_start=-0.005 #start of the theta scan in rad
theta_end=0.005 #end of the theta scan in rad

###############################################
#PRE CALCULATION
###############################################
wavelength=sc.h*sc.c/(energy*1000*sc.e)#wavelength in meters.
if shifted_energy!=None:
    print("Applying shifted energy...")
    shifted_wavelength=sc.h*sc.c/(shifted_energy*1000*sc.e)