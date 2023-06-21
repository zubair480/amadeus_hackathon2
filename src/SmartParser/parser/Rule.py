import os
import re

from GrammarDesc import GrammarDesc
from parser import helper
from parser.Grammar import Grammar
from parser.MatchField import MatchField
from parser.Validator import Validator
from parser.ValidatorList import ValidatorList


class Rule:

    def __init__(self, grammarDesc:GrammarDesc):
        self.grammarDesc = grammarDesc
        self.full_text = None
        self.current_text = None
        self.result = {}
        self.final_result = []
        self.counter = 0

    def consume(self, followers):
        pass
        for follower in followers:

            separator = follower.precede_separator
            if separator == ".":
                separator = "\."

            search_expression = f"^{separator}{follower.expression}"
            m = re.search(search_expression, self.current_text)

            # print(self.current_text)
            # print("", follower.field_name)
            # print(f"{separator}{follower.expression}")
            #print(m)

            if not m and follower.type == MatchField.MATCH_FIELD_MANDATORY and follower.field_name not in self.result:
                return None

            if m:
                self.counter += 1
                if follower.new_res:
                    if len(self.result) > 0:
                        self.final_result += [self.result]
                        self.result = {}

                self.current_text = self.current_text[len(m.group(0)):]
                value = m.group()[len(follower.precede_separator):]

                if follower.validator:
                    validate_result = follower.validator.validate(value)

                    '''
                    if validate_result["CODE"] == Validator.CODE_REJECT:
                        print(f"{value} has been rejected!")

                    if validate_result["CODE"] == Validator.CODE_REPLACE:
                        print(f"{value} has been replaced with {validate_result['NEW_VALUE']}!")
                        value = validate_result['NEW_VALUE']
                    '''

                if follower.repeated:
                    if follower.field_name not in self.result:
                        self.result[follower.field_name] = []
                    self.result[follower.field_name] += [value]
                else:
                    if follower.field_name in self.result:
                        self.result[follower.field_name + "_" +str(self.counter)] = value
                    else:
                        self.result[follower.field_name] = value

                return follower
        return None

    def match2(self, text):
        self.full_text = text
        self.current_text = text

        self.result = {}

        g = Grammar(self.grammarDesc)
        g.buildSyntaxTree()

        node = self.grammarDesc.rules[0]
        node = self.consume([node])
        while node != None:
            #print("--- ", node.field_name)
            node = self.consume(node.gr_followers)

        if len(self.current_text) > 0:
            #print("NOT PARSED", self.current_text, self.result)
            return None

        if len(self.final_result) > 0:
            return self.final_result + [self.result]
        else:
            return self.result



    def match(self, text):
        temp = text
        res = {}

        fieldIndex = 0
        while fieldIndex < len(self.grammarDesc):
            field = self.grammarDesc[fieldIndex]

            m = re.search(f"^{field.precede_separator}{field.expression}", temp)

            # couldn't match but the field is mandatory
            if not m and field.type == MatchField.MATCH_FIELD_MANDATORY and field.field_name not in res:
                return None

            if field.repeated and not m:
                fieldIndex += 1

            # could match
            if m:

                temp = temp[len(m.group(0)):]
                value = m.group()[len(field.precede_separator):]
                '''
                if field.validator:
                    validate_result = field.validator.validate(value)

                    if validate_result["CODE"] == Validator.CODE_REJECT:
                        print(f"{value} has been rejected!")

                    if validate_result["CODE"] == Validator.CODE_REPLACE:
                        print(f"{value} has been replaced with {validate_result['NEW_VALUE']}!")
                        value = validate_result['NEW_VALUE']
                '''

                if field.repeated:
                    if field.field_name not in res:
                        res[field.field_name] = []
                    res[field.field_name] += [value]
                else:
                    res[field.field_name] = value

            if not field.repeated:
                fieldIndex += 1

        if res == {}:
            return None

        return res