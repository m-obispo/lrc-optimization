import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

x = np.linspace(0.25,1,1000)
y1 = np.zeros(len(x))
y2 = np.zeros(len(x))

a = 5
x0 = 0.5

def Newton_Rapson(f, df, x0, erro):
	DeltaX = 10*erro
	c = 0
	while abs(DeltaX) > erro:
		y0 = f(x0)
		dy0 = df(x0)
		DeltaX = -y0/dy0
		x0 = x0 + DeltaX
		c += 1
	#print(c)
	return x0

def CEP(x):
    return a*((x0/x)**12 - (x0/x)**6)

def d_CEP(x):
    return a*(12*(x0/x)**(12) - 6*(x0/x)**(6))/x

def d2_CEP(x):
    return a*(168*(x0/x)**(12) - 42*(x0/x)**(6))/x/x

def approxilator(f, df, d2f, x):
    xo = 0.56
    print(xo)
    return d2f(xo)*(x-xo)**2 + f(xo)

for i in range(len(x)):
    y1[i] = float(CEP(x[i]))
    y2[i] = float(approxilator(CEP, d_CEP, d2_CEP, x[i]))

plt.suptitle("Curva de Energia Potencial", fontsize = 20)
#plt.title("$ \\omega $ = "+str(omega), fontsize = 18)
plt.plot(x, np.zeros(len(x)), 'k:')
plt.plot(x, y1, 'r', label = 'erf($\\omega r)/r$')
plt.plot(x, y2, 'k--', label = 'erfc($\\omega r)/r$')
plt.xlabel('$r (\\mathring{A})$', fontsize = 18)
plt.xticks(np.arange(0.25, 1.0, step=0.1), fontsize = '10')
plt.yticks(np.arange(-1.5, 0.25, step=0.25), fontsize = '10')
plt.xlim(0.45,1.0)
plt.ylim(-1.5,0.25)
plt.legend(fontsize = 16)
plt.grid()
plt.show()
