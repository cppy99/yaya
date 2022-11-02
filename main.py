import discord,requests,aiohttp,urllib,textwrap,json
import datetime
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check, MemberConverter
from googletrans import Translator
import contextlib
import io
import random
import sys
import socket
import requests
import threading
import os
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash.utils import manage_commands
from pretty_help import DefaultMenu, PrettyHelp
from discord import ActionRow, Button, ButtonStyle
# ^^ All of our necessary imports

#Define our bot
client = discord.Client()


client = commands.Bot(command_prefix="py")

client.remove_command("help")

slash = SlashCommand(client, sync_commands=True)

reactions = [":white_check_mark:", ":stop_sign:", ":no_entry_sign:"]

@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.online, activity=discord.Game(name='pyhelp')) #Bot status, change this to anything you like
	print("Bot online")
  #will print "bot online" in the console when the bot is online


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.command(name="say")
async def say(ctx, *, arg):
  await ctx.message.delete()
  await ctx.send(arg)

@client.command(name='buttons', description='sends you some nice Buttons')
async def buttons(ctx: commands.Context):
    components = [ActionRow(Button(label='Option Nr.1',
                                   custom_id='option1',
                                   emoji="🆒",
                                   style=ButtonStyle.green
                                   ),
                            Button(label='Option Nr.2',
                                   custom_id='option2',
                                   emoji="🆗",
                                   style=ButtonStyle.blurple)),
                  ActionRow(Button(label='A Other Row',
                                   custom_id='sec_row_1st option',
                                   style=ButtonStyle.red,
                                   emoji='😀'),
                            Button(url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                                   label="This is an Link",
                                   style=ButtonStyle.url,
                                   emoji='🎬'))
                  ]
    an_embed = discord.Embed(title='Here are some Button\'s', description='Choose an option', color=discord.Color.random())
    msg = await ctx.send(embed=an_embed, components=components)

    def _check(i: discord.Interaction, b):
        return i.message == msg and i.member == ctx.author

    interaction, button = await client.wait_for('button_click', check=_check)
    button_id = button.custom_id

    # This sends the Discord-API that the interaction has been received and is being "processed"
    await interaction.defer()
    # if this is not used and you also do not edit the message within 3 seconds as described below,
    # Discord will indicate that the interaction has failed.

    # If you use interaction.edit instead of interaction.message.edit, you do not have to defer the interaction,
    # if your response does not last longer than 3 seconds.
    await interaction.edit(embed=an_embed.add_field(name='Choose', value=f'Your Choose was `{button_id}`'),
                           components=[components[0].disable_all_buttons(), components[1].disable_all_buttons()])

    # The Discord API doesn't send an event when you press a link button so we can't "receive" that.

@client.command(name="rps")
async def rps(ctx, arg):
  hasil = ["Rock","Paper","Scissor"]
  random = random.choice(hasil)
  if arg == "":
    await ctx.send(f"{arg} vS {random}")
    await ctx.send("You wins!!")
    

 
  
@client.command(aliases=["cal","calculator","cl"])
async def add(ctx, a: int, arg, b: int):
  if arg == "+":
    hasil = a + b
    await ctx.reply(f"{a} + {b} = {hasil}")
  elif arg == "-":
    hasil = a - b
    await ctx.reply(f"{a} - {b} = {hasil}")
  elif arg == "x":
    hasil = a * b
    await ctx.reply(f"{a} x {b} = {hasil}")
  elif arg == "/":
    hasil = a // b
    await ctx.reply(f"{a} / {b} = {hasil}")
  else:
    await ctx.send("Enter (+,/,-,x")


@client.command(name="dm") # You can add more aliases here
async def dm(ctx, user:MemberConverter=None, *, args=None):
	while args != None and args != "" and not args.isspace():
		try:
			await user.send(args.replace(user.mention, ""))
			await ctx.send(f"Message sent to {user.name}#{user.discriminator} :white_check_mark:")
		except discord.errors.Forbidden:
			await ctx.send(f"Could not send messsage to {user.name}#{user.discriminator} :x:")
			pass
		except commands.CommandInvokeError:
			await ctx.send(f"Could not send messsage to {user.name}#{user.discriminator} :x:")
			pass
		return
	await ctx.send(f"Please enter a message with the command\nUsage : `{client.command_prefix}dm <member> <message>`")

@client.command(name="arg")
async def test(ctx, *args):
    arguments = ', '.join(args)
    await ctx.send(f'{len(args)} arguments: {arguments}')



@client.command()
async def report(self, ctx, user : discord.Member, *reason):
    channel = self.bot.get_channel(1037338406394548295) #since it's a cog u need self.bot
    author = ctx.message.author
    rearray = ' '.join(reason[:]) #converts reason argument array to string
    if not rearray: #what to do if there is no reason specified
        await channel.send(f"{author} has reported {user}, reason: Not provided")
        await ctx.message.delete() #I would get rid of the command input
    else:
        await channel.send(f"{author} has reported {user}, reason: {rearray}")
        await ctx.message.delete()

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

@client.command(name='ddos',breif="ler")
async def ddos(ctx, ip, port, times, threads, methods):
    if ctx.author.id not in buyers:
        await ctx.send("mana bisa paok lo wibu anjg")
    else:
        await ctx.reply(f"**Ddos Attack To {ip}:{port}**")
        os.system(f"python3 ddos.py {ip} {port} {times} {threads} {methods}")
        

@slash.slash(name='clear', description='clear messages in the channel')
@commands.has_permissions(manage_messages=True)
async def clean(ctx: SlashContext,limit: int):
        await ctx.channel.purge(limit=limit)
        embed1 = discord.Embed(title = "Clear Massage", description=f"**• Massage telah dihapus dari {limit} Oleh {ctx.author.mention}",color = discord.Color(0x000000))
        await ctx.send(embed=embed1, delete_after=10)
        await ctx.message.delete()
  
@client.command(name="string",description="Show Basic String")
async def string(ctx: PrettyHelp):
  embed = discord.Embed(title="String", color=(0x000000))
  embed.set_author(name="Python",icon_url="https://i.postimg.cc/9F9dp1x1/2f9c11f9e55efbf1791f12c06d60729b.jpg")
  embed.add_field(name="1.Check if a contains only number",value='''
  ```py
  print("2022".isnumeric()) #True
print("2022 year".isnumeric()) #False
  ```
  ''')
  embed.add_field(name="2.Split a string on a spefic character",value='''
  ```py
  print("This is a string".split(" "))
#Output:['This', 'is', 'a', 'string']
  ```''')
  embed.add_field(name="3.Check if a string capital",value='''
  ```py
  print("Hello World".istitle()) #True
  ```''')
  embed.add_field(name="4.Check if the first character of a string is lowercase",value='''
  ```py
  print("oRanGe"[0].islower()) #True
print("oRanGe"[1].islower()) #False
  ```
  ''')
  embed.add_field(name="5.Write a program to return entire lowercase of a string",value='''
  ```py
  print("HeLLo".lower()) #hello
  ```
  ''')
  embed.add_field(name="6.How would you capitalize the first character of a string",value='''
  ```py
  print("my name is jhony".capitalize())
 #Output : My name is jhony
  ````
  ''')
  embed.add_field(name="7.Write a program to return entire upper of a string",value='''
  ```py
  print("hello".upper()) #HELLO
  ```
  ''')
  await ctx.send(embed=embed)

@client.command(name="ip", description="Example Track IP")
async def code(ctx):
  example = """```python
import os,sys
import json
import time
from urllib import request
os.system("clear")
print(" IP TRACKER ".center(25,"="),"\n")

url = "http://ipapi.co/"
ip = input("Input the IP Address : ")
request = request.urlopen(url + ip + "/json")
data_json = json.loads(request.read())

print("\nIP : " + str(data_json['ip']))
print("Country : " + str(data_json['country_name']))
print("Country Code : " + str(data_json['country_code']))
print("Country Iso : " + str(data_json['country_code_iso3']))
print("Country Capital : " + str(data_json['country_capital']))
print("Country tld : " + str(data_json['country_tld']))
print("Region : " + str(data_json['region']))
print("Region Code : " + str(data_json['region_code']))
print("City : " + str(data_json['city']))
print("Continent Code : " + str(data_json['continent_code']))
print("InEu : " + str(data_json['in_eu']))
print("Postal Code : " + str(data_json['postal']))
print("Latitude : " + str(data_json['latitude']))
print("Longitude : " + str(data_json['longitude']))
print("Timezone : " + str(data_json['timezone']))
print("Utc offset : " + str(data_json['utc_offset']))
print("Country Calling Code " + str(data_json['country_calling_code']))
print("Currency : " + str(data_json['currency']))
print("Currency Name : " + str(data_json['currency_name']))
print("Languages : " + str(data_json['languages']))
print("ASN : " + str(data_json['asn']))
print("ISP : " + str(data_json['org']))
print("Google Maps : https://maps.google.com/?q=" + str(data_json['latitude'])+','+str(data_json['longitude']))
print("\n\n\33[31;1m[!]\33[0m \33[33;1mWait for 10 seconds to open google maps automatically")
time.sleep(10)
os.system(f"xdg-open https://maps.google.com/?q={data_json['latitude']},{data_json['longitude']}")
```
"""
  await ctx.send(example)



@slash.slash(name="ping", description="Ping Pong")
async def _help(ctx: SlashContext):
	await ctx.send(content="pong!")

@slash.slash(name="python", description="Python interpreter")
async def terx(ctx, *, code):
    str_obj = io.StringIO() #Retrieves a stream of data
    try:
        with contextlib.redirect_stdout(str_obj):
            exec(code)
    except Exception as e:
        return await ctx.send(f"Output: ```{e.__class__.__name__}: {e}```")
    await ctx.send(f'Output: ```{str_obj.getvalue()}```')

@client.command(name="console",description="Interpreter")
async def python(ctx, *, code):
    str_obj = io.StringIO() #Retrieves a stream of data
    try:
        with contextlib.redirect_stdout(str_obj):
            exec(code)
    except Exception as e:
        return await ctx.send(f"Output: ```{e.__class__.__name__}: {e}```")
    await ctx.send(f'Output: ```{str_obj.getvalue()}```')

@slash.slash(name="weather", description="See the weather")
async def weather(ctx, weather):
    async with aiohttp.ClientSession() as session:
        apiurl = f"http://api.weatherstack.com/current?access_key=82658b49a57b43e125c050225d48c55c&query={weather}"
        r = requests.get(apiurl)
        print(r)
        print(r.text)
        kingman = json.loads(r.text)
        city = kingman['request']['query']
        localtime = kingman['current']['observation_time']
        wind_speed = kingman['current']['wind_speed']
        wind_degree = kingman['current']['wind_degree']
        temperature = kingman['current']['temperature']
        weather_icons = kingman['current']['weather_icons'][0]
        weather_descriptions = kingman['current']['weather_descriptions'][0]
        humidity = kingman['current']['humidity'] 
        print(city)
        print(localtime)
        print(wind_speed)
        print(wind_degree)
        print(temperature)
        print(weather_icons)
        print(weather_descriptions)
        print(humidity)
        embed=discord.Embed(title="Temperature", description=f"```{temperature}°C```", color=0x00000)
        embed.set_footer(name="Current weather", icon_url=f"{weather_icons}")
        embed.add_field(name="Wind direction speed", value=f"```{wind_speed}```", inline=True)
        embed.add_field(name="Degrees", value=f"```{wind_degree}```", inline=True)
        embed.add_field(name="Weather description", value=f"```{weather_descriptions}```", inline=True)
        embed.add_field(name="Humidity", value=f"```{humidity}```", inline=True)
        embed.set_footer(text=f"{localtime}")
        await ctx.send(embed=embed)

@slash.slash(name="checkweb", description="Tracker Website")
async def _checkweb(ctx, website = None):
    if website is None: 
        await ctx.send("No website! ex:`https://google.com`")
    else:
        try:
            req = requests.get(website).status_code
        except Exception as e:
            await ctx.send(embed=discord.Embed(title='*Website Is Down!*',description=f'```Responded with a status code of:\n{e}```'))
        if req == 404:
            await ctx.send(embed=discord.Embed(name='Site is Down!',value=f'```Responded with a status code of {e}```'))
        else:
            await ctx.send(embed=discord.Embed(title='*Website is Alive!*', description=f'```Responded with a status code of {req}```'))

@slash.slash(name="lyrics", description="Looking for song lyrics") # adding aliases to the command so they they can be triggered with other names
async def lyrics(ctx: SlashContext, *, search = None):
    """A command to find lyrics easily!"""
    if not search: # if user hasnt given an argument, throw a error and come out of the command
        embed = discord.Embed(
            title = "No search argument!",
            description = "You havent entered anything, so i couldnt find lyrics!"
        )
        return await ctx.reply(embed = embed)
        # ctx.reply is available only on discord.py version 1.6.0, if you have a version lower than that use ctx.send
    
    song = urllib.parse.quote(search) # url-encode the song provided so it can be passed on to the API
    
    async with aiohttp.ClientSession() as lyricsSession:
        async with lyricsSession.get(f'https://some-random-api.ml/lyrics?title={song}') as jsondata: # define jsondata and fetch from API
            if not 300 > jsondata.status >= 200: # if an unexpected HTTP status code is recieved from the website, throw an error and come out of the command
                return await ctx.send(f'Recieved poor status code of {jsondata.status}')

            lyricsData = await jsondata.json() # load the json data into its json form

    error = lyricsData.get('error')
    if error: # checking if there is an error recieved by the API, and if there is then throwing an error message and returning out of the command
        return await ctx.send(f'Recieved unexpected error: {error}')

    songLyrics = lyricsData['lyrics'] # the lyrics
    songArtist = lyricsData['author'] # the author's name
    songTitle = lyricsData['title'] # the song's title
    songThumbnail = lyricsData['thumbnail']['genius'] # the song's picture/thumbnail

    # sometimes the song's lyrics can be above 4096 characters, and if it is then we will not be able to send it in one single message on Discord due to the character limit
    # this is why we split the song into chunks of 4096 characters and send each part individually
    for chunk in textwrap.wrap(songLyrics, 4096, replace_whitespace = False):
        embed = discord.Embed(
            title = songTitle,
            description = chunk,
            color = (0x000000),
            timestamp = datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url = songThumbnail)
        await ctx.send(embed = embed)

# Space given text by user
@slash.slash(name="space", description="Space your text", options=[manage_commands.create_option( #create an arg
    name = "text", #Name the arg as "text"
    description = "The text to space", #Describe arg
    option_type = 3, #option_type 3 is string
    required = True #Make arg required
  )])
async def _space(ctx: SlashContext, sentence):
	newword = "" #define new sentence
	for char in sentence: #For each character in given sentence
		newword = newword + char + "   " #Add to new sentence  with space
	await ctx.send(content=newword) #send mew sentence
  
menu = DefaultMenu(
    "\U0001F44D",
    "👎",
    "❌",
    active_time=15,
    delete_after_timeout=True,
)

# Custom ending note
ending_note = "The ending note from {ctx.bot.user.name}\nFor command {help.clean_prefix}{help.invoked_with}"

index_title = "Python Help"

no_category = "BetaTester cmd {/}"


show_index = "hi"

sort_commands = "Hello"

client.help_command = PrettyHelp(menu=menu, ending_note=ending_note,index_title=index_title,no_category=no_category,sort_commands=sort_commands,show_index=show_index)

no_category = "String"


show_index = "hi"

sort_commands = "Hello"

client.help_command = PrettyHelp(menu=menu, ending_note=ending_note,index_title=index_title,no_category=no_category,sort_commands=sort_commands,show_index=show_index)



#Run our webserver, this is what we will ping

#Run our bot
client.run(os.getenv("TOKEN")) 
