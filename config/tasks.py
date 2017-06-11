from base_config import BaseConfig


class TasksLog(BaseConfig):

    @property
    def tasks_raw(self):
        return self.config.get("tasks", {})

    def task(self, level_id):
        return self.tasks_raw.get(level_id)

    @tasks_raw.setter
    def tasks_raw(self, value):
        self.config["tasks"] = value
        self.save_config()

    def log_task(self, level_id, task):
        tasks = self.tasks_raw
        tasks.update({level_id: task})
        self.tasks_raw = tasks

    def clean_tasks(self):
        self.tasks_raw = {}
