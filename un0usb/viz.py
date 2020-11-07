'''
Wrapper for viz
'''

import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import datetime

from .version import __version__


class FView(object):

    def readfile(self,npzPath):
        """Reads NPZ"""

        data = np.load(npzPath)

        SAMPLES_PER_LINE = 16384
        GAINS_MAX = 32
        def gain_expand(gain):
            return [gain[x // (SAMPLES_PER_LINE // GAINS_MAX)] / 1000.0 for x in range(SAMPLES_PER_LINE)]

        def ptstoline(start,stop):
            return [1 if (x >= start and x < stop) else 0 for x in range(SAMPLES_PER_LINE)]

        def ntons(dataT):
            return str(int(dataT/0.128))

        t1 = data["t_delay"]+1
        t2 = t1 + data["t_on"]
        t3 = t2 + data["t_inter"]
        t4 = t3 + data["t_off"]

        PON = ptstoline(t1,t2)
        POFF = ptstoline(t3,t4 )
        m = int(15000//64)

        f = [k*63.75/SAMPLES_PER_LINE for k in range(SAMPLES_PER_LINE)]
        FFT = np.abs(np.fft.fft(data["signal"][0]))
        plt.figure(figsize=(20,10))
        plt.subplot(2, 1, 1)

        plt.plot(data["t"],gain_expand(data["gain"]),"y",label="Gain")
        plt.plot(data["t"],data["signal"][0],"b",label="Signal")
        plt.plot(data["t"][0:64*5],PON[0:64*5],"g",label="HV Pulse")
        plt.xlabel("us")
        plt.ylabel("Amplitude")
        plt.legend()
        title = str(data["timestamp"])+ ": "+str(data['nblines'])+ " lines.\n"
        title += "Waveform. PulseOn: "+ntons(data["t_on"])+"ns, damping of "+ntons(data["t_off"])+"ns.\n"
        title += "Python: version "+str(__version__)+". BIN: author:"+str(data["author"])+", version:"+str(data["version"])

        plt.subplot(2, 2, 3)
        plt.plot(data["t"][0:m],data["signal"][0][0:m],alpha=0.3,label="Signal")
        plt.plot(data["t"][0:m],PON[0:m],label="Pulse on")
        plt.plot(data["t"][0:m],POFF[0:m], label="Dampening")
        plt.title('Pulse waveform')
        plt.ylabel('V')
        plt.ylabel('us')
        plt.legend()

        plt.subplot(2, 2, 4)
        plt.title('Spectrum composition')
        plt.plot(f[10:len(FFT)//2],FFT[10:len(FFT)//2])
        plt.xlabel('Freq (MHz)')
        plt.ylabel('Energy')

        plt.suptitle(title)
        plt.tight_layout()
        plt.savefig(npzPath.split(".")[0]+".jpg")
        plt.show()
        
