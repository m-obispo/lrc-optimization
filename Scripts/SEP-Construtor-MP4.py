import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

dashes = ['----', '---------', '-----------', '-----------',\
          '-----------', '-----------', '-----------', '-----------']

MP4 = np.zeros(21)

#MP4 - Referência

# R = np.hstack((np.arange(3,5.1,0.1),np.arange(3.25,4.35,0.1)))
R = np.arange(3,5.1,0.1)
R_order = R.argsort()

#Teta = np.hstack((np.arange(0,360,10),np.arange(85,285,10)))
Teta = np.arange(0,360,10)
Teta_order = Teta.argsort()

for k in range(36):
    mp4 = []
    mp4_1 = []

    keywords = ['Counterpoise', 'corrected', 'energy']
    with open('../Logs/Logs/H2O2-Kr_'+str(k)+'.log','r') as g:
        for line in g:
            linha = line.split()
            if linha[:3] == keywords:
                #print(linha, linha[4])
                mp4.append(float(linha[4])/219474.6305)
                #print('Energia '+str(k)+':',float(linha[4]))

    # with open('../Logs/Logs-mp4/H2O2-Kr_'+str(k)+'-1.log','r') as g:
    #     for line in g:
    #         linha = line.split()
    #         if linha[:3] == keywords:
    #             #print(linha, linha[4])
    #             mp4_1.append(float(linha[4])/219474.6305)
    #             #print('Energia '+str(k)+':',float(linha[4]))

    # mp4 = np.hstack((np.array(mp4),np.array(mp4_1)))

    MP4 = np.vstack((MP4,np.array(mp4)))

# for k in range(85,285,10):
#     mp4 = []
#     mp4_1 = []

#     keywords = ['Counterpoise', 'corrected', 'energy']
#     with open('../Logs/Logs-mp4/H2O2-Kr_'+str(k)+'.log','r') as g:
#         for line in g:
#             linha = line.split()
#             if linha[:3] == keywords:
#                 #print(linha, linha[4])
#                 mp4.append(float(linha[4])/219474.6305)
#                 #print('Energia '+str(k)+':',float(linha[4]))

#     with open('../Logs/Logs-mp4/H2O2-Kr_'+str(k)+'-1.log','r') as g:
#         for line in g:
#             linha = line.split()
#             if linha[:3] == keywords:
#                 #print(linha, linha[4])
#                 mp4_1.append(float(linha[4])/219474.6305)
#                 #print('Energia '+str(k)+':',float(linha[4]))

#     mp4 = np.hstack((np.array(mp4),np.array(mp4_1)))

#     MP4 = np.vstack((MP4,np.array(mp4)))


with open('../Logs/Logs/H2O2-Kr_inf.log','r') as g:
    for line in g:
        linha = line.split()
        keywords = ['Counterpoise', 'corrected', 'energy']
        #print(linha)
        if linha[:3] == ['Counterpoise', 'corrected', 'energy']:
            #print(linha[4])
            Einf = float(linha[4])/219474.6305

    print(Einf)

    # plt.suptitle("Curvas de Energia Potencial")
    # plt.title("Ângulo diédrico: $ \\theta $ = "+str(k)+"0.0")
    # plt.ylim()
    # plt.plot(R, mp2, 'r', label = 'MP2, $\\alpha = %0.0f$'%(10*k))
    # plt.plot(R, mp3, 'g', label = 'MP3, $\\alpha = %0.0f$'%(10*k))
    # plt.plot(R, mp4SDQ, '-', label = 'MP4, $\\alpha = %0.0f$'%(10*k))
    # plt.legend(loc = '2')


# MP4 = MP4[:,R_order] 
# R = R[R_order]

# MP4 = MP4[Teta_order,:]
# Teta = Teta[Teta_order]

# Plot 3D

# r,teta = np.meshgrid(R,Teta)
E_grid = MP4[1:,:] - Einf

# fig = plt.figure(figsize = (12, 10), dpi = 100)
# ax1 = fig.add_subplot(projection = '3d')
# ax1.set_title('Superfície de Energia Potencial (MP4)', fontsize = 18)
# ax1.plot_surface(r,teta,E_grid,cmap='twilight',rcount = 100,ccount = 100)
# ax1.set_xlabel('R $(\\mathring{A})$', fontsize = 18)
# ax1.set_ylabel('$\\theta$ $(^o)$', fontsize = 18)
# ax1.set_zlabel('Energia $(cm^{-1})$', fontsize = 18)
# plt.show()

# Plot 2D

R_plot = np.arange(3,5.1,0.001)
CEP_R = InterpolatedUnivariateSpline(R, E_grid[0,:])
V_r = CEP_R(R_plot)

Teta_plot = np.arange(0,360,0.001)
CEP_Teta = InterpolatedUnivariateSpline(Teta, E_grid[:,5])
V_teta = CEP_Teta(Teta_plot)

# plt.subplot(121)
plt.suptitle("Curvas de Energia Potencial (MP4)", fontsize = '22')
plt.title("Ângulo diédrico: $ \\theta = 0 ^o$", fontsize = '20')
plt.xlabel('$R (\\mathring{A})$', fontsize = '18')
plt.ylabel('Energia $(cm^{-1})$', fontsize = '18')
plt.ylim()
plt.yticks(fontsize = '14')
plt.xticks(fontsize = '14')
plt.plot(R, E_grid[0,:], 'ko', label = 'MP4')
plt.plot(R_plot, V_r, 'k-')
plt.grid()
plt.legend(fontsize = '18')

plt.show()

# plt.subplot(122)
plt.title("Distância $\\mathrm{H_2O_2 - Kr}: R  = 3,5\\, \\mathring{A}$", fontsize = '20')
plt.xlabel('$\\theta (^o)$', fontsize = '18')
plt.ylabel('Energia $(cm^{-1})$', fontsize = '18')
plt.ylim()
plt.yticks(fontsize = '14')
plt.xticks(fontsize = '14')
plt.plot(Teta, E_grid[:,5], 'ko', label = 'MP4')
plt.plot(Teta_plot, V_teta, 'k-')
plt.grid()
plt.legend(fontsize = '18')

plt.show()
