from Keyboard import Keyboard


def long_match_unit(str1, str2):
    combs = []
    for i in range(len(str1)):
        combs.append(str1[:i] + str1[i + 1:])
    for co in combs:
        if co == str2:
            return True
    return False


def short_match_unit(str1, str2):
    i = 0
    j = 0
    missing = 0
    while i < len(str1):
        if str1[i] == str2[j]:
            i += 1
            j += 1
        else:
            j += 1
            missing += 1
        if missing > 1:
            return False
    if len(str2) - j > 1:
        return False
    return missing == 0 or j == len(str2)


class Matcher:
    MATCH = 0
    SWAP_MATCH = 1
    SHORT_MATCH = 2
    LONG_MATCH = 3
    NO_MATCH = -1

    def __init__(self, kb, data_list, fixed_length):
        self.keyboard = kb
        self.data_list = data_list
        self.fixed_length = fixed_length
        self.std_key_diff = Keyboard.key_distance(self.keyboard, 'T', 'J')

    def direct_diff(self, str1, str2):
        if str1 == "" and str2 == "":
            return 0
        if str1 == "":
            return self.std_key_diff * len(str2)
        if str2 == "":
            return self.std_key_diff * len(str1)
        return self.keyboard.key_distance(str1[0], str2[0]) + self.direct_diff(str1[1:], str2[1:])

    def equal_match_unit(self, str1, str2):
        swaps = []
        if len(str1) == 2:
            swaps.append(str1[1] + str1[0])
        else:
            for i in range(len(str1) - 1):
                swaps.append(str1[:i] + str1[i + 1] + str1[i] + str1[i + 2:])
        for sw in swaps:
            if sw == str2:
                return self.std_key_diff
        return self.direct_diff(str1, str2)

    def all_diff(self, input_str):
        distance_list = []

        if self.fixed_length:
            match len(input_str) - len(self.data_list[0]):
                case 0:
                    if len(input_str) > 1:
                        for data in self.data_list:
                            distance_list.append(self.equal_match_unit(input_str, data))
                    else:
                        for data in self.data_list:
                            distance_list.append(self.keyboard.key_distance(input_str, data))
                case 1:
                    if len(input_str) > 2:
                        for data in self.data_list:
                            if long_match_unit(input_str, data):
                                distance_list.append(self.std_key_diff)
                            else:
                                distance_list.append(self.NO_MATCH)
                case -1:
                    if len(input_str) > 1:
                        for data in self.data_list:
                            if short_match_unit(input_str, data):
                                distance_list.append(self.std_key_diff)
                            else:
                                distance_list.append(self.NO_MATCH)
            return distance_list

        elif len(input_str) == 1:
            for data in self.data_list:
                if len(data) == 1:
                    distance_list.append(self.keyboard.key_distance(input_str, data))
                else:
                    distance_list.append(self.NO_MATCH)

        elif len(input_str) == 2:
            for data in self.data_list:
                match len(input_str) - len(data):
                    case 0:
                        distance_list.append(self.equal_match_unit(input_str, data))
                    case -1:
                        if short_match_unit(input_str, data):
                            distance_list.append(self.std_key_diff)
                    case _:
                        distance_list.append(self.NO_MATCH)
        else:
            for data in self.data_list:
                match len(input_str) - len(data):
                    case 0:
                        distance_list.append(self.equal_match_unit(input_str, data))
                    case -1:
                        if short_match_unit(input_str, data):
                            distance_list.append(self.std_key_diff)
                    case 1:
                        if long_match_unit(input_str, data):
                            distance_list.append(self.std_key_diff)
                    case _:
                        distance_list.append(self.NO_MATCH)
        return distance_list



mt = Matcher(Keyboard(1, 2), ["QWE", "ABCF", "JFL"], True)
print(mt.all_diff("JFK"))
