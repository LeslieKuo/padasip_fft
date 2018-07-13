#This file is made by using time field shuffle to reduce noise
#Example: ../mic/AUDIO1.wav
#Manual measure result: delta T = 56 point Rdelay，cutRtail. Power R0.025 L0.08
from scipy.io import wavfile
import numpy as np
import padasip as pa
import ANCfunc as anc

name = "interval_vol22_"
# alignnum = 74 #for Vol20
alignnum = 70 #for vol18
#su, sv, orate = anc.splitChannel("F:/AllProgram/pycharmPros/padasip/single/interval8_16result.wav","raw_manual")
su, sv, orate = anc.splitChannel("F:/AllProgram/pycharmPros/padasip/mix/Vol22.wav","interval_result")
type1 = anc.mergeChannel(su,sv,orate,str="afterInverse"+str(alignnum)+".wav")

# # alignnum = 70 #for Val13
# su = su[:-alignnum]
# sv = sv[alignnum:]
# # su, sv = anc.correlationFunc(su, sv)


# anc.plotfft2(su, orate, ' u')
# anc.plotfft2(sv, orate, ' v')
# print("near noise data is ", su)
# print("near signal data is ", sv)
# type = anc.mergeChannel(su,sv,orate,str="afterAlign"+str(alignnum)+".wav")
#
# su, sv, key = anc.changeAmplitude(su, sv)
# type2 = anc.mergeChannel(su,sv,orate,str="afterChangeAmplit"+str(alignnum)+".wav")
# result = sv - su
# result = result/key
# result = result.astype(np.int16)
# # result = anc.boundary(result)
# # print(result.dtype)
#
#
# wavfile.write("./output/"+name+str(alignnum)+'_result.wav', orate, result)
# anc.plotfft2(result, orate, str(alignnum)+'result')
# anc.plotfft(result, orate, str(alignnum)+'result')

#测试插值
su, sv, key = anc.changeAmplitude(su, sv)
type2 = anc.mergeChannel(su,sv,orate,str="afterChangeAmplit"+str(alignnum)+".wav")
# ulist ,vlist = anc.interpolate_value(su, 0.125), anc.interpolate_value(sv, 0.125)
# (align_num, min_dist) = anc.find_min_positition(ulist[0],vlist[0])
(num, dist) = anc.align_ref(72,su,sv)
print("after align_ref, the align Num is ",num)
print("after align_ref, the dist is ",dist)
succ, svcc = anc.correlationFunc(su, sv)
(align_num, min_dist) = anc.find_min_positition(su, sv)
print("After find min positition, min_dist is ",min_dist)
print("After find min position, align_num is ",align_num)

su = su[:-num]
sv = sv[num:]
type = anc.mergeChannel(su,sv,orate,str="afterAlign"+str(num)+".wav")
result = sv - su
result = result/key
result_abs = np.abs(result)
result_abs = result_abs.astype(np.int16)
result = result.astype(np.int16)
wavfile.write("./output/"+name+str(num)+'_result.wav', orate, result)
# wavfile.write("./output/"+name+'_absresult.wav', orate, result_abs)
#以上为测试内容