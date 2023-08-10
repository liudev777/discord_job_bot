import lightbulb
import hikari
import os
import dotenv
import miru
from database import User, Database
from hikari import Embed


# load plugins from the extensions folder
dotenv.load_dotenv()
bot = lightbulb.BotApp(token=os.environ['DISCORD_TOKEN'], intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT | hikari.Intents.GUILD_MEMBERS)

bot.load_extensions("extensions.leetcode")
miru.install(bot)
bot.load_extensions("extensions.roles")
# bot.load_extensions("extensions.role2")
bot.load_extensions("extensions.jobs")
bot.load_extensions("extensions.channel")
bot.load_extensions("extensions.create_role")


@bot.listen(hikari.StartingEvent)
async def on_started(event: hikari.StartingEvent) -> None:
    print("Bot is now ready.")


@bot.listen(hikari.StartedEvent)
async def started(event: hikari.StartedEvent) -> None:
    # await post_jobs()
    pass

@bot.command
@lightbulb.command("help", "displays commands")
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    description = (
        f"- /leet: displays leetcode questions\n- /p: displays user job parameters\n\n- /set help: displays a list of setter commands to configure job search parameters"

    )
    embed = Embed(
        title="Commands",
        description=description
    )

    await ctx.respond(embed=embed)

# @bot.listen()
# async def member_update(event: hikari.MemberUpdateEvent):
#     print("member updated")
#     before_roles = set(event.old_member.role_ids)
#     after_roles = set(event.member.role_ids)

#     added_roles = after_roles - before_roles
#     removed_roles = before_roles - after_roles
#     user_db = User(Database())

#     for role_id in added_roles:
#         if not await user_db.role_is_in_db(str(role_id)):
#             print('skip')
#             continue
#         await user_db.insert_role(str(event.member.id), str(role_id), str(event.guild_id))
    
#     for role_id in removed_roles:
#         if not await user_db.user_has_role(str(role_id)):
#             continue
#         await user_db.delete_role(str(event.member.id), str(role_id), str(event.guild_id))

# Runs the bot
def run() -> None:
    bot.run()

__all__ = ["run", "post_jobs"]

if __name__ == "__main__":
    run()