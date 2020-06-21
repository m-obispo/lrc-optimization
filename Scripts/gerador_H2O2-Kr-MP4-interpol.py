import numpy as np

#i_file = sys.argv[1]
#funct = sys.argv[2]
#basis = sys.argv[3]

#try:
#    open(i_file,"r")
#except:
#    print("Erro na abertura do arquivo")
#    exit()

funct = 'mp4'
base = 'aug-cc-PVTz'

interpol = True

M = 36 #No. de pontos das curvas angulares
N = 21 #No. de pontos das curvas radiais

def cabecalho(r,np,fu,b, i):
    return "%mem="+r+"GB\n%nproc="+np+"\n%Chk=/home/matheus/.tcc/chk/H2O2-Kr_"+str(i)+".chk"+\
            "\n#p "+fu+"/"+b+" int=ultrafine counterpoise=2 Scan\n\nTCC\n\n0,1 0,1 0,1\n"

def geraEntradas(omega=0.0):
    '''
    Gera as entradas para o Gaussian com o valor de ômega dado.
    -----------------------------------------------------
    Params:
    
    omega = 0.0: Valor do parâmetro de longo alcance para funcionais da LRC-DFT.
    '''
    ram = '8'
    nproc = '8'
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
            
    if interpol:
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
    else:
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

    #Pai, te amo

#0 1
#O
#O       1        1.45000
#H       1        0.96600     2      108.00000
#H       2        0.96600     1      108.00000     3        0.02562
#Kr      3        4.20766     1      147.92161     2        0.02562
