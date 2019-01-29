from pprint import pformat
from uuid import uuid4

from datetime import datetime

from config.dictionary import CommandMessages
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
    def add_code_bunch(message, split=True):
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
                                       "message": message,
                                       "added": datetime.now(),
                                       "original_length": len(codes)})

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
                return bunch_id, next_code, username, finished, next_bunch

    @staticmethod
    def add_code_result(bunch_id, result):
        CodesQueue.processed[bunch_id]["results"].append(result)

    @staticmethod
    def finalize_bunch(bunch_id):
        if bunch_id in CodesQueue.pending:
            CodesQueue.pending.pop(bunch_id)

    @staticmethod
    def reset():
        CodesQueue.processed = {}
        CodesQueue.pending = {}

    @staticmethod
    def soft_reset():
        for bunch_id in CodesQueue.pending:
            codes_left = CodesQueue.pending[bunch_id]["codes"]
            if len(codes_left):
                CodesQueue.pending[bunch_id]["codes"] = [codes_left[-1]]

    @staticmethod
    def codes_queue_repr():
        result = {}
        for bunch_id, codes in CodesQueue.pending.iteritems():
            result.setdefault(codes.get("username"), {}).update({bunch_id: codes.get("codes")})
        return pformat(result)

    @staticmethod
    def codes_queue_statistic_repr():
        result = ""
        for bunch_id, codes in CodesQueue.pending.iteritems():
            time_spent = datetime.now() - codes.get("added")
            result += CommandMessages.CODE_STATISTICS.format(
                nickname=codes.get("username"),
                codes_length=codes.get("original_length") - len(codes.get("codes")),
                total_length=codes.get("original_length"),
                time_spent=time_spent.seconds)
        return result
