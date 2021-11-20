
import asyncio
import os
import discord
import datetime

from gw2.gw2 import Gw2

TOKEN = os.getenv('DISCORD_TOKEN')
KEY = "!yk"

bot = discord.Client()


class Bot:

    def __init__(self):
        pass

    def run(self):
        bot.run(TOKEN)

### READY ###
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=KEY))

### REPLY ###
@bot.event
async def on_message(message):

    # make sure bot does not respond to itself
    if message.author == bot.user:
        return

    # Vars
    myid = "<@!" + str(bot.user.id) + ">"
    author_id = message.author.mention

    # commands
    if message.content.startswith(KEY + " "):

        words = message.content.split()

        ### GW2 ###
        # Dailies
        # i.e. "!yk dailies T4", "!yk dailies recommended"
        if len(words) == 3:
            words[1] = words[1].lower()
            words[2] = words[2].upper()
            accepted_words = ["T1", "T2", "T3", "T4", "RECOMMENDED"]
            if (words[1] == "dailies" or words[1] == "daily") and words[2] in accepted_words:
                tier = words[2]
                gw2 = Gw2()
                gw2.update_achi_dict()
                dailies = gw2.get_dailies(tier)

                if dailies == False:
                    await message.channel.send(author_id + " bad format. Try it like " + KEY + " dailies T4")
                    return

                else:
                    today = str(datetime.datetime.today())
                    today = str(today.split()[0])
                    embedVar = discord.Embed(
                        title="Fractal dailies of " + today, color=0x0066ff)
                    frac_str = ""
                    for daily in dailies:
                        frac_str += ":cyclone: " + daily + "\n"
                    embedVar.add_field(
                        name="Daily fractals " + tier, value=frac_str, inline=False)
                    await message.channel.send(embed=embedVar)
                    return
