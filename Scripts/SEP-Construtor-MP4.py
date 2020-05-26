import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

dashes = ['----', '---------', '-----------', '-----------',\
          '-----------', '-----------', '-----------', '-----------']

SCF = np.zeros(21)
MP2 = np.zeros(21)
MP3 = np.zeros(21)
MP4DQ = np.zeros(21)
MP4SDQ = np.zeros(21)
MP4SDTQ = np.zeros(21)

for k in range(36):
    N = []
    R = []
    scf = []
    mp2 = []
    mp3 = []
    mp4DQ = []
    mp4SDQ = []
    mp4SDTQ = []
    #print(k)
    with open('../Logs-MP4/H2O2-Kr_'+str(k)+'.log','r') as g:
        c = 0
        for line in g:
            linha = line.split()
            if c == 3 and linha != dashes:
                # print(linha)
                N.append(float(linha[0]))
                R.append(float(linha[1]))
                # scf.append(float(linha[2]))
                # mp2.append(float(linha[3]))
                # mp3.append(float(linha[4]))
                # mp4DQ.append(float(linha[5]))
                # mp4SDQ.append(float(linha[6]))
                mp4SDTQ.append(float(linha[7])/219474.6305)
            if linha == ['Summary', 'of', 'the', 'potential', 'surface', 'scan:'] \
            or linha == ['N', 'R1', 'SCF', 'MP2', 'MP3', 'MP4DQ', 'MP4SDQ', 'MP4SDTQ'] \
            or linha == dashes:
                c += 1

    N = np.array(N)
    R = np.array(R)
    # SCF = np.vstack((SCF,np.array(scf)))
    # MP2 = np.vstack((MP2,np.array(mp2)))
    # MP3 = np.vstack((MP3,np.array(mp3)))
    # MP4DQ = np.vstack((MP4DQ,np.array(mp4DQ)))
    # MP4SDQ = np.vstack((MP4SDQ,np.array(mp4SDQ)))
    MP4SDTQ = np.vstack((MP4SDTQ,np.array(mp4SDTQ)))

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

E_grid = MP4SDTQ[1:,:] - Einf

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
