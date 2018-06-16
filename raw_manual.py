#This file is made by using time field shuffle to reduce noise
#Example: ../mic/AUDIO1.wav
#Manual measure result: delta T = 56 point Rdelay，cutRtail. Power R0.025 L0.08
from scipy.io import wavfile
import numpy as np
import padasip as pa
import ANCfunc as anc


su, sv, orate = anc.splitChannel("F:/AllProgram/pycharmPros/padasip/single/interval8_16result.wav","raw_manual")
# print(len(su))
su = su[:-67]
sv = sv[67:]
wavfile.write('ex10suraw.wav', orate, su)
wavfile.write('ex10svraw.wav', orate, sv)
# print(len(su), len(sv))
anc.plotfft(su, orate, ' u')
anc.plotfft(sv, orate, ' v')
print("near noise data is ", su)
print("near signal data is ", sv)
type = anc.mergeChannel(su,sv,orate)
# print(type)
# result = sv - su*0.025/0.08
#
# result = sv - su*0.073/0.56
result = sv - su*0.123/0.92*1.01
result = anc.boundary(result)
print(result.dtype)
print(result)
result = result.astype(np.int16)
print(result.dtype)
# _max = np.max(np.abs(result))
# result /= _max
wavfile.write('ex10raw.wav', orate, result)
anc.plotfft(result, orate, 'result')