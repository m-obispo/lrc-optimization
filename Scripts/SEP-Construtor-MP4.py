import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

dashes = ['----', '---------', '-----------', '-----------',\
          '-----------', '-----------', '-----------', '-----------']

SCF = np.zeros(21)
MP4 = np.zeros(21)

#MP4 - Referência

for k in range(36):
    R = np.arange(3,5.1,0.1)
    mp4 = []

    keywords = ['Counterpoise', 'corrected', 'energy']
    with open('../Calc-maq-Arthur/Logs/H2O2-Kr_'+str(k)+'.log','r') as g:
        for line in g:
            linha = line.split()
            if linha[:3] == keywords:
                #print(linha, linha[4])
                mp4.append(float(linha[4])/219474.6305)
                #print('Energia '+str(k)+':',float(linha[4]))
    with open('../Calc-maq-Arthur/Logs/H2O2-Kr_'+str(k)+'.log','r') as g:
        for line in g:
            linha = line.split()
            if linha[:3] == keywords:
                #print(linha, linha[4])
                mp4.append(float(linha[4])/219474.6305)
                #print('Energia '+str(k)+':',float(linha[4]))

    MP4 = np.vstack((MP4,np.array(mp4)))


with open('../Logs-MP4/H2O2-Kr_inf.log','r') as g:
    for line in g:
        linha = line.split()
        #print(linha)
        if len(linha) == 4 and linha[2] == 'UMP4(SDTQ)=':
            print(linha[3][:14])
            Einf = float(linha[3][:14])*10**(float(linha[3][-3:]))/219474.6305

    print(Einf)

    # plt.suptitle("Curvas de Energia Potencial")
    # plt.title("Ângulo diédrico: $ \\theta $ = "+str(k)+"0.0")
    # plt.ylim()
    # plt.plot(R, mp2, 'r', label = 'MP2, $\\alpha = %0.0f$'%(10*k))
    # plt.plot(R, mp3, 'g', label = 'MP3, $\\alpha = %0.0f$'%(10*k))
    # plt.plot(R, mp4SDQ, '-', label = 'MP4, $\\alpha = %0.0f$'%(10*k))
    # plt.legend(loc = '2')

# plt.show()

# Plot 3D
Teta = np.arange(0,360,10)
r,teta = np.meshgrid(R,Teta)

E_grid = MP4[1:,:] - Einf

ax1 = plt.subplot(111, projection='3d')
ax1.set_title('Superfície de Energia Potencial (MP4)')
ax1.plot_surface(r,teta,E_grid,cmap='twilight',rcount = 100,ccount=100)
ax1.set_xlabel('R $(\\mathring{A})$')
ax1.set_ylabel('$\\theta$ $(^o)$')
ax1.set_zlabel('Energia $(cm^{-1})$')
plt.show()

# Plot 2D

plt.subplot(121)
plt.suptitle("Curvas de Energia Potencial (MP4)", fontsize = '22')
plt.title("Ângulo diédrico: $ \\theta = 0 ^o$", fontsize = '20')
plt.xlabel('$R (\\mathring{A})$', fontsize = '18')
plt.ylabel('Energia $(cm^{-1})$', fontsize = '18')
plt.ylim()
plt.yticks(fontsize = '14')
plt.xticks(fontsize = '14')
plt.plot(R, E_grid[0,:], 'g', label = 'MP4')
plt.grid()
plt.legend(fontsize = '18')

plt.subplot(122)
plt.suptitle("Curvas de Energia Potencial (MP4)", fontsize = '22')
plt.title("Distância $\\mathrm{H_2O_2 - Kr}: R  = 3,5\\, \\mathring{A}$", fontsize = '20')
plt.xlabel('$\\theta (^o)$', fontsize = '18')
plt.ylabel('Energia $(cm^{-1})$', fontsize = '18')
plt.ylim()
plt.yticks(fontsize = '14')
plt.xticks(fontsize = '14')
plt.plot(Teta, E_grid[:,5], 'r', label = 'MP4')
plt.grid()
plt.legend(fontsize = '18')

plt.show()
