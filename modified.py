import ANCfunc as anc
import numpy as np
from scipy.io import wavfile

name = "Mdrone1500"
file = "./mix/8016-Vol13-s.wav"
file1000 = "./mix/M1000.wav"
filedrone = "./mix/M1500_light.wav"
# splitu = "./output/M1000reappearsplitU.wav"
# splitv = "./output/M1000reappearsplitV.wav"
# orate, splitu = wavfile.read(splitu)
# orate2, splitv = wavfile.read(splitv)
# anc.plotfft(splitu,orate,"splitu")
# anc.plotfft(splitv,orate2,"splitv")

u, v, rate = anc.splitChannel(filedrone, name)
# u, v, rate = anc.splitChannel("F:/AllProgram/pycharmPros/padasip/mix/Malign.wav", name)
# file = "F:/AllProgram/pycharmPros/padasip/mix/LNdroneRSxie.wav"
# # file = "F:/AllProgram/pycharmPros/padasip/single/light.wav"
# u, v, rate = anc.splitChannel(file, "origin")
anc.plotfft(u, rate, name+' u')
anc.plotfft2(u, rate, name+' u')
anc.plotfft(v, rate, name+' v')
anc.plotfft2(v, rate, name+' v')
# cu, cv = anc.correlationFunc(u, v)
cu = u[:-51]
cv = v[51:]
#a = anc.mergeChannel(cu, cv, rate, str=name+"_merge.wav")
music = anc.ANC_filter(cu, cv)
maxm = max(music)
music = music/maxm * 32700
music = music.astype(np.int16)
wavfile.write("./output/"+name+'_result.wav', rate, music)
anc.plotfft2(music, rate, name+'_result')
anc.plotfft(music, rate, name+'_result')
music10 = music[:240000]
music20 = music[240000:480000]
music30 = music[480000:]
anc.plotfft(music10,rate,"music10")
anc.plotfft(music20,rate,"music20")
anc.plotfft(music30,rate,"music30")
anc.plotfft2(music10,rate,"music10")
anc.plotfft2(music20,rate,"music20")
anc.plotfft2(music30,rate,"music30")


