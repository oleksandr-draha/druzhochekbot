from datetime import datetime

from base_config import BaseConfig


class ErrorsLog(BaseConfig):

    @property
    def errors_raw(self):
        return self.config.get("errors", [])

    @errors_raw.setter
    def errors_raw(self, value):
        self.config["errors"] = value
        self.save_config()

    def log_error(self, error):
        errors = self.errors_raw
        if len(errors) >= 100:
            errors.pop(0)
        errors.append([datetime.now(), error])
        self.errors_raw = errors

    def clean_errors(self):
        self.errors_raw = []

    def repr_errors(self):
        errors = ""
        for date_error, error in self.errors_raw:
            errors += str(date_error) + '\r\n' + error.replace('\n', '\r\n') + '\r\n'
        return errors
