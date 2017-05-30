from config.bot_settings import BotSettingsConfig
from config.commands import CommandsConfig
from config.errors import ErrorsLog
from config.game_settings import GameSettingsConfig
from config.timeouts import TimeoutsConfig
from config.unknown_log import UnknownLog

bot_settings = BotSettingsConfig("yaml\\bot_settings.yaml")
commands = CommandsConfig("yaml\\commands.yaml")
errors_log = ErrorsLog("yaml\\errors_log.yaml")
game_settings = GameSettingsConfig("yaml\\game_settings.yaml")
timeouts = TimeoutsConfig("yaml\\timeouts.yaml")
unknown_log = UnknownLog("yaml\\unknown_log.yaml")
