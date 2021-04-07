'''
Main FPGA control script
'''

import numpy as np
import datetime

from time import sleep
from un0usb.csr_map import CsrMap
from un0usb.ftdi_dev import FtdiDevice
from .version import __version__

class FpgaControl(object):
    """Collection of FPGA control functions via FTDI API"""
    MAX_LINES = 32
    WORDS_PER_LINE = 16384

    def __init__(self, ftdi_url, spi_freq=1E6):
        """Initialize FPGA controller.

        Keyword arguments:
         ftdi_url -- FTDI device url, which can be obtained by Ftdi.show_devices()
         freq -- SPI frequency up to 8E6 (for FPGA running on 64 MHz)
        """
        self._ftdi = FtdiDevice(ftdi_url, spi_freq)
        self.csr = CsrMap(self._ftdi)

    def reset(self):
        """Reset FPGA logic"""
        self._ftdi.reset_logic_on()
        sleep(0.01)
        self._ftdi.reset_logic_off()

    def reload(self):
        """Reload FPGA configuration from flash"""
        self._ftdi.reset_config_on()
        sleep(0.01)
        self._ftdi.reset_config_off()
        sleep(0.5)

    def read_lines(self, n):
        """Read 'n' number of lines from SRAM buffer

        Maxinum 'n' -- 32
        """
        # reset external ram address to read from the memory beginning
        self.csr.ramraddrrst = 1
        res = []
        for _ in range(n):
            # read lines (16384 words per line) one by one
            line = self.csr.ramdata
            res += [line]
        return res

    def set_pulseform(self, initDelay=5, POn=16, PInter=16, Poff=5000):
        """Set pulser.
        8 ~ 42ns
        16 ~ 167ns
        25 ~ 208ns
        32 ~ 250ns
        50 units ~ 420ns
        100 ~ 794ns
        250 ~  1.5us
        1000 ~ 1833ns
        2500 ~ 1.5us
        Keyword arguments:
          initDelay -- ncycles before acquisition starts
          POn -- width of the pulse
          PInter -- time between Pon and PDamp
          Poff -- damping period
        """
        if initDelay:
            self.csr.initdel= initDelay
        if POn:
            self.csr.ponw = POn
        if PInter:
            self.csr.interw = PInter
        if Poff:
            self.csr.poffw = Poff

    def stdNDTacq(self):
        """Do standard acquisition - 32lines, interleaved, standard gain.
        """
        self.do_acquisition(acq_lines=32, gain=None, double_rate=True)
        now = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        return self.save(name_file=now+"_ndt")

    def do_acquisition(self, acq_lines=1, gain=None, double_rate=False):
        """Do acquisitions.
        
        Keyword arguments:
          acq_lines -- number of lines to sample: int 1 .. 32
          gain -- list with gain values: None or list with length of 32
          double_rate -- enable/disable interleaving mode: bool
        """
        if gain:
            self.csr.dacgain = gain
        else:
            gain = [int(100 + ((1000-100)*x*x*x/32/32/32)) for x in range(32)]
            self.csr.dacgain = gain
        self.csr.nblines = acq_lines - 1
        self.csr.drmode = int(double_rate)
        self.csr.acqstart = 1
        while (not self.csr.acqdone):
            sleep(0.01)
        return self.read_lines(acq_lines)

    def disconnect(self):
        """Disconnect from FTDI and close all open ports"""
        self._ftdi.close_connection()

    def line_to_voltage(self, line):
        """Extracting voltage reading from line raw data"""
        SAMPLE_W = 10
        SAMPLE_N = 2 ** SAMPLE_W
        res = [((2 * 1.0) / SAMPLE_N) * ((w & (SAMPLE_N - 1)) - SAMPLE_N // 2) for w in line]
        return np.array(res)

    def get_data(self):
        """
        Return the last measurement datas into a dictionnary
        """
        acq_res = self.read_lines(self.csr.nblines + 1)
        all_acqs = []

        for _, acq in enumerate(acq_res):
            all_acqs.append(self.line_to_voltage(acq))

        t_axis = [x*256.0/len(acq_res[0]) for x in range(len(acq_res[0]))]
        now = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        data = {"signal": all_acqs,
                "t": t_axis,
                "nblines": int(self.csr.nblines+1),
                "gain": self.csr.dacgain,
                "t_on": self.csr.ponw, 
                "dac": self.csr.dacout,
                "t_inter": self.csr.interw,
                "t_off": self.csr.poffw,
                "t_delay": self.csr.initdel,
                "author": self.csr.author,
                "version": self.csr.version,
                "doublerate": self.csr.drmode,
                "libversion": str(__version__),
                "timestamp": str(now),
                "nameFile": None}
        return data

    def save(self, name_file=None):
        """Save just one acquisition in npz file format"""
        data = self.get_data()
        if name_file is None:
            name_file = data["timestamp"]

        data["nameFile"] = str(name_file)
        np.savez_compressed(name_file, **data )

        return name_file+".npz"

class Acquisition(object):
    def empty():
        return False

if __name__ == "__main__":
    # init FTDI device
    fpga = FpgaControl('ftdi://ftdi:2232:/', spi_freq=8E6)

    # reload configuration (optional step - just to fill BRAM (DACGAIN registers) with initial values)
    fpga.reload()

    # reset fpga
    fpga.reset()

    # read initial state of INITDEL register
    print("initdel = 0x%x" % fpga.csr.initdel)
    # write new value to the INITDEL
    fpga.csr.initdel = 0x20
    # read current state of INITDEL register
    print("initdel = 0x%x" % fpga.csr.initdel)

    # read DACGAIN array initial state
    print("dacgain = ", fpga.csr.dacgain)
    # write new values to the DACGAIN
    fpga.csr.dacgain = [200 + i for i in range(32)]
    # read DACGAIN array current state
    print("dacgain = ", fpga.csr.dacgain)

    # some LED3 blinking
    fpga.csr.led3 = 1
    sleep(1)
    fpga.csr.led3 = 0
    sleep(0.3)
    fpga.csr.led3 = 1
    sleep(0.3)
    fpga.csr.led3 = 0

    # reset fpga again (optional)
    fpga.reset()

    # close FTDI interface
    fpga.disconnect()
