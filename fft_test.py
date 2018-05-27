import wave
import pyaudio
import ANCfunc as anc
import numpy
import pylab


# wf = "bbLN1100RS300.wav"
wf ="F:/AllProgram/pycharmPros/padasip/record/mcu1100.wav"
su, sv, framerate = anc.splitChannel(wf)
anc.plotfft(su, framerate, 'origin u')
# anc.plotfft(sv, framerate, 'origin v')
wr = "F:/AllProgram/pycharmPros/padasip/record/rec1100.wav"
su, sv, framerate = anc.splitChannel(wr)
anc.plotfft(su, framerate, 'REC u')
# su, sv = anc.correlationFunc(su, sv)
# music = anc.ANC_filter(su, sv)
# wave_data = music
# anc.plotfft(wave_data,framerate, 'result')
