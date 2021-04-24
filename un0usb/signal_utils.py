#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Some functions to manipulate the data from the
    un0rick board.

    __author__ = "Jean-Michel Leyrie"
    __license__ = "GPLv3"
    __version__ = "0.1"
"""
import numpy as np

def interpolate_double(arr):
    """
    Double the size of an array of values.
    Each interleaved data is the mean of the 2 surrounded values.

    Parameter
    ----------
        arr: array to be interpolated.

    Return
    -------
        Numpy array
            interpolated array, so double the size of "arr"
    """
    res = np.empty((len(arr)*2,))
    res[0::2] = arr
    res[1::2] = (arr + np.append(arr[1:], (arr[-1])))/2
    return res

def interleave(arr, odd_first=True):
    """
    Interleave an array of arrays :
    1. Even arrays are averaged among themselves.
    2. Odd arrays are averaged among themselves.
    3. Even et odd arrays are interleaved

    Parameters
    ----------
        arr: Array of arrays to be interleaved

        odd_first: Boolean
            The odd arrays will be in odd positions in the result.

    Return
    ------
        Numpy array
            One array, with the averaged and interleaved data.
            Double the size of arr.
    """
    res = np.empty((len(arr[0])*2,), dtype=arr[0].dtype)

    if odd_first:
        res[0::2] = np.sum(arr[1::2], axis=0)/(len(arr)/2)
        res[1::2] = np.sum(arr[::2], axis=0)/(len(arr)/2)
    else:
        res[0::2] = np.sum(arr[::2], axis=0)/(len(arr)/2)
        res[1::2] = np.sum(arr[1::2], axis=0)/(len(arr)/2)
    return res

def process_data(data, interleaved=False):
    """
    Extract, mean and interleave the data from a measurement.

    Parameters
    ----------
    data: dict
        Array of measurements arrays.
        data["signal"] Shall contains the measurements arrays
        data["t"] shall contains the time axis

    interleaved: Boolean. Indicate if the resulted array shall interleave
                 or not the measurements. If True, the time axis will
                 be interpolated.

    Return
    ------
    Numpy array: One array of tuples containing the result.
                 Each element of the array is a (time, data) tuple.


    """
    if interleaved:
        res_data = interleave(data["signal"])
        res_time = interpolate_double(data["t"])

    else:
        # Just mean the acquisition lines between them
        res_data = np.sum(data["signal"], axis=0)/len(data["signal"])
        res_time = data["t"]

    return np.stack((res_time, res_data), axis=1)
