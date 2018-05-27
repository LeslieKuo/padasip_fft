from scipy.io import wavfile
import numpy as np
import padasip as pa
import ANCfunc as anc

orate, signal = wavfile.read('sin300_10s.wav')
orate2, noise = wavfile.read('sin1400_10s.wav')
u,v = anc.pre_combine(0,signal, noise, 0.9,0.7,0.2,0.9,0,0,0,0)
anc.plotfft(u, orate)
#anc.plotfft(v, orate2)
u, v = anc.correlationFunc(u, v)
music = anc.ANC_filter(u, v)
# anc.plotfft(u,orate)
# anc.plotfft(v, orate2)