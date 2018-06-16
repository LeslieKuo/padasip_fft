from scipy.io import wavfile
import numpy as np
import padasip as pa
import ANCfunc as anc


# su, sv, orate = anc.splitChannel('AUDIO.wav')
# sv = sv[320000:]
# su = su[320000:]

orate, signal = wavfile.read('ex9splitU.wav')
orate2, noise = wavfile.read('ex9splitV.wav')
# u,v = anc.pre_combine(signal, noise, 0.1,1,0.2,0.9,1,-1,-1,1)
# wavfile.write('ex9combineU.wav',orate, u)
# wavfile.write('ex9combineV.wav',orate, v)
# su,sv = anc.pre_combine(3000,signal, noise, 0.1,1,0.2,0.6,1,-1,-1,1)
# wavfile.write('ex9combineU.wav', orate, su)
# wavfile.write('ex9combineV.wav', orate, sv)
u ,v = signal,noise
u, v = anc.correlationFunc(u, v)
print(type(u))
wavfile.write('ex9corru.wav', orate, u)
wavfile.write('ex9corrv.wav', orate, v)
music = anc.ANC_filter(u, v)
wavfile.write('ex9filtermusic.wav', orate, music)

