#This file is to run a test of the selected geometry. it will plot all respective distances 
import numpy as np
import matplotlib.pyplot as plt
import config as cf
import mk_sample as mks
import matplotlib.patches as patches
y_arr=np.linspace(0,cf.N_px*cf.pxsize,cf.N_px)
range_x=cf.slits_depth+cf.stepvac+cf.mll_depth+cf.N_slices_ff*cf.slicevac
min_pxsize=np.amin(((cf.slits_depth/cf.slits_steps),cf.stepvac,cf.stepsize_z,cf.slicevac))
x_arr=np.arange(0,range_x,min_pxsize)
pxsize=cf.pxsize
#DRAW SLITS
x_minslit=0
x_maxslit=cf.slits_depth
x_medslit=(x_maxslit-x_minslit)/2
y_slitl=np.linspace(0,cf.slit_offset,100)
x_slitleft=0*np.ones((100))
x_slitright=x_maxslit*np.ones((100))
y_slitu=np.linspace(cf.slit_offset+cf.slits_size,cf.N_px*cf.pxsize,100)
x_slithorz=np.linspace(x_minslit,x_maxslit,100)
y_slithorzup=(cf.slit_offset+cf.slits_size)*np.ones((100))
y_slithorzdown=cf.slit_offset*np.ones((100))
#Draw LENS
x_minmll=x_maxslit+cf.stepvac
x_maxmll=x_minmll+cf.mll_depth
y_minmll=cf.mll_offset+mks.wedged_mll_x(n_layer=cf.n_begin,focallength=cf.f,z=0,wavelength=cf.wavelength)
y_maxmll=cf.mll_offset+mks.wedged_mll_x(n_layer=cf.n_end,focallength=cf.f,z=0,wavelength=cf.wavelength)
#Adding example rays
x_ax_rays=np.linspace(0,1.1*x_maxmll,1000)
#PLOTTING
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
for p in [
    patches.Rectangle(
        (x_minmll, y_minmll+cf.mll_offset),   # mll(x,y)
        (x_maxmll-x_minmll),          # mllwidth
        (y_maxmll-y_minmll),          # mllheight
        hatch='/',
        facecolor="blue",
    ),
    patches.Rectangle( #slit lower
        (0,0 ), cf.slits_depth, cf.slit_offset,
        facecolor="red",
    ),
    patches.Rectangle( #slit upper
        (0,cf.slit_offset+cf.slits_size ), cf.slits_depth, y_arr[-1]-(cf.slit_offset+cf.slits_size),
        facecolor="red",
    ),
]:
    ax1.add_patch(p)
for i in range(0,10,1):
    y_ax_rays=np.sin(cf.theta)*x_ax_rays+y_arr[-1]*i/10
    ax1.plot(x_ax_rays,y_ax_rays,"g--")
ax1.set_autoscaley_on(False)
ax1.set_ylim([0,cf.slit_offset+cf.slits_size+y_arr[-1]-(cf.slit_offset+cf.slits_size)])
ax1.set_xlim([0,x_maxmll*1.1])
plt.show()