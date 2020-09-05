import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import InterpolatedUnivariateSpline
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

colors = {'wb97xd': 'g',
          'lc-blyp':'b',
          'lc-wpbe':'r'}

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
        keywords = ['Counterpoise:', 'corrected', 'energy']
        if linha[:3] == keywords:
            # print(linha)
            Einf_1 = float(linha[4])/219474.6305
    #print(Einf_1)

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
        # print(scf)

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
    #print(E2_grid)

Teta = np.arange(0,360,10)
r,teta = np.meshgrid(R,Teta)

#Plot 2D

#fig, [graf1, graf2] = plt.subplots(1,2)
# graf3 = graf1.twinx()
# graf4 = graf2.twinx()

#plt.subplot(121)

fig = plt.figure(figsize = (12, 8), dpi = 100)

CEP_R0 = InterpolatedUnivariateSpline(R, E0_grid[0,:])
CEP_R1 = InterpolatedUnivariateSpline(R, E1_grid[0,:])
if default: CEP_R2 = InterpolatedUnivariateSpline(R, E2_grid[0,:])

R_plot = np.arange(3,5.1,0.001)

E0 = CEP_R0(R_plot)
E1 = CEP_R1(R_plot)
if default: E2 = CEP_R2(R_plot)

plt.suptitle("Curvas de Energia Potencial", fontsize = '22')
plt.title("Ângulo diédrico: $ \\theta = 0 ^o$", fontsize = '20')
plt.grid()
plt.xlabel('$R (\\mathring{A})$', fontsize = '18')
plt.ylabel('Energia $(cm^{-1})$', fontsize = '18')
plt.plot(R, E0_grid[0,:], 'kv', label = 'MP4')
plt.plot(R_plot, E0, 'k')
plt.plot(R, E1_grid[0,:], colors[funct]+'o', label = funct)
plt.plot(R_plot, E1, colors[funct])
if default: 
    plt.plot(R, E2_grid[0,:], colors[funct]+'s', label = funct+' (Padrão)')
    plt.plot(R_plot, E2, colors[funct]+'--')
plt.legend(fontsize = '18')
plt.show()

fig = plt.figure(figsize = (12, 8), dpi = 100)

CEP_T0 = InterpolatedUnivariateSpline(Teta, E0_grid[:,5])
CEP_T1 = InterpolatedUnivariateSpline(Teta, E1_grid[:,5])
if default: CEP_T2 = InterpolatedUnivariateSpline(Teta, E2_grid[:,5])

Teta_plot = np.arange(0,360,0.001)

E0 = CEP_T0(Teta_plot)
E1 = CEP_T1(Teta_plot)
if default: E2 = CEP_T2(Teta_plot)

#plt.subplot(122)
plt.title("Distância $\\mathrm{H_2O_2 - Kr}: R  = 3,5\\, \\mathring{A}$", fontsize = '20')
plt.grid()
plt.legend(fontsize = '18')
plt.xlabel('$\\theta (^o)$', fontsize = '18')
plt.ylabel('Energia $(cm^{-1})$', fontsize = '18')
plt.plot(Teta, E0_grid[:,5], 'kv', label = 'MP4')
plt.plot(Teta_plot, E0, 'k')
plt.plot(Teta, E1_grid[:,5], colors[funct]+'o', label = funct)
plt.plot(Teta_plot, E1, colors[funct])
if default: 
    plt.plot(Teta, E2_grid[:,5], colors[funct]+'s', label = funct+' (Padrão)')
    plt.plot(Teta_plot, E2, colors[funct]+'--')
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


