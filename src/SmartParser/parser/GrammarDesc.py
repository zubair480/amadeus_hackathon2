import os

from parser import helper
from parser.MatchField import MatchField
from parser.ValidatorList import ValidatorList


class GrammarDesc:
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules


CPM = GrammarDesc("CPM",
           [MatchField(MatchField.MATCH_FIELD_MANDATORY, "CPM", "Header", terminator=True)])

CARRIER = GrammarDesc("CARRIER",
            [MatchField(MatchField.MATCH_FIELD_MANDATORY, "mm(a)", "AirlineDesignator", validator=ValidatorList(helper.load_file_list(os.path.dirname(__file__)+'/data/airline_codes.txt'))),
               MatchField(MatchField.MATCH_FIELD_MANDATORY, "fff(f)(a)", "FlightNumber", depends_on=["AirlineDesignator"]),
               MatchField(MatchField.MATCH_FIELD_OPTIONAL, "ff", "DepartureDate", precede_separator="/", depends_on=["FlightNumber"] ),
               MatchField(MatchField.MATCH_FIELD_MANDATORY, "mm(m)(m)(m)(m)(m)(m)(m)(m)", "RegistrationNumber", precede_separator=".", depends_on=["DepartureDate", "FlightNumber"], terminator=True),
               MatchField(MatchField.MATCH_FIELD_OPTIONAL, "aaa", "DepartureStation", precede_separator=".", depends_on=["RegistrationNumber"], terminator=True),
               MatchField(MatchField.MATCH_FIELD_OPTIONAL, "m{1,12}", "ULD_configuration", precede_separator=".", depends_on=["RegistrationNumber", "DepartureStation"], terminator=True)
           ])

ULD = GrammarDesc("ULD",
       [MatchField(MatchField.MATCH_FIELD_MANDATORY, "m(m)(m)", "ULDBayDesignation", precede_separator="-", depends_on=["LoadCategory"], new_res=True),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "amm((fffff)mm(a))", "ULDTypeCode", precede_separator="/", depends_on=["ULDBayDesignation"]),
            MatchField(MatchField.MATCH_FIELD_CONDITIONAL, "aaa", "UnloadingStation", precede_separator="/", depends_on=["ULDBayDesignation", "ULDTypeCode"]),
            MatchField(MatchField.MATCH_FIELD_CONDITIONAL, "f(f)(f)(f)(f)", "Weight", precede_separator="/", depends_on=["UnloadingStation", "LoadCategory", "ULDBayDesignation"]),
            MatchField(MatchField.MATCH_FIELD_MANDATORY, "a(a)", "LoadCategory", precede_separator="/", repeated=True, depends_on=["Weight", "ULDTypeCode", "ULDBayDesignation", "LoadCategory"]),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "f", "VolumeCode", depends_on=["LoadCategory"]),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "aaa/mm", "ContourCode",  precede_separator=".", depends_on=["LoadCategory", "VolumeCode"]),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "aaa(/f(f)(f))", "IMP",  precede_separator=".", depends_on=["LoadCategory", "IMP"], repeated=True)
       ])