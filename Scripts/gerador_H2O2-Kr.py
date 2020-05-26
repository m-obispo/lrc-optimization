import numpy as np

#i_file = sys.argv[1]
#funct = sys.argv[2]
#basis = sys.argv[3]

#try:
#    open(i_file,"r")
#except:
#    print("Erro na abertura do arquivo")
#    exit()

def cabecalho(r,np,fu,b):
    return "%mem="+r+"GB\n%nproc="+np+"\n#p "+fu+"/"+b \
           +" int=ultrafine Scan\n\nPTCC\n\n0 1\n"

ram = '2'
nproc = '2'

#Distâncias (em angstroms) e ângulos (em graus) da geometria do sistema H2O2-Kr
D = 1.450             #Distância O-O
d = 0.966             #Distância O-H
chi = 108.0*np.pi/180 #Ângulo O-O-H
teta1 = 0.0           #Ângulo entre uma das ligações O-H e o eixo y
teta2 = 0.0           #Ângulo entre uma das ligaçẽos O-H e o eixo y
dTeta = 10.*np.pi/180 #Passo da variação de teta1 e teta2
R = 8.0               #Distância entre O-O e Kr
dR = 0.1              #Passo da variação de R

atom = ['O','O','H','H','Kr']
x = [0.0, 0.0, 0.0, 0.0, 0.0]
y = [0.0, 0.0, d*np.sin(chi)*np.cos(teta1), d*np.sin(chi)*np.cos(teta2), R]
z = [D/2, -D/2, D/2 - d*np.cos(chi), - D/2 + d*np.cos(chi), 0.0]

#with open('teste.xyz','w') as h:
#    for i in range(len(atom)):
#        h.write(cabecalho(ram,nproc,'mp4','aug-cc-PVTz'))
#        h.write(atom[i]+'   '+str(x[i])+'   '+str(y[i])+'   '+str(z[i]))
#        h.write('\n')
#
#t=0
#k=0
#c=0

for t in range(36):
    x = [0.0, 0.0, d*np.sin(chi)*np.sin(teta1+dTeta*t), d*np.sin(chi)*np.sin(teta2), 0.0]
    y = [0.0, 0.0, d*np.sin(chi)*np.cos(teta1+dTeta*t), d*np.sin(chi)*np.cos(teta2), 0.0]#R-t*dR
    z = [D/2, -D/2, D/2 - d*np.cos(chi), - D/2 + d*np.cos(chi), 0.0]
    with open('../Inputs/H2O2-Kr_'+str(t)+'.com','w') as h:
        h.write(cabecalho(ram,nproc,'mp4','aug-cc-PVTz'))
        print(t)
        for j in range(len(atom)-1):
            h.write(atom[j]+"   "+str(x[j])+"  "+str(y[j])+"  "+str(z[j])+"\n")
        h.write('Kr   0.    R1    0.')
        h.write('\n Variables:\n R1 3.0 S 20 +0.1\n')
        h.write("\n")

    #Pai, te amo

#0 1
#O
#O       1        1.45000
#H       1        0.96600     2      108.00000
#H       2        0.96600     1      108.00000     3        0.02562
#Kr      3        4.20766     1      147.92161     2        0.02562
