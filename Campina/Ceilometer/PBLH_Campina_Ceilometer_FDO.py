import glob
from netCDF4 import Dataset, num2date
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
#from waveletFunctions import wavelet
from scipy.signal import find_peaks

import os
import matplotlib.colors as colors
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.ticker
import matplotlib as mpl
import cmaps


cfiles = sorted(glob.glob('/home/flavio/data/atto/ceilometer_camp/202212_ATTO/20221201*'))
print(cfiles)

cfile = cfiles[0]
file = Dataset(cfile)
    
times = file.variables['time']
vtimes = num2date(times[:], times.units)
rangem = file.variables['range'][0:166]
timestr = []

for x in range(len(vtimes)):
    timestr.append(str(vtimes[x]))

datas = pd.to_datetime(timestr)
bcorrect = []
temp = []
for i in range(len(datas)):
    bprofil = file.variables['beta_raw'][i, 0:166].data
    beta = np.log(bprofil)
    bcorrect.append(beta)
    tmp = file.variables['temp_ext'][i]*0.1
    temp.append(tmp)

z = np.arange(15, 15375, 15)
alt = z[0:166]*0.9659

file.close()

betadf = pd.DataFrame(bcorrect)
betadf = betadf.interpolate(method='polynomial', order=2)
betadf.index = datas
betadf = betadf.resample('5Min').mean()

dft = pd.DataFrame(temp)
dft.index = datas
dft = dft.resample('5Min').mean()


variance = []
variance2 = []
mmean = []

ndatas = betadf.index

mbeta = []
print('Variance')
for i in range(len(betadf)):
    print('Variance calc time: ', ndatas[i])
    nbeta = betadf.iloc[i]
    mbeta.append(betadf.iloc[i])

    flut2 = []
    k = 3
    
    for j in range (0, 110):
        flut2.append((nbeta[j]-np.nanmean(nbeta[0:55]))**2)
        k += 1

    variance.append(flut2)

alta = alt[0:110]
altura = alta[10]
peaksmaxid = 10

pbl = []
alti = alta[6:110] #[6:65]
# 00 UTC até 09:55 UTC
# 20 HL até 05:55 HL

for l in range(0, 24):
    title = str(ndatas[l])
    print(title)
    #alturas:
    print('#####################################')
    print(ndatas[l])
    print('#####################################')
    print(' ')
    print(' ')
    pbl.append(-9999)


for l in range(24, 120):
    title = str(ndatas[l])
    print(title)
    #alturas:
    print('#####################################')
    print(ndatas[l])
    print('#####################################')
    print(' ')
    print(' ')
    pbl.append(-9999)



######################################################################
######################################################################
### DAY TIME
### VARIANCIA
######################################################################
######################################################################

acam = 120
alta = alt[0:120]
flut = []
variance = []
print('Calculo da Variancia')
for i in range(len(betadf)):
    print('Variance calc time: ', ndatas[i])
    nbeta = betadf.iloc[i]
    mbeta.append(betadf.iloc[i])

    flut2 = []
    k = 3
    
    for j in range (0, acam):
        flut2.append((nbeta[j]-np.nanmean(nbeta[0:55]))**2)
        k += 1

    variance.append(flut2)

alta = alt[0:120]
altura = alta[5]
peaksmaxid = 5

alti = alta[2:acam] #[6:65]
print('10 UTC - 06 LT - Day Time')
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

#Each hour are 12 index (l)
for l in range(120, 132):
    title = str(ndatas[l])
    print(title)
    #alturas:
    print('#####################################')
    print(ndatas[l])
    print('#####################################')
    print(' ')
    print(' ')

    # Variancias
    xvari = variance[l]
    varis = xvari[6:acam]

    # Picos nas variancias
    varipeaks = find_peaks(varis)[0]

    #Altura dos picos em metros
    picos = alti[varipeaks]

    # Criar uma camada entre o pico atual nas condicoes em metros:
    cond = []
    for m in picos:
        if (m > altura-25 and m < altura+15):
            cond.append(m)
    print('Alturas na condicao')
    print(cond)

    # Indices dos níveis com picos atendidos pela condicao:
    idpeaks = []
    for m in range(len(cond)):
        idpeaks.append(np.argwhere(cond[m] == alti)[0][0])
    print('Indices dos picos')
    print(idpeaks)

    # Achando qual é o pico maior entre os níveis

    peaksmax = 0
    for m in idpeaks:
        print('Index peaks:', m)
        peak = varis[m]
        if peak > peaksmax:
            print(peak)
            print(peak > peaksmax)
            peaksmax = peak
            peaksmaxid = m
            print('Peak Max: ', peaksmax)

    altura = alti[peaksmaxid]

    cflgmean = np.mean(mbeta[l][0:70])
    print('Rain Mask value: ', cflgmean)

    #Arbitrary value. I need to confirm in plot if it's ok

    if cflgmean > 16.2 and cflgmean < 18.9:
        print('%%%%%%%%%%%%%%%%%%%%%%')
        print('RAIN FLAG: ', cflgmean)
        altura = -9999

    pbl.append(altura)
    print('Altura: ', altura)



for l in range(132, 144):
    title = str(ndatas[l])
    print(title)
    #alturas:
    print('#####################################')
    print(ndatas[l])
    print('#####################################')
    print(' ')
    print(' ')

    # Variancias
    xvari = variance[l]
    varis = xvari[6:acam]

    # Picos nas variancias
    varipeaks = find_peaks(varis)[0]

    #Altura dos picos em metros
    picos = alti[varipeaks]

    # Criar uma camada entre o pico atual nas condicoes em metros:
    cond = []
    for m in picos:
        if (m > altura-15 and m < altura+25):
            cond.append(m)
    print('Alturas na condicao')
    print(cond)

    # Indices dos níveis com picos atendidos pela condicao:
    idpeaks = []
    for m in range(len(cond)):
        idpeaks.append(np.argwhere(cond[m] == alti)[0][0])
    print('Indices dos picos')
    print(idpeaks)

    # Achando qual é o pico maior entre os níveis

    peaksmax = 0
    for m in idpeaks:
        print('Index peaks:', m)
        peak = varis[m]
        if peak > peaksmax:
            print(peak)
            print(peak > peaksmax)
            peaksmax = peak
            peaksmaxid = m
            print('Peak Max: ', peaksmax)

    altura = alti[peaksmaxid]

    cflgmean = np.mean(mbeta[l][0:70])
    print('Rain Mask value: ', cflgmean)

    if cflgmean > 16.2 and cflgmean < 18.9:
        print('%%%%%%%%%%%%%%%%%%%%%%')
        print('RAIN FLAG: ', cflgmean)
        altura = -9999

    pbl.append(altura)
    print('Altura: ', altura)


## 12 as 13
for l in range(144, 156):
    title = str(ndatas[l])
    print(title)
    #alturas:
    print('#####################################')
    print(ndatas[l])
    print('#####################################')
    print(' ')
    print(' ')

    # Variancias
    xvari = variance[l]
    varis = xvari[6:acam]

    # Picos nas variancias
    varipeaks = find_peaks(varis)[0]

    #Altura dos picos em metros
    picos = alti[varipeaks]

    # Criar uma camada entre o pico atual nas condicoes em metros:
    cond = []
    for m in picos:
        if (m > altura-15 and m < altura+35):
            cond.append(m)
    print('Alturas na condicao')
    print(cond)

    # Indices dos níveis com picos atendidos pela condicao:
    idpeaks = []
    for m in range(len(cond)):
        idpeaks.append(np.argwhere(cond[m] == alti)[0][0])
    print('Indices dos picos')
    print(idpeaks)

    # Achando qual é o pico maior entre os níveis

    peaksmax = 0
    for m in idpeaks:
        print('Index peaks:', m)
        peak = varis[m]
        if peak > peaksmax:
            print(peak)
            print(peak > peaksmax)
            peaksmax = peak
            peaksmaxid = m
            print('Peak Max: ', peaksmax)

    altura = alti[peaksmaxid]

    cflgmean = np.mean(mbeta[l][0:70])
    print('Rain Mask value: ', cflgmean)

    if cflgmean > 16.2 and cflgmean < 18.9:
        print('%%%%%%%%%%%%%%%%%%%%%%')
        print('RAIN FLAG: ', cflgmean)
        altura = -9999

    pbl.append(altura)
    print('Altura: ', altura)


# 13 e 14 UTC
for l in range(156, 168):
    title = str(ndatas[l])
    print(title)
    #alturas:
    print('#####################################')
    print(ndatas[l])
    print('#####################################')
    print(' ')
    print(' ')

    # Variancias
    xvari = variance[l]
    varis = xvari[6:acam]

    # Picos nas variancias
    varipeaks = find_peaks(varis)[0]

    #Altura dos picos em metros
    picos = alti[varipeaks]

    # Criar uma camada entre o pico atual nas condicoes em metros:
    cond = []
    for m in picos:
        if (m > altura-5 and m < altura+35):
            cond.append(m)
    print('Alturas na condicao')
    print(cond)

    # Indices dos níveis com picos atendidos pela condicao:
    idpeaks = []
    for m in range(len(cond)):
        idpeaks.append(np.argwhere(cond[m] == alti)[0][0])
    print('Indices dos picos')
    print(idpeaks)

    # Achando qual é o pico maior entre os níveis

    peaksmax = 0
    for m in idpeaks:
        print('Index peaks:', m)
        peak = varis[m]
        if peak > peaksmax:
            print(peak)
            print(peak > peaksmax)
            peaksmax = peak
            peaksmaxid = m
            print('Peak Max: ', peaksmax)

    altura = alti[peaksmaxid]

    cflgmean = np.mean(mbeta[l][0:70])
    print('Rain Mask value: ', cflgmean)

    if cflgmean > 16.2 and cflgmean < 18.9:
        print('%%%%%%%%%%%%%%%%%%%%%%')
        print('RAIN FLAG: ', cflgmean)
        altura = -9999

    pbl.append(altura)
    print('Altura: ', altura)

# 14 as 15 UTC
for l in range(168, 180):
    title = str(ndatas[l])
    print(title)
    #alturas:
    print('#####################################')
    print(ndatas[l])
    print('#####################################')
    print(' ')
    print(' ')

    # Variancias
    xvari = variance[l]
    varis = xvari[6:acam]

    # Picos nas variancias
    varipeaks = find_peaks(varis)[0]

    #Altura dos picos em metros
    picos = alti[varipeaks]

    # Criar uma camada entre o pico atual nas condicoes em metros:
    cond = []
    for m in picos:
        if (m > altura-15 and m < altura+65):
            cond.append(m)
    print('Alturas na condicao')
    print(cond)

    # Indices dos níveis com picos atendidos pela condicao:
    idpeaks = []
    for m in range(len(cond)):
        idpeaks.append(np.argwhere(cond[m] == alti)[0][0])
    print('Indices dos picos')
    print(idpeaks)

    # Achando qual é o pico maior entre os níveis

    peaksmax = 0
    for m in idpeaks:
        print('Index peaks:', m)
        peak = varis[m]
        if peak > peaksmax:
            print(peak)
            print(peak > peaksmax)
            peaksmax = peak
            peaksmaxid = m
            print('Peak Max: ', peaksmax)

    altura = alti[peaksmaxid]

    cflgmean = np.mean(mbeta[l][0:70])
    print('Rain Mask value: ', cflgmean)

    if cflgmean > 16.2 and cflgmean < 18.9:
        print('%%%%%%%%%%%%%%%%%%%%%%')
        print('RAIN FLAG: ', cflgmean)
        altura = -9999

    pbl.append(altura)
    print('Altura: ', altura)


#15 as 16 UTC
for l in range(180, 196):
    title = str(ndatas[l])
    print(title)
    #alturas:
    print('#####################################')
    print(ndatas[l])
    print('#####################################')
    print(' ')
    print(' ')

    # Variancias
    xvari = variance[l]
    varis = xvari[6:acam]

    # Picos nas variancias
    varipeaks = find_peaks(varis)[0]

    #Altura dos picos em metros
    picos = alti[varipeaks]

    # Criar uma camada entre o pico atual nas condicoes em metros:
    cond = []
    for m in picos:
        if (m > altura-35 and m < altura+25):
            cond.append(m)
    print('Alturas na condicao')
    print(cond)

    # Indices dos níveis com picos atendidos pela condicao:
    idpeaks = []
    for m in range(len(cond)):
        idpeaks.append(np.argwhere(cond[m] == alti)[0][0])
    print('Indices dos picos')
    print(idpeaks)

    # Achando qual é o pico maior entre os níveis

    peaksmax = 0
    for m in idpeaks:
        print('Index peaks:', m)
        peak = varis[m]
        if peak > peaksmax:
            print(peak)
            print(peak > peaksmax)
            peaksmax = peak
            peaksmaxid = m
            print('Peak Max: ', peaksmax)

    altura = alti[peaksmaxid]

    cflgmean = np.mean(mbeta[l][0:70])
    print('Rain Mask value: ', cflgmean)

    if cflgmean > 16.2 and cflgmean < 18.9:
        print('%%%%%%%%%%%%%%%%%%%%%%')
        print('RAIN FLAG: ', cflgmean)
        altura = -9999

    pbl.append(altura)
    print('Altura: ', altura)


## 16 as 17
altura = alta[26]
peaksmaxid = 26
for l in range(196, 204):
    title = str(ndatas[l])
    print(title)
    #alturas:
    print('#####################################')
    print(ndatas[l])
    print('#####################################')
    print(' ')
    print(' ')

    # Variancias
    xvari = variance[l]
    varis = xvari[6:acam]

    # Picos nas variancias
    varipeaks = find_peaks(varis)[0]

    #Altura dos picos em metros
    picos = alti[varipeaks]

    # Criar uma camada entre o pico atual nas condicoes em metros:
    cond = []
    for m in picos:
        if (m > altura-5 and m < altura+35):
            cond.append(m)
    print('Alturas na condicao')
    print(cond)

    # Indices dos níveis com picos atendidos pela condicao:
    idpeaks = []
    for m in range(len(cond)):
        idpeaks.append(np.argwhere(cond[m] == alti)[0][0])
    print('Indices dos picos')
    print(idpeaks)

    # Achando qual é o pico maior entre os níveis

    peaksmax = 0
    for m in idpeaks:
        print('Index peaks:', m)
        peak = varis[m]
        if peak > peaksmax:
            print(peak)
            print(peak > peaksmax)
            peaksmax = peak
            peaksmaxid = m
            print('Peak Max: ', peaksmax)

    altura = alti[peaksmaxid]

    cflgmean = np.mean(mbeta[l][0:70])
    print('Rain Mask value: ', cflgmean)

    if cflgmean > 14.1 and cflgmean < 16.1:
        print('%%%%%%%%%%%%%%%%%%%%%%')
        print('RAIN FLAG: ', cflgmean)
        altura = -9999

    pbl.append(altura)
    print('Altura: ', altura)

for l in range(204, 216):
    title = str(ndatas[l])
    print(title)
    #alturas:
    print('#####################################')
    print(ndatas[l])
    print('#####################################')
    print(' ')
    print(' ')

    # Variancias
    xvari = variance[l]
    varis = xvari[6:acam]

    # Picos nas variancias
    varipeaks = find_peaks(varis)[0]

    #Altura dos picos em metros
    picos = alti[varipeaks]

    # Criar uma camada entre o pico atual nas condicoes em metros:
    cond = []
    for m in picos:
        if (m > altura-5 and m < altura+35):
            cond.append(m)
    print('Alturas na condicao')
    print(cond)

    # Indices dos níveis com picos atendidos pela condicao:
    idpeaks = []
    for m in range(len(cond)):
        idpeaks.append(np.argwhere(cond[m] == alti)[0][0])
    print('Indices dos picos')
    print(idpeaks)

    # Achando qual é o pico maior entre os níveis

    peaksmax = 0
    for m in idpeaks:
        print('Index peaks:', m)
        peak = varis[m]
        if peak > peaksmax:
            print(peak)
            print(peak > peaksmax)
            peaksmax = peak
            peaksmaxid = m
            print('Peak Max: ', peaksmax)

    altura = alti[peaksmaxid]

    cflgmean = np.mean(mbeta[l][0:70])
    print('Rain Mask value: ', cflgmean)

    if cflgmean > 16.2 and cflgmean < 18.9:
        print('%%%%%%%%%%%%%%%%%%%%%%')
        print('RAIN FLAG: ', cflgmean)
        altura = -9999

    pbl.append(altura)
    print('Altura: ', altura)


for l in range(216, 228):
    title = str(ndatas[l])
    print(title)
    #alturas:
    print('#####################################')
    print(ndatas[l])
    print('#####################################')
    print(' ')
    print(' ')

    # Variancias
    xvari = variance[l]
    varis = xvari[6:acam]

    # Picos nas variancias
    varipeaks = find_peaks(varis)[0]

    #Altura dos picos em metros
    picos = alti[varipeaks]

    # Criar uma camada entre o pico atual nas condicoes em metros:
    cond = []
    for m in picos:
        if (m > altura-5 and m < altura+35):
            cond.append(m)
    print('Alturas na condicao')
    print(cond)

    # Indices dos níveis com picos atendidos pela condicao:
    idpeaks = []
    for m in range(len(cond)):
        idpeaks.append(np.argwhere(cond[m] == alti)[0][0])
    print('Indices dos picos')
    print(idpeaks)

    # Achando qual é o pico maior entre os níveis

    peaksmax = 0
    for m in idpeaks:
        print('Index peaks:', m)
        peak = varis[m]
        if peak > peaksmax:
            print(peak)
            print(peak > peaksmax)
            peaksmax = peak
            peaksmaxid = m
            print('Peak Max: ', peaksmax)

    altura = alti[peaksmaxid]

    cflgmean = np.mean(mbeta[l][0:70])
    print('Rain Mask value: ', cflgmean)

    if cflgmean > 28.2 and cflgmean < 28.9:
        print('%%%%%%%%%%%%%%%%%%%%%%')
        print('RAIN FLAG: ', cflgmean)
        altura = -9999

    pbl.append(altura)
    #pbl.append(-9999)
    print('Altura: ', altura)

######################################################################
######################################################################
### END OF THE DAY
### VARIANCE
######################################################################
######################################################################


for l in range(228, 240):
    title = str(ndatas[l])
    
    #alturas:
    print(' ')
    print('Loop: ', l)
    print('#####################################')
    print(ndatas[l])
    print('#####################################')
    print(' ')
    
    # Variancias
    xvari = variance[l]
    varis = xvari[6:acam]

    # Picos nas variancias
    varipeaks = find_peaks(varis)[0]

    #Altura dos picos em metros
    picos = alti[varipeaks]

    # Criar uma camada entre o pico atual nas condicoes em metros:
    cond = []
    for m in picos:
        if (m > altura-35 and m < altura+5):
            cond.append(m)
    print('Alturas na condicao')
    print(cond)

    # Indices dos níveis com picos atendidos pela condicao:
    idpeaks = []
    for m in range(len(cond)):
        idpeaks.append(np.argwhere(cond[m] == alti)[0][0])
    print('Indices dos picos')
    print(idpeaks)

    # Achando qual é o pico maior entre os níveis

    peaksmax = 0
    for m in idpeaks:
        print('Index peaks:', m)
        peak = varis[m]
        if peak > peaksmax:
            print(peak)
            print(peak > peaksmax)
            peaksmax = peak
            peaksmaxid = m
            print('Peak Max: ', peaksmax)

    altura = alti[peaksmaxid]

    cflgmean = np.mean(mbeta[l][0:70])
    print('Rain Mask value: ', cflgmean)

    if cflgmean > 16.2 and cflgmean < 18.9:
        print('%%%%%%%%%%%%%%%%%%%%%%')
        print('RAIN FLAG: ', cflgmean)
        altura = -9999

    pbl.append(altura)
    #pbl.append(-9999)
    print('Altura: ', altura)


# 20 as 21 UTC
for l in range(240, 252):
    title = str(ndatas[l])
    
    #alturas:
    print(' ')
    print('Loop: ', l)
    print('#####################################')
    print(ndatas[l])
    print('#####################################')
    print(' ')
    
    # Variancias
    xvari = variance[l]
    varis = xvari[6:acam]

    # Picos nas variancias
    varipeaks = find_peaks(varis)[0]

    #Altura dos picos em metros
    picos = alti[varipeaks]

    # Criar uma camada entre o pico atual nas condicoes em metros:
    cond = []
    for m in picos:
        if (m > altura-35 and m < altura+5):
            cond.append(m)
    print('Alturas na condicao')
    print(cond)

    # Indices dos níveis com picos atendidos pela condicao:
    idpeaks = []
    for m in range(len(cond)):
        idpeaks.append(np.argwhere(cond[m] == alti)[0][0])
    print('Indices dos picos')
    print(idpeaks)

    # Achando qual é o pico maior entre os níveis

    peaksmax = 0
    for m in idpeaks:
        print('Index peaks:', m)
        peak = varis[m]
        if peak > peaksmax:
            print(peak)
            print(peak > peaksmax)
            peaksmax = peak
            peaksmaxid = m
            print('Peak Max: ', peaksmax)

    altura = alti[peaksmaxid]

    cflgmean = np.mean(mbeta[l][0:70])
    print('Rain Mask value: ', cflgmean)

    if cflgmean > 13.2 and cflgmean < 15.9:
        print('%%%%%%%%%%%%%%%%%%%%%%')
        print('RAIN FLAG: ', cflgmean)
        altura = -9999

    pbl.append(altura)
    #pbl.append(-9999)
    print('Altura: ', altura)

#altura = alta[40]
#peaksmaxid = 40

for l in range(252, 264):
    title = str(ndatas[l])
    
    #alturas:
    print(' ')
    print('Loop: ', l)
    print('#####################################')
    print(ndatas[l])
    print('#####################################')
    print(' ')
    
    # Variancias
    xvari = variance[l]
    varis = xvari[6:acam]

    # Picos nas variancias
    varipeaks = find_peaks(varis)[0]

    #Altura dos picos em metros
    picos = alti[varipeaks]

    # Criar uma camada entre o pico atual nas condicoes em metros:
    cond = []
    for m in picos:
        if (m > altura-45 and m < altura+5):
            cond.append(m)
    print('Alturas na condicao')
    print(cond)

    # Indices dos níveis com picos atendidos pela condicao:
    idpeaks = []
    for m in range(len(cond)):
        idpeaks.append(np.argwhere(cond[m] == alti)[0][0])
    print('Indices dos picos')
    print(idpeaks)

    # Achando qual é o pico maior entre os níveis

    peaksmax = 0
    for m in idpeaks:
        print('Index peaks:', m)
        peak = varis[m]
        if peak > peaksmax:
            print(peak)
            print(peak > peaksmax)
            peaksmax = peak
            peaksmaxid = m
            print('Peak Max: ', peaksmax)

    altura = alti[peaksmaxid]

    cflgmean = np.mean(mbeta[l][0:70])
    print('Rain Mask value: ', cflgmean)

    if cflgmean > 16.2 and cflgmean < 18.9:
        print('%%%%%%%%%%%%%%%%%%%%%%')
        print('RAIN FLAG: ', cflgmean)
        altura = -9999

    pbl.append(altura)
    print('Altura: ', altura)


for l in range(264, 288):
    title = str(ndatas[l])
    
    #alturas:
    print(' ')
    print('Loop: ', l)
    print('#####################################')
    print(ndatas[l])
    print('#####################################')
    print(' ')
    # NIGHT - not realiable

    pbl.append(-9999)
    print('Altura: ', altura)


# Saving the PBL values in text file
blhvar = pd.DataFrame(pbl) 
blhvar = round(blhvar, 2) 
blhvar.index = pd.to_datetime(ndatas)

blhvar.to_csv('/home/flavio/data/atto/ceilometer_camp/blh/'+title[0:10]+'_BLH.csv', header=False)

#PLOT FIGURE
print(' ')
print('--------------------------------------')
print('Plotting figures')
print('--------------------------------------')
print(' ')

#########COLOR
blues = cm.get_cmap('jet', 50)
#blues = blues.reversed()
greens = cm.get_cmap('RdYlGn', 50)
greens = greens.reversed()
greensred = cm.get_cmap('hsv', 100)
greensred = greensred.reversed()
yelredbck = cm.get_cmap('hot', 100)
yelredbck = yelredbck.reversed()

newcolors = np.vstack((blues(np.linspace(0.15, 0.22, 3)),
                       greens(np.linspace(0.05, 0.3, 5)),
                       greensred(np.linspace(0.677, 0.8, 5)),
                       yelredbck(np.linspace(0.16, 0.95, 15))))


newcmap = ListedColormap(newcolors)

cmap = mpl.cm.jet(np.linspace(0.65, 1, 29))
#ccmap = np.vstack((blues(np.linspace(0.15, 0.25, 3)),
#                   cmap))
ccmap = np.vstack((mpl.cm.terrain(np.linspace(0, 0.48, 16)),
                    cmap))
jetcmap = ListedColormap(ccmap)
print(cfiles)

datas = []

for f in range(len(cfiles)):
    datas = []
    print(f)
    cfile = cfiles[f]
    print(cfile)
    file = Dataset(cfile)

    times = file.variables['time']
    vtimes = num2date(times[:], times.units)

    timestr = []
    for x in range(len(vtimes)):
        timestr.append(str(vtimes[x]))


    for i in range(len(vtimes)):
        datas.append(pd.to_datetime(timestr[i]))

    datestring = str(vtimes[0])
    dia = datestring[0:10]
    print('Data: ', datestring[0:10])
    #print('Hora: ', datestring[10:20])

    range_gate = file.variables['range_gate'][:]
    z = file.variables['range'][:]

    if z[9] > 17000:
        print('Found if')
        z = np.linspace(15, 15360, 15, endpoint=True)

    height = z[0:207]*0.9659

    tilt = 0.96592582628
    print('Tilt: ', tilt)

    bscats = []
    gradient = []
    grad = []
    varia = []
    vsst = []
    global_ws = []
    periods = []

    for x in range(len(vtimes)):
        print(vtimes[x])
        bscat = file.variables['beta_raw'][x,0:207]
        bscats.append(np.log(bscat))

    backs = np.concatenate((bscats))
    xx = len(datas)
    yy = len(height)

    backs = backs.reshape((xx, yy))
    
    df = pd.DataFrame(backs)
    df.index = datas
    df = df.resample('5Min').mean()
    datass = df.index

    
    #xx1 = df[0:156].index
    xx1 = df[0:288].index
    xy1 = height

    x2, y2 = np.meshgrid(xx1, xy1)
    scatter = df[0:288].values
    scatter2 = np.transpose(scatter)

    y3 = dft.values

    blhvari = np.loadtxt('/home/flavio/data/atto/ceilometer_camp/blh/'+dia+'_BLH.csv', dtype='str,float', delimiter=',', usecols=(0, 1), unpack=True)
    
    print('Shape x2: ', x2.shape)

    print('Max Scatter: ', scatter2.max())
    print('Min Scatter: ', scatter2.min())

    #clevs = np.linspace(8, 17, 90, endpoint=True)
    #clevs = np.linspace(11.8, 14.1, 90, endpoint=True)
    clevs = np.linspace(8, 14, 60, endpoint=True)

    print('Plotting...')
    fig, ax = plt.subplots(figsize=(21,7))
    print('Fig created')
    #cs = ax.contourf(x2, y2, scatter2, clevs, cmap=jetcmap, extend='both')
    cs = ax.contourf(x2, y2, scatter2, clevs, cmap=cmaps.WhBlGrYeRe, extend='both')
    #cs = ax.contourf(x2, y2, scatter2, clevs, cmap=cmaps.MPL_gist_rainbow_r, extend='both')
    ax.grid()
    cb1 = ax.plot(xx1, blhvari[1], ".k", markersize=12, label='BLH')
    #cb2 = ax.plot(xx1, blhsond[1], "^r", markersize=14, label='Sounding')

    #ax1 = ax.twinx()
    #ax1.plot(xx1,y3, '--k', linewidth=4, label='Temperature')
    #ax1.plot(xx1,y3, '--k', markersize=12)

    from matplotlib.lines import Line2D

    legend_elements = [Line2D([0], [0], marker='o', color='w', label='Scatter',
                                markerfacecolor='k', markersize=12),
                       Line2D([0], [0], marker='^', color='w', label='Scatter',
                                markerfacecolor='r', markersize=13)]

    ax.legend(legend_elements, ["BLH", "Sounding"], bbox_to_anchor=(1.15, 1),
                         loc='upper left', borderaxespad=0., prop={'size': 12})

    #ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
    locator = mdates.HourLocator(interval=1)
    #locator = mdates.MinuteLocator(interval=30)
    #locator.MAXTICKS = 8
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    fig.autofmt_xdate()
    #ax.set_ylim(0, 3000)
    ax.set_ylim(0, 2000)
    ax.set_yticks([100, 150, 200, 250, 300, 400, 500, 600, 700, 900, 1000, 1100, 1200, 1300, 1400, 1500, 
                    1600, 1700, 1800, 1900, 2000])
    #ax1.set_ylim(29, 34)
    # ax.set_yticks([100, 150, 200, 250, 300, 400, 500, 600, 700, 900, 1000, 1100, 1200, 1300, 1400, 1500, 
    #                 1600, 1700, 1800, 1900, 2000, 2500, 3000])
    cbar = plt.colorbar(cs)
    cbar.set_label('Range-corrected \u03B2 [arb.units]', rotation=90)
    plt.title('CHM15k - ATTO - '+dia)
    plt.xlabel('Time (UTC)')
    #plt.ylabel('Height (m)')
    ax.set_ylabel('Height (m)')
    #ax1.set_ylabel('Temperature (°C)')
    plt.tight_layout()

    fig.savefig('/home/flavio/data/atto/ceilometer_camp/py/figs/'+dia+'ceilometer_contourf.png', format='png', dpi=200)

    
    #plt.show()
    plt.close()
   
