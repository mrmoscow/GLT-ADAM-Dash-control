#*******************************************************************************
# ALMA - Atacama Large Millimiter Array
# (c) Associated Universities Inc., 2011
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
#

version = "0.4"

from math import floor, log, sqrt, fabs
from numpy import mean, std
from sys import stdout
import pylab
import os.path
from os import listdir

class stabilityData:
    """Utility class which reads data from one or more text files,
    interprets the data as either amplitude or phase time-series,
    and produces Allan variance (amp) or Allan deviation (phase) plots.
    """
    verbose = True
    debug = False

    freqRFGHz = 0.0     # RF frequency to use for converting degrees to fs.
    dataIsLog = False   # If true, amplitudes will be converted to linear units before computing Allan variance.

    stopOnDiscontinuity = False
    discoThresh = 0.0   # Threshold above which jumps are considered a discontinuity and data reading should stop.

    def __init__(self, filename, tau0, delim = '\t', dataCol = 0, startRow = 0, stopRow = 0):
        """Initialize a stabilityData object:
        filename: the text file to read from disk
        tau0: the sampling interval of the file, typically in seconds
        delim: what delimiter character to use when splitting columns
        dataCol: zero-indexed column of data to extract
        startRow: zero-indexed row where actual data starts
        stopRow: zero-indexed row which is after the end of data to be read.  0 means read all data.
        """

        self.filename = filename
        self.tau0 = tau0 if tau0 > 0 else 1.0e-6    # minimum is one microsecond
        self.delim = delim
        self.dataCol = dataCol if dataCol >= 0 else 0
        self.startRow = startRow if startRow >= 0 else 0
        self.stopRow = stopRow if stopRow >= 0 else 0
        if self.debug:
            print("stabilityData:", self.initText())
        if len(self.filename) > 0:
            self.readDataArray()

    def initText(self):
        """Returns a string consisting of the parameters setup by the constructor.
        """
        delimT = self.delim if self.delim != '\t' else '\\t'
        return "filename=%s tau0=%f delim='%s' datacol=%d startRow=%d stopRow=%d" % (self.filename, self.tau0, delimT, self.dataCol, self.startRow, self.stopRow)

    def readDataArray(self):
        """Reads amplitude or phase stabilty data from the specified text file.
        Optionally stops if a big jump larger than self.discoThresh is encountered.
        """
        # reset data and result arrays:
        self.dataArray = []
        self.result = [[],[]]

        # read all lines in the file:
        try:
            f = open(self.filename, 'r')
            lines = f.readlines()
            f.close()
        except:
            print("Exception reading file 1:", self.filename)
            return False

        # iterate and parse each line:
        maxLine = len(lines)
        if self.stopRow > 0 and maxLine > self.stopRow:
            maxLine = self.stopRow
        if self.debug:
            print("readDataArray:", self.initText(), "maxLine=%d" % (maxLine))

        lastData = 0.0;     # last valid value seen
        validData = False;  # true if a valid value has been seen
        dataExceptions = 0; # count the number of data conversion exceptions to print at the end.

        lineNum = 0;
        while lineNum < maxLine:
            line = lines[lineNum]
            if lineNum >= self.startRow:
                # split the line using the specified delimiter:
                tokens = line.split(self.delim)
                # remove empty strings from the list to guard against repeated delims:
                tokens = [t for t in tokens if t != '']
                try:
                    # strip any other whitespace which might be attached and convert to float:
                    val = float(tokens[self.dataCol].strip())
                except:
                    # either the index was out of range or the item couldn't be converted to float.
                    dataExceptions += 1
                else:
                    # check for big discontinuities and quit the loop early if found:
                    if self.stopOnDiscontinuity and validData and fabs(val - lastData) > self.discoThresh:
                        print("Discontinuity at line:", lineNum, "stopping.")
                        lineNum = maxLine
                    # otherwise append the data and save the last value:
                    else:
                        self.dataArray.append(val)
                        lastData = val
                        validData = True
            lineNum += 1
        if dataExceptions > 0:
            print("got", dataExceptions, "exceptions while reading", self.filename)
        if self.verbose:
            print("read", len(self.dataArray), "points from", self.filename)

        #print(self.dataArray)
        basename, ext = os.path.splitext(self.filename)
        i = basename.upper().find("RF")
        try:
            self.freqRFGHz = float(basename[i+2:i+5])
        except:
            try:
                self.freqRFGHz = float(basename[i+2:i+4])
            except:
                self.freqRFGHz = 0.0
        if self.freqRFGHz > 0.0:
            print("freqRFGHz=", self.freqRFGHz)

    def write(self, filename = '', delim = '\t'):
        """Writes the resulting Allan variance or deviation result to a text file.
        The output filename may be provided or it will be generated automatically from the source filename.
        """
        if filename == '':
            filename = os.path.splitext(self.filename)[0]
            filename += "-AV.txt"
        output = open(filename, 'w')
        L = len(self.result[0])
        #print(self.result[0])
        for i in range(L):
            output.write(str(self.result[0][i]))
            output.write(delim)
            output.write(str(self.result[1][i]))
            output.write("\n")
        output.close()
        if self.verbose:
            print("wrote" , L, "points to", filename)

    def logToLinear(self):
        """Converts the data array from dBm to mW.
        """
        for i in range(len(self.dataArray)):
            self.dataArray[i] = 10 ** (self.dataArray[i] / 10)

    def plot(self):
        """Displays a simple plot of the resulting curve of Allan variance or devaition vs. time.
        """
        pylab.plot(self.result[0], self.result[1], '-')
        ax = pylab.gca()
        ax.set_xscale('log')
        ax.set_yscale('log')
        pylab.xlabel("T (sec)")
        pylab.ylabel(self.yAxisLabel)
        pylab.xlim(1,1000)
        pylab.ylim(0.1, 100)
        pylab.grid()
        pylab.draw()
        pylab.show()

    def plotAmpSpecs(self):
        pylab.plot((0.05, 100), (5.0e-7, 5.0e-7), 'k-', lw = 3)
        pylab.plot((300, 300), (4.0e-6, 4.0e-6), 'ks')

    def plotPhaseSpecsFs(self):
        if self.freqRFGHz > 0.0:
            pylab.plot((20, 300), (10, 10), 'k-', lw = 3)
        else:
            print("plotPhaseSpecsFs: Cannot plot fs spec line where Y-axis is in degrees.")
#
    def computeAllanVar(self, TMin = 0.05, TMax = 300.0, fastMode = False):
        """computes normalized Allan variance for a range of integration times.
        params:
            self.dataArray: time series array of input data
            fastMode: if True uses fewer integration times between TMin and TMax to speed computation
            TMin, TMax: starting and ending integration time
        returns:
            self.result: a pair of arrays having the integration times and Allan vars.
        """
        self.yAxisLabel = "Allan variance (sigma^2(T))"

        if (self.dataIsLog):
            self.logToLinear()

        # check parameters:
        N = len(self.dataArray)
        dataDuration = N * self.tau0

        if (dataDuration < 10 * TMax):
            print("computeAllanVar warning: dataArray size is < 10 x Tmax.")

        if (dataDuration < TMax):
            TMax = dataDuration
            print("computeAllanVar: adjusted TMax =", TMax)

        if TMin < self.tau0:
            print("computeAllanVar: adjusted TMin = tau0 =", self.tau0)
            TMin = self.tau0

        self.result = [[], []]

        if (fastMode):
            # calculate the values of K to use in fast mode:
            maxJ = int(floor(log(float(N - 1) / 3.0) / log(2.0)))
            for j in range(0, maxJ + 1):
                K = 2 ** j
                T = K * self.tau0
                if (T <= TMax):
                    self.result[0].append(K * self.tau0)
                    AVar = self.AVar(self.getAveragesArray(K))
                    self.result[1].append(AVar)
                    if self.verbose:
                        stdout.write('.')
            if self.verbose:
                stdout.write('\n')
        else:
            # calculate the values of K to use in normal mode:
            maxK = int(TMax / self.tau0) + 1
            minM = N / maxK
            if (minM < 2):
                # at least two groups are required
                minM = 2
                maxK = N / minM
            for K in range(1, maxK):
                self.result[0].append(K * self.tau0)
                AVar = self.AVar(self.getAveragesArray(K))
                self.result[1].append(AVar)
                if self.verbose:
                    if (K % 100 == 0):
                        stdout.write('.')
            if self.verbose:
                stdout.write('.\n')

    def compute2PtAllanDev(self, TMin = 1.0, TMax = 300.0):
        """Computes the 2-point Allan standard deviation with a fixed averaging time,
        tau0 and intervals T between TMin and TMax seconds.
        If tau0 < TMin, the data will first be averaged into intervals of approximately TMin.
        Equation from ALMA-80.04.00.00-005-B-SPE:
        sigma^2(2,T,tau) = 0.5 * < [phi.tau(t + T) - phi.tau(t)] ^ 2 >  where
        phi.tau = the average of the absolute or differential phase over time tau = 10 seconds.
        < ... > means the average over the data sample which should extend to 10 or 20 x Tmax seconds.
        """
        #print("In compute2Pt-1 ")
        self.yAxisLabel = "Allan deviation (sigma(2, t=10s, T)"
        if (self.freqRFGHz > 0.0):
            self.yAxisLabel += " (fs))"
        else:
            self.yAxisLabel += " (deg))"

        # before processing, make sure that the phase data doesn't wrap around:
        self.unwrapPhase()
        #print("In compute2Pt- after unwrap")
        #print("In tau",self.tau0,TMin,TMax)
        # TMin must be at least the minimum averaging time, tau0:
        if TMin < self.tau0:
            print("computeAllanVar: adjusted TMin = tau0 =", self.tau0)
            TMin = self.tau0

        # compute number of whole tau0 intervals in TMin:
        NMin = int(TMin / self.tau0)
        print("In compute2Pt- after NMin",NMin)
        # compute new TMin rounded down to whole tau0 intervals:
        newTMin = self.tau0 * float(NMin)
        print("In compute2Pt- after nweTmin",newTMin,"Ole TMin" ,TMin,"self.tau",)
        if (newTMin < TMin):
            print("computeAllanVar: adjusted TMin =", NMin, "*", self.tau0, "=", newTMin)
            TMin = newTMin

        # If more than one sample fits in the new TMin
        if (NMin > 1.0):
            # integrate TMin worth of samples:
            #print("check if we are here, The K NMin is",NMin)
            self.getAveragesArray(NMin)
            NMin = 1.0
        #    print("check if we are here 2",NMin)
        else:
            # otherwise use the original array:
            self.averagesArray = self.dataArray
        #self.averagesArray = self.dataArray
        print("In compute2Pt- after averageArray",NMin,'len of dataArray',len(self.dataArray),len(self.averagesArray))
        # check TMax parameter in light of above adjustments:
        dataDuration = len(self.averagesArray) * TMin
        print("the dataDuration",dataDuration,TMax)
        # TMax can be no longer than the data set:
        if (TMax > dataDuration):
            TMax = dataDuration
        TMax=dataDuration/10.0
        print("compute2PtAllanDev: adjusted TMax =", TMax)

        # warn on insufficient data to keep errors reasonable:
        if (dataDuration < 10 * TMax):
            print("compute2PtAllanDev warning: data duration is < 10 * TMax.")

        self.result = [[], []]

        NMax = int(TMax / TMin)

        print("compute2PtAllanDev: TMin=", TMin, "TMax=", TMax, "NMin=", NMin, "NMax=", NMax)
        if self.debug:
            print("compute2PtAllanDev: TMin=", TMin, "TMax=", TMax, "NMin=", NMin, "NMax=", NMax)
        #iterate over the values for increasing group sizes, K:
        print("Just test")
        for K in range(int(NMin), int(NMax) + 1):
            # calculate T for this iteration and save to the output time array:
            self.result[0].append(K * TMin)
            # calculate ADev for this iteration and save to the output Allan array:a
            ADev = self.ADev(self.averagesArray, K)
            self.result[1].append(ADev)
            #print("Test","K",K,ADev,ADev)
            if self.verbose:
                stdout.write('.')
        if self.verbose:
            stdout.write('\n')


    def unwrapPhase(self):
        numPts = 0
        for i in range(len(self.dataArray) - 1):
            diffPhase=self.dataArray[i+1]-self.dataArray[i]
            if (diffPhase > 180):
                self.dataArray[i] -= 360
                numPts += 1
            elif (diffPhase < -180):
                self.dataArray[i] += 360
                numPts += 1
        if (self.verbose and numPts > 0):
            print("Unwrapped phase for", numPts, "points.")

    def AVar(self, inputArray):
        """Returns the overlapping Allan variance from an inputArray
        AVar = 1/(2*(N-1)*mean^2) * sum (inputArray(i) - inputArray(i+1))^2
        """
        # get the mean, for normalization:
        x0 = mean(inputArray)
        M = len(inputArray)
        # take the sum of the squares of differences and normalize:
        return sum(self.diffSquared(inputArray)) / (float(2 * (M - 1)) * x0 * x0)

    def ADev(self, inputArray, K):
        """Returns the 2-point Allan standard deviation of an inputArray
        ADev = sqrt(0.5 * < [phi.tau(t + T) - phi.tau(t)] ^ 2 >) where
        phi.tau = the average of the absolute or differential phase over time tau.
        < ... > means the average over the data sample
        If freqRFGHz>0 compute differences converted to fs at the given frequency.
        """
        if (self.freqRFGHz > 0.0):
            period = 1.0 / (float(self.freqRFGHz) * 1.0e9)
            fsDeg = (period * 1.0e15) / 360.0

        M = len(inputArray)
        sum = 0
        for aIndex in range(M - K):
            # accumulate a sum of squares of differences...
            diff = inputArray[aIndex] - inputArray[aIndex + K]
            # optionally converted to fs:
            if (self.freqRFGHz > 0.0):
                diff *= fsDeg
            sum += diff ** 2.0

        # and divide by the number of differences, multiply by 0.5, take the square root for standard deviation:
        numDiffs = float(M - K - 1)
        adev = sqrt(0.5 * sum / numDiffs)
        errorBar = adev / sqrt(numDiffs)
        if self.debug:
            print("ADev: M=", M, "numDiffs=", numDiffs, "ADev=", adev, "errorBar=", errorBar)
        return adev

    def diffSquared(self, inputArray):
        """Takes inputArray and returns an array consisting of the differences
        between adjacent elements, squared.
        """
        dX = []
        for i in range(len(inputArray) - 1):
            dX.append((inputArray[i+1] - inputArray[i]) ** 2)
        return dX

    def getAveragesArray(self, K):
        """returns self.averagesArray from self.DataArray, where each element of averagesArray
        contains the mean over non-overlapping groups of K samples of the original data.
        """
        self.averagesArray = []
        # N is the size of the input data array:
        N = len(self.dataArray)
        # K is the number of points to group and average:
        if (K < 1):
            if self.verbose:
                print("getAveragesArray warning: K < 1")
            K = 1
        if (K > N):
            K = N
            if self.verbose:
                print("getAveragesArray warning: K > N")
        # M is number of groups:
        M = N / K
        for i in range(int(M)):
            i0 = i * K
            self.averagesArray.append(sum(self.dataArray[i0 : i0 + K]) / float(K))
        if self.debug:
            print("getAveragesArray N=", N, "K=", K, "M=", M, "result=", len(self.averagesArray), "points")
        print("getAveragesArray N=", N, "K=", K, "M=", M, "result=", len(self.averagesArray), "points")
        return self.averagesArray

def onePhase(filename, tau0 = 0.5, delim = ' ', dataCol = 0, startRow = 0, stopRow = 0, discoThresh = 0.0, TMin = 1.0, plot = False):
    """Reads the specified file, computes Allan deviation for tau0 <= T <= 300s, and writes out a results file.
    filename: the text file to read from disk
    tau0: the sampling interval of the file, typically in seconds
    delim: what delimiter character to use when splitting columns
    dataCol: zero-indexed column of data to extract
    startRow: zero-indexed row where actual data starts
    stopRow: zero-indexed row which is after the end of data to be read.  0 means read all data.
    discoThresh: stops reading input if a discontinuity larger than this value is seen.  0.0 means don't stop.
    """
    try:
        S = stabilityData('', tau0, delim, dataCol, startRow, stopRow)
        if (discoThresh > 0.0):
            S.stopOnDiscontinuity = True
            S.discoThresh = discoThresh
        S.filename = filename
        S.readDataArray()
        S.compute2PtAllanDev(TMin)
    except:
        print("Exception reading file: 2", filename)
    try:
        basename, ext = os.path.splitext(filename)
        outfile = basename + "-AV" + ".txt"
        S.write(outfile)
    except:
        print("Exception writing output file:", outfile)
    if plot:
        S.plot()
        S.plotPhaseSpecsFs()
    return S

def bulkPhase(fileExt = '.txt', tau0 = 0.5, delim = ' ', dataCol = 0, startRow = 0, stopRow = 0, discoThresh = 0.0, TMin = 1.0, plot = False):
    """Computes Allan deviation and writes a results file corresponding to every
    file in the current directory having the specified extension.
    """
    files = listdir(".")
    for filename in files:
        basename, ext = os.path.splitext(filename)
        if (ext == fileExt and basename.find("-AV") and basename.find("AllanVar") < 0):
          if (basename.find("Phase") == 0 ):
            print(filename,tau0,dataCol,startRow,stopRow,TMin)
            S = onePhase(filename, tau0, delim, dataCol, startRow, stopRow, discoThresh, TMin)
            if plot:
                S.plot()
    if plot:
        S.plotPhaseSpecsFs()

def oneAmp(filename, tau0 = 0.05, delim = '\t', dataCol = 0, startRow = 0, stopRow = 0, discoThresh = 0.0, dataIsLog = False, plot = False):
    """Reads the specified file, computes Allan variance for tau0 <= T <= 300s, and writes out a results file.
    filename: the text file to read from disk
    tau0: the sampling interval of the file, typically in seconds
    delim: what delimiter character to use when splitting columns
    dataCol: zero-indexed column of data to extract
    startRow: zero-indexed row where actual data starts
    stopRow: zero-indexed row which is after the end of data to be read.  0 means read all data.
    discoThresh: stops reading input if a discontinuity larger than this value is seen.  0.0 means don't stop.
    """
    try:
        S = stabilityData('', tau0, delim, dataCol, startRow, stopRow)
        if (discoThresh > 0.0):
            S.stopOnDiscontinuity = True
            S.discoThresh = discoThresh
        S.filename = filename
        S.dataIsLog = dataIsLog
        S.readDataArray()
        S.computeAllanVar()
    except:
        print("Exception reading file:", filename)
    try:
        basename, ext = os.path.splitext(filename)
        outfile = basename + "-AV" + ".txt"
        S.write(outfile)
    except:
        print("Exception writing output file:", outfile)
    if plot:
        S.plot()
        S.plotAmpSpecs()
    return S

def bulkAmp(fileExt = '.txt', tau0 = 0.05, delim = '\t', dataCol = 0, startRow = 0, stopRow = 0, discoThresh = 0.0, dataIsLog = False, plot = False):
    """Computes Allan variance and writes a results file corresponding to every
    file in the current directory having the specified extension.
    Skips files with '-AV' in their filename.
    """
    files = listdir(".")
    for filename in files:
        basename, ext = os.path.splitext(filename)
        if (ext == fileExt and basename.find("-AV") < 0):
            S = oneAmp(filename, tau0, delim, dataCol, startRow, stopRow, discoThresh, dataIsLog)
            if plot:
                S.plot()
    if plot:
        S.plotAmpSpecs()

