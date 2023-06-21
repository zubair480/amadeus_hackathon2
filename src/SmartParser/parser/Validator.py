class Validator:

    CODE_ACCEPT = "ACCEPT"
    CODE_REJECT = "REJECT"
    CODE_REJECT = "SUGGEST"
    CODE_REPLACE = "REPLACE"

    def __init__(self):
        pass

    def validate(self, value):
        return {"CODE": "CODE_REJECT"}