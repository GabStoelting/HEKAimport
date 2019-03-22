# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 12:50:45 2014

@author: Stölting
"""

import struct
import numpy as np


def DATload(raw_data, data_pos, sample_count, sample_type, scaling_factor, leak):
    output = np.empty(sample_count)
    sample = 0
    if sample_type == b"\x00": # If data is stored as int16 proceed as follows
        sample_size = 2            
        for i in np.arange(data_pos, data_pos+(sample_size*sample_count),sample_size):
            output[sample] = int(struct.unpack('h', raw_data[i:i+sample_size])[0])*scaling_factor
            sample += 1
        if leak == True:
            print( "Leak!")
            sample = 0
            for i in np.arange(data_pos+(sample_size*sample_count), data_pos+(2*sample_size*sample_count), sample_size):
                output[sample] += int(struct.unpack('h', raw_data[i:i+sample_size])[0])*scaling_factor
                sample += 1
        return output
        
    if sample_type == b"\x01": # If data is stored as int32 proceed as follows
        sample_size = 4            
        for i in np.arange(data_pos, data_pos+(sample_size*sample_count),sample_size):
            output[sample] = int(struct.unpack('i', raw_data[i:i+sample_size])[0])*scaling_factor
            sample += 1
        if leak == True:
            print( "Leak!")
            sample = 0
            for i in np.arange(data_pos+(sample_size*sample_count), data_pos+(2*sample_size*sample_count), sample_size):
                output[sample] += int(struct.unpack('i', raw_data[i:i+sample_size])[0])*scaling_factor
                sample += 1
        return output        
        
    if sample_type == b"\x02": # If data is stored as float32 proceed as follows
        sample_size = 4  
        print( "float32"  )        
        for i in np.arange(data_pos, data_pos+(sample_size*sample_count),sample_size):
            output[sample] = float(struct.unpack('f', raw_data[i:i+sample_size])[0])*scaling_factor
            sample += 1
        if leak == True:
            print( "Leak!")
            sample = 0
            for i in np.arange(data_pos+(sample_size*sample_count), data_pos+(2*sample_size*sample_count), sample_size):
                output[sample] += float(struct.unpack('f', raw_data[i:i+sample_size])[0])*scaling_factor
                sample += 1
        return output                

    if sample_type == b"\x03": # If data is stored as float64 proceed as follows
        sample_size = 8            
        for i in np.arange(data_pos, data_pos+(sample_size*sample_count),sample_size):
            output[sample] = float(struct.unpack('d', raw_data[i:i+sample_size])[0])*scaling_factor
            sample += 1
        if leak == True:
            print( "Leak!")
            sample = 0
            for i in np.arange(data_pos+(sample_size*sample_count), data_pos+(2*sample_size*sample_count), sample_size):
                output[sample] += float(struct.unpack('d', raw_data[i:i+sample_size])[0])*scaling_factor
                sample += 1
        return output                        