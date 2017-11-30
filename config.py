import optical_constants as oc
#General experimental parameters
energy=17.3 #energy in kev
wavelength=6.62*10**-34*2.99*10**8/(energy*1000*1.6022*10**-19)#wavelength in meters
f=0.0025 #geometrical focal length in meters
theta=-0.007001098235294117 #tilt of the incoming beam -0.0065

#simulation parameters
pxsize=0.2*10**-9 #px size in x direction in m
stepsize_z=10*10**-9
N_px=5*10**5
#---------------------------------------------

#---------------------------------------------
#optical constants of multilayer materials
delta_1=oc.delta_W_17_3
beta_1=oc.beta_W_17_3
delta_2=oc.delta_Si_17_3
beta_2=oc.beta_Si_17_3
#--------------------------

#MLL
#number of layers in MLL
n_begin=322 #first layer
n_end=5822 #last layer
mll_depth=6*10**-6
mll_offset=0#0.0001-0.77*10**-5 #offset in meters
#--------------------------
#grating
grating_period=10*10**-9
grating_layers=500
grating_depth=10*10**-6 #depth of grating
#--------------------------
#SLITS
slits_size=30*10**-6 #size in meters
slits_depth=10*10**-6
slit_offset=7.5*10**-6
slits_delta=oc.delta_W_17_3
slits_beta=oc.beta_W_17_3
slits_steps=100 #number of steps in slit
#.............................................
#Vacuum
stepvac=1*10**-6#1 # distance if step is a single distance propagation
N_slices_ff=2000 #farfield slices
slicevac=0.25*10**-5 #distance of a single slice in vac if multiple slices are calculated
#---------------------
#displaying optiosn
#nf image
save_intensity=True
size_intensity_arr=(2000,2000)
#ff image
size_ff_arr=(4000,4000)
#----------------------
#Advanced stuff and pre-calculations
corr_factor_z=39.36 #correction factor in z direction. There is still a wrong scaling along this axis. !
slicevac_corr=slicevac*corr_factor_z