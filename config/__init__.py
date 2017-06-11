from os import path

from config.bot_settings import BotSettingsConfig
from config.codes import CodesLog
from config.commands import CommandsConfig
from config.errors import ErrorsLog
from config.game_settings import GameSettingsConfig
from config.last_activity import ActivityLog
from config.tasks import TasksLog
from config.timeouts import TimeoutsConfig
from config.unknown_log import UnknownLog

bot_settings = BotSettingsConfig(path.join("yaml", "bot_settings.yaml"))
commands = CommandsConfig(path.join("yaml", "commands.yaml"))
errors_log = ErrorsLog(path.join("yaml", "errors_log.yaml"))
game_settings = GameSettingsConfig(path.join("yaml", "game_settings.yaml"))
timeouts = TimeoutsConfig(path.join("yaml", "timeouts.yaml"))
unknown_log = UnknownLog(path.join("yaml", "unknown_log.yaml"))
codes_log = CodesLog(path.join("yaml", "codes.yaml"))
tasks_log = TasksLog(path.join("yaml", "tasks.yaml"))
activity_log = ActivityLog(path.join("yaml", "activity.yaml"))
