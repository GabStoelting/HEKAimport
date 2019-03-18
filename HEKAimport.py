# -*- coding: utf-8 -*-
"""
Created on Mon Aug 04 13:55:38 2014

@author: Stölting
"""
import struct
import numpy as np
import pandas as pd
import PULimport
import PGFimport
import DATimport

class HEKAfile(object):
    
    def __init__(self, filename):
        if filename is "":
            return
        
        self.filename  = filename
        try:
            patchmaster_file = open(filename, 'rb')
        except:
            raise NameError("Sorry, but "+filename+" couldn't be opened.")
            
        self.patchmaster_data = patchmaster_file.read()      
        
        # Check for "DAT2" signature in the beginning of the file
        if "DAT2" not in str(struct.unpack("8s", self.patchmaster_data[0:8])[0]):
            raise NameError("Sorry, but "+filename+" does not appear to be a properly bundled HEKA Patchmaster file.")
            return
    
        number_of_items = struct.unpack('i', self.patchmaster_data[48:52])[0]
        
        self.start_dict = {}
        self.stop_dict = {}

        # Read the positions of the bundled data files
        for i in np.arange(0, number_of_items):
            data_type = b"".join(struct.unpack("4c", self.patchmaster_data[72+(i*16):76+(i*16)]))
            self.start_dict[data_type] = int(struct.unpack("i", self.patchmaster_data[64+(i*16):68+(i*16)])[0])
            self.stop_dict[data_type] = int(struct.unpack("i", self.patchmaster_data[68+(i*16):72+(i*16)])[0])   

        self.pulfile = PULimport.PULfile(self.patchmaster_data, int(self.start_dict[b".pul"]))
       
        self.pgffile = PGFimport.PGFfile(self.patchmaster_data, int(self.start_dict[b".pgf"]))
        
    def get_Groups(self):
        return self.pulfile.Groups
    
    # Return a dictionary of the groups within the bundled ".pul"-file
    def get_GroupDict(self):
        groupDict = {}
        for group in self.pulfile.Groups:
            groupDict[group.Label] = group
        return groupDict
            
    # Return all series within a group
    def get_Series(self, group):
       return group.Series 
       
       
    def get_Sweeps_byindex(self, group_index, series_index, ZeroOffset=False):
        
        Sweeps = pd.DataFrame()
        
        for sweep in self.pulfile.Groups[group_index].Series[series_index].Sweeps:
            for trace in sweep.Traces:   
                trace_data = DATimport.DATload(self.patchmaster_data, trace.Data, trace.DataPoints, trace.DataFormat, (trace.DataScaler*10**12), False)
                if ZeroOffset:
                    trace_data = trace_data - (trace.ZeroData*10**12) # Diese fixe Multiplikation mit 10**12 ist doof wenn ich V-Mon Daten zeigen will (Die brauchen ja nicht auf nV umgestellt werden...)
                time = np.linspace(0, trace.DataPoints*trace.XInterval, num=trace.DataPoints, endpoint=False)
                trace_df = pd.DataFrame(trace_data, index=time, columns=[trace.Label.decode().split('\x00')[0]])            
                Sweeps = pd.concat([Sweeps, trace_df], axis=1) # Sweeps beinhaltet am Ende alle Datenpunkte in einem Pandas DataFrame
                    
        return Sweeps
        
    def get_Sweeps(self, series, ZeroOffset=False):
        
        Sweeps = pd.DataFrame()
        
        for sweep in series.Sweeps:
            for trace in sweep.Traces:
                trace_data = DATimport.DATload(self.patchmaster_data, trace.Data, trace.DataPoints, trace.DataFormat, (trace.DataScaler*10**12), False)
                if ZeroOffset:
                    trace_data = trace_data - (trace.ZeroData*(trace.DataScaler*10**12))
                time = np.linspace(0, trace.DataPoints*trace.XInterval, num=trace.DataPoints, endpoint=False)
                trace_df = pd.DataFrame(trace_data, index=time, columns=[trace.Label.decode().split('\x00')[0]])            
                Sweeps = pd.concat([Sweeps, trace_df], axis=1) # Sweeps beinhaltet am Ende alle Datenpunkte in einem Pandas DataFrame
                    
        return Sweeps 
    

    # This function should be moved to a separate file
    # Maybe, one could make it a "helper" functions bundle or something...    
    def get_IV(self, time, group_index, series_index):
        stim_ID = 0
        VoltageIncMode = 0
        Voltages = []
        
        for i in range(0, group_index):
            stim_ID=stim_ID+self.pulfile.Groups[i].Children
        stim_ID = stim_ID+series_index
       
        stimrec = self.pgffile.StimulationRecords[stim_ID]

        try:
            for j, time_point in enumerate(time):
                t = 0
                for segment in stimrec.ChannelRecords[0].StimSegmentRecords:
                    if time_point < t+segment.Duration and time_point > t:
                        Voltages.append(segment.Voltage+segment.DeltaVFactor*segment.DeltaVIncrement*j)
                        VoltageIncMode = segment.VoltageIncMode
                    t = t +segment.Duration
            if(VoltageIncMode==1):
                return Voltages[::-1]
            if(VoltageIncMode==0):
                return Voltages
        except TypeError:
            t = 0
            for segment in stimrec.ChannelRecords[0].StimSegmentRecords:
                if time < t+segment.Duration and time > t:
                    Voltages.append(segment.Voltage)
                t = t +segment.Duration
            return Voltages
            
        
    def save_Sweeps(self, filename, selected_group, selected_series):
        Sweeps = self.get_Sweeps_byindex(selected_group, selected_series)
        Sweeps.to_csv(filename)
        
    
    
