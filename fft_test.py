import wave
import pyaudio
import ANCfunc as anc
from scipy.io import wavfile
import numpy
import pylab



# ws = "F:/AllProgram/pycharmPros/padasip/single/AUDIOLN1100RS700.wav"
# wf ="F:/AllProgram/pycharmPros/padasip/record/LNmix900_1400.wav"
# mix = "F:/AllProgram/pycharmPros/padasip/mix/bLNx900_1400_sRS500.wav"
# mic = "F:/AllProgram/pycharmPros/padasip/mic/W1000P16.wav"
# mic1 = "F:/AllProgram/pycharmPros/padasip/mic/AUDIO1.wav"
# name = mic[-11:]
# name = name[:-4]
# print(name)
# single = "F:/AllProgram/pycharmPros/padasip/single/bLN700_sRS500.wav"
# #wf ="F:/AllProgram/pycharmPros/padasip/record/bLN1300sRS500.wav"
# su, sv, framerate = anc.splitChannel(mic1, 'fft_test')
# #anc.plotfft(su, framerate, name+' u')
# anc.plotfft2(su, framerate, name+' u')
# anc.plotfft(sv, framerate, name+' v' )
# # wr = "F:/AllProgram/pycharmPros/padasip/record/rec1100.wav"
# # su, sv, framerate = anc.splitChannel(wr)
# # anc.plotfft(su, framerate, 'REC u')
#
# corrcoef1 = anc.corr_coef(su,sv)
# print("the origin corrcoef is "+ str(corrcoef1))
# print(type(su))
# su, sv = anc.correlationFunc(su, sv)
# corrcoef2 = anc.corr_coef(su,sv)
# print("After correlation, the corrcoef is "+ str(corrcoef2))
# music = anc.ANC_filter(su, sv)
# wavfile.write('fft_test.py_result.wav', framerate, music)
# wave_data = music
# anc.plotfft(wave_data,framerate, name+'result')



dronerecord = "F:/AllProgram/pycharmPros/padasip/single/drone_record.wav"
dru,drv,orate = anc.splitChannel(dronerecord,"dronerecord")
dru = dru[:320000]
anc.plotfft(dru,orate,"dronerecord")

pleaserecord = "F:/AllProgram/pycharmPros/padasip/single/please_record.wav"
pru,prv,orate2 = anc.splitChannel(pleaserecord,"pleaserecord")
pru = pru[:320000]
anc.plotfft(pru,orate2,"pleaserecord")
ru, rv = anc.pre_combine(pru,dru,0.1,1,0.4,0.8,num=66,uSignalFlag=1,uNoiseFlag=-1,vSignalFlag=-1,vNoiseFlag=1)
cru, crv = anc.correlationFunc(ru, rv)
rmusic = anc.ANC_filter(cru, crv)
wavfile.write('drone_please1.wav', orate, rmusic)
anc.plotfft(rmusic, orate, 'result')

drone = "F:/AllProgram/pycharmPros/padasip/single/drone42s.wav"
please = "F:/AllProgram/pycharmPros/padasip/single/please.wav"
du, dv, rate = anc.splitChannel(drone, 'orgindrone')
pu, pv, prate = anc.splitChannel(please, 'orgindrone')
du = du[:441000]
pu = pu[:441000]
anc.plotfft(pu, rate, 'originmusic')
anc.plotfft(du, rate, 'origindrone_noise')
print(len(du))
print(rate)
print(prate)
u, v = anc.pre_combine(pu,du,0.1,1,0.4,0.8,num=66,uSignalFlag=1,uNoiseFlag=-1,vSignalFlag=-1,vNoiseFlag=1)
wavfile.write('drone_U.wav', rate, u)
wavfile.write('drone_V.wav', rate, v)
anc.plotfft(u, rate, 'combineU')
anc.plotfft(v, rate, 'combineV')
cu, cv = anc.correlationFunc(u, v)
# cu = u[:-67]
# cv = v[67:]
# a = anc.mergeChannel(cu, cv, rate, str="drone_please.wav")
music = anc.ANC_filter(cu, cv)
wavfile.write('drone_please.wav', rate, music)
anc.plotfft(music, rate, 'result')