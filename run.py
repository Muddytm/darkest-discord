import config
import helper_functions as hf
import json
import random
import discord
from discord.ext import commands
import functions as f
import os

main_channel = "testing"

TOKEN = config.app_token

BOT_PREFIX = "!"
client = commands.Bot(command_prefix=commands.when_mentioned_or(BOT_PREFIX))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print ("parsin message")

    await client.process_commands(message)


@client.command(pass_context=True, no_pm=False)
async def register(ctx, stuff=""):
    """Register by DMing the bot with !register."""
    if not ctx.message.channel.is_private:
        return

    print ("got in.")

    name = hf.clean(ctx.message.author.name)
    id = str(ctx.message.author.id)

    for filename in os.listdir("data/players"):
        if id in filename:
            await client.send_message(ctx.message.author,
                                      "You've already arrived in the hamlet.")
            return

    with open("data/players/{}_{}.json".format(name, id), "w") as outfile:
        data = {"name": name, "id": id}
        json.dump(data, outfile)

    await client.send_message(ctx.message.author,
                              "You've arrived in the hamlet...make yourself at home, such as it is.")


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
