from base_config import BaseConfig


class CommandsConfig(BaseConfig):

    @property
    def code(self):
        return self.config.get("commands", {}).get("code").split()

    @property
    def codes_(self):
        return self.config.get("commands", {}).get("codes").split()

    @property
    def codes_all(self):
        return self.config.get("commands", {}).get("codesall")

    @property
    def tasks_all(self):
        return self.config.get("commands", {}).get("tasksall")

    @property
    def task_html(self):
        return self.config.get("commands", {}).get("taskhtml")

    @property
    def approve(self):
        return self.config.get("commands", {}).get("approve")

    @property
    def disapprove(self):
        return self.config.get("commands", {}).get("disapprove")

    @property
    def reset(self):
        return self.config.get("commands", {}).get("reset")

    @property
    def pause(self):
        return self.config.get("commands", {}).get("pause")

    @property
    def resume(self):
        return self.config.get("commands", {}).get("resume")

    @property
    def stop(self):
        return self.config.get("commands", {}).get("stop")

    @property
    def edit(self):
        return self.config.get("commands", {}).get("edit")

    @property
    def status(self):
        return self.config.get("commands", {}).get("status")

    @property
    def task(self):
        return self.config.get("commands", {}).get("task")

    @property
    def codes_history(self):
        return self.config.get("commands", {}).get("codes_history")

    @property
    def hints(self):
        return self.config.get("commands", {}).get("hints")

    @property
    def info(self):
        return self.config.get("commands", {}).get("info")

    @property
    def help(self):
        return self.config.get("commands", {}).get("help")

    @property
    def gap(self):
        return self.config.get("commands", {}).get("gap")

    @property
    def add_admin(self):
        return self.config.get("commands", {}).get("add_admin")

    @property
    def delete_admin(self):
        return self.config.get("commands", {}).get("delete_admin")

    @property
    def add_field(self):
        return self.config.get("commands", {}).get("add_field")

    @property
    def add_kc(self):
        return self.config.get("commands", {}).get("add_kc")

    @property
    def delete_field(self):
        return self.config.get("commands", {}).get("delete_field")

    @property
    def delete_kc(self):
        return self.config.get("commands", {}).get("delete_kc")

    @property
    def edit_admin_pass(self):
        return self.config.get("commands", {}).get("edit_admin_pass")

    @property
    def edit_field_pass(self):
        return self.config.get("commands", {}).get("edit_field_pass")

    @property
    def edit_kc_pass(self):
        return self.config.get("commands", {}).get("edit_kc_pass")

    @property
    def clean_admin(self):
        return self.config.get("commands", {}).get("cleanadmin")

    @property
    def clean_field(self):
        return self.config.get("commands", {}).get("cleanfield")

    @property
    def clean_kc(self):
        return self.config.get("commands", {}).get("cleankc")

    @property
    def clean_errors_(self):
        return self.config.get("commands", {}).get("clean_errors")

    @property
    def clean_unknown(self):
        return self.config.get("commands", {}).get("clean_unknown")

    @property
    def clean_memory(self):
        return self.config.get("commands", {}).get("clean_memory")

    @property
    def alert(self):
        return self.config.get("commands", {}).get("alert")

    @property
    def chat_message(self):
        return self.config.get("commands", {}).get("chat_message")

    @property
    def token(self):
        return self.config.get("commands", {}).get("token")

    @property
    def message(self):
        return self.config.get("commands", {}).get("message")

    @property
    def message_admin(self):
        return self.config.get("commands", {}).get("message_admin")

    @property
    def message_field(self):
        return self.config.get("commands", {}).get("message_field")

    @property
    def message_kc(self):
        return self.config.get("commands", {}).get("message_kc")

    @property
    def send_source(self):
        return self.config.get("commands", {}).get("send_source")

    @property
    def send_errors(self):
        return self.config.get("commands", {}).get("errors")

    @property
    def send_unknown(self):
        return self.config.get("commands", {}).get("unknown")

    @property
    def codes(self):
        return self.config.get("commands", {}).get("codes_limit")

    @property
    def login(self):
        return self.config.get("commands", {}).get("login")

    @property
    def passwords(self):
        return self.config.get("commands", {}).get("pass")

    @property
    def host(self):
        return self.config.get("commands", {}).get("host")

    @property
    def game(self):
        return self.config.get("commands", {}).get("game")

    @property
    def tag_field_(self):
        return self.config.get("commands", {}).get("tag_field")

    @property
    def autohandbrake_(self):
        return self.config.get("commands", {}).get("autohandbrake")

    @property
    def handbrake_set(self):
        return self.config.get("commands", {}).get("handbrake_set")

    @property
    def set_group_chat(self):
        return self.config.get("commands", {}).get("set_group_chat")

    @property
    def codes_statistic(self):
        return self.config.get("commands", {}).get("codes_statistic")

    @property
    def log_activity(self):
        return self.config.get("commands", {}).get("activity")
