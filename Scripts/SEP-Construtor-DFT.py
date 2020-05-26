import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

dashes = ['----', '---------', '-----------']

SCF = np.zeros(21)

funct = 'wb97xd'

for k in range(36):
    N = []
    R = []
    scf = []

    print(k)
    dashes1 = ['----', '---------', '-----------']
    with open('../Logs-'+funct+'/H2O2-Kr_'+str(k)+'.log','r') as g:
        c = 0
        for line in g:
            linha = line.split()
            if c == 3 and linha != dashes1:
                print(linha)
                N.append(float(linha[0]))
                R.append(float(linha[1]))
                scf.append(float(linha[2]))#/219474.6305)
                    #print(scf)
            if linha == ['Summary', 'of', 'the', 'potential', 'surface', 'scan:'] \
            or linha == ['N', 'R1', 'SCF'] or linha == dashes1:
                c += 1

    print(scf)
    N = np.array(N)
    R = np.array(R)
    SCF = np.vstack((SCF,np.array(scf)))


with open('../Logs-'+funct+'/H2O2-Kr_inf.log','r') as g:
    for line in g:
        linha = line.split()
        # print(linha)
        if len(linha) == 9 and linha[:2] == ['SCF', 'Done:']:
            # print(linha)
            Einf = float(linha[4])

    print(Einf)


#Plot 3D
Teta = np.arange(0,360,10)
r,teta = np.meshgrid(R,Teta)

E_grid = SCF[1:,:] - Einf

print(E_grid)

ax1 = plt.subplot(111, projection='3d')
ax1.set_title('Superfície de Energia Potencial - '+funct)
ax1.plot_surface(r,teta,E_grid,cmap='twilight',rcount = 100,ccount=100)
ax1.set_xlabel('R $(\\mathring{A})$')
ax1.set_ylabel('$\\theta$ $(^o)$')
ax1.set_zlabel('Energia')
plt.show()

#Plot 2D

plt.subplot(121)
plt.suptitle("Curvas de Energia Potencial - "+funct, fontsize = '22')
plt.title("Ângulo diédrico: $ \\theta = 0 ^o$", fontsize = '20')
plt.xlabel('$R (\\mathring{A})$', fontsize = '18')
plt.ylabel('Energia', fontsize = '18')
plt.ylim()
plt.yticks(fontsize = '14')
plt.xticks(fontsize = '14')
plt.plot(R, E_grid[0,:], 'g', label = funct)
plt.grid()
plt.legend(fontsize = '18')

plt.subplot(122)
plt.suptitle("Curvas de Energia Potencial - "+funct, fontsize = '22')
plt.title("Distância $\\mathrm{H_2O_2 - Kr}: R  = 3,5\\, \\mathring{A}$", fontsize = '20')
plt.xlabel('$\\theta (^o)$', fontsize = '18')
plt.ylabel('Energia', fontsize = '18')
plt.ylim()
plt.yticks(fontsize = '14')
plt.xticks(fontsize = '14')
plt.plot(Teta, E_grid[:,5], 'r', label = funct)
plt.grid()
plt.legend(fontsize = '18')

plt.show()
