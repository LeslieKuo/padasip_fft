#This file is made by using time field shuffle to reduce noise
#Example: ../mic/AUDIO1.wav
#Manual measure result: delta T = 56 point Rdelay，cutRtail. Power R0.025 L0.08
from scipy.io import wavfile
import numpy as np
import padasip as pa
import ANCfunc as anc

name = "interval"
#su, sv, orate = anc.splitChannel("F:/AllProgram/pycharmPros/padasip/single/interval8_16result.wav","raw_manual")
su, sv, orate = anc.splitChannel("F:/AllProgram/pycharmPros/padasip/mix/Vol13.wav","interval_result")
type1 = anc.mergeChannel(su,sv,orate,str="afterInverse.wav")
alignnum = 68
su = su[:-alignnum]
sv = sv[alignnum:]
# su, sv = anc.correlationFunc(su, sv)

# print(len(su), len(sv))
anc.plotfft2(su, orate, ' u')
anc.plotfft2(sv, orate, ' v')
print("near noise data is ", su)
print("near signal data is ", sv)
type = anc.mergeChannel(su,sv,orate,str="afterAlign"+str(alignnum)+".wav")

su, sv , key = anc.changeAmplitude(su, sv)
type2 = anc.mergeChannel(su,sv,orate,str="afterChangeAmplit"+str(alignnum)+".wav")
# result = sv + su*0.08/0.45*1.01
result = sv - su
result = result/key
result = result.astype(np.int16)
# result = anc.boundary(result)
# print(result.dtype)




# _max = np.max(np.abs(result))
# result /= _max
wavfile.write("./output/"+name+str(alignnum)+'_result.wav', orate, result)
anc.plotfft2(result, orate, str(alignnum)+'result')
anc.plotfft(result, orate, str(alignnum)+'result')