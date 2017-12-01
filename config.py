import optical_constants as oc
#General experimental parameters
energy=17.3 #energy in kev
wavelength=6.62*10**-34*2.99*10**8/(energy*1000*1.6022*10**-19)#wavelength in meters
f=0.0025 #geometrical focal length in meters
scanmode="single" #This is very important. If "single" is chosen only a single shot is taken. "efficiency" does a scan of mll depth and measures the efficiency (not implemented yet) ."omegatheta" does an omegathetascan (not implemented yet). 

#simulation parameters
pxsize=0.2*10**-9 #px size in x direction in m
stepsize_z=10*10**-9
N_px=5*10**5
#---------------------------------------------
#Incident wave
incident_type="plane"#shape of the incident wave (right now only plane wave supported. For this enter "plane")
theta=-0.0065 #angle of the incident wave in rad 

#---------------------------------------------
#optical constants of multilayer materials
delta_1=oc.delta_W_17_3
beta_1=oc.beta_W_17_3
delta_2=oc.delta_Si_17_3
beta_2=oc.beta_Si_17_3
#--------------------------

#MLL
#number of layers in MLL
mll_type="flat" #choose "flat" or wedged
n_begin=322 #first layer
n_end=5822 #last layer
mll_depth=6*10**-6
mll_offset=0#0.0001-0.77*10**-5 #offset in meters
#--------------------------
#SLITS
mk_slit=True #True if slit should be used
slits_size=30*10**-6 #size in meters
slits_depth=10*10**-6
slit_offset=7.5*10**-6
slits_delta=oc.delta_W_17_3
slits_beta=oc.beta_W_17_3
slits_steps=100 #number of steps in slit
#.............................................
#Vacuum
stepvac=1*10**-6#1 # distance if step is a single distance propagation
N_slices_ff=500 #farfield slices
slicevac=1*10**-5 #distance of a single slice in vac if multiple slices are calculated
#---------------------
#..................................................
#######################################
#SCANNING PARAMETERS. please jump to the respective section to choose your scanning parameters
#######################################
#Single
#nf image (intensity in the lens)
save_intensity=True
size_intensity_arr=(2000,2000)
#ff image (intensity after lens of the focus etc)
size_ff_arr=(4000,4000)
#----------------------
