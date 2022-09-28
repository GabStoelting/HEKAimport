# -*- coding: utf-8 -*-
"""
Created on Mon Aug 04 13:55:38 2014

@author: Stölting
"""
import struct
import re
import numpy as np
import pandas as pd

class HEKAfile(dict):
    
    def __init__(self, *args, **kwargs):
        super(HEKAfile, self).__init__(*args, **kwargs)

    def load_patchmaster(self, filename):
        if filename == "":
            return
        else:
            self.filename = filename

        try:
            patchmaster_file = open(self.filename, 'rb')
        except:
            raise NameError("Sorry, but " + self.filename + " couldn't be opened.")

        self.patchmaster_data = patchmaster_file.read()

        # Check for "DAT2" signature in the beginning of the file
        if "DAT2" not in str(struct.unpack("8s", self.patchmaster_data[0:8])[0]):
            raise NameError(
                "Sorry, but " + self.filename + " does not appear to be a properly bundled HEKA Patchmaster file.")
            return

        number_of_items = struct.unpack('i', self.patchmaster_data[48:52])[0]

        self.start_dict = {}
        self.stop_dict = {}

        # Read the positions of the bundled data files
        for i in np.arange(0, number_of_items):
            data_type = b"".join(struct.unpack("4c", self.patchmaster_data[72 + (i * 16):76 + (i * 16)]))
            self.start_dict[data_type] = int(struct.unpack("i", self.patchmaster_data[64 + (i * 16):68 + (i * 16)])[0])
            self.stop_dict[data_type] = int(struct.unpack("i", self.patchmaster_data[68 + (i * 16):72 + (i * 16)])[0])

        self.pulfile = PULfile(self.patchmaster_data, int(self.start_dict[b".pul"]))

        self.pgffile = PGFfile(self.patchmaster_data, int(self.start_dict[b".pgf"]))

        for group in self.pulfile.Groups:
            self[group.Label] = group
       
    def get_Sweeps_byindex(self, group_index, series_index, ZeroOffset=False):
        
        Sweeps = pd.DataFrame()
        
        for sweep in self.pulfile.Groups[group_index].Series[series_index].Sweeps:
            for trace in sweep.Traces:   
                trace_data = DATload(self.patchmaster_data, trace.Data, trace.DataPoints, trace.DataFormat, (trace.DataScaler * 10 ** 12), False)
                if ZeroOffset:
                    trace_data = trace_data - (trace.ZeroData*10**12) # Diese fixe Multiplikation mit 10**12 ist doof wenn ich V-Mon Daten zeigen will (Die brauchen ja nicht auf nV umgestellt werden...)
                time = np.linspace(0, trace.DataPoints*trace.XInterval, num=trace.DataPoints, endpoint=False)
                trace_df = pd.DataFrame(trace_data, index=time, columns=[trace.Label.decode().split('\x00')[0]])            
                Sweeps = pd.concat([Sweeps, trace_df], axis=1) # Sweeps beinhaltet am Ende alle Datenpunkte in einem Pandas DataFrame
                    
        return Sweeps
        
    def get_Sweeps(self, series, ZeroOffset=False):
        
        Sweeps = pd.DataFrame()
        
        for sweep in self.Series[series].Sweeps:
            for trace in sweep.Traces:
                trace_data = DATload(self.patchmaster_data, trace.Data, trace.DataPoints, trace.DataFormat, (trace.DataScaler * 10 ** 12), False)
                if ZeroOffset:
                    trace_data = trace_data - (trace.ZeroData*(trace.DataScaler*10**12))
                time = np.linspace(0, trace.DataPoints*trace.XInterval, num=trace.DataPoints, endpoint=False)
                trace_df = pd.DataFrame(trace_data, index=time, columns=[trace.Label])            
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
        time = np.full((self.pulfile.Groups[group_index].Series[series_index].Children, 1), time)
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
                print(segment.Voltage)
                if time < t+segment.Duration and time > t:
                    Voltages.append(segment.Voltage)
                t = t +segment.Duration
            return Voltages
            
        
    def save_Sweeps(self, filename, selected_group, selected_series):
        Sweeps = self.get_Sweeps_byindex(selected_group, selected_series)
        Sweeps.to_csv(filename)


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
        self.AdcMode = Data_List[5]
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
        self.LockIn_Skip = Data_List[40]
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

        # These are the definitions for the binary format of the individual tree levels
        self.root_struct = 'ii32sii10d320s32iii'
        self.stimulation_struct = 'i32s32s32sidddddiiiiic????c?c????32s32s????i'
        self.channel_struct = 'iii8shc?cc??hccii8sdddc???hhih?ciiddddddddiiiiiidccccccccddc?c13cddiid124siii'
        self.stimseg_struct = '=ibbbbdidddiddiid'

        self.StimulationRecords = []

        self.__datapos = data_pos

        self.__datapos = self.read_tree(raw_data, self.__datapos)
        self.__datapos, root_data, root_children = read_level(raw_data, self.__datapos, self.Level_Sizes[0],
                                                                 self.root_struct)

        for stimrec in np.arange(0, root_children):
            self.__datapos, stimrec_data, stimrec_children = read_level(raw_data, self.__datapos,
                                                                           self.Level_Sizes[1], self.stimulation_struct)
            self.StimulationRecords.append(PGFStimulationRecord(stimrec_data, stimrec_children))

            for channelrec in np.arange(0, stimrec_children):
                self.__datapos, channelrec_data, channelrec_children = read_level(raw_data, self.__datapos,
                                                                                     self.Level_Sizes[2],
                                                                                     self.channel_struct)
                self.StimulationRecords[-1].ChannelRecords.append(
                    PGFChannelRecord(channelrec_data, channelrec_children))

                for stimsegrec in np.arange(0, channelrec_children):
                    self.__datapos, stimsegrec_data, stimsegrec_children = read_level(raw_data, self.__datapos,
                                                                                         self.Level_Sizes[3],
                                                                                         self.stimseg_struct)
                    self.StimulationRecords[-1].ChannelRecords[-1].StimSegmentRecords.append(
                        PGFStimSegmentRecord(stimsegrec_data, stimsegrec_children))

    def read_tree(self, data, start_pos):
        # Start to read tree
        Magic = struct.unpack('4s', data[start_pos:start_pos + 4])[0]
        # Check for proper endianess
        if b"eerT" not in Magic:
            print("Sorry but I can't import files with a different endianess yet.")
            quit()

        Levels = struct.unpack('i', data[start_pos + 4:start_pos + 8])[0]
        self.Level_Sizes = []
        for i in np.arange(0, Levels):
            self.Level_Sizes.append(struct.unpack('i', data[start_pos + 8 + (i * 4):start_pos + 12 + (i * 4)])[0])
        return start_pos + 12 + (i * 4)


class PULTrace(object):

    def __init__(self, Data_List, children, raw_data):
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

        # trace_data should contain the actual data of the trace
        # TODO: determine what to do with the DataScaler
        self.trace_data = DATload(raw_data, self.Data, self.DataPoints, self.DataFormat, self.DataScaler,
                                            False)


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

    def get_df(self):
        return_df = pd.DataFrame([])

        for sweep in self.Sweeps:
            for i, trace in enumerate(sweep.Traces):
                temporary_trace_df = pd.DataFrame({trace.Label: trace.trace_data})
                index = np.arange(0, len(trace.trace_data) * trace.XInterval, trace.XInterval)
                temporary_trace_df.index = index
                return_df = pd.concat([return_df, temporary_trace_df], axis=1)
        return return_df


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


class PULfile(object):

    def __init__(self, raw_data, data_pos):

        # These are the definitions for the binary format of the individual tree levels
        self.root_struct = "ii32s80s400sdiihhi32h32s"
        self.group_struct = "i32s80siiidd"
        self.series_struct = "i32s80siiiic?ccdd40s40s40s40s32c4d96c400s80s40s40s40s40sii4d40s40s40s40s96c"
        self.sweep_struct = "i32siiidd4ddiihhhh4dii16d"
        self.trace_struct = "i32siiiiiiih?cccccddd8sdd8sdddddddddddi?chddiidddiidiiii10dddddii"

        self.Groups = []

        self.__datapos = data_pos

        self.__datapos = self.read_tree(raw_data, self.__datapos)  # Extract the header definitions

        # self.__datapos, root_data, root_children = self.read_root(raw_data, self.__datapos) # Read the highest tree level
        self.__datapos, root_data, root_children = read_level(raw_data, self.__datapos, self.Level_Sizes[0],
                                                                 self.root_struct)  # Read the highest tree level

        # Iterate through all available groups
        for group in np.arange(0, root_children):
            # Read group
            self.__datapos, group_data, group_children = read_level(raw_data, self.__datapos, self.Level_Sizes[1],
                                                                       self.group_struct)
            # Add to list of groups
            self.Groups.append(PULGroups(group_data, group_children))

            # Iterate through the series within the current group
            for series in np.arange(0, group_children):
                # Read series
                self.__datapos, series_data, series_children = read_level(raw_data, self.__datapos,
                                                                             self.Level_Sizes[2], self.series_struct)
                # Add the current series to the list of series
                self.Groups[-1].Series.append(PULSeries(series_data, series_children))

                # Iterate through all sweeps
                for sweep in np.arange(0, series_children):
                    # Read current sweep
                    self.__datapos, sweep_data, sweep_children = read_level(raw_data, self.__datapos,
                                                                               self.Level_Sizes[3], self.sweep_struct)
                    # Add current sweep to list
                    self.Groups[-1].Series[-1].Sweeps.append(PULSweep(sweep_data, sweep_children))

                    # Iterate through all traces
                    for trace in np.arange(0, sweep_children):
                        # Read current trace
                        self.__datapos, trace_data, trace_children = read_level(raw_data, self.__datapos,
                                                                                   self.Level_Sizes[4],
                                                                                   self.trace_struct)
                        # Add current trace to list of traces
                        self.Groups[-1].Series[-1].Sweeps[-1].Traces.append(
                            PULTrace(trace_data, trace_children, raw_data))

    def read_tree(self, data, start_pos):
        # Start to read tree
        Magic = struct.unpack('4s', data[start_pos:start_pos + 4])[0]

        # Check for proper endianess
        if b"eerT" not in Magic:
            print("Sorry but I can't import files with a different endianess yet.")
            quit()

        # Extract the sizes of the definitions for the headers of the different
        # hierarchy levels of the tree
        Levels = struct.unpack('i', data[start_pos + 4:start_pos + 8])[0]
        self.Level_Sizes = []
        for i in np.arange(0, Levels):
            self.Level_Sizes.append(struct.unpack('i', data[start_pos + 8 + (i * 4):start_pos + 12 + (i * 4)])[0])
        return start_pos + 12 + (i * 4)  # Return the current position within the file


def DATload(raw_data, data_pos, sample_count, sample_type, scaling_factor, leak):
    output = np.empty(sample_count)
    sample = 0
    if sample_type == b"\x00":  # If data is stored as int16 proceed as follows
        sample_size = 2
        for i in np.arange(data_pos, data_pos + (sample_size * sample_count), sample_size):
            output[sample] = int(struct.unpack('h', raw_data[i:i + sample_size])[0]) * scaling_factor
            sample += 1
        if leak == True:
            print("Leak!")
            sample = 0
            for i in np.arange(data_pos + (sample_size * sample_count), data_pos + (2 * sample_size * sample_count),
                               sample_size):
                output[sample] += int(struct.unpack('h', raw_data[i:i + sample_size])[0]) * scaling_factor
                sample += 1
        return output

    if sample_type == b"\x01":  # If data is stored as int32 proceed as follows
        sample_size = 4
        for i in np.arange(data_pos, data_pos + (sample_size * sample_count), sample_size):
            output[sample] = int(struct.unpack('i', raw_data[i:i + sample_size])[0]) * scaling_factor
            sample += 1
        if leak == True:
            print("Leak!")
            sample = 0
            for i in np.arange(data_pos + (sample_size * sample_count), data_pos + (2 * sample_size * sample_count),
                               sample_size):
                output[sample] += int(struct.unpack('i', raw_data[i:i + sample_size])[0]) * scaling_factor
                sample += 1
        return output

    if sample_type == b"\x02":  # If data is stored as float32 proceed as follows
        sample_size = 4
        print("float32")
        for i in np.arange(data_pos, data_pos + (sample_size * sample_count), sample_size):
            output[sample] = float(struct.unpack('f', raw_data[i:i + sample_size])[0]) * scaling_factor
            sample += 1
        if leak == True:
            print("Leak!")
            sample = 0
            for i in np.arange(data_pos + (sample_size * sample_count), data_pos + (2 * sample_size * sample_count),
                               sample_size):
                output[sample] += float(struct.unpack('f', raw_data[i:i + sample_size])[0]) * scaling_factor
                sample += 1
        return output

    if sample_type == b"\x03":  # If data is stored as float64 proceed as follows
        sample_size = 8
        for i in np.arange(data_pos, data_pos + (sample_size * sample_count), sample_size):
            output[sample] = float(struct.unpack('d', raw_data[i:i + sample_size])[0]) * scaling_factor
            sample += 1
        if leak == True:
            print("Leak!")
            sample = 0
            for i in np.arange(data_pos + (sample_size * sample_count), data_pos + (2 * sample_size * sample_count),
                               sample_size):
                output[sample] += float(struct.unpack('d', raw_data[i:i + sample_size])[0]) * scaling_factor
                sample += 1
        return output


def get_struct(struct_list, size):
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
    rString = struct_list[0]
    i = 1

    while ((struct.calcsize(rString) < size) & (i < len(struct_list))):
        rString = rString + struct_list[i]
        i += 1

    return rString


def read_level(data, start_pos, level_size, struct_string):
    """
     read_level allows to read one level of the HEKA tree headers

     Inputs:
                 data: Raw data
                 start_pos: Current position in file
                 level_size: Size of the current level header description
                 struct_string: Header struct format string
    """
    # I need to check if this regex really works for all struct format strings...
    struct_list = re.findall(r"[=]*[0-9]*[a-z,?]", struct_string)

    # returns new position in file, data grouped according to the documentation and the number of children
    sString = get_struct(struct_list, level_size)
    actSize = struct.calcsize(sString)

    return start_pos + level_size + 4, struct.unpack(sString, data[start_pos:start_pos + actSize]), \
           struct.unpack('i', data[start_pos + level_size:start_pos + level_size + 4])[0]
