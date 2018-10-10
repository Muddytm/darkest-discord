import config
import helper_functions as hf
import json
import random
import discord
from discord.ext import commands
import functions as f
import os

main_channel = "testing"
hero_max = 1

TOKEN = config.app_token

BOT_PREFIX = "!"
client = commands.Bot(command_prefix=commands.when_mentioned_or(BOT_PREFIX))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)


@client.command(pass_context=True, no_pm=False)
async def register(ctx, stuff=""):
    """Register by DMing the bot with !register."""
    if not ctx.message.channel.is_private:
        return

    name = hf.clean(ctx.message.author.name)
    id = str(ctx.message.author.id)

    for filename in os.listdir("data/players"):
        if id in filename:
            await client.send_message(ctx.message.author,
                                      "You've already registered.")
            return

    with open("data/players/{}_{}.json".format(name, id), "w") as outfile:
        data = {"name": name, "id": id}
        json.dump(data, outfile)

    await client.send_message(ctx.message.author,
                              "You've registered with Darkest Discord!")
    await client.send_message(ctx.message.author,
                              "Type `!newhero` to create a hero (maximum of 1).")


@client.command(pass_context=True, no_pm=False)
async def newhero(ctx, stuff=""):
    """Begin hero creation process."""
    if not ctx.message.channel.is_private:
        return

    name = hf.clean(ctx.message.author.name)
    id = str(ctx.message.author.id)
    data = hf.get_player(name, id)

    classes = []
    for filename in os.listdir("data/classes"):
        if ".json" in filename:
            classes.append(filename.replace(".json", "").capitalize())

    if "setup" not in data:
        data["setup"] = 1

        await client.send_message(ctx.message.author,
                                  ("A new hero arrives in the hamlet. Which class are they?"
                                   "\nType `!newhero class`, replacing `class` with one of the following:"
                                   "\n\n{}".format("\n- ".join(classes)))


@client.command(pass_context=True)
async def test(ctx, stuff="horrors"):
    """Just a test command."""
    await client.send_message(ctx.message.channel,
                              "*\"Ghoulish {}, brought low, and driven into the mud!*\"".format(stuff))


@client.command(pass_context=True)
@commands.has_any_role("Devs")
async def dismiss(ctx, stuff=""):
    """Close the bot."""
    response = f.dismiss_bot_phrase().strip()
    await client.send_message(ctx.message.channel, "*\"{}\"*".format(response))
    await client.logout()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


#client.loop.create_task(do_thing())
client.run(TOKEN)
