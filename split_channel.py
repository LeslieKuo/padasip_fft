import numpy as np
from scipy.io import wavfile
import ANCfunc as anc

# def splitChannel(srcMusicFile):
#     #read
#     sampleRate, musicData = wavfile.read(srcMusicFile)
#     #
#     left = []
#     right = []
#     for item in musicData:
#         left.append(item[0])
#         right.append(item[1])
#
#     wavfile.write('splitU.wav' , sampleRate, np.array(left))
#     wavfile.write('splitV.wav', sampleRate, np.array(right))



su,sv,orate =anc.splitChannel('src.wav')