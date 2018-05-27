from scipy.io import wavfile
import numpy as np
import padasip as pa
import wave
import pyaudio
import numpy
import pylab

def correlationFunc(U,V):
# 需要归一化再求互相关！
    Uorigin, Vorigin = U, V
    U, V = U.astype(np.float64), V.astype(np.float64)
    U_max = np.max(np.abs(U))
    V_max = np.max(np.abs(V))
    U /= U_max
    V /= V_max
    csame = np.correlate(U, V, "same")
    ref = np.argmax(csame)
    half_len = len(U) // 2

    d = abs(ref - half_len)
    print("delaytime number is ",d)
    a, b = Uorigin, Vorigin
    if ref < half_len :
        a = a[:len(a)-d]
        b = b[d:]
        print("lastPremeter delay")
    else:
        b = b[:len(a)-d]
        a = a[d:]
        print("frontPremeter delay")

    a = a.astype(np.int16)
    b = b.astype(np.int16)
    print("the length of corr result U ,V is ",len(a), len(b))
    return a, b

def ANC_filter(U, V):
    # filtering
    # n = 20  # length of filter
    n = 40
    Udelay = pa.input_from_history(U, n)[:-1]
    #Vdelay = V[n - 1:-1]
    Vdelay = V[n-1:-1]
    f = pa.filters.FilterRLS(mu=0.99, n=n)
    y, e, w = f.run(Vdelay, Udelay)
    music = e.astype(np.int16)
    music = music[44100:]
    mmax = np.max(music)
    music = music * 32768 // mmax
    music = music.astype(np.int16)
    print("the length of filter result is ",len(music))
    return music

def pre_combine(num,signal,noise, u1,u2,v1,v2, uSignalFlag,uNoiseFlag,vSignalFlag,vNoiseFlag):
    uNoise = noise
    usignal = signal
    vNoise = noise
    vsignal = signal
    if uSignalFlag == 1: #signal delay need cut tail
        usignal = signal[:len(signal)-num]
    elif uSignalFlag == -1:#signal ahead. need to cut head
        usignal = signal[num:]
    if vSignalFlag == 1: #signal delay need cut tail
        vsignal = signal[:len(signal)-num]
    elif vSignalFlag == -1:#signal ahead. need to cut head
        vsignal = signal[num:]
    if uNoiseFlag == 1: #noise delay , Need to cut tail
        uNoise = noise[:len(noise)-num]
    elif uNoiseFlag == -1:
        uNoise = noise[num:]  #noise ahead, Need to cut head
    if vNoiseFlag == 1:  # noise delay , Need to cut tail
        vNoise = noise[:len(noise) - num]
    elif vNoiseFlag == -1:
        vNoise = noise[num:]  # noise ahead, Need to cut head

    up = u1 + u2
    vp = v1 + v2
    U = u1*usignal/up + u2*uNoise/up
    V = v1*vsignal/vp + v2*vNoise/vp

    Uout, Vout = U.astype(np.int16), V.astype(np.int16)
    print("the combine result: coefficients",u1,u2,v1,v2)
    return Uout, Vout

def splitChannel(srcMusicFile):
    #read
    sampleRate, musicData = wavfile.read(srcMusicFile)
    #
    left = []
    right = []
    for item in musicData:
        left.append(item[0])
        right.append(item[1])
    splitu, splitv = np.array(left), np.array(right)
    key = 32768/np.max(splitu)
    splitu = splitu*key
    splitv = splitv*key
    splitu, splitv = splitu.astype(np.int16), splitv.astype(np.int16)
    wavfile.write('ex9splitU.wav', sampleRate, splitu)
    wavfile.write('ex9splitV.wav', sampleRate, splitv)
    return splitu, splitv, sampleRate

def plotfft(wave_data,framerate,title):
    N = 44100
    start = 0  # 开始采样位置
    df = framerate / (N - 1)  # 分辨率
    freq = [df * n for n in range(0, N)]  # N个元素
    wave_data2 = wave_data[start:start + N]
    c = numpy.fft.fft(wave_data2) * 2 / N
    # 常规显示采样频率一半的频谱
    d = int(len(c) / 2)
    # 仅显示频率在4000以下的频谱
    while freq[d] > 4000:
        d -= 10
    pylab.plot(freq[:d - 1], abs(c[:d - 1]), 'r')
    pylab.title(title)
    pylab.show()