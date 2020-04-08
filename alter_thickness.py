import config as cf
import numpy as np
corrected_layers=np.load(cf.fnam_corr)
N_layers=int(cf.n_end-cf.n_begin)
#First sampling the corrected_layers array with the given px size
pxsize=cf.pxsize
corrected_layers_samp=np.round(corrected_layers*10**-9/pxsize)*pxsize
plt.plot(corrected_layers_samp)
plt.plot(corrected_layers*10**-9)