import config
import random
import discord
from discord.ext.commands import Bot

BOT_PREFIX = ""
TOKEN = config.app_token

client = Bot(command_prefix=BOT_PREFIX)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.send_message(message.channel, message.channel.name)


# @client.command(name='8ball',
#                 description="Answers a yes/no question.",
#                 brief="Answers from the beyond.",
#                 aliases=['eight_ball', 'eightball', '8-ball'],
#                 pass_context=True)
# async def eight_ball(context):
#     possible_responses = [
#         'That is a resounding no',
#         'It is not looking likely',
#         'Too hard to tell',
#         'It is quite possible',
#         'Definitely',
#     ]
#     await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#client.loop.create_task(do_thing())
client.run(TOKEN)
