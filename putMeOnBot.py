import os
import discord
import random
import asyncio
from discord.ext import commands
from youtubesearchpython import VideosSearch

token = "TOKEN"

intents = discord.Intents.all()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)
chosen_person_id = None
recommendations = {}

@bot.event
async def on_ready():
    new_username = "Put Me On"
    await bot.user.edit(username=new_username)
    print(f'Bot username changed to:      {new_username}')
    await choose_person_periodically()

@bot.event
async def on_message(message):
    if message.author.bot: #if the bot sends a link, do nothing
        return
    if "youtube.com" in message.content.lower() or "youtu.be" in message.content.lower() and message.author != bot.user:
        await message.delete() #delete all youtube links sent 
    await bot.process_commands(message) #process other commands

async def choose_person_periodically():
    while True:
        await asyncio.sleep(43200) #the time to choose somoene is set to 12 hours
        await choose_random_person()


async def choose_random_person():
    global chosen_person_id
    server = bot.get_guild(SERVERID)
    members = [member for member in server.members if not member.bot] #all the members in the server except bot
    random_member = random.choice(members) #chooses a random person using random.choice
    chosen_person_id = random_member.id #whoever is chosen at random is "the chosen one"
    await server.text_channels[0].send(f"{random_member.mention}, you have been chosen!")


@bot.command()
async def rec(ctx, *, song: str):
    global chosen_person_id
    if ctx.author.id == chosen_person_id: #checks if person asking is 'chosen one'
        recommendations[ctx.author.id] = song #stores the song in the recommended dictionary
        youtube_url = get_youtube_url(song) #searches the song on youtube and gets link
        await ctx.send(f"Thank you, {ctx.author.name}, for recommending '{song}! {youtube_url}")
        chosen_person_id = None #resets after the recommendation. So prev 'chosen one' cant forever recommend
    else:
        await ctx.send("Sorry, you are NOT the Chosen One.") #if non chosen one tries to use command

class CustomHelpCommand(commands.DefaultHelpCommand):
    def get_command_signature(self, command):
        return f"{self.clean_prefix}{command.qualified_name} {command.signature}"

    async def send_bot_help(self, mapping):
        help_message = (
        "Hi! I am a bot that will randomly choose someone in the server to recommend a song of their choosing. \n \n"
        "Once someone has been chosen, please recommend a song with this format: '!rec Title by Artist' \n \n"
        )
        destination = self.get_destination()
        await destination.send(help_message)


bot.help_command = CustomHelpCommand()


def get_youtube_url(query):
    videos_search = VideosSearch(query, limit = 1) #only one video will be fetched
    results = videos_search.result() #the result is obtained
    if results and "link" in results["result"][0]: #if the link is obtained, show result
        return results["result"][0]["link"] #if no link is obtained, no result
    else:
        return "Youtube link not found."

bot.run(token)