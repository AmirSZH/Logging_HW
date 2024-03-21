import logging
import datetime
#pip install discordwebhook for this
from discordwebhook import Discord


logging.basicConfig(
    level=logging.INFO,
    filename='basic_logs.log',
    format='%(name)s - %(levelname)s -%(message)s'
)


birthday = datetime.date(1999, 1, 10)
today = datetime.date.today()
days_since_birthday = (today - birthday).days

date_format = f"%(asctime)s ({days_since_birthday} days since my birthday) %(levelname)s: %(message)s"

main_formatter = logging.Formatter(f"%(asctime)s ({days_since_birthday} days since my birthday) %(levelname)s: %(message)s- %(lineno)d")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("log_file.log", mode = 'w')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(main_formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(main_formatter)
logger.addHandler(stream_handler)
class DiscordBotHandler(logging.Handler):
    """Handler to send telegram messages using bot"""
    def __init__(self, webhooks_url):
        super().__init__()
        self.webhooks_url = webhooks_url

    def emit(self, record: logging.LogRecord):
        discord = Discord(url=self.webhooks_url)
        discord.post(content=self.format(record))

class BirthdayFilter(logging.Filter):
    def __init__(self):
        super().__init__()

    def filter(self, record):

        return not ('sample' in record.msg.lower())
root_logger = logging.getLogger()

webhooks_url = "https://discordapp.com/api/webhooks/1220432664431952033/EoZ-CL9_vqawRHEi02oSJKHRqqNucDb-wn1Eoj_2FHsTXuw-BhyBF5CXzNvBouC1C1bB"
discord_console = DiscordBotHandler(webhooks_url)
discord_console.setLevel(logging.DEBUG)
discord_console.setFormatter(main_formatter)
birthday_filter = BirthdayFilter()
discord_console.addFilter(birthday_filter)

root_logger.addHandler(discord_console)


root_logger.info("This is a sample log message.")
root_logger.critical("prod is down")
