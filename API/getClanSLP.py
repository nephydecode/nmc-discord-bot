import requests
import os
import json
import discord
from roninAddConverter import roninAddConverter
from replit import db
import sys

def getClanSLP(clan):

	# Initialise the embeded
	if clan.lower() == "oasis":
		color = discord.Color.blue()
	elif clan.lower() == "lunar":
		color = discord.Color.gold()
	elif clan.lower() == "kopi":
		color = discord.Color.dark_purple()
	elif clan.lower() == "sol":
		color = discord.Color.red()
	else:
		color = discord.Color.light_gray()
		return discord.Embed(title="Eh no such clan leh", color=color)
		
	embed = discord.Embed(title = clan.capitalize() +  " clan's Daily Updates", color = color)

	roninAddDb = json.loads(db.get_raw("roninAdd"))[clan.lower()]

	try:
		for user in roninAddDb:
    #get 0x
			roninAdd = roninAddConverter(user["scholarRonin"]) 
			url = "https://axie-infinity.p.rapidapi.com/get-update/" + roninAdd +"?id=" + roninAdd

			payload={}
			headers = {
				'x-rapidapi-host': 'axie-infinity.p.rapidapi.com',
				'x-rapidapi-key': os.environ['x-rapidapi-key']
			}

			response = requests.request("GET", url, headers=headers, data=payload)

			json_data = json.loads(response.text)
			print(json_data)
			thename = json_data['leaderboard']['name']

			if thename is None:
				break 
			else:
				todaySlp = json_data['slp']['todaySoFar']
				ytdSlp = json_data['slp']['yesterdaySLP']
				avg = json_data['slp']['average']
				totalSlp = json_data['slp']['total']
				mmr = json_data['leaderboard']['elo']

			embed.add_field(name = thename, value = "Today's SLP: " + str(todaySlp) + ", Ytd SLP: " + str(ytdSlp) + ", Average SLP: " + str(avg) + ", Total SLP: " + str(totalSlp) + ", MMR: " + str(mmr) ,inline=False)

		return embed
	except:
		embed=discord.Embed(title="Oops!", color = discord.Color.light_gray())
		embed.add_field(name="Error", value=sys.exc_info()[0])
		return embed
    # print("sys.exc_info()[0], "occurred.")
		

