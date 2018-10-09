import config
import random
import discord
from discord.ext.commands import Bot

main_channel = "testing"

BOT_PREFIX = ""
TOKEN = config.app_token

client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.send_message(message.channel, message.channel.name)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#client.loop.create_task(do_thing())
client.run(TOKEN)
