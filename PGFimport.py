# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 09:06:58 2014

@author: Stölting
"""

import struct
import numpy as np

class PGFStimulationRecord(object):
    
    def __init__(self, Data_List, children):
        self.Children = children  
        self.ChannelRecords = []
        
        self.Mark = Data_List[0]
        self.EntryName = Data_List[1]
        self.FileName = Data_List[2]
        self.AnalName = Data_List[3]
        self.DataStartSegment = Data_List[4]
        self.DataStartTime = Data_List[5]
        self.SampleInterval = Data_List[6]
        self.SweepInterval = Data_List[7]
        self.LeakDelay = Data_List[8]
        self.FilterFactor = Data_List[9]
        self.NumberSweeps = Data_List[10]
        self.NumberLeaks = Data_List[11]
        self.NumberAverages = Data_List[12]
        self.ActualAdcChannels = Data_List[13]
        self.ActualDacChannels = Data_List[14]
        self.ExtTrigger = Data_List[15]
        self.NoStartWait = Data_List[16]
        self.UseScanRates = Data_List[17]
        self.NoContAq = Data_List[18]
        self.HasLockIn = Data_List[19]
        self.OldStartMacKind = Data_List[20]
        self.OldEndMacKind = Data_List[21]
        self.AutoRange = Data_List[22]
        self.BreakNext = Data_List[23]
        self.IsExpanded = Data_List[24]
        self.LeakCompMode = Data_List[25]
        self.HasChirp = Data_List[26]
        self.OldStartMacro = Data_List[27]
        self.OldEndMacro = Data_List[28]
        self.IsGapFree = Data_List[29]
        self.HandledExternally = Data_List[30]
        self.Filler1 = Data_List[31]
        self.Filler2 = Data_List[32]
        self.CRC = Data_List[33]

        
class PGFChannelRecord(object):
    
    def __init__(self, Data_List, children):
        self.Children = children
        self.StimSegmentRecords = []        
        
        self.Mark = Data_List[0]
        self.LinkedChannel = Data_List[1]
        self.CompressionFactor = Data_List[2]
        self.YUnit = Data_List[3]
        self.AdcChannel = Data_List[4]
        self.AdcMode= Data_List[5]
        self.DoWrite = Data_List[6]
        self.LeakStore = Data_List[7]
        self.AmplMode = Data_List[8]
        self.OwnSegTime = Data_List[9]
        self.SetLastSegVmemb = Data_List[10]
        self.DacChannel = Data_List[11]
        self.DacMode = Data_List[12]
        self.HasLockInSquare = Data_List[13]
        self.RelevantXSegment = Data_List[14]
        self.RelevantYSegment = Data_List[15]
        self.DacUnit = Data_List[16]
        self.Holding = Data_List[17]
        self.LeakHolding = Data_List[18]
        self.LeakSize = Data_List[19]
        self.LeakHoldMode = Data_List[20]
        self.LeakAlternate = Data_List[21]
        self.AltLeakAveraging = Data_List[22]
        self.LeakPulseOn = Data_List[23]
        self.StimToDacID = Data_List[24]
        self.CompressionMode = Data_List[25]
        self.CompressionSkip = Data_List[26]
        self.DacBit = Data_List[27]
        self.HasLockInSine = Data_List[28]
        self.BreakMode = Data_List[29]
        self.ZeroSeg = Data_List[30]
        self.Filler1 = Data_List[31]
        self.Sine_Cycle = Data_List[32]
        self.Sine_Amplitude = Data_List[33]
        self.LockIn_VReversal = Data_List[34]
        self.Chirp_StartFreq = Data_List[35]
        self.Chirp_EndFreq = Data_List[36]
        self.Chirp_MinPoints = Data_List[37]
        self.Square_NegAmpl = Data_List[38]
        self.Square_DurFactor = Data_List[39]
        self.LockIn_Skip= Data_List[40]
        self.Photo_MaxCycles = Data_List[41]
        self.Photo_SegmentNo = Data_List[42]
        self.LockIn_AvgCycles = Data_List[43]
        self.Imaging_RoiNo = Data_List[44]
        self.Chirp_Skip = Data_List[45]
        self.Chirp_Amplitude = Data_List[46]
        self.Photo_Adapt = Data_List[47]
        self.Sine_Kind = Data_List[48]
        self.Chirp_PreChirp = Data_List[49]
        self.Sine_Source = Data_List[50]
        self.Square_NegSource = Data_List[51]
        self.Square_PosSource = Data_List[52]
        self.Chirp_Kind = Data_List[53]
        self.Chirp_Source = Data_List[54]
        self.DacOffset = Data_List[55]
        self.AdcOffset = Data_List[56]
        self.TraceMathFormat = Data_List[57]
        self.HasChirp = Data_List[58]
        self.Square_Kind = Data_List[59]
        self.Filler2 = Data_List[60]
        self.Square_Cycle = Data_List[61]
        self.Square_PosAmpl = Data_List[62]
        self.CompressionOffset = Data_List[63]
        self.PhotoMode = Data_List[64]
        self.BreakLevel = Data_List[65]
        self.TraceMath = Data_List[66]
        self.OldCRC = Data_List[67]
        self.Filler3 = Data_List[68]
        self.CRC = Data_List[69]
    
class PGFStimSegmentRecord(object):
    
    def __init__(self, Data_List, children):
        self.Children = children
        
        self.Mark = Data_List[0]
        self.Class = Data_List[1]
        self.DoStore = Data_List[2]
        self.VoltageIncMode = Data_List[3]
        self.DurationIncMode = Data_List[4]
        self.Voltage = Data_List[5]
        self.VoltageSource = Data_List[6]
        self.DeltaVFactor = Data_List[7]
        self.DeltaVIncrement = Data_List[8]
        self.Duration = Data_List[9]
        self.DurationSource = Data_List[10]
        self.DeltaTFactor = Data_List[11]
        self.DeltaTIncrement = Data_List[12]
        self.Filler1 = Data_List[13]
        self.CRC = Data_List[14]
        self.ScanRate = Data_List[15]
            
class PGFfile(object):
    
    def __init__(self, raw_data, data_pos):
        self.StimulationRecords = []

        self.__datapos = data_pos
        
        self.__datapos = self.read_tree(raw_data, self.__datapos)
        self.__datapos, root_data, root_children = self.read_root(raw_data, self.__datapos)
        
        for stimrec in np.arange(0, root_children):
            self.__datapos, stimrec_data, stimrec_children = self.read_stimulationrecord(raw_data, self.__datapos)
            self.StimulationRecords.append(PGFStimulationRecord(stimrec_data, stimrec_children))
            
            for channelrec in np.arange(0, stimrec_children):
                self.__datapos, channelrec_data, channelrec_children = self.read_channelrecord(raw_data, self.__datapos)
                self.StimulationRecords[-1].ChannelRecords.append(PGFChannelRecord(channelrec_data, channelrec_children))
                
                for stimsegrec in np.arange(0, channelrec_children):
                    self.__datapos, stimsegrec_data, stimsegrec_children = self.read_stimsegmentrecord(raw_data, self.__datapos)
                    self.StimulationRecords[-1].ChannelRecords[-1].StimSegmentRecords.append(PGFStimSegmentRecord(stimsegrec_data, stimsegrec_children))
                    
        
    
    def read_tree(self, data, start_pos):      
        # Start to read tree
        Magic = struct.unpack('4s', data[start_pos:start_pos+4])[0]
        # Check for proper endianess
        if b"eerT" not in Magic:
            print( "Sorry but I can't import files with a different endianess yet.")
            quit()
            
        Levels = struct.unpack('i', data[start_pos+4:start_pos+8])[0]
        self.Level_Sizes = []
        for i in np.arange(0, Levels):
            self.Level_Sizes.append(struct.unpack('i', data[start_pos+8+(i*4):start_pos+12+(i*4)])[0])
        return start_pos+12+(i*4)
    
    def read_root(self, data, start_pos):
        # Now read the root, check for size
        if self.Level_Sizes[0] < 584:
            print( "Level Size Error PGF Root")
            print( "Should be >= 584 but is "+str(self.Level_Sizes[0]))
            quit()
        #returns new position in file, data grouped according to the documentation and the number of children

        return start_pos+self.Level_Sizes[0]+4, struct.unpack('ii32sii10d320s32iii', data[start_pos:start_pos+584]), struct.unpack('i', data[start_pos+self.Level_Sizes[0]:start_pos+self.Level_Sizes[0]+4])[0]
        
        
    def read_stimulationrecord(self, data, start_pos):
        # Now continue to the group record, check for size
        if self.Level_Sizes[1] < 248:
            print( "Level Size Error Group")
            print( "Should be >= 248 but is "+str(self.Level_Sizes[1]))
            quit()
           
        #returns new position in file, data grouped according to the documentation and the number of children
        return start_pos+self.Level_Sizes[1]+4, struct.unpack('i32s32s32sidddddiiiiic????c?c????32s32s????i', data[start_pos:start_pos+248]), struct.unpack('i', data[start_pos+self.Level_Sizes[1]:start_pos+self.Level_Sizes[1]+4])[0]
        
    
    def read_channelrecord(self, data, start_pos):
        # Now go on with the series record, check for size
        if self.Level_Sizes[2] < 400:
            print( "Level Size Error Series")
            print( "Should be >= 400 but is "+str(self.Level_Sizes[2]))
            quit()

        #returns new position in file, data grouped according to the documentation and the number of children
        return start_pos+self.Level_Sizes[2]+4, struct.unpack('iii8shc?cc??hccii8sdddc???hhih?ciiddddddddiiiiiidccccccccddc?c13cddiid124siii', data[start_pos:start_pos+400]), struct.unpack('i', data[start_pos+self.Level_Sizes[2]:start_pos+self.Level_Sizes[2]+4])[0]
        
        
    def read_stimsegmentrecord(self, data, start_pos):
        # Now go on with the series record, check for size
        if self.Level_Sizes[3] < 80:
            print( "Level Size Error Sweep")
            print( "Should be >= 80 but is "+str(self.Level_Sizes[3]))
            quit()
         
        #returns new position in file, data grouped according to the documentation and the number of children
        return start_pos+self.Level_Sizes[3]+4, struct.unpack('=ibbbbdidddiddiid', data[start_pos:start_pos+80])  , struct.unpack('i', data[start_pos+self.Level_Sizes[3]:start_pos+self.Level_Sizes[3]+4])[0]
            
        
             