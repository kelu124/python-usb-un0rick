'''
Wrapper for viz
'''

import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import datetime

from .version import __version__


class FView(object):

    SAMPLES_PER_LINE = 16384
    GAINS_MAX = 32

    def gain_expand(self,gain,DR=False):
        if DR:
            nbPtsLine = self.SAMPLES_PER_LINE*2
        else:
            nbPtsLine = self.SAMPLES_PER_LINE
        return [gain[x // (nbPtsLine // self.GAINS_MAX)] / 1000.0 for x in range(nbPtsLine)]

    def ptstoline(self,start,stop,DR=False):
        if DR:
            nbPtsLine = self.SAMPLES_PER_LINE*2 
        else:
            nbPtsLine = self.SAMPLES_PER_LINE

        return [1 if (x >= start and x < stop) else 0 for x in range(nbPtsLine)]

    def ntons(self,N,DR=False):
        """Converts N units in nanosecs. Not impacted by DR."""
        return str(int(N/0.128))


    def readfile(self,npzPath):
        """Reads NPZ"""

        data = np.load(npzPath)
        if (data["nblines"]==32) & (data["doublerate"]==1):
            self.plotNDT(data)
        else:
            self.plotFirst(data)

        return data


    def plotFirst(self,data, show=True, save=True):
 
        t = data["t"]
        t1 = data["t_delay"]
        t2 = t1 + data["t_on"]
        t3 = t2 + data["t_inter"]
        t4 = t3 + data["t_off"]

        PON = self.ptstoline(t1,t2)
        POFF = self.ptstoline(t3,t4)
        m = int(15000//64)

        f = [k*63.75/self.SAMPLES_PER_LINE for k in range(len(data["signal"][0]))]

        FFT = np.abs(np.fft.fft(data["signal"][0]))

        plt.figure(figsize=(20,10))
        plt.subplot(2, 1, 1)

        plt.plot(t,self.gain_expand(data["gain"]),"y",label="Gain")
        plt.plot(t,data["signal"][0],"b",label="Signal")
        plt.plot(t[0:64*5],PON[0:64*5],"g",label="HV Pulse")
        plt.xlabel("us")
        plt.ylabel("Amplitude")
        plt.legend()
        title = str(data["timestamp"])+ ": "+str(data['nblines'])+ " lines.\n"
        title += "Waveform. PulseOn: "+self.ntons(data["t_on"])+"ns, damping of "+self.ntons(data["t_off"])+"ns.\n"
        title += "Python: version "+str(__version__)+". BIN: author:"+str(data["author"])+", version:"+str(data["version"])

        plt.subplot(2, 2, 3)
        plt.plot(t[0:m],data["signal"][0][0:m],alpha=0.3,label="Signal")
        plt.plot(t[0:m],PON[0:m],label="Pulse on")
        plt.plot(t[0:m],POFF[0:m], label="Dampening")
        plt.title('Pulse waveform')
        plt.ylabel('V')
        plt.ylabel('us')
        plt.legend()

        plt.subplot(2, 2, 4)
        plt.title('Spectrum composition')
        plt.plot(f[25:len(FFT)//2],FFT[25:len(FFT)//2])
        plt.xlabel('Freq (MHz)')
        plt.ylabel('Energy')

        plt.suptitle(title)
        plt.tight_layout()
        if save:
            plt.savefig(str(data["nameFile"])+".jpg")
        
        if show:
            plt.show()

        plt.close()
        plt.clf()

    def plotNDT(self,data,fCentral=None,bandwidth=None,
                show=True, save=True):
        if (data["nblines"]==32) & (data["doublerate"]==1):

            t1 = data["t_delay"]
            t2 = t1 + data["t_on"]
            t3 = t2 + data["t_inter"]
            t4 = t3 + data["t_off"]

            PON = self.ptstoline(t1,t2,DR=True)
            POFF = self.ptstoline(t3,t4,DR=True)
            m = int(15000//64)
            Npts = self.SAMPLES_PER_LINE * 2

            # Interleave data, so create a new matrix, double the size
            # of the original signal
            signal = np.empty((len(data["signal"][0])*2,),
                              dtype=data["signal"][0].dtype)

            # Compute even and odd datas.
            signal[0::2] = np.sum(data["signal"][::2], axis=0)/(data["nblines"]/2)
            signal[1::2] = np.sum(data["signal"][1::2], axis=0)/(data["nblines"]/2)

            t = [T*63.75*4/len(signal) for T in range(len(signal))]
            f = [2*k*63.75/Npts for k in range(Npts)]

            rawSignal = np.array(signal, copy=True)  
            FFT = np.abs(np.fft.fft(signal))
            if fCentral and bandwidth:
                FFT_clean = np.fft.fft(signal)
                N = len(f)//2
                for i in range(N+1):
                    if f[i] < (fCentral*(1-bandwidth)) or f[i]> (fCentral*(1+bandwidth)):
                        FFT_clean[i] = 0
                        FFT_clean[-i] = 0
                signal = np.real(np.fft.ifft(FFT_clean))
                msignal = np.max(np.abs(signal))
                signal = [float(x/msignal) for x in signal]

            plt.figure(figsize=(20,10))
            plt.subplot(2, 1, 1)

            plt.plot(t,self.gain_expand(data["gain"],DR=True),"y",label="Gain")
            
            if fCentral and bandwidth:
                plt.plot(t,rawSignal,"b",label="Raw signal" ,alpha = 0.3)
                plt.plot(t,signal,"r",label="Filtered signal (normalized)")
            else:
                plt.plot(t,signal,"b",label="Signal")

            plt.plot(t[0:64*5],PON[0:64*5],"g",label="HV Pulse")
            plt.xlim(0, 50) 
            plt.xlabel("us")
            plt.ylabel("Amplitude")
            plt.legend()
            title = str(data["timestamp"])+ ": "+str(data['nblines'])+ " lines.\n"
            title += "NDT averaged waveform (first 50us). PulseOn: "+self.ntons(data["t_on"])+"ns, damping of "+self.ntons(data["t_off"])+"ns.\n"
            title += "Python: saved version "+str(__version__)+" (saved with "+str(data["libversion"])+"). BIN: author:"+str(data["author"])+", version:"+str(data["version"])

            plt.subplot(2, 2, 3)
            if fCentral and bandwidth:
                plt.plot(t[0:m],rawSignal[0:m],"b",label="Raw signal" ,alpha = 0.1)
                plt.plot(t[0:m],signal[0:m],"r",label="Filtered signal (normalized)",alpha=0.3)
            else:
                plt.plot(t[0:m],signal[0:m],"b",label="Signal") 
            plt.plot(t[0:m],PON[0:m],label="Pulse on")
            plt.plot(t[0:m],POFF[0:m], label="Dampening")
            plt.title('Pulse waveform')
            plt.ylabel('V')
            plt.ylabel('us')
            plt.legend()

            plt.subplot(2, 2, 4)
            plt.title('Spectrum composition')
            plt.plot(f[50:len(FFT)//2],FFT[50:len(FFT)//2])
            if fCentral:
                if bandwidth:
                    plt.plot(f[50:len(FFT_clean)//2],np.abs(FFT_clean)[50:len(FFT_clean)//2])
            plt.xlabel('Freq (MHz)')
            plt.ylabel('Energy')

            plt.suptitle(title)
            plt.tight_layout()

            if save:
                plt.savefig(str(data["nameFile"])+"_ndt.jpg")
        
            if show:
                plt.show()
            
            plt.close()
            plt.clf()

        else:
            print("Conditions - 32 lines & double rate - not met for this plot.")
     
