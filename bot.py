import lightbulb
import hikari
import os
import dotenv
import miru

# load plugins from the extensions folder
dotenv.load_dotenv()
bot = lightbulb.BotApp(token=os.environ['DISCORD_TOKEN'])
bot.load_extensions("extensions.leetcode")
miru.install(bot)
bot.load_extensions("extensions.roles")
bot.load_extensions("extensions.jobs")


@bot.listen(hikari.StartingEvent)
async def on_started(event: hikari.StartingEvent) -> None:
    print("Bot is now ready.")


@bot.listen(hikari.StartedEvent)
async def started(event: hikari.StartedEvent) -> None:
    # await post_jobs()
    pass


# Runs the bot
def run() -> None:
    bot.run()

__all__ = ["run", "post_jobs"]

if __name__ == "__main__":
    run()