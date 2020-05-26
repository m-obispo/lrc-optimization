import numpy as np
import matplotlib.pyplot as plt
import mpmath as mp

mp.dps = 15; mp.pretty = True

omega = 0.4

x = np.linspace(0.3,10,1000)
y1 = np.zeros(len(x))
y2 = np.zeros(len(x))

for i in range(len(x)):
    y1[i] = float(mp.erf(omega*x[i])/x[i])
    y2[i] = float(mp.erfc(omega*x[i])/x[i])

plt.suptitle("Correções de Longo Alcance", fontsize = 20)
plt.title("$ \\omega $ = "+str(omega), fontsize = 18)
plt.plot(x, y1, 'r', label = 'erf($\\omega r)/r$')
plt.plot(x, y2, 'b', label = 'erfc($\\omega r)/r$')
plt.plot(x, y1+y2, 'k', label = '1/r')
plt.xlabel('$r (\\mathring{A})$', fontsize = 18)
plt.xticks(np.arange(0, 11, step=1), fontsize = '16')
plt.legend(fontsize = 16)
plt.grid()
plt.show()
