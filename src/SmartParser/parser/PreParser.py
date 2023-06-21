import copy

from Parser import Parser
from RegionMatcher import RegionMatcher, RegionMatch
from parser import helper, GrammarDesc



class PreparseResult():
    def __init__(self, preparsed_lines):
        self.preparsed_lines = preparsed_lines


class PreParser():
    def __init__(self):
        super().__init__()
        self.SI_content = None
        self.header_pos = None
        self.SI_pos = None

        self.unparsable_regions = None
        self.preparsed_lines = []
        self.parser = Parser()

    def findHeader(self):
        for i in range(len(self.lines)):
            if self.lines[i] == "CPM":
                self.header_pos = i

    def findSI(self):
        for i in range(len(self.lines)):
            if "SI" in self.lines[i].split(" ")  :
                self.SI_pos = i

    def find_SI_content(self):
        if self.SI_pos and self.SI_pos > 0:
            self.SI_content = self.lines[self.SI_pos:]




    def preparse_engine(self, lines):
        self.lines = lines

        self.findHeader()
        self.findSI()
        self.find_SI_content()
        if self.header_pos == None:
            return []

        self.to_be_preparsed_lines = self.lines[self.header_pos+1:]

        print(f"header = {self.header_pos}, SI= {self.SI_pos}")
        print("----- SI Content")
        print(self.SI_content)
        self.preparsed_lines = self.preparse()

        self.unparsable_regions = self.identify_unparsable_regions(self.preparsed_lines)
        self.try_to_join_regions()

        SI = []
        if self.SI_content:
            SI = self.SI_content
        return ["CPM"] + self.to_be_preparsed_lines + SI

    def try_to_join_regions(self):
        for region in self.unparsable_regions:
            if len(region) <= 5:
                if region[0] > 0:
                    self.join_region([region[0]-1]+region)
                else:
                    self.join_region(region)

    def join_region(self, region:list):
        self.region_matcher = RegionMatcher()
        self._join_region(region, [])

        best_match = self.region_matcher.find_best_match()

        print("Ok Best match: ",best_match.configuration)

        print("-----")
        for line in self.to_be_preparsed_lines:
            print(line)
        self.fillMatch(best_match)

        print("-----")
        for line in self.to_be_preparsed_lines:
            print(line)


    def fillMatch(self, match:RegionMatch):

        for i in range(len(match.configuration)):
            region = match.configuration[i]
            for j in region:
                self.to_be_preparsed_lines[j]=""
            self.to_be_preparsed_lines[region[0]] = match.matchList[i][0]


    def _join_region(self, avaliable_field, region):

        if len(avaliable_field) == 0:
            matches = []
            for r in region:
                s = ""
                for sr in r:
                    s += self.to_be_preparsed_lines[sr]
                matchRes = self.parse_line_magic(s, [GrammarDesc.CARRIER, GrammarDesc.ULD])

                matches += [(s, matchRes)]
            self.region_matcher.addMatch(RegionMatch(region, matches))

            return

        newregion = copy.deepcopy(region)
        newregion = newregion + [[avaliable_field[0]]]
        self._join_region(avaliable_field[1:], newregion)

        newregion = copy.deepcopy(region)
        if len(region) > 0:
            newregion[-1] += [avaliable_field[0]]
            self._join_region(avaliable_field[1:], newregion)

    def identify_unparsable_regions(self, preparsed_lines)->list:
        res = []

        buf = []
        for i in range(len(preparsed_lines)):
            if preparsed_lines[i] == None:
                if len(buf) == 0:
                    buf += [i]
                else:
                    if buf[-1] == i-1:
                        buf += [i]
                    else:
                        res += [buf]
                        buf = [i]
        if len(buf) > 0:
            res += [buf]

        return res

    def parse_line_magic(self, line, grammars):
        res = []

        for grammar in grammars:
            res += [self.parser.parse_line(line, grammar)]

        return res


    def preparse(self):
        '''
        Identify not parsable lines
        :param lines:
        :return:
        '''
        print("preparse")

        i = 0
        header = None
        carrier = None
        ulds = []
        preparsed_lines = []

        while i < len(self.to_be_preparsed_lines):
            line = self.to_be_preparsed_lines[i]

            tmp_carrier = None
            tmp_uld = None
            result = None

            tmp_carrier = self.parser.parse_line(line, GrammarDesc.CARRIER)
            if tmp_carrier:
                carrier = tmp_carrier
                result = carrier
                print("carrier found!")

            tmp_uld = self.parser.parse_line(line, GrammarDesc.ULD)
            if tmp_uld:
                result = tmp_uld
                ulds += [tmp_uld]
                #print("uld found", line)

            if result:
                preparsed_lines += [result]
            else:
                print("Invalid line", line)
                preparsed_lines += [None]
            i += 1

        print(preparsed_lines)
        #self.join(lines, parsing_result)
        return preparsed_lines


