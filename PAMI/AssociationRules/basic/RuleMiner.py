from PAMI.AssociationRules.basic import abstract as _ab


class RuleMiner(_ab._AssociationRules):
    """
    temporalDatabaseStats is class to get stats of database.
        Attributes:
        ----------
        frequentPattern : list or dict
            list
        measure: condition to calculate the strength of rule
            str
        threshold: condition to satisfy
            int
        Methods:
        -------
        startMine()
    """

    _iFile = str()
    _measure = str()
    _threshold = float()
    _finalPatterns = {}
    _sep = str()

    '''def __init__(self, iFile, measure, threshold, sep):
        """
        :param iFile: input file name or path
        :type iFile: str
        :param measure: measure used to mine the rules
        :type measure: str
        :param threshold: constraint
        :type threshold: float
        :param sep: seperator of the file
        :type sep: str
        """
        self._iFile = iFile
        self._measure = measure
        self._threshold = threshold
        self._finalPatterns = {}
        self._sep = sep'''

    def _readPatterns(self):
        self._frequentPatterns = {}
        if isinstance(self._iFile, _ab._pd.DataFrame):
            pattern, support = [], []
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'pattern' in i:
                pattern = self._iFile['pattern'].tolist()
            if 'support' in i:
                support = self._iFile['support'].tolist()
            for i in range(len(pattern)):
                s = '\t'.join(pattern[i])
                self._frequentPatterns[s] = support[i]
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line = line.strip()
                    line = line.split(':')
                    s = line[0].split(self._sep)
                    s = ''.join(line[0])
                    self._frequentPatterns[s.strip()] = int(line[1])
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            line = line.split(':')
                            s = line[0].split(self._sep)
                            s = ''.join(line[0])
                            self._frequentPatterns[s.strip()] = int(line[1])
                except IOError:
                    print("File Not Found")
                    quit()

    def _generation(self, prefix, suffix):
        if len(suffix) == 1:
            conf = self._generaeWithConfidence(prefix, suffix[0])
        for i in range(len(suffix)):
            suffix1 = suffix[:i] + suffix[i + 1:]
            prefix1 = prefix + ' ' + suffix[i]
            for j in range(i + 1, len(suffix)):
                conf = self._generaeWithConfidence(prefix + ' ' + suffix[i], suffix[j])
                # self._generation(prefix+ ' ' +suffix[i], suffix[i+1:])
            self._generation(prefix1, suffix1)


    def _generaeWithConfidence(self, lhs, rhs):
        s = lhs + ' ' + rhs
        if self._frequentPatterns.get(s) == None:
            return 0
        minimum = self._frequentPatterns[s]
        conflhs = minimum / self._frequentPatterns[lhs]
        confrhs = minimum / self._frequentPatterns[rhs]
        print(s, conflhs, confrhs)
        if conflhs >= self._threshold:
            s1 = lhs + '->' + rhs
            self._finalPatterns[s1] = conflhs
        if confrhs >= self._threshold:
            s1 = rhs + '->' + lhs
            self._finalPatterns[s1] = confrhs
        return conflhs

    def _generaeWithLift(self, lhs, rhs):
        s = lhs + ' ' + rhs
        if self._frequentPatterns.get(s) == None:
            return 0
        minimum = self._frequentPatterns[s]
        conflhs = minimum / self._frequentPatterns[lhs]
        confrhs = minimum / self._frequentPatterns[rhs]
        liftlhs = conflhs / self._frequentPatterns[rhs]
        rightrhs = confrhs / self._frequentPatterns[lhs]
        if liftlhs >= self._threshold:
            s1 = lhs + '->' + rhs
            self._finalPatterns[s1] = conflhs
        if rightrhs >= self._threshold:
            s1 = rhs + '->' + lhs
            self._finalPatterns[s1] = confrhs
        return conflhs

    def _generaeWithLeverage(self, lhs, rhs):
        s = lhs + ' ' + rhs
        if self._frequentPatterns.get(s) == None:
            return 0
        minimum = self._frequentPatterns[s]
        conflhs = minimum / self._frequentPatterns[lhs]
        confrhs = minimum / self._frequentPatterns[rhs]
        liftlhs = conflhs / self._frequentPatterns[rhs]
        rightrhs = confrhs / self._frequentPatterns[lhs]
        if liftlhs >= self._threshold:
            s1 = lhs + '->' + rhs
            self._finalPatterns[s1] = conflhs
        if rightrhs >= self._threshold:
            s1 = rhs + '->' + lhs
            self._finalPatterns[s1] = confrhs
        return conflhs

    def startMine(self):
        self._startTime = _ab._time.time()
        self._readPatterns()
        print(len(self._frequentPatterns))
        k = [i for i in self._frequentPatterns.keys() if len(i) == 1]
        for i in range(len(k)):
            suffix = k[:i] + k[i + 1:]
            prefix = k[i]
            for j in range(i + 1, len(k)):
                conf = self._generaeWithConfidence(k[i], k[j])
            self._generation(prefix, suffix)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss
        print("Association rules successfully  generated from frequent patterns ")

    def getMemoryUSS(self):
        """Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process

        :rtype: float
        """

        return self._memoryUSS

    def getMemoryRSS(self):
        """Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process

        :rtype: float
        """

        return self._memoryRSS

    def getRuntime(self):
        """Calculating the total amount of runtime taken by the mining process

        :return: returning total amount of runtime taken by the mining process

        :rtype: float
        """

        return self._endTime - self._startTime

    def getPatternsAsDataFrame(self):
        """Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe

        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        # dataFrame = dataFrame.replace(r'\r+|\n+|\t+',' ', regex=True)
        return dataFrame

    def save(self, outFile):
        """Complete set of frequent patterns will be loaded in to a output file

        :param outFile: name of the output file

        :type outFile: file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            s1 = x.strip() + ":" + str(y)
            writer.write("%s \n" % s1)

    def getPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns

        :rtype: dict
        """
        return self._finalPatterns

    def printResults(self):
        print("Total number of Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in ms:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 5 or len(_ab._sys.argv) == 6:
        if len(_ab._sys.argv) == 6:
            _ap = RuleMiner(_ab._sys.argv[1], _ab._sys.argv[3], float(_ab._sys.argv[4]), _ab._sys.argv[5])
        if len(_ab._sys.argv) == 5:
            _ap = RuleMiner(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        _ap.startMine()
        print("Total number of Association Rules:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in ms:", _ap.getRuntime())
    else:
        _ap = RuleMiner('patterns.txt', 'confidence', 0.8, '\t')
        _ap.startMine()
        print("Total number of Association Rules:", len(_ap.getPatterns()))
        _ap.save('output.txt')
        _ap.printResults()
        print("Error! The number of input parameters do not match the total number of parameters provided")