#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module to display continiously a 2D signal with openCV2.
    The aim of this module is to be faster than pyplot.
    The signal is displayed without axis nor text strings.

    __author__ = "Jean-Michel Leyrie"
    __license__ = "GPLv3"
    __version__ = "0.1"
"""

import cv2
import numpy as np

class Plotter():
    """ A class used to display a signal on screen using opencv """
    canvas = None
    line_color_rvb = (0, 255, 0)
    name = None

    def __init__(self, size, xrange, yrange, name="OpenCV Plotter"):
        """
        Parameters
        ----------
        size : tuple
            Shall contains (width, heigh) of the openCV window.
            OpenCV axis reference.

        xrange : tuple
            Shall contains (xmin, xmax) of the x axis window.
            Data axis reference.

        yrange : tuple
            Shall contains (ymin, ymax) of the y axis window.
            Data axis reference.

        name : str
            Name of the OpenCV window
        """
        self.width, self.height = size
        xmin, xmax = xrange
        ymin, ymax = yrange
        self.xfactor = self.width / (abs(xmax)+abs(xmin))
        self.yfactor = self.height / (abs(ymax)+abs(ymin))
        self.xaxis_position = ymax * self.yfactor
        self.name = name

    def to_opencv_references(self, xy_arr):
        """
        Change the axis references from standard X/Y to
        OpenCV references.

        Parameter
        ----------
        xy_arr : list
            [x, y] data to display. Ex: [[x1, y1], [x2, y2] ...]

        Return
        -------
        list
            xy copy transposed in the openCV axis references
        """
        _xy_arr = xy_arr.copy()
        _xy_arr[:, 0] *= self.xfactor
        _xy_arr[:, 1] = self.xaxis_position - _xy_arr[:, 1]* self.yfactor

        return _xy_arr

    def plot(self, xy_arr, wait_ms=10):
        """
        Plot a numpy array using openCV.

        Parameters
        ----------
        xy_arr : list
            [x, y] data to display. Ex: [[x1, y1], [x2, y2] ...]
        """
        self.canvas = np.ones((self.height, self.width, 3), np.int8)
        signal = self.to_opencv_references(xy_arr).astype(np.int32)
        img = cv2.polylines(self.canvas, [signal], False,
                            self.line_color_rvb, thickness=1)
        cv2.imshow(self.name, img)
        cv2.waitKey(wait_ms)

if __name__ == "__main__":
    ### Example
    PLT = Plotter(size=(800, 500),
                  xrange=(-10, 300),
                  yrange=(-100, 100),
                  name="Sinus plot")

    # Plot y=i*sin(50x), with
    #   x = 0 to 300
    #   i = 0 to 100
    X = np.arange(-10, 300)
    for i in range(100):
        Y = np.sin(X*50+i)*i
        SIGNAL = np.stack((X, Y), axis=1)
        PLT.plot(SIGNAL)

    cv2.waitKey(0)
