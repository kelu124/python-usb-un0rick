#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Command line tool to display the signal acquired by the un0rick
    in real time.

    __author__ = "Jean-Michel Leyrie"
    __license__ = "GPLv3"
    __version__ = "0.1"
"""
import argparse
from . import fpga_ctrl as USB
from .utils import cvplotter
from .utils import signal_utils as sigutils

def init_un0rick(device='ftdi://ftdi:2232:/'):
    """ un0rick board initialisation """
    fpga = USB.FpgaControl(device, spi_freq=8E6)
    fpga.reload()
    fpga.reset()
    return fpga

def continuous_acq(acq_lines=32, double_rate=True):
    """
    Perform a continuous acquisition, and display it
    in a opencv container.

    Parameters
    ----------
    acq_lines: Integer
        From 1 to 32. Number of lines acquired by the FPGA.

    double_rate: Boolean
        Perform acquisitions à double rates to be able to interleave the
        measurements.
    """
    fpga = init_un0rick()
    while 1:
        fpga.do_acquisition(acq_lines=acq_lines, double_rate=double_rate)
        # Make a copy of the signal to avoid problems with modifications
        # as it should impact un0usb.fpga
        data = fpga.get_data().copy()
        res = sigutils.process_data(data, interleaved=double_rate)
        cvplotter.Plotter((800, 500), (0, 256), (-1, 1)).plot(res)

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description="Start a continuous "
                                                 "acquisition and real time "
                                                 "display")
    PARSER.add_argument("-l", "--acqlines",
                        type=int,
                        help="Acquisition lines. Shall be from 1 to 32.",
                        default=1)

    PARSER.add_argument("-d", "--doublerate",
                        help="Acquisition lines. Shall be from 1 to 32.",
                        default=False,
                        action="store_true")

    ARGS = PARSER.parse_args()
    continuous_acq(ARGS.acqlines, ARGS.doublerate)
