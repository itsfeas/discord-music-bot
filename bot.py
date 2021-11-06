from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from discord.utils import get 
from pynput.keyboard import Key, Controller
import urllib
from urllib import parse
import time
import json


client = commands.Bot(command_prefix = '-')
queue ={}

@client.event
async def on_ready():
    print('Bot is ready.')
    
#@client.command(pass_context=True)
#async def join(ctx):
    #channel = ctx.author.voice.channel
    #await channel.connect()
    #await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)

    
@client.command(brief="Plays a single video, from a youtube URL")
async def play(ctx, url): 
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
    
    url_parsed = parse.urlparse(url)
    qsl = parse.parse_qs(url_parsed.query)
    video_id=(qsl['v'][0])    
    
    YT_KEY='AIzaSyBF2OR7lpNTEbNLHTKtqUdj1gQujh73Coo'
    
    search_url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={YT_KEY}&part=contentDetails'
    req = urllib.request.Request(search_url)
    response = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(response)
    all_data = data['items']
    duration = all_data[0]['contentDetails']['duration']
    
    #try:
        #minutes = int(duration[2:].split('M')[0])
    #except:
        #minutes = 0
    #seconds = int(duration[-3:-1])    
    #length = (minutes*60)+seconds
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True.'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)
    queue[len(queue)+1] = url

    print(queue)
  
    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']                
        voice.play(FFmpegPCMAudio(URL, executable="C:/ffmpeg/bin/ffmpeg.exe", **FFMPEG_OPTIONS))
        voice.is_playing()
        cplaying = list(queue.keys())[list(queue.values()).index(url)]
        print(cplaying)
    else: 
        #await ctx.send("Already playing song")
      
        return

@client.command(pass_context=True)
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    
    user = ctx.message.author.mention
    await ctx.send(f"Bot was stopped by {user}")    

@client.command(pass_context=True)
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.pause()
    
    print(cplaying)
    
    user = ctx.message.author.mention
    await ctx.send(f"Bot was paused by {user}")        
    
@client.command(pass_context=True, aliases=['unpause'])
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.resume()
    
@client.command(pass_context=True)
async def skip(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True.'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)
    
    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(queue[n], download=False)
        URL = info['formats'][0]['url']                
        voice.play(FFmpegPCMAudio(URL, executable="C:/ffmpeg/bin/ffmpeg.exe", **FFMPEG_OPTIONS))
        voice.is_playing()
            
    else: 
        await ctx.send("Already playing song")


@client.command(pass_context=True)
async def jump(ctx, num):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True.'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)
    
    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(queue[int(num)], download=False)
        URL = info['formats'][0]['url']                
        voice.play(FFmpegPCMAudio(URL, executable="C:/ffmpeg/bin/ffmpeg.exe", **FFMPEG_OPTIONS))
        voice.is_playing()
        cplaying = list(queue.keys())[list(queue.values()).index(url)]    
    else: 
        await ctx.send("Already playing song")

#@client.command(pass_context=True)
#async def queue(ctx):
    #await ctx.send(


try:
    client.run('CLIENT-TOKEN')
except:
    client.run('CLIENT-TOKEN')
    
