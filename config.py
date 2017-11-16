import optical_constants as oc
#General experimental parameters
energy=17.3 #energy in kev
f=0.005 #geometrical focal length in meters
theta=-0.0065 #tilt of the incoming beam

#simulation parameters
pxsize=0.05*10**-9 #px size in x direction in m
stepsize_z=10*10**-9
N_px=4*10**6
#---------------------------------------------
#SLITS
slits_size=35*10**-6 #size in meters
slits_depth=100*10**-6
slit_offset=0.0001+10.5*10**-6
slits_delta=oc.delta_W_17_3
slits_beta=oc.beta_W_17_3
slits_steps=100 #number of steps in slit
#.............................................
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
mll_offset=0.0001-4*10**-5 #offset in meters
#--------------------------
#grating
grating_period=10*10**-9
grating_layers=500
grating_depth=10*10**-6 #depth of grating
#--------------------------
#Vacuum
stepvac=1 # distance if step is a single distance propagation
N_slices_ff=4000 #farfield slices
slicevac=0.00002 #distance of a single slice in vac if multiple slices are calculated
#---------------------
#displaying optiosn
#nf image
save_intensity=True
size_intensity_arr=(2000,2000)
#ff image
size_ff_arr=(4000,4000)
#----------------------
wavelength=6.62*10**-34*2.99*10**8/(energy*1000*1.6022*10**-19) #wavelength in meters