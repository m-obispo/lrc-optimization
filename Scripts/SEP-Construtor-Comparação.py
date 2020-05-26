import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys

# MP2 = np.zeros(21)
# MP3 = np.zeros(21)
# MP4DQ = np.zeros(21)
# MP4SDQ = np.zeros(21)
MP4 = np.zeros(21)
SCF = np.zeros(21)
SCF2 = np.zeros(21)

funct = sys.argv[1]
default = True

def minimo(arr):
    return (np.amin(arr), np.where(arr == np.amin(arr)))

#MP4 - Referência

for k in range(36):
    N = np.arange(21)
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

    MP4 = np.vstack((MP4,np.array(mp4)))


with open('../Calc-maq-Arthur/Logs/H2O2-Kr_inf.log','r') as g:
    for line in g:
        linha = line.split()
        #print(linha)
        if linha[:3] == keywords:
            Einf_0 = float(linha[4])/219474.6305
    print(Einf_0)

E0_grid = MP4[1:,:] - Einf_0

#DFT - Otimizada

for k in range(36):
    N = np.arange(21)
    R = np.arange(3,5.1,0.1)
    scf = []
    keywords = ['Counterpoise:', 'corrected', 'energy']
    with open('../Logs/Logs-'+funct+'/H2O2-Kr_'+str(k)+'.log','r') as g:
        for line in g:
            linha = line.split()
            if linha[:3] == keywords:
           	    scf.append(float(linha[4])/219474.6305)
                #print(float(linha[4])/219474.6305)
    
    SCF = np.vstack((SCF,np.array(scf)))
    #print(SCF)

with open('../Logs/Logs-'+funct+'/H2O2-Kr_inf.log','r') as g:
    for line in g:
        linha = line.split()
        # print(linha)
        if linha[:3] == keywords:
            # print(linha)
            Einf_1 = float(linha[4])/219474.6305
    print(Einf_1)

E1_grid = SCF[1:,:] - Einf_1

#DFT - Padrão

if default:
    for k in range(36):
        N = np.arange(21)
        R = np.arange(3,5.1,0.1)
        scf = []
        keywords = ['Counterpoise:', 'corrected', 'energy']
        with open('../Logs/Logs-'+funct+'-default/H2O2-Kr_'+str(k)+'.log','r') as g:
            for line in g:
                linha = line.split()
                if linha[:3] == keywords:
               	    scf.append(float(linha[4])/219474.6305)
                    #print(float(linha[4])/219474.6305)
        print(scf)

        SCF2 = np.vstack((SCF2,np.array(scf)))
        #print(SCF)

    with open('../Logs/Logs-'+funct+'-default/H2O2-Kr_inf.log','r') as g:
        for line in g:
            linha = line.split()
            # print(linha)
            if linha[:3] == keywords:
                # print(linha)
                Einf_2 = float(linha[4])/219474.6305
        print(Einf_2)
    E2_grid = SCF2[1:,:] - Einf_2

Teta = np.arange(0,360,10)
r,teta = np.meshgrid(R,Teta)

print(E2_grid)

#Plot 2D

#fig, [graf1, graf2] = plt.subplots(1,2)
# graf3 = graf1.twinx()
# graf4 = graf2.twinx()

#plt.subplot(121)
plt.suptitle("Curvas de Energia Potencial", fontsize = '22')
plt.title("Ângulo diédrico: $ \\theta = 0 ^o$", fontsize = '20')
plt.grid()
plt.xlabel('$R (\\mathring{A})$', fontsize = '18')
plt.ylabel('Energia $(cm^{-1})$', fontsize = '18')
plt.plot(R, E0_grid[0,:], 'k', label = 'MP4')
plt.plot(R, E1_grid[0,:], 'r', label = funct)
if default: 
    plt.plot(R, E2_grid[0,:], 'r--', label = funct+' (Padrão)')
plt.legend(fontsize = '18')
plt.show()

#plt.subplot(122)
plt.title("Distância $\\mathrm{H_2O_2 - Kr}: R  = 3,5\\, \\mathring{A}$", fontsize = '20')
plt.grid()
plt.legend(fontsize = '18')
plt.xlabel('$\\theta (^o)$', fontsize = '18')
plt.ylabel('Energia $(cm^{-1})$', fontsize = '18')
plt.plot(Teta, E0_grid[:,5], 'k', label = 'MP4')
plt.plot(Teta, E1_grid[:,5], 'r', label = funct)
if default: 
    plt.plot(Teta, E2_grid[:,5], 'r--', label = funct+' (Padrão)')
plt.legend(fontsize = '18')
plt.show()

dE = MP4[1:,:] - SCF[1:,:]

print(dE.max())

#Plot 3D

# ax1 = plt.subplot(111, projection='3d')
# ax1.set_title('Superfície de Energia Potencial (Comparativo)')
# ax1.plot_surface(r,teta,dE,cmap='twilight_r',rcount = 100,ccount=100, label = 'Diferença')
# ax1.set_xlabel('R $(\\mathring{A})$')
# ax1.set_ylabel('$\\theta$ $(^o)$')
# ax1.set_zlabel('Energia $(cm^{-1})$')
# plt.show()


