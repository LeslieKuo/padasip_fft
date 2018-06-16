import wave
import pyaudio
import ANCfunc as anc
import numpy as np
import pylab
from scipy.io import wavfile
import numpy
#
mic1 = "F:/AllProgram/pycharmPros/padasip/mix/bLNx900_1400_sRS500.wav"
su, sv, framerate = anc.splitChannel(mic1, 'fft_test')
su = su[32000:32050]
sv = sv[32000:32050]
U = [1,3,3,4,5,6,7,8]
V = [8,13,12,14,16,10,6,6]
uu,vv = np.array(U),np.array(V)
a,b = anc.correlationFunc(su, sv)
print("u after corr is ", a)
print("v after corr is", b)
U_max = np.max(np.abs(U))
V_max = np.max(np.abs(V))
mmax = np.max([U_max, V_max])
U /= mmax
V /= mmax
print(U,V)
half_len = len(U) // 2

csame = np.correlate(U, V, "same")
ref = np.argmax(csame)+1
print(ref)
print(csame)
d = abs(ref - half_len)
print(d)

# noise = "F:/AllProgram/pycharmPros/padasip/mix/sin900.wav"
# signal = "F:/AllProgram/pycharmPros/padasip/mix/sin1400.wav"
# su, sv, orate = anc.splitChannel(signal)
# su2, sv2, framerate2 = anc.splitChannel(noise)
# equal, none = anc.pre_combine(su,sv,1,0,1,1)
# U =  su/4 + su2/4
# Uout = U.astype(np.int16)
# wavfile.write('ex9mix900_1400.wav', orate,Uout)
# anc.plotfft(Uout, orate, 'origin u')

# wr = "F:/AllProgram/pycharmPros/padasip/record/rec1100.wav"
# su, sv, framerate = anc.splitChannel(wr)
# anc.plotfft(su, framerate, 'REC u')


# su, sv = anc.correlationFunc(su, sv)
# music = anc.ANC_filter(su, sv)
# wave_data = music
# anc.plotfft(wave_data,framerate, 'result')
