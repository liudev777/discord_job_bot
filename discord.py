import lightbulb
import os
import dotenv

dotenv.load_dotenv()
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
bot = lightbulb.BotApp(token=DISCORD_TOKEN)