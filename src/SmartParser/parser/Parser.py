
from parser import helper, GrammarDesc
from parser.Corrector import Corrector

from parser.Rule import Rule


class Parser:

    def __init__(self):
        self.lines = []

        self.header = None
        self.res_carrier = None
        self.res_uld = []
        self.si = []

        self.preparsed_lines = []


    def parse_text(self, text):
        self.lines = text.split("\n")
        self.remove_empty_lines()
        from PreParser import PreParser
        preparser = PreParser()
        self.lines = preparser.preparse_engine(self.lines)


        self.parse_header()
        self.parse_carrier()

        while len(self.lines) > 0:
            res = self.parse_uld()
            if not res:
                break

        res = {"Header": self.header, "Carrier": self.res_carrier, "ULDs": self.res_uld}
        if preparser.SI_content:
            res["SI"] = preparser.SI_content


        return res

    def parse_file(self, filename):
        text = helper.load_file_simple(filename)
        return self.parse_text(text)


    def remove_empty_lines(self):
        res = []
        for line in self.lines:
            tmp = line.strip()
            if len(tmp) > 0:
                res += [line.strip()]

        self.lines = res

    def show(self, text, result):
        pass
        #print(f"{text} --> {result}")


    def parse_header(self):
        line = self.pop()
        if not line:
            return None

        result = self.parse_line(line, GrammarDesc.CPM)

        self.show(line, result)
        self.header = result
        return result

    def pop(self):
        if len(self.lines) > 0:
            return self.lines.pop(0)
        else:
            return None

    def parse_line(self, line, grammar):
        rule = Rule(grammar)
        result = rule.match2(line)
        if not result:
            corrector = Corrector()
            fixedValue = corrector.fix(line, grammar)
            if fixedValue:
                result = rule.match2(fixedValue)

        return result

    def parse_uld(self):
        line = self.pop()
        if not line:
            return None

        result = self.parse_line(line, GrammarDesc.ULD)
        if result:
            self.res_uld += [result]
        self.show(line, result)
        return result


    def parse_carrier(self):

        line = self.pop()
        if not line:
            return None
        result = self.parse_line(line, GrammarDesc.CARRIER)
        if result:
            self.res_carrier = result
        self.show(line, result)

        return result




