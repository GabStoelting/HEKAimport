# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 09:06:58 2014

@author: Stölting
"""

import struct
import numpy as np

class PULTrace(object):
    
    def __init__(self, Data_List, children):
        self.Children = children  
        
        self.Mark = Data_List[0]
        self.Label = Data_List[1].decode("UTF-8").rstrip("\x00")
        self.TraceID = Data_List[2]
        self.Data = Data_List[3]
        self.DataPoints = Data_List[4]
        self.InternalSolution = Data_List[5]
        self.AverageCount = Data_List[6]
        self.LeakID = Data_List[7]
        self.LeakTraces = Data_List[8]
        self.DataKind = Data_List[9]
        self.UseXStart = Data_List[10]
        self.TcKind = Data_List[11]
        self.RecordingMode = Data_List[12]
        self.AmplIndex = Data_List[13]
        self.DataFormat = Data_List[14]
        self.DataAbscissa = Data_List[15]
        self.DataScaler = Data_List[16]
        self.TimeOffset = Data_List[17]
        self.ZeroData = Data_List[18]
        self.YUnit = Data_List[19]
        self.XInterval = Data_List[20]
        self.XStart = Data_List[21]
        self.XUnit = Data_List[22]
        self.YRange = Data_List[23]
        self.YOffset = Data_List[24]
        self.Bandwidth = Data_List[25]
        self.PipetteResistance = Data_List[26]
        self.CellPotential = Data_List[27]
        self.SealResistance = Data_List[28]
        self.CSlow = Data_List[29]
        self.GSeries = Data_List[30]
        self.RsValue = Data_List[31]
        self.GLeak = Data_List[32]
        self.MConductance = Data_List[33]
        self.LinkDAChannel = Data_List[34]
        self.ValidYrange = Data_List[35]
        self.AdcMode = Data_List[36]
        self.AdcChannel = Data_List[37]
        self.Ymin = Data_List[38]
        self.Ymax = Data_List[39]
        self.SourceChannel = Data_List[40]
        self.ExternalSolution = Data_List[41]
        self.CM = Data_List[42]
        self.GM = Data_List[43]
        self.Phase = Data_List[44]
        self.DataCRC = Data_List[45]
        self.CRC = Data_List[46]
        self.GS = Data_List[47]
        self.SelfChannel = Data_List[48]
        self.InterleaveSize = Data_List[49]
        self.InterleaveSkip = Data_List[50]
        self.ImageIndex = Data_List[51]
        self.TrMarkers = Data_List[52:54]
        self.SECM_X = Data_List[54]
        self.SECM_Y = Data_List[55]
        self.SECM_Z = Data_List[56]
        self.TrHolding = Data_List[57]
        self.TcEnumerator = Data_List[58]
        self.Filler = Data_List[59]
        
class PULSweep(object):
    
    def __init__(self, Data_List, children):
        self.Children = children
        self.Traces = []        
        
        self.Mark = Data_List[0]
        self.Label = Data_List[1].decode("UTF-8").rstrip("\x00")
        self.AuxDataFileOffset = Data_List[2]
        self.StimCount = Data_List[3]
        self.SweepCount = Data_List[4]
        self.Time = Data_List[5]
        self.Timer = Data_List[6]
        self.SwUserParams = Data_List[7]
        self.Temperature = Data_List[8]
        self.OldIntSol = Data_List[9]
        self.OldExtSol = Data_List[10]
        self.DigitalIn = Data_List[11]
        self.SweepKind = Data_List[12]
        self.DigitalOut = Data_List[13]
        self.Filler1 = Data_List[14]
        self.SwMarkers = Data_List[15]
        self.Filler2 = Data_List[16]
        self.CRC = Data_List[17]
        self.SwHolding = Data_List[18]
    
class PULSeries(object):
    
    def __init__(self, Data_List, children):
        self.Children = children
        self.Sweeps = []        
        
        self.Mark = Data_List[0]
        self.Label = Data_List[1].decode("UTF-8").rstrip("\x00")
        self.Comment = Data_List[2]
        self.SeriesCount = Data_List[3]
        self.NumberSweeps = Data_List[4]
        self.AmplStateOffset = Data_List[5]
        self.AmplStateSeries = Data_List[6]
        self.SeriesType = Data_List[7]
        self.UseXStart = Data_List[8]
        self.Filler1 = Data_List[9]
        self.Filler2 = Data_List[10]
        self.Time = Data_List[11]
        self.PageWidth = Data_List[12]
        self.SwUserParamDescr = Data_List[13]
        self.Filler3 = Data_List[14]
        self.SeUserParams1 = Data_List[15]
        self.LockInParams = Data_List[16]
        self.AmplifierState = Data_List[17]
        self.Username = Data_List[18]        
        self.SeUserParamDescr1 = Data_List[19]        
        self.Filler4 = Data_List[20]
        self.CRC = Data_List[21]       
        self.SeUserParams2 = Data_List[22]
        self.SeUserParamDescr2 = Data_List[23]
        self.ScanParams = Data_List[24]  
            
class PULGroups(object):
    
    def __init__(self, Data_List, children):
        self.Children = children
        self.Series = []
        
        self.Mark = Data_List[0]
        self.Label = Data_List[1].decode("UTF-8").rstrip("\x00")
        self.Text = Data_List[2]
        self.ExperimentNumber = Data_List[3]
        self.GroupCount = Data_List[4]
        self.CRC = Data_List[5]
        self.MatrixWidth = Data_List[6]
        self.MatrixHeight = Data_List[7]



"""

 This class is responsible for handling the bundled ".pul"-file
 
 It has to be initialized with the raw file handle and the starting 
 position of the bundled ".pul"-file
"""
class PULfile(object):
    
    def __init__(self, raw_data, data_pos):
        self.Groups = []

        self.__datapos = data_pos

        self.__datapos = self.read_tree(raw_data, self.__datapos) # Extract the header definitions
        
        self.__datapos, root_data, root_children = self.read_root(raw_data, self.__datapos) # Read the highest tree level

        # Iterate through all available groups
        for group in np.arange(0, root_children):
            # Read group
            self.__datapos, group_data, group_children = self.read_group(raw_data, self.__datapos)
            # Add to list of groups
            self.Groups.append(PULGroups(group_data, group_children))

            
            # Iterate through the series within the current group
            for series in np.arange(0, group_children):
                # Read series
                self.__datapos, series_data, series_children = self.read_series(raw_data, self.__datapos)
                # Add the current series to the list of series
                self.Groups[-1].Series.append(PULSeries(series_data, series_children))
                
                # Iterate through all sweeps
                for sweep in np.arange(0, series_children):
                    # Read current sweep
                    self.__datapos, sweep_data, sweep_children = self.read_sweep(raw_data, self.__datapos)
                    # Add current sweep to list
                    self.Groups[-1].Series[-1].Sweeps.append(PULSweep(sweep_data, sweep_children))
                    
                    # Iterate through all traces 
                    for trace in np.arange(0, sweep_children):
                        # Read current trace
                        self.__datapos, trace_data, trace_children = self.read_trace(raw_data, self.__datapos)
                        # Add current trace to list of traces
                        self.Groups[-1].Series[-1].Sweeps[-1].Traces.append(PULTrace(trace_data, trace_children))
    
    def read_tree(self, data, start_pos):      
        # Start to read tree
        Magic = struct.unpack('4s', data[start_pos:start_pos+4])[0]

        # Check for proper endianess
        if b"eerT" not in Magic:
            print("Sorry but I can't import files with a different endianess yet.")
            quit()
        
        # Extract the sizes of the definitions for the headers of the different
        # hierarchy levels of the tree
        Levels = struct.unpack('i', data[start_pos+4:start_pos+8])[0]
        self.Level_Sizes = []
        for i in np.arange(0, Levels):
            self.Level_Sizes.append(struct.unpack('i', data[start_pos+8+(i*4):start_pos+12+(i*4)])[0])
        return start_pos+12+(i*4) # Return the current position within the file
    
    def read_root(self, data, start_pos):
        # Now read the root, check for size
        if self.Level_Sizes[0] < 640:
            print("Level Size Error Root")
            print("Should be >= 640 but is "+str(self.Level_Sizes[0]))
            quit()
        #returns new position in file, data grouped according to the documentation and the number of children

        return start_pos+self.Level_Sizes[0]+4, struct.unpack('ii32s80s400sdiihhi32h32s', data[start_pos:start_pos+640]), struct.unpack('i', data[start_pos+self.Level_Sizes[0]:start_pos+self.Level_Sizes[0]+4])[0]
        
        
    def read_group(self, data, start_pos):
        # Now continue to the group record, check for size
        if self.Level_Sizes[1] < 144:
            print("Level Size Error Group")
            print("Should be >= 144 but is "+str(self.Level_Sizes[1]))
            quit()
           
        #returns new position in file, data grouped according to the documentation and the number of children
        return start_pos+self.Level_Sizes[1]+4, struct.unpack('i32s80siiidd', data[start_pos:start_pos+144]), struct.unpack('i', data[start_pos+self.Level_Sizes[1]:start_pos+self.Level_Sizes[1]+4])[0]
        
    
    def read_series(self, data, start_pos):
        # Now go on with the series record, check for size
        if self.Level_Sizes[2] < 1408:
            print("Level Size Error Series")
            print("Should be >= 1408 but is "+str(self.Level_Sizes[2]))
            quit()

        #returns new position in file, data grouped according to the documentation and the number of children
        return start_pos+self.Level_Sizes[2]+4, struct.unpack('i32s80siiiic?ccdd40s40s40s40s32c4d96c400s80s40s40s40s40sii4d40s40s40s40s96c', data[start_pos:start_pos+1408]), struct.unpack('i', data[start_pos+self.Level_Sizes[2]:start_pos+self.Level_Sizes[2]+4])[0]
        
        
    def read_sweep(self, data, start_pos):
        # Now go on with the series record, check for size
        if self.Level_Sizes[3] < 288:
            print( "Level Size Error Sweep")
            print( "Should be >= 288 but is "+str(self.Level_Sizes[3]))
            quit()
            
        #returns new position in file, data grouped according to the documentation and the number of children
        return start_pos+self.Level_Sizes[3]+4, struct.unpack('i32siiidd4ddiihhhh4dii16d', data[start_pos:start_pos+288])  , struct.unpack('i', data[start_pos+self.Level_Sizes[3]:start_pos+self.Level_Sizes[3]+4])[0]
            
        
    def read_trace(self, data, start_pos):
        # Now go on with the series record, check for size
        if self.Level_Sizes[4] < 424:
            print( "Level Size Error Trace")
            print( "Should be >= 424 but is "+str(self.Level_Sizes[4]))
            quit()

        #returns new position in file, data grouped according to the documentation (only for 424 used in an older PatchMaster version!) and the number of children
        return start_pos+self.Level_Sizes[4]+4, struct.unpack('i32siiiiiiih?cccccddd8sdd8sdddddddddddi?chddiidddiidiiii10dddddii', data[start_pos:start_pos+424]), struct.unpack('i', data[start_pos+self.Level_Sizes[4]:start_pos+self.Level_Sizes[4]+4])[0]
            