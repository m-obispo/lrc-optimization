import numpy as np
from scipy.optimize import minimize
import os
import sys
import time
#Bibliotecas gráficas
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

#Abre o arquivo .log do programa de otimização
log = open('../Optimizer-log.txt','w')

gauss_version = 'g09'
TCC_dir = '/home/matheus/.tcc'

# gauss_version = 'g16' 
# TCC_dir = '/home/matheus/TCC'

funct = sys.argv[1]
base = 'aug-cc-PVTz'

log.write("\nFuncional: "+funct+
        "\nBase: "+base)

def minimo(arr):
    '''Retorna o valor mínimo de um array e sua posição'''
    return (np.amin(arr), np.where(arr == np.amin(arr)))

def cabecalho(r, np, fu, b, omega=0.0):
    '''
    Imprime o cabeçalho de uma entrada do Gaussian.
    ----------------------------------------------------- 
    Params:

    r : (str) Quantidade de Memória RAM máxima a ser utilizada nos cálculos.
    np: (str) Número de núcleos do processador a serem usados nos cálculos. 
    fu: (str) Funcional da DFT ou método de cálculo a ser empregado.
    b: (str) Conjunto de base para os orbitais.
    omega = 0.0: (float) Valor do parâmetro de longo alcance para funcionais da LRC-DFT
    '''
    if omega >= 0.0 and omega < 1.0:
        omegaFormat = '0'+str(int(omega*10**9))
        omegaFormat = omegaFormat[:5]+'00000'
        print("omega = ",omega)
        return "%mem="+r+"GB\n%nproc="+np+"\n#p "+fu+"/"+b \
               +" iop(3/107="+omegaFormat+") iop(3/108="+omegaFormat+")" \
               +" int=ultrafine counterpoise=2 Scan\n\nTCC\n\n0 1\n"
    elif omega >= 0.0 and omega > 1.0:
        omegaFormat = str(int(omega*10**10))
        omegaFormat = omegaFormat[:5]+'00000'
        print("omega = ",omega)
        return "%mem="+r+"GB\n%nproc="+np+"\n#p "+fu+"/"+b \
               +" iop(3/107="+omegaFormat+") iop(3/108="+omegaFormat+")" \
               +" int=ultrafine counterpoise=2 Scan\n\nTCC\n\n0 1\n"
    else:
        return "%mem="+r+"GB\n%nproc="+np+"\n#p "+fu+"/"+b \
               +" int=ultrafine counterpoise=2 Scan\n\nTCC\n\n0 1\n"
#


M = 36 #No. de pontos das curvas angulares
N = 21 #No. de pontos das curvas radiais

interpol = True #Habilita o modo de interpolação detalhada ao redor de pontos de mínimo

log.write("\nNo. de pontos das curvas angulares: {}".format(M)+
          "\nNo. de pontos das curvas radiais: {}".format(N))
if interpol: log.write('Pontos adicionais ao redor dos mínimos serão calculados')

nram = '8'
npro = '8'

print('Gerando Entradas...')
log.write('\nGerando Entradas...')
def geraEntradas(ram, nproc, omega=0.0):
    '''
    Gera as entradas para o Gaussian com o valor de ômega dado.
    -----------------------------------------------------
    Params:
    
    ram : (str) Quantidade de Memória RAM máxima a ser utilizada nos cálculos.
    nproc: (str) Número de núcleos do processador a serem usados nos cálculos. 
    omega = 0.0: (float) Valor do parâmetro de longo alcance para funcionais da LRC-DFT.
    '''
    #Distâncias (em angstroms) e ângulos (em graus) da geometria do sistema H2O2-Kr
    D = 1.450                   #Distância O-O
    d = 0.966                   #Distância O-H
    chi = 108.0*np.pi/180.0     #Ângulo O-O-H
    teta1 = 0.0                 #Ângulo entre uma das ligações O-H e o eixo y
    teta2 = 0.0                 #Ângulo entre uma das ligaçẽos O-H e o eixo y
    dTeta = 10.0*np.pi/180.0    #Passo da variação de teta1 e teta2
    R = 8.0                     #Distância entre O-O e Kr

    atom = ['O','O','H','H','Kr']
    x = [0.0, 0.0, 0.0, 0.0, 0.0]
    y = [0.0, 0.0, d*np.sin(chi)*np.cos(teta1), d*np.sin(chi)*np.cos(teta2), R]
    z = [D/2, -D/2, D/2 - d*np.cos(chi), - D/2 + d*np.cos(chi), 0.0]

    for t in range(M):
            x = [0.0, 0.0, d*np.sin(chi)*np.sin(teta1+dTeta*t), d*np.sin(chi)*np.sin(teta2), 0.0]
            y = [0.0, 0.0, d*np.sin(chi)*np.cos(teta1+dTeta*t), d*np.sin(chi)*np.cos(teta2), 0.0]#R-t*dR
            z = [D/2, -D/2, D/2 - d*np.cos(chi), - D/2 + d*np.cos(chi), 0.0]
            with open('../Inputs/Inputs-'+funct+'/H2O2-Kr_'+str(t)+'.com','w') as h:
                h.write(cabecalho(ram,nproc,funct,base,omega))
                print(t)
                for j in range(len(atom)-1):
                    h.write(atom[j]+"(Fragment=1)   "+str(x[j])+"  "+str(y[j])+"  "+str(z[j])+"\n")
                h.write('Kr(Fragment=2)   0.    R1    0.')
                h.write('\n Variables:\n R1 3.0 S 20 +0.1\n')
                h.write("\n")
        
    if interpol:
        for t in range(M):
            x = [0.0, 0.0, d*np.sin(chi)*np.sin(teta1+dTeta*t), d*np.sin(chi)*np.sin(teta2), 0.0]
            y = [0.0, 0.0, d*np.sin(chi)*np.cos(teta1+dTeta*t), d*np.sin(chi)*np.cos(teta2), 0.0]#R-t*dR
            z = [D/2, -D/2, D/2 - d*np.cos(chi), - D/2 + d*np.cos(chi), 0.0]
            with open('../Inputs/Inputs-'+funct+'/H2O2-Kr_'+str(t)+'_1.com','w') as h:
                h.write(cabecalho(ram,nproc,funct,base,omega))
                print(t)
                for j in range(len(atom)-1):
                    h.write(atom[j]+"(Fragment=1)   "+str(x[j])+"  "+str(y[j])+"  "+str(z[j])+"\n")
                h.write('Kr(Fragment=2)   0.    R1    0.')
                h.write('\n Variables:\n R1 3.25 S 10 +0.1\n')
                h.write("\n")
    
        for t in np.arange(8.5, 28.5):
            x = [0.0, 0.0, d*np.sin(chi)*np.sin(teta1+dTeta*t), d*np.sin(chi)*np.sin(teta2), 0.0]
            y = [0.0, 0.0, d*np.sin(chi)*np.cos(teta1+dTeta*t), d*np.sin(chi)*np.cos(teta2), 0.0]#R-t*dR
            z = [D/2, -D/2, D/2 - d*np.cos(chi), - D/2 + d*np.cos(chi), 0.0]
            with open('../Inputs/Inputs-'+funct+'/H2O2-Kr_'+str(int(10*t))+'.com','w') as h:
                h.write(cabecalho(ram,nproc,funct,base,omega))
                print(t)
                for j in range(len(atom)-1):
                    h.write(atom[j]+"(Fragment=1)   "+str(x[j])+"  "+str(y[j])+"  "+str(z[j])+"\n")
                h.write('Kr(Fragment=2)   0.    R1    0.')
                h.write('\n Variables:\n R1 3.0 S 20 +0.1\n')
                h.write("\n")

        for t in np.arange(8.5, 28.5):
            x = [0.0, 0.0, d*np.sin(chi)*np.sin(teta1+dTeta*t), d*np.sin(chi)*np.sin(teta2), 0.0]
            y = [0.0, 0.0, d*np.sin(chi)*np.cos(teta1+dTeta*t), d*np.sin(chi)*np.cos(teta2), 0.0]#R-t*dR
            z = [D/2, -D/2, D/2 - d*np.cos(chi), - D/2 + d*np.cos(chi), 0.0]
            with open('../Inputs/Inputs-'+funct+'/H2O2-Kr_'+str(int(10*t))+'.com','w') as h:
                h.write(cabecalho(ram,nproc,funct,base,omega))
                print(t)
                for j in range(len(atom)-1):
                    h.write(atom[j]+"(Fragment=1)   "+str(x[j])+"  "+str(y[j])+"  "+str(z[j])+"\n")
                h.write('Kr(Fragment=2)   0.    R1    0.')
                h.write('\n Variables:\n R1 3.25 S 10 +0.1\n')
                h.write("\n")
        

MP4 = np.zeros(21)
#Lê os logs com os dados da SEP de referência (MP4)
print('Lendo energias de referência (MP4)...')
log.write('\n\nLendo energias de referência (MP4)...')
for k in range(M): #[0,17]: 
    R = np.arange(3,5.1,0.1)
    R1 = np.arange(3.25,4.25,0.1)
    mp4 = []
    keywords = ['Counterpoise', 'corrected', 'energy']
    with open('../Logs/Logs/H2O2-Kr_'+str(k)+'.log','r') as g:
        for line in g:
            linha = line.split()
            #print(linha)
            if linha[:3] == keywords:
                # print(linha, linha[-1])
                mp4.append(float(linha[-1]))
                # print('Energia '+str(k)+':',float(linha[-1]/219474.6305))
                log.write('\nArquivo '+g.name+' lido com sucesso!')

    with open('../Logs/Logs/H2O2-Kr_'+str(k)+'.log','r') as g:
        for line in g:
            linha = line.split()
            #print(linha)
            if linha[:3] == keywords:
                # print(linha, linha[-1])
                mp4.append(float(linha[-1]))
                # print('Energia '+str(k)+':',float(linha[-1]/219474.6305))
                log.write('\nArquivo '+g.name+' lido com sucesso!')

    MP4 = np.vstack((MP4,np.array(mp4)))

MP4 = MP4[1:,:]
print('Sucesso!')

print('Declarando parâmetros da otimização...')
log.write('\n\nDeclarando parâmetros da otimização...')
vetorUnit = np.repeat(1.,N)
#pesoInicial = np.array([1.0*vetorUnit, 2.0*vetorUnit])
pesoAngular = np.append(np.repeat(0.5, 10), np.append(np.repeat(1.0, 16), np.repeat(0.5, 10)))
pesoTotal = np.array([x*vetorUnit for x in pesoAngular]) 
count = 0 #Conta o número de iterações do Gaussian

# def rovibes():
#     '''TBA'''
#     return 0

def SEP(omega):
    '''
    Lê os logs com os dados da SEP a ser otimizada (DFT) e realiza o cálculo da diferença entre esta e a SEP de referência.
    -----------------------------------------------------
    Params:
    
    omega: (ndarray) Valores dos parâmetros de longo alcance para cada ponto angular a ser otimizado.
    '''
    global R, DFT, MP4, dE, MSE, count
    #Valor dos pesos do erro médio quadrático para cada coordenada angular
    SCF = np.zeros(21)
    log.write('\n\nIteração no. '+str(count)+' iniciada')

    geraEntradas(nram, npro, omega)      #Gera as entradas a serem utilizadas pelo Gaussian.

    t0 = time.time()
    os.system('bash roda-tudo.sh '+funct)               #Executa os cálculos do Gaussian, um por vez.
    print('Tempo de execução do Gaussian (s): ', time.time()-t0)
    
    log.write('\nIteração no. '+str(count)+' finalizada!'+
            '\nTempo de execução do Gaussian (s): '+str(time.time()-t0)+'\n')
            
    count += 1

    for k in range(M): #[0,17]: 
        R = np.arange(3,5.1,0.1)
        scf = []
        keywords = ['Counterpoise:', 'corrected', 'energy']
        with open('../Logs/Logs-'+funct+'/H2O2-Kr_'+str(k)+'.log','r') as g:
            for line in g:
                linha = line.split()
                if linha[:3] == keywords:
               	    scf.append(float(linha[-1]))
                    # print('Energia '+str(k)+':',float(linha[-1]/219474.6305))
            log.write('\nArquivo '+g.name+' lido com sucesso!')
                    #print(scf)

        SCF = np.vstack((SCF,np.array(scf)))
        #print(SCF)

    DFT = SCF[1:,:]
    print(DFT)
    dE = np.abs(MP4 - DFT)
    dE2 = dE*dE
    MSE = (dE2*pesoTotal).mean()

    print('Erro máximo: ', np.amax(dE))
    print('Menores energias: ',minimo(MP4), minimo(DFT))
    print("Erro médio quadrático: ", MSE)

    log.write('\nErro máximo: {}'.format(np.amax(dE)))
    log.write('\nMenores energias: {}, {}'.format(minimo(MP4), minimo(DFT)))
    log.write("\nErro médio quadrático: {}".format(MSE))

    return MSE

#Definindo rotina de otimização
print('\n\nIniciando otimização...')
ti = time.time()
# resultado = minimize(SEP, np.append(0.25, pesoInicial), method="BFGS", options = {'disp':True, 'eps':1e-3})
resultado = minimize(SEP, 0.25, method="Nelder-Mead", options = {'disp':True,'fatol': 1e-7})
tf = time.time() - ti

wOpt = resultado['x']# = 0.25 para wb97xd
                     # = 1.35 para lc-blyp
		             # = 0.55 para lc-wpbe

#Calcula e formata o tempo de execução total
tfh = int(tf/60/60)
tfm = int((tf/60/60 - int(tf/60/60))*60)
str_TF = str(tfh)+'h'+str(tfm)+'min'

#Escreve os resultados finais

print('---RESULTADOS FINAIS---')
print('-----------------------')
print(resultado)
print('Tempo total de execução da otimização: ',str_TF)
print('-----------------------')

with open('../resultado_'+funct+'.txt', 'w') as h:
    h.write('----------------RESULTADOS FINAIS--------------\n')
    h.write('Tempo total de execução da otimização: '+str_TF+'\n\n')
    for i in resultado:
        h.write(str(i)+": "+str(resultado[i])+"\n")
    for i in range(len(DFT[:,0])):
        h.write('\n----------------- TETA = '+str(float(i*10))+' ------------------\n')
        h.write('\n R - ------- DFT -------- ------- MP4 ---------\n')
        for j in range(len(R)):
            #print(i,j)
            #h.write(str(R[j])+"       "+str(DFT[i,j])+"       "+str(MP4[i,j])+"\n")
            h.write("%0.9f   %0.9f   %0.9f\n"%(R[j], DFT[i,j], MP4[i,j]))
    h.write('-----------------------------------------------\n')

log.write('\n\n----------------RESULTADOS FINAIS--------------\n')
log.write('Tempo total de execução da otimização: '+str_TF+'\n\n')
for i in resultado:
    log.write(str(i)+": "+str(resultado[i])+"\n")
for i in range(len(DFT[:,0])):
    log.write('\n----------------- TETA = '+str(float(i*10))+' ------------------\n')
    log.write('\n R - ------- DFT -------- ------- MP4 ---------\n')
    for j in range(len(R)):
        #print(i,j)
        #h.write(str(R[j])+"       "+str(DFT[i,j])+"       "+str(MP4[i,j])+"\n")
        log.write("%0.9f   %0.9f   %0.9f\n"%(R[j], DFT[i,j], MP4[i,j]))
log.write('-----------------------------------------------\n')

#Plot 3D
#Teta = np.arange(0,360,10)
#r,teta = np.meshgrid(R,Teta)

# ax1 = plt.subplot(111, projection='3d')
# ax1.set_title('Superfície de Energia Potencial (Comparativo)')
# ax1.plot_surface(r,teta,DFT,cmap='twilight_r',rcount = 100,ccount=100, label = 'Diferença')
# ax1.set_xlabel('R $(\\mathring{A})$')
# ax1.set_ylabel('$\\theta$ $(^o)$')
# ax1.set_zlabel('Energia $(cm^{-1})$')
# plt.show()

#Plot 2D

# #plt.suptitle("Curvas de Energia Potencial", fontsize = '22')
# fig, [graf1, graf2] = plt.subplots(1,2)
# graf3 = graf1.twinx()
# graf4 = graf2.twinx()
#
# graf1.set_title("Ângulo diédrico: $ \\theta = 100 ^o$", fontsize = '20')
# graf1.grid()
# graf1.set_xlabel('$R (\\mathring{A})$', fontsize = '18')
# graf1.set_ylabel('Energia $(cm^{-1})$', fontsize = '18')
# graf3.set_ylabel('Energia $(cm^{-1})$', fontsize = '18')
# graf1.set_ylim()
# graf1.plot(R, MP4, 'k', label = 'MP4')
# graf3.plot(R, DFT, 'g', label = 'DFT')
# graf1.legend()
# graf3.legend()
#
# graf2.set_title("Distância $\\mathrm{H_2O_2 - Kr}: R  = 3,5\\, \\mathring{A}$", fontsize = '20')
# graf2.grid()
# graf2.legend(fontsize = '18')
# graf2.set_xlabel('$\\theta (^o)$', fontsize = '18')
# graf2.set_ylabel('Energia $(cm^{-1})$', fontsize = '18')
# graf4.set_ylabel('Energia $(cm^{-1})$', fontsize = '18')
# graf2.plot(Teta, dE[:,5], 'k', label = 'MP4')
# #graf4.plot(Teta, DFT[:,5], 'r', label = 'DFT')
# graf2.legend(fontsize = '18')
# graf4.legend(fontsize = '18')
#
# plt.show()

log.close()

#       wb97xd
#      fun: 7.950941737661435e-06
# hess_inv: array([[81067.657761]])
#      jac: array([0.])
#  message: 'Optimization terminated successfully.'
#     nfev: 33
#      nit: 3
#     njev: 11
#   status: 0
#  success: True
#        x: array([0.25111888])

#def rodaTudo(gv,dir,fu, interpolation = False):
#    '''
#    Roda todas as entradas geradas na versão do Gaussian especificada.
#    ----------------------------------------------------- 
#    Params:
#
#    gv : (str) Versão do Gaussian (commando de inicialização).
#    dir: (str) Diretório de trabalho, i.e. onde se localizam as pastas com as entradas e saídas do Gaussian. 
#    fu: (str) Funcional da DFT ou método de cálculo a ser empregado.
#    interpolation: (Bool) Habilita a interpolação de pontos ao redor de mínimos.
#    '''
#    for i in range(M):
#        print('Rodando a entrada {0} no Gaussian {1}...'.format(i, gv[1:]))
#        os.system(gv+dir+'/Inputs/Inputs-'+fu+'/H2O2-Kr_'+str(i)+'.com '+\
#                     dir+'Logs/Logs-'+fu+'/H2O2-Kr_'+str(i)+'.log &')
#        os.system('sleep 10')
#    if interpolation:
#        for i in range(M):
#            print('Rodando a entrada {0} no Gaussian {1}...'.format(i, gv[1:]))
#            os.system(gv+dir+'/Inputs/Inputs-'+fu+'/H2O2-Kr_'+str(i)+'-1.com '+\
#                         dir+'Logs/Logs-'+fu+'/H2O2-Kr_'+str(i)+'-1.log &')
#            os.system('sleep 10')
#        for i in np.arange(8.5, 28.5):
#            print('Rodando a entrada {0} no Gaussian {1}...'.format(i, gv[1:]))
#            os.system(gv+dir+'/Inputs/Inputs-'+fu+'/H2O2-Kr_'+str(i)+'.com '+\
#                     dir+'Logs/Logs-'+fu+'/H2O2-Kr_'+str(i)+'.log &')
#            os.system('sleep 10')
#        for i in np.arange(8.5, 28.5):
#            print('Rodando a entrada {0} no Gaussian {1}...'.format(i, gv[1:]))
#            os.system(gv+dir+'/Inputs/Inputs-'+fu+'/H2O2-Kr_'+str(i)+'-1.com '+\
#                         dir+'Logs/Logs-'+fu+'/H2O2-Kr_'+str(i)+'-1.log &')
#            os.system('sleep 10')

