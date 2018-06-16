from scipy.io import wavfile
import pandas as pds
import numpy as np
import padasip as pa
import wave
import pyaudio
import pylab
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

def boundary(array):
    for i in array:
        if i > 32768:
            i = 32768
        elif i <-32767:
            i = 32767
    return array

def corr_coef(a,b):
    a, b = a.astype(np.float64), b.astype(np.float64)
    a = pds.Series(a)
    b = pds.Series(b)
    corr = a.corr(b)
    print(corr)
    return corr

def correlationFunc(U,V):
# 需要归一化再求互相关！
    Uorigin, Vorigin = U, V
    U, V = U.astype(np.float64), V.astype(np.float64)
    U_max = np.max(np.abs(U))
    V_max = np.max(np.abs(V))
    mmax = np.max([U_max,V_max])
    U /= mmax
    V /= mmax
    csame = np.correlate(U, V, "same")
    ref = np.argmax(csame)+1
    print("The reference of max is ",ref)
    half_len = len(U) // 2
    print("The half length is  ", half_len)

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
    #music = music[44100:]
    mmax = np.max(music)
    music = music * 32768 // mmax
    music = music.astype(np.int16)
    print("the length of filter result is ",len(music))
    return music

def pre_combine(signal,noise, u1,u2,v1,v2,num=0, uSignalFlag=0,uNoiseFlag=0,vSignalFlag=0,vNoiseFlag=0):
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
def mergeChannel(u,v,rate):
    left = u
    right = v
    # m = np.array([left, right])
    # m = m.astype(np.float64)
    print(type(left))
    m = list(zip(left,right))
    m = np.array(m)
    print(type(m))
    wavfile.write('ex10merge.wav', rate, m)
    return m.dtype
def splitChannel(srcMusicFile,str):
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
    wavfile.write(str+'splitU.wav', sampleRate, splitu)
    wavfile.write(str+'splitV.wav', sampleRate, splitv)
    return splitu, splitv, sampleRate

def plotfft(wave_data,framerate,title,maxY = 20000):
    N = 44100
    start = 0  # 开始采样位置
    df = framerate / (N - 1)  # 分辨率
    freq = [df * n for n in range(0, N)]  # N个元素
    wave_data2 = wave_data[start:start + N]
    c = np.fft.fft(wave_data2) * 2 / N
    # 常规显示采样频率一半的频谱
    d = int(len(c) / 2)
    # 仅显示频率在4000以下的频谱
    while freq[d] > 4000:
        d -= 10

    ax = subplot(111)
    xmajorLocator = MultipleLocator(500)  # 将x主刻度标签设置为20的倍数
    xmajorFormatter = FormatStrFormatter('%1.1f')  # 设置x轴标签文本的格式
    xminorLocator = MultipleLocator(50)  # 将x轴次刻度标签设置为5的倍数
    # 设置主刻度标签的位置,标签文本的格式
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.xaxis.set_major_formatter(xmajorFormatter)
    # 显示次刻度标签的位置,没有标签文本
    ax.xaxis.set_minor_locator(xminorLocator)
    ax.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度

    ymajorLocator = MultipleLocator(5000)  # 将y轴主刻度标签设置为0.5的倍数
    ymajorFormatter = FormatStrFormatter('%1.1f')  # 设置y轴标签文本的格式
    yminorLocator = MultipleLocator(500)  # 将此y轴次刻度标签设置为0.1的倍数
    ax.yaxis.set_major_locator(ymajorLocator)
    ax.yaxis.set_major_formatter(ymajorFormatter)
    ax.yaxis.set_minor_locator(yminorLocator)
    ax.yaxis.grid(True, which='minor')  # y坐标轴的网格使用次刻度




    pylab.plot(freq[:d - 1], abs(c[:d - 1]), 'r')
    pylab.axis([0,4000,0, maxY])
    pylab.title(title)
    pylab.show()

def plotfft2(wave_data,framerate,title,maxY = 30000):
    N = 44100
    start = 0  # 开始采样位置
    df = framerate / (N - 1)  # 分辨率
    freq = [df * n for n in range(0, N)]  # N个元素
    wave_data2 = wave_data[start:start + N]
    c = np.fft.fft(wave_data2) * 2 / N
    # 常规显示采样频率一半的频谱
    d = int(len(c) / 2)
    # 仅显示频率在4000以下的频谱
    while freq[d] > 4000:
        d -= 10

    ax = subplot(111)
    xmajorLocator = MultipleLocator(500)  # 将x主刻度标签设置为20的倍数
    xmajorFormatter = FormatStrFormatter('%1.1f')  # 设置x轴标签文本的格式
    xminorLocator = MultipleLocator(50)  # 将x轴次刻度标签设置为5的倍数
    # 设置主刻度标签的位置,标签文本的格式
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.xaxis.set_major_formatter(xmajorFormatter)
    # 显示次刻度标签的位置,没有标签文本
    ax.xaxis.set_minor_locator(xminorLocator)
    ax.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度

    ymajorLocator = MultipleLocator(maxY/15)  # 将y轴主刻度标签设置为0.5的倍数
    ymajorFormatter = FormatStrFormatter('%1.1f')  # 设置y轴标签文本的格式
    yminorLocator = MultipleLocator(maxY/60)  # 将此y轴次刻度标签设置为0.1的倍数
    ax.yaxis.set_major_locator(ymajorLocator)
    ax.yaxis.set_major_formatter(ymajorFormatter)
    ax.yaxis.set_minor_locator(yminorLocator)
    ax.yaxis.grid(True, which='minor')  # y坐标轴的网格使用次刻度




    pylab.plot(freq[:d - 1], abs(c[:d - 1]), 'r')
    pylab.axis([0,4000,0, maxY])
    pylab.title(title)
    pylab.show()