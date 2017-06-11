from base_config import BaseConfig


class CodesLog(BaseConfig):

    @property
    def codes_raw(self):
        return self.config.get("codes", {})

    def codes(self, level_id):
        return self.codes_raw.get(level_id, {})

    def get_username(self, code, level_id):
        for username, codes in self.codes(level_id).iteritems():
            if username != "__all__" and code in codes:
                return username

    @codes_raw.setter
    def codes_raw(self, value):
        self.config["codes"] = value
        self.save_config()

    def log_code(self, code, level_id, username):
        codes = self.codes_raw
        if code.lower() not in codes.get(level_id, {}).get('__all__', []):
            codes.setdefault(level_id, {}).setdefault(username, []).append(code.lower())
            codes.setdefault(level_id, {}).setdefault('__all__', []).append(code.lower())
            self.codes_raw = codes
            return
        return self.get_username(code, level_id)

    def clean_codes(self):
        self.codes_raw = {}

    def repr_codes_by_level(self, level_id):
        codes_entered = self.codes(level_id)
        all_codes = ""
        for username, user_codes in codes_entered.iteritems():
            if username != "__all__":
                codes_template = u"<b>{username}</b>: {codes}\r\n"
                user_codes_formatted = ' '.join(user_codes)
                all_codes += codes_template.format(username=username,
                                                   codes=user_codes_formatted)
        return all_codes

    def repr_codes_all(self):
        all_codes = ""
        for level, codes in self.codes_raw.iteritems():
            all_codes += "---------\r\n{level}:\r\n---------\r\n\r\n".format(level=level)
            for username, user_codes in codes.iteritems():
                if username != "__all__":
                    codes_template = u"{username}: {codes}\r\n"
                    user_codes_formatted = ' '.join(user_codes)
                    all_codes += codes_template.format(username=username,
                                                       codes=user_codes_formatted)
        return all_codes
