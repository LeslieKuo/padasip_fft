from scipy.io import wavfile
import pandas as pds
import numpy as np
import padasip as pa
import wave
import pyaudio
import pylab
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from scipy import interpolate

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
    # only use 3 seconds to correlate
    U3 = U[24000:96000]
    V3 = V[24000:96000]
    # U3 = U[74000:96000]
    # V3 = V[74000:96000]
    csame = np.correlate(U3, V3, "same")
    ref = np.argmax(csame)+1
    print("The reference of max is ", ref)
    half_len = len(U3) // 2
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
    # mmax = np.max(music)
    # print(mmax)
    # music = music * 32768 // mmax
    # music = music.astype(np.int16)
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
def mergeChannel(u,v,rate,str="ex10merge.wav"):
    left = u
    right = v
    # m = np.array([left, right])
    # m = m.astype(np.float64)
    # print(type(left))
    m = list(zip(left,right))
    m = np.array(m)
    # print(type(m))
    wavfile.write("./output/"+str, rate, m)
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
    splitu, splitv = splitu.astype(np.int16), splitv.astype(np.int16)
    return splitu, -splitv, sampleRate
    # return splitu, splitv, sampleRate
def changeAmplitude(u,v):
    # max_value = max(np.max(u), np.max(v))
    # ukey, vkey = max_value/np.max(u), max_value/np.max(v)*1.1
    max_value = max(np.average(np.abs(u)),np.average(np.abs(v)))
    ukey, vkey = max_value / np.average(np.abs(u)), max_value / np.average(np.abs(v))
    au, av = u * ukey, v * vkey
    au, av = au.astype(np.int16), av.astype(np.int16)
    key = 0
    str = "nothing"
    if ukey >1:
        key = ukey
        str = "amplify U"
        print(str)
    elif vkey >1:
        key = vkey
        str = "amplify V"
        print(str)
    print("changeAmlitude key is ",key)
    return au,av,key

def plotfft(wave_data,framerate,title,maxY = 10000):#maxY=20000
    N = 44100
    start = 0  # 开始采样位置
    df = framerate / (N - 1)  # 分辨率
    freq = [df * n for n in range(0, N)]  # N个元素
    wave_data2 = wave_data[start:start + N]
    c = np.fft.fft(wave_data2) * 2 / N
    # 常规显示采样频率一半的频谱
    d = int(len(c) / 2)
    # 仅显示频率在4000以下的频谱
    while freq[d] > 10000:
        d -= 10

    ax = subplot(111)
    xmajorLocator = MultipleLocator(1000)  # 将x主刻度标签设置为20的倍数
    xmajorFormatter = FormatStrFormatter('%1.1f')  # 设置x轴标签文本的格式
    xminorLocator = MultipleLocator(100)  # 将x轴次刻度标签设置为5的倍数
    # 设置主刻度标签的位置,标签文本的格式
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.xaxis.set_major_formatter(xmajorFormatter)
    # 显示次刻度标签的位置,没有标签文本
    ax.xaxis.set_minor_locator(xminorLocator)
    ax.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度

    ymajorLocator = MultipleLocator(1000)  # 将y轴主刻度标签设置为0.5的倍数
    ymajorFormatter = FormatStrFormatter('%1.1f')  # 设置y轴标签文本的格式
    yminorLocator = MultipleLocator(100)  # 将此y轴次刻度标签设置为0.1的倍数
    ax.yaxis.set_major_locator(ymajorLocator)
    ax.yaxis.set_major_formatter(ymajorFormatter)
    ax.yaxis.set_minor_locator(yminorLocator)
    ax.yaxis.grid(True, which='minor')  # y坐标轴的网格使用次刻度

    pylab.plot(freq[:d - 1], abs(c[:d - 1]), 'r')
    pylab.axis([0, 10000, 0, maxY])
    pylab.title(title)
    pylab.show()

def plotfft2(wave_data,framerate,title,maxY = 1000):
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

def find_min_positition(su, sv):
    min_result = (0, math.inf)
    for align in range(1, 100):
        su_ = su[:-align]
        sv_ = sv[align:]
        value_ave = np.average(np.abs(su_-sv_))
        # value_max = np.max(np.abs(su_-sv_))
        # value = min(value_ave,value_max)
        if value_ave <min_result[1]:
            min_result = (align, value_ave)

    # #以下是肉眼
    # su_ = su[:-72]
    # sv_ = sv[72:]
    # value_ave = np.average(np.abs(su_ - sv_))
    # min_result = (72, value_ave)
    return min_result

def phase_shift(signal,phase):
    assert 0 <= phase <= 1
    x = np.arange(0, len(signal))
    y = np.array(signal)
    f = interpolate.interp1d(x, y)
    xnew = np.arange(phase, len(signal)-1, 1)
    # xnew = np.arange(0, len(signal) - 1, phase)
    ynew = f(xnew)
    return ynew
#
# 插值一次，记录八个list ，sulist  svlist 分别用find min dist 做八次筛选
# def find_accurate_min_dist(su,sv, positition,phase):
#     accurate_result = (0, math.inf)
#     assert 1 <= positition <= 100
#     assert 0 <= phase <= 1
#     for accurate_num in range(-1,1,phase):
#         su_ = su[:-positition-accurate_num]
#         sv_ = sv[positition+accurate_num:]
#         value = np.average(np.abs(su_-sv_))
#         if value < accurate_result[1]:
#             accurate_result = (positition+accurate_num, value)
#     return accurate_result

def interpolate_value(signal,phase):
    assert 0 <= phase <= 1
    x = np.arange(0, len(signal))
    y = np.array(signal)
    f = interpolate.interp1d(x, y)
    xnew = np.arange(0, len(signal) - 1, phase)
    ynew = f(xnew)
    ylist =[]
    ylist.append(ynew[::8])
    ylist.append(ynew[1::8])
    ylist.append(ynew[2::8])
    ylist.append(ynew[3::8])
    ylist.append(ynew[4::8])
    ylist.append(ynew[5::8])
    ylist.append(ynew[6::8])
    ylist.append(ynew[7::8])
    # print(type(ylist[0]))
    return ylist

def align_ref(ref_align_num,su,sv):
    assert 20 <= ref_align_num
    min_result = (ref_align_num, math.inf)
    for delta in range(-20, 20):
        su_ = su[:-ref_align_num-delta]
        sv_ = sv[ref_align_num+delta:]
        value_ave = np.average(np.abs(su_-sv_))
        # value_max = np.max(np.abs(su_-sv_))
        # value = min(value_ave,value_max)
        if value_ave <min_result[1]:
            min_result = (ref_align_num+delta, value_ave)
    return min_result