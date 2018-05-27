from scipy.io import wavfile
import ANCfunc as anc
import os

src_wav = "F:/ANCfile/src"
wav_name = os.listdir(src_wav)
print(type(wav_name[0]))
print(wav_name[0])
# u is noise
# su, sv, orate = anc.splitChannel(wav_name[0])
#
# sv = sv[320000:]
# su = su[320000:]
#
#
# #u, v = anc.correlationFunc(sv, su)
# u, v = anc.correlationFunc(su, sv)
# wavfile.write('ex9corru.wav', orate, u)
# wavfile.write('ex9corrv.wav', orate, v)
# music = anc.ANC_filter(u, v)
# wavfile.write('ex9filtermusic.wav', orate, music)

su, sv, orate = anc.splitChannel(src_wav+'/'+wav_name[0])
music = sv
writepath = "F:/ANCfile/write_result"
writepath = writepath +"/ex9.wav"
wavfile.write(writepath, orate, music)
