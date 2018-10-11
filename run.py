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

    # Check if player already has player file
    for filename in os.listdir("data/players"):
        if id in filename:
            await client.send_message(ctx.message.author,
                                      "You've already registered.")
            return

    # Create new player file
    with open("data/players/{}_{}.json".format(name, id), "w") as outfile:
        data = {"name": name, "id": id}
        json.dump(data, outfile)

    await client.send_message(ctx.message.author,
                              "You've registered with Darkest Discord!")
    await client.send_message(ctx.message.author,
                              "Type `!newhero` to create a hero (maximum of 1).")


# NEW HERO CREATION PROCESS ----------------------------------------------------
@client.command(pass_context=True, no_pm=False)
async def newhero(ctx, *stuff):
    """Begin hero creation process."""
    if not ctx.message.channel.is_private:
        return

    player_name = hf.clean(ctx.message.author.name)
    id = str(ctx.message.author.id)
    data = hf.get_player(player_name, id)

    # Setting this here allows the name character limit to be changed easily.
    name_limit = 32

    # Get a list of classes with capitalized names
    classes = []
    for filename in os.listdir("data/classes"):
        if ".json" in filename:
            classes.append(filename.replace(".json", "").capitalize())

    # Begin setup, create setup variable in player data
    if "setup" not in data:
        await client.send_message(ctx.message.author,
                                  ("A new hero arrives in the hamlet. The denizens are curious...what is their name?"
                                   "\nType `!newhero yourheroname` with the desired name. {} character limit.".format(str(name_limit))))
        data["setup"] = 1
    # Take name given by user and make a hero file from it
    elif data["setup"] == 1 and stuff:
        hero_name = hf.clean("_".join(stuff))
        if len(hero_name) > name_limit:
            await client.send_message(ctx.message.author,
                                      "This name is too long for your allies to address you by. {} characters is the limit.".format(str(name_limit)))
            return
        for filename in os.listdir("data/heroes"):
            if filename.lower() == "{}.json".format(hero_name).lower():
                await client.send_message(ctx.message.author,
                                          "A hero of this name already resides in the hamlet.")
                return

        hero_data = {"display_name": hero_name.replace("_", " "), "name": hero_name}
        hf.push_hero(hero_data, hero_name)

        data["heroes"] = []
        data["heroes"].append(hero_name)

        await client.send_message(ctx.message.author,
                                  "Your hero has introduced themselves as {}.".format(hero_name.replace("_", " ")))
        await client.send_message(ctx.message.author,
                                  ("Inquiries about their...occupation, have arisen. Which class are they?"
                                   "\nType `!newhero class`, where `class` is one of these options:"
                                   "\n\n - {}".format("\n - ".join(classes))))
        data["setup"] = 2
    # Take class given by user and establish hero as class
    elif data["setup"] == 2 and stuff:
        class_name = hf.clean(" ".join(stuff))
        if class_name.lower().capitalize() not in classes:
            await client.send_message(ctx.message.author,
                                      "No class by that name was found.")
            return
        else:
            await client.send_message(ctx.message.author,
                                      "You have chosen the *{}*.".format(class_name.lower().capitalize()))

            hero_data = hf.get_hero(data["heroes"][len(data["heroes"]) - 1])
            hero_data["class"] = class_name.lower().capitalize()
            hf.push_hero(hero_data, hero_data["name"])

            await client.send_message(ctx.message.author,
                                      "Before adventuring, you must first answer the questions put before you by the hamlet's local psychologist.")

            quests = ["To seek fame and fortune!",
                      "To undo the horrors that lurk in the depths.",
                      "To atone for my wrongdoings, and redeem myself.",
                      "To relieve myself of this clawing boredom!"]
            await client.send_message(ctx.message.author,
                                      "\"What is your quest?\"")

            data["setup"] = 3


    hf.push_player(data, player_name, id)


# OTHER COMMANDS ---------------------------------------------------------------
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


# PUT POSSIBLE TIMED BITS HERE -------------------------------------------------
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
