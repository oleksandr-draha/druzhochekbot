from uuid import uuid4

from telegram.driver import TelegramDriver


class CodesQueue():
    # {1: {"nickname": "nick",
    # "codes": ["code1", "codes2"],
    # "message": MessageObject} }
    pending = {}
    # {1: {"nickname": "nick",
    # "codes": ["code1
    # "results": ["result1", "result2"],
    # "message": MessageObject}}
    processed = {}

    @staticmethod
    def add_code_bunch(message, split=False):
        command = TelegramDriver.extract_command(message)
        username = message["username"]
        codes = message["text"].replace(command, '').rstrip().lstrip()
        if split:
            codes = codes.split()
            codes = [code.lower() for code in codes]
            codes = list(set(codes))
        else:
            codes = [codes]
        uuid = str(uuid4())
        CodesQueue.pending.setdefault(uuid,
                                      {"username": username,
                                       "codes": codes,
                                       "message": message})

    @staticmethod
    def get_next_code():
        if len(CodesQueue.pending):
            keys = CodesQueue.pending.keys()
            bunch_id = keys[0]
            next_bunch = CodesQueue.pending.pop(bunch_id)
            if len(next_bunch["codes"]):
                next_code = next_bunch["codes"].pop(0)
                CodesQueue.pending.setdefault(bunch_id, next_bunch)
                CodesQueue.processed.setdefault(bunch_id, next_bunch)
                CodesQueue.processed[bunch_id].setdefault("results", [])
                username = next_bunch["message"]["username"]
                if len(next_bunch["codes"]) == 0:
                    finished = True
                else:
                    finished = False
                return bunch_id, next_code, username, finished

    @staticmethod
    def add_code_result(bunch_id, result):
        CodesQueue.processed[bunch_id]["results"].append(result)
