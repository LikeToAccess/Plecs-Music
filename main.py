# -*- coding: utf-8 -*-
# filename          : main.py
# description       : Discord music bot
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 02-01-2021
# version           : v1.0
# usage             : python main.py
# notes             : 
# license           : MIT
# py version        : 3.7.9 (must run on 3.6 or higher)
#==============================================================================
from discord.ext import commands, tasks
import speedtest
import discord
import os
import youtube_dl


client = discord.Client()
bot = commands.Bot(command_prefix=["!","`","~","please "], help_command=None, case_insensitive=True)
st = speedtest.Speedtest() 


@bot.event
async def on_ready():
	print("Logged in as {0.user}".format(bot))
	#status.start()

@bot.command()
async def play(ctx, url : str):
	song = os.path.isfile("song.mp3")
	try:
		if song:
			os.remove("song.mp3")
	except PermissionError:
		await ctx.send("oops")
		return
	voice_channel = discord.utils.get(ctx.guild.voice_channels, name="▶voice-chat")
	await voice_channel.connect()
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	
	ydl_opts = {
		"format": "bestaudio/best",
		"postprocessors": [{
			"key": "FFmpegExtractAudio",
			"preferredcodec": "mp3",
			"preferredquality": "96",
		}],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])
	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			os.rename(file, "song.mp3")
	voice.play(discord.FFmpegPCMAudio("song.mp3"))


	await ctx.message.delete()
	print("SUCCESS: played audio.")

# @bot.command()
# async def leave(ctx):
# 	voice_channel = discord.utils.get(ctx.guild.voice_channels, name="▶voice-chat")
# 	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
# 	await voice.disconnect()
#	await ctx.message.delete()

@tasks.loop(seconds=20)
async def status():
	upload = int(st.upload()/60000)
	await bot.change_presence(status=discord.Status.online, activity=discord.Game(f"at {upload}% network performance!"))

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	if message.content.startswith("is the server down"):
		packet_loss = os.system("ping 192.168.50.99 -n 2 -w 1")
		if packet_loss == 0:
			await message.channel.send("Nope!")
		elif packet_loss == 1:
			await message.channel.send("Server is dead!!!")
		else:
			await message.channel.send(f"Error Unknown: {packet_loss} (should be either 0 or 1).")
	elif message.content.startswith("is the server slow"):
		upload = int(st.upload()/60000)
		print(upload)
		await message.channel.send(f"Network is at *{upload}%* performace!")

@bot.command(pass_context = True)
async def leave(ctx, name="leave"):
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	await voice.disconnect()
	await ctx.message.delete()
	print("SUCCESS: left VC.")

@bot.command()
async def join(ctx, name="join"):
	voice_channel = discord.utils.get(ctx.guild.voice_channels, name="▶voice-chat")
	await voice_channel.connect()
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	await ctx.message.delete()
	print("SUCCESS: joined VC.")
	
# Credit to Crazy#9999
@bot.command(name="carson")
async def carson(ctx):
	await ctx.message.delete()
	print("I'm gunna fuck a child!")
	await ctx.send("I'm gunna fuck a child!")
	await ctx.message.delete()
	print("SUCCESS: carson.")

@bot.command()
async def pause(ctx):
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	voice.pause()
	await ctx.message.delete()
	print("SUCCESS: paused audio.")

@bot.command()
async def resume(ctx):
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	voice.resume()
	await ctx.message.delete()
	print("SUCCESS: unpaused audio.")

@bot.command()
async def stop(ctx):
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	voice.stop()
	await ctx.message.delete()
	print("SUCCESS: stopped audio.")



bot.run("Nzc2Njg4MzM4Mjk1NTg2ODU2.X64hYg.4cGSEYm1MCal7pzBjZYQjK9ONDQ")
