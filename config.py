import optical_constants as oc
import scipy.constants as sc
#General experimental parameters
energy=17.3 #energy in kev,if shifted_energy is NOne, this is the incident energy AND the energy that the lens is designed for. IF shifted_energy has a value, the incident beam has the energy shifted_energy

f=0.015 #geometrical focal length in meters
scanmode="single" #This is very important. If "single" is chosen only a single shot is taken. "efficiency" does a scan of mll depth and measures the efficiency (not implemented yet) ."omegatheta" does an omegathetascan (not implemented yet). 
#save_directory="F:/Simulations/BPM_MLL/single/papers/esrf_paper_18/test_normal4.h5"#This is the filename how the data should be saved. None will lead to the data NOT being saved
save_directory="/gpfs/cfel/cxi/scratch/user/murrayke/Simulations/S180504B_16_1kev_efficiency_WC_SiC.h5"
#save_directory=None
#simulation parameters
pxsize=0.8*10**-9 #px size in x direction in m
stepsize_z=10*10**-9#stepsize in mll
N_px=10*10**5
#---------------------------------------------
#Incident wave
incident_type="plane"#shape of the incident wave (right now only plane wave supported. For this enter "plane")
amplitude=1
theta=0 #angle of the incident wave in rad (for omegatheta the theta array is being defined below)
shifted_energy=None # If this is None, the incident wavelength is calculacted with the energy. If this has a value, the incident energy is shifted_energy and the lens design is for energy.

#---------------------------------------------
#optical constants of multilayer materials
delta_1=oc.delta_WC_17_3
beta_1=oc.beta_WC_17_3
delta_2=oc.delta_SiC_17_3
beta_2=oc.beta_SiC_17_3
#--------------------------

#MLL
#number of layers in MLL
mll_type="wedged" #choose "flat" or wedged
n_begin=13714 #first layer
n_end= n_begin+6389*2 #last layer
mll_depth=7*10**-6
mll_offset=0*10**-6#0.0001-0.77*10**-5 #offset in meters
sigma_flat=None # this is the sigma of the layers. None means the optical constants are like a rect function-> faster calculation!
sigma_wedge=None
flip_mll=False# should the mll be flipped ? rotation axis orthogonal to optical axis. This is needed for full field simulation

#--------------------------
#SLITS
mk_slit=True #True if slit should be used
slits_size=60*10**-6 #size in meters
slits_depth=100*10**-6
slit_offset=0.00012
slits_delta=delta_1
slits_beta=beta_1
slits_steps=100 #number of steps in slit
#.............................................
#Vacuum
stepvac=1*10**-6#1 # distance if step is a single distance propagation
N_slices_ff=5000 #farfield slices after lens.
N_slices_bf=1000 #slices before lens (possibly 0 if no special data is needed there)
slicevac=5*10**-6 #distance of a single slice in vac in ff or before the mll
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
save_ot_beforelens=True #This specifies if the intensity before the lens and after slitting should be saved.
save_ot_inlens=False #This specifies if the intensity image inside the lens should be saved 
save_ot_afterlens=True #This specifies if the intensity image after the lens should be saved 
save_ot_wave=True #This specifies if the complex valued wave array at the exit pupil should be saved
save_ot_wave_end=False #This specifies if the complex valued wave array at the end of the simulation
save_ot_focus=True #This specifies if the focal plane wavefront should be saved
#######################################
#EFFICIENCY 
#-------------------------------------
#General parameters
N_depth=6 #number of images taken (number of lens thickness values)
depth_start=5.8*10**-6 #start of efficiency scan in m
depth_end=7*10**-6 #end of efficiency scan in m

#######################################
#OMEGATHETA
#--------------------------------------
#General parameters
N_theta=11 #number of images taken (number of theta values)
theta_start=-0.005 #start of the theta scan in rad
theta_end=0.005 #end of the theta scan in rad

###############################################
#PRE CALCULATION
###############################################
wavelength=sc.h*sc.c/(energy*1000*sc.e)#wavelength in meters.
if shifted_energy!=None:
    print("Applying shifted energy...")
    shifted_wavelength=sc.h*sc.c/(shifted_energy*1000*sc.e)