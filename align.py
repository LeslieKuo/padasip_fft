import ANCfunc as anc
import numpy as np
from scipy.io import wavfile

filename = "./mix/Minterval.wav"
name = filename[6:-4]
u, v, rate = anc.splitChannel(filename,name)
# file = "F:/AllProgram/pycharmPros/padasip/mix/LNdroneRSxie.wav"
# # file = "F:/AllProgram/pycharmPros/padasip/single/light.wav"
# u, v, rate = anc.splitChannel(file, "origin")
anc.plotfft2(u, rate, ' u')
anc.plotfft2(v, rate, ' v')
# cu, cv = anc.correlationFunc(u, v)
cu = u[:-49]
cv = v[49:]
#a = anc.mergeChannel(cu, cv, rate, str= name)
music = anc.ANC_filter(cu, cv)
wavfile.write(name, rate, music)
anc.plotfft2(music, rate, name+'_result')