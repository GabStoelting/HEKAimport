# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 16:56:18 2019

This file contains some common function (hence "cf") used by many of the other files

@author: Gabriel
"""

import struct
import re

"""
# get_struct allows to return a struct format string from a list up to a maximum size
#
# Inputs:
#           struct_list: A list of individual components of a struct format string
#           size: The intended size of the returned struct format string
#
# Returns a struct format string with at least the intended size but be careful that the actual
# size might be larger! If required, check the result against the intended size!
"""

def get_struct(struct_list, size):
    rString = struct_list[0]
    i = 1
    
    while((struct.calcsize(rString)<size) & (i<len(struct_list))):
        rString = rString+struct_list[i]
        i+=1
        
    return rString


"""
 read_level allows to read one level of the HEKA tree headers
 
 Inputs:
             data: Raw data
             start_pos: Current position in file
             level_size: Size of the current level header description
             struct_string: Header struct format string
"""

def read_level(data, start_pos, level_size, struct_string):

    # I need to check if this regex really works for all struct format strings...
    struct_list = re.findall(r"[=]*[0-9]*[a-z,?]", struct_string)
    
    #returns new position in file, data grouped according to the documentation and the number of children
    sString = get_struct(struct_list, level_size)       
    actSize = struct.calcsize(sString)
        
    return start_pos+level_size+4, struct.unpack(sString, data[start_pos:start_pos+actSize]), struct.unpack('i', data[start_pos+level_size:start_pos+level_size+4])[0]
