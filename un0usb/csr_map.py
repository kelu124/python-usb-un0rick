

class CsrMap:
    """Control/Status register map"""

    # INITDEL - Initial pulse delay -- 0 - 1 period of 127.5 MHz, 1 - 2 periods, etc.
    INITDEL_ADDR = 0x00
    INITDEL_WIDTH = 8
    INITDEL_MASK = 0xff

    # PONW - Pon width -- 0 - 1 period of 127.5 MHz, 1 - 2 periods, etc.
    PONW_ADDR = 0x01
    PONW_WIDTH = 8
    PONW_MASK = 0xff

    # POFFW - Poff width -- 0 - 1 period of 127.5 MHz, 1 - 2 periods, etc.
    POFFW_ADDR = 0x02
    POFFW_WIDTH = 8
    POFFW_MASK = 0xff

    # INTERW - Intermediate delay width -- 0 - 1 period of 127.5 MHz, 1 - 2 periods, etc.
    INTERW_ADDR = 0x03
    INTERW_WIDTH = 8
    INTERW_MASK = 0xff

    # DRMODE - Double resolution mode -- add 1 to INITDEL whe line is even
    DRMODE_ADDR = 0x04
    DRMODE_WIDTH = 1
    DRMODE_MASK = 0x1

    # DACOUT - DAC out -- value for the DAC idle state
    DACOUT_ADDR = 0x07
    DACOUT_WIDTH = 10
    DACOUT_MASK = 0x3ff

    # DACGAIN - DAC gain
    DACGAIN_ADDR = 0x20
    DACGAIN_WIDTH = 10
    DACGAIN_MASK = 0x3ff
    DACGAIN_N = 32

    # ACQSTART - Start acquisition
    ACQSTART_ADDR = 0x50
    ACQSTART_WIDTH = 1
    ACQSTART_MASK = 0x1

    # ACQDONE - Acquisition is done
    ACQDONE_ADDR = 0x51
    ACQDONE_WIDTH = 1
    ACQDONE_MASK = 0x1

    # NBLINES - Number of lines per acquisition -- 0 - 1 line, 1 - 2 lines, etc.
    NBLINES_ADDR = 0x52
    NBLINES_WIDTH = 8
    NBLINES_MASK = 0xff

    # ACQBUSY - Acquisition is busy
    ACQBUSY_ADDR = 0x53
    ACQBUSY_WIDTH = 1
    ACQBUSY_MASK = 0x1

    # LED1 - LED1 (LED_ACQUISITION) control
    LED1_ADDR = 0x63
    LED1_WIDTH = 1
    LED1_MASK = 0x1

    # LED2 - LED2 (LED_SiNGLE/nLOOP) control
    LED2_ADDR = 0x64
    LED2_WIDTH = 1
    LED2_MASK = 0x1

    # LED3 - LED3 control
    LED3_ADDR = 0x65
    LED3_WIDTH = 1
    LED3_MASK = 0x1

    # TOPTURN1 - TOP_TURN1 status
    TOPTURN1_ADDR = 0x66
    TOPTURN1_WIDTH = 1
    TOPTURN1_MASK = 0x1

    # TOPTURN2 - TOP_TURN2 status
    TOPTURN2_ADDR = 0x67
    TOPTURN2_WIDTH = 1
    TOPTURN2_MASK = 0x1

    # TOPTURN3 - TOP_TURN3 status
    TOPTURN3_ADDR = 0x68
    TOPTURN3_WIDTH = 1
    TOPTURN3_MASK = 0x1

    # JUMPER1 - Jumper1 status
    JUMPER1_ADDR = 0x69
    JUMPER1_WIDTH = 1
    JUMPER1_MASK = 0x1

    # JUMPER2 - Jumper2 status
    JUMPER2_ADDR = 0x6A
    JUMPER2_WIDTH = 1
    JUMPER2_MASK = 0x1

    # JUMPER3 - Jumper3 status
    JUMPER3_ADDR = 0x6B
    JUMPER3_WIDTH = 1
    JUMPER3_MASK = 0x1

    # OUT1ICE - OUT1_ICE output control
    OUT1ICE_ADDR = 0x6C
    OUT1ICE_WIDTH = 1
    OUT1ICE_MASK = 0x1

    # OUT2ICE - OUT2_ICE output control
    OUT2ICE_ADDR = 0x6D
    OUT2ICE_WIDTH = 1
    OUT2ICE_MASK = 0x1

    # OUT3ICE - OUT3_ICE output control
    OUT3ICE_ADDR = 0x6E
    OUT3ICE_WIDTH = 1
    OUT3ICE_MASK = 0x1

    # RAMDATA - Read data from the external RAM
    RAMDATA_ADDR = 0xA0
    RAMDATA_WIDTH = 16
    RAMDATA_MASK = 0xffff
    RAMDATA_N = 16384

    # RAMRADDRRST - Reset external RAM read address
    RAMRADDRRST_ADDR = 0xA1
    RAMRADDRRST_WIDTH = 1
    RAMRADDRRST_MASK = 0x1

    # RAMFINC - Fill external RAM with incrementing data pattern
    RAMFINC_ADDR = 0xA4
    RAMFINC_WIDTH = 1
    RAMFINC_MASK = 0x1

    # RAMFDEC - Fill external RAM with decrementing data pattern
    RAMFDEC_ADDR = 0xA5
    RAMFDEC_WIDTH = 1
    RAMFDEC_MASK = 0x1

    # RAMFDONE - Filling of external RAM is done
    RAMFDONE_ADDR = 0xA6
    RAMFDONE_WIDTH = 1
    RAMFDONE_MASK = 0x1

    # AUTHOR - Author
    AUTHOR_ADDR = 0xF0
    AUTHOR_WIDTH = 8
    AUTHOR_MASK = 0xff

    # VERSION - Version
    VERSION_ADDR = 0xF1
    VERSION_WIDTH = 8
    VERSION_MASK = 0xff

    def __init__(self, ftdidev):
        self._ftdi = ftdidev

    @property
    def initdel(self):
        """Get current INITDEL register value"""
        data = self._ftdi.spi_read(self.INITDEL_ADDR, len=1, burst='fixed')
        return data[0] & self.INITDEL_MASK

    @initdel.setter
    def initdel(self, val):
        """Set INITDEL register with new value"""
        data = val & self.INITDEL_MASK
        self._ftdi.spi_write(self.INITDEL_ADDR, [data], burst='fixed')

    @property
    def ponw(self):
        """Get current PONW register value"""
        data = self._ftdi.spi_read(self.PONW_ADDR, len=1, burst='fixed')
        return data[0] & self.PONW_MASK

    @ponw.setter
    def ponw(self, val):
        """Set PONW register with new value"""
        data = val & self.PONW_MASK
        self._ftdi.spi_write(self.PONW_ADDR, [data], burst='fixed')

    @property
    def poffw(self):
        """Get current POFFW register value"""
        data = self._ftdi.spi_read(self.POFFW_ADDR, len=1, burst='fixed')
        return data[0] & self.POFFW_MASK

    @poffw.setter
    def poffw(self, val):
        """Set POFFW register with new value"""
        data = val & self.POFFW_MASK
        self._ftdi.spi_write(self.POFFW_ADDR, [data], burst='fixed')

    @property
    def interw(self):
        """Get current INTERW register value"""
        data = self._ftdi.spi_read(self.INTERW_ADDR, len=1, burst='fixed')
        return data[0] & self.INTERW_MASK

    @interw.setter
    def interw(self, val):
        """Set INTERW register with new value"""
        data = val & self.INTERW_MASK
        self._ftdi.spi_write(self.INTERW_ADDR, [data], burst='fixed')

    @property
    def drmode(self):
        """Get current DRMODE register value"""
        data = self._ftdi.spi_read(self.DRMODE_ADDR, len=1, burst='fixed')
        return data[0] & self.DRMODE_MASK

    @drmode.setter
    def drmode(self, val):
        """Set DRMODE register with new value"""
        data = val & self.DRMODE_MASK
        self._ftdi.spi_write(self.DRMODE_ADDR, [data], burst='fixed')

    @property
    def dacout(self):
        """Get current DACOUT register value"""
        data = self._ftdi.spi_read(self.DACOUT_ADDR, len=1, burst='fixed')
        return data[0] & self.DACOUT_MASK

    @dacout.setter
    def dacout(self, val):
        """Set DACOUT register with new value"""
        data = val & self.DACOUT_MASK
        self._ftdi.spi_write(self.DACOUT_ADDR, [data], burst='fixed')

    @property
    def dacgain(self):
        """Get current DACGAIN registers values"""
        data = self._ftdi.spi_read(self.DACGAIN_ADDR, len=self.DACGAIN_N, burst='incr')
        return [w & self.DACGAIN_MASK for w in data]

    @dacgain.setter
    def dacgain(self, val):
        """Set DACGAIN registers with new values"""
        data = [w & self.DACGAIN_MASK for w in val]
        self._ftdi.spi_write(self.DACGAIN_ADDR, data, burst='incr')

    @property
    def acqstart(self):
        """Get current ACQSTART register value"""
        return 0

    @acqstart.setter
    def acqstart(self, val):
        """Set ACQSTART register with new value"""
        data = val & self.ACQSTART_MASK
        self._ftdi.spi_write(self.ACQSTART_ADDR, [data], burst='fixed')

    @property
    def acqdone(self):
        """Get current ACQDONE register value"""
        data = self._ftdi.spi_read(self.ACQDONE_ADDR, len=1, burst='fixed')
        return data[0] & self.ACQDONE_MASK

    @property
    def nblines(self):
        """Get current NBLINES register value"""
        data = self._ftdi.spi_read(self.NBLINES_ADDR, len=1, burst='fixed')
        return data[0] & self.NBLINES_MASK

    @nblines.setter
    def nblines(self, val):
        """Set NBLINES register with new value"""
        data = val & self.NBLINES_MASK
        self._ftdi.spi_write(self.NBLINES_ADDR, [data], burst='fixed')

    @property
    def acqbusy(self):
        """Get current ACQBUSY register value"""
        data = self._ftdi.spi_read(self.ACQBUSY_ADDR, len=1, burst='fixed')
        return data[0] & self.ACQBUSY_MASK

    @property
    def led1(self):
        """Get current LED1 register value"""
        data = self._ftdi.spi_read(self.LED1_ADDR, len=1, burst='fixed')
        return data[0] & self.LED1_MASK

    @led1.setter
    def led1(self, val):
        """Set LED1 register with new value"""
        data = val & self.LED1_MASK
        self._ftdi.spi_write(self.LED1_ADDR, [data], burst='fixed')

    @property
    def led2(self):
        """Get current LED2 register value"""
        data = self._ftdi.spi_read(self.LED2_ADDR, len=1, burst='fixed')
        return data[0] & self.LED2_MASK

    @led2.setter
    def led2(self, val):
        """Set LED2 register with new value"""
        data = val & self.LED2_MASK
        self._ftdi.spi_write(self.LED2_ADDR, [data], burst='fixed')

    @property
    def led3(self):
        """Get current LED3 register value"""
        data = self._ftdi.spi_read(self.LED3_ADDR, len=1, burst='fixed')
        return data[0] & self.LED3_MASK

    @led3.setter
    def led3(self, val):
        """Set LED3 register with new value"""
        data = val & self.LED3_MASK
        self._ftdi.spi_write(self.LED3_ADDR, [data], burst='fixed')

    @property
    def topturn1(self):
        """Get current TOPTURN1 register value"""
        data = self._ftdi.spi_read(self.TOPTURN1_ADDR, len=1, burst='fixed')
        return data[0] & self.TOPTURN1_MASK

    @property
    def topturn2(self):
        """Get current TOPTURN2 register value"""
        data = self._ftdi.spi_read(self.TOPTURN2_ADDR, len=1, burst='fixed')
        return data[0] & self.TOPTURN2_MASK

    @property
    def topturn3(self):
        """Get current TOPTURN3 register value"""
        data = self._ftdi.spi_read(self.TOPTURN3_ADDR, len=1, burst='fixed')
        return data[0] & self.TOPTURN3_MASK

    @property
    def jumper1(self):
        """Get current JUMPER1 register value"""
        data = self._ftdi.spi_read(self.JUMPER1_ADDR, len=1, burst='fixed')
        return data[0] & self.JUMPER1_MASK

    @property
    def jumper2(self):
        """Get current JUMPER2 register value"""
        data = self._ftdi.spi_read(self.JUMPER2_ADDR, len=1, burst='fixed')
        return data[0] & self.JUMPER2_MASK

    @property
    def jumper3(self):
        """Get current JUMPER3 register value"""
        data = self._ftdi.spi_read(self.JUMPER3_ADDR, len=1, burst='fixed')
        return data[0] & self.JUMPER3_MASK

    @property
    def out1ice(self):
        """Get current OUT1ICE register value"""
        data = self._ftdi.spi_read(self.OUT1ICE_ADDR, len=1, burst='fixed')
        return data[0] & self.OUT1ICE_MASK

    @out1ice.setter
    def out1ice(self, val):
        """Set OUT1ICE register with new value"""
        data = val & self.OUT1ICE_MASK
        self._ftdi.spi_write(self.OUT1ICE_ADDR, [data], burst='fixed')

    @property
    def out2ice(self):
        """Get current OUT2ICE register value"""
        data = self._ftdi.spi_read(self.OUT2ICE_ADDR, len=1, burst='fixed')
        return data[0] & self.OUT2ICE_MASK

    @out2ice.setter
    def out2ice(self, val):
        """Set OUT2ICE register with new value"""
        data = val & self.OUT2ICE_MASK
        self._ftdi.spi_write(self.OUT2ICE_ADDR, [data], burst='fixed')

    @property
    def out3ice(self):
        """Get current OUT3ICE register value"""
        data = self._ftdi.spi_read(self.OUT3ICE_ADDR, len=1, burst='fixed')
        return data[0] & self.OUT3ICE_MASK

    @out3ice.setter
    def out3ice(self, val):
        """Set OUT3ICE register with new value"""
        data = val & self.OUT3ICE_MASK
        self._ftdi.spi_write(self.OUT3ICE_ADDR, [data], burst='fixed')

    @property
    def ramdata(self):
        """Get all data from RAMDATA buffer"""
        data = self._ftdi.spi_read(self.RAMDATA_ADDR, len=self.RAMDATA_N, burst='fixed')
        return [w & self.RAMDATA_MASK for w in data]

    @property
    def ramraddrrst(self):
        """Get current RAMRADDRRST register value"""
        return 0

    @ramraddrrst.setter
    def ramraddrrst(self, val):
        """Set RAMRADDRRST register with new value"""
        data = val & self.RAMRADDRRST_MASK
        self._ftdi.spi_write(self.RAMRADDRRST_ADDR, [data], burst='fixed')

    @property
    def ramfinc(self):
        """Get current RAMFINC register value"""
        return 0

    @ramfinc.setter
    def ramfinc(self, val):
        """Set RAMFINC register with new value"""
        data = val & self.RAMFINC_MASK
        self._ftdi.spi_write(self.RAMFINC_ADDR, [data], burst='fixed')

    @property
    def ramfdec(self):
        """Get current RAMFDEC register value"""
        return 0

    @ramfdec.setter
    def ramfdec(self, val):
        """Set RAMFDEC register with new value"""
        data = val & self.RAMFDEC_MASK
        self._ftdi.spi_write(self.RAMFDEC_ADDR, [data], burst='fixed')

    @property
    def ramfdone(self):
        """Get current RAMFDONE register value"""
        data = self._ftdi.spi_read(self.RAMFDONE_ADDR, len=1, burst='fixed')
        return data[0] & self.RAMFDONE_MASK

    @property
    def author(self):
        """Get current AUTHOR register value"""
        data = self._ftdi.spi_read(self.AUTHOR_ADDR, len=1, burst='fixed')
        return data[0] & self.AUTHOR_MASK

    @property
    def version(self):
        """Get current VERSION register value"""
        data = self._ftdi.spi_read(self.VERSION_ADDR, len=1, burst='fixed')
        return data[0] & self.VERSION_MASK
