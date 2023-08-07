import json
import hikari
import lightbulb
from hikari import Embed, Color
from jsearch import Jsearch

"""
Job related bot commands
"""

jobs_plugin = lightbulb.Plugin("jobs", "post job listings")

# Sends a list of jobs to the discord channel
async def embed_job(job_data) -> Embed:
    print(job_data.get("employer_name"))
    responsibilities = "\n".join("- " + r for r in job_data.get("job_responsibilities")) if job_data.get("job_responsibilities") else "N/A"
    qualifications = "\n".join("- " + r for r in job_data.get("job_qualifications")) if job_data.get("job_qualifications") else "N/A"

    description = (
        f'Job Title: {job_data.get("job_title", "N/A")}\n\n'
        f'Employment type: {job_data.get("job_employment_type", "N/A")}\n\n'
        f'Description: {job_data.get("job_description", "N/A")[:500]}...\n\n'
        f'Qualifications:\n {qualifications}\n\n'
        f'Responsibilities:\n {responsibilities}\n\n'
        f'{job_data.get("job_city")} {job_data.get("job_state")}\n\n'
    )

    embed = Embed(
        title = job_data.get("employer_name", "N/A"),
        description = description,
        url = job_data.get("job_apply_link", "N/A"),
    )
    embed.set_thumbnail(job_data.get("employer_logo"))
    return embed


async def post_jobs() -> None:
    channel_id = 1129920047444402376
    unique_role_combination = await fetch_unique_roles()
    for role_combinations in unique_role_combination:
        if not role_combinations:
            continue
        print([role for role in role_combinations])
        job_search_string = "Software Developer " + " ".join([role for role in role_combinations])
        print(job_search_string, "\n")
        for job_data in Jsearch(job_search_string).get_job():
            await jobs_plugin.bot.rest.create_message(channel_id, embed= await embed_job(job_data))


@jobs_plugin.command
@lightbulb.option("query", "thing you wanna search for idk")
@lightbulb.command("response", "grabs the response url")
@lightbulb.implements(lightbulb.SlashCommand)
async def response(ctx):
    # pp(Jsearch(ctx.options.query).response.json())
    data = Jsearch(ctx.options.query).response.json()
    with open('data1.json', 'w') as outfile:
        json.dump(data, outfile)
    await ctx.respond("responded")

    
# returns all the existing unique combinations of discord roles
async def fetch_unique_roles() -> set:
    print("posting jobs\n")
    guild_id = 1115031539256926278
    members = await jobs_plugin.bot.rest.fetch_members(guild_id)
    unique_role_combination = set()
    unique_role_colors = set()
    excluded_role_colors = [Color(0x00000), Color(0xf1c40f)]

    me = jobs_plugin.bot.get_me()

    for member in members:
        # skip if member is bot
        if member.id == me.id:
            continue
        
        roles = await member.fetch_roles()
        role_ids = tuple([role.name for role in roles if role.color not in excluded_role_colors])
        unique_role_combination.add(role_ids)
        role_colors = tuple([role.color for role in roles if role.color not in excluded_role_colors])
        unique_role_colors.add(role_colors)

    print(len(unique_role_combination))
    print(unique_role_combination)
    print(unique_role_colors)
    return unique_role_combination
    

@jobs_plugin.command
@lightbulb.command("list", "list job postings")
@lightbulb.implements(lightbulb.SlashCommand)
async def list(ctx):
    await post_jobs()


def load(bot):
    bot.add_plugin(jobs_plugin)

def unload(bot):
    bot.remove_plugin(jobs_plugin)