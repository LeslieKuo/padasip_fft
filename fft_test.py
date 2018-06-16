import wave
import pyaudio
import ANCfunc as anc
from scipy.io import wavfile
import numpy
import pylab


# wf = "bbLN1100RS300.wav"
ws = "F:/AllProgram/pycharmPros/padasip/single/AUDIOLN1100RS700.wav"
wf ="F:/AllProgram/pycharmPros/padasip/record/LNmix900_1400.wav"
mix = "F:/AllProgram/pycharmPros/padasip/mix/bLNx900_1400_sRS500.wav"
mic = "F:/AllProgram/pycharmPros/padasip/mic/W1000P16.wav"
mic1 = "F:/AllProgram/pycharmPros/padasip/mic/AUDIO1.wav"
name = mic[-11:]
name = name[:-4]
print(name)
single = "F:/AllProgram/pycharmPros/padasip/single/bLN700_sRS500.wav"
#wf ="F:/AllProgram/pycharmPros/padasip/record/bLN1300sRS500.wav"
su, sv, framerate = anc.splitChannel(mic1, 'fft_test')
#anc.plotfft(su, framerate, name+' u')
anc.plotfft2(su, framerate, name+' u')
anc.plotfft(sv, framerate, name+' v' )
# wr = "F:/AllProgram/pycharmPros/padasip/record/rec1100.wav"
# su, sv, framerate = anc.splitChannel(wr)
# anc.plotfft(su, framerate, 'REC u')

corrcoef1 = anc.corr_coef(su,sv)
print("the origin corrcoef is "+ str(corrcoef1))
print(type(su))
su, sv = anc.correlationFunc(su, sv)
corrcoef2 = anc.corr_coef(su,sv)
print("After correlation, the corrcoef is "+ str(corrcoef2))
music = anc.ANC_filter(su, sv)
wavfile.write('fft_test.py_result.wav', framerate, music)
wave_data = music
anc.plotfft(wave_data,framerate, name+'result')
