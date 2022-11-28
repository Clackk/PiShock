from requests.models import REDIRECT_STATI
from redbot.core import commands
import discord
import requests
import json
from requests.structures import CaseInsensitiveDict
import random




class PiShock(commands.Cog):
    """Control PiShock from Discord"""

    def __init__(self, bot):
        self.bot = bot
        
    @commands.group()
    async def setup(self, ctx):
        """Set PiShock settings"""
        if ctx.invoked_subcommand is None:
            await ctx.send("you need to specify a setting to change")
    
    @setup.command()
    async def apikey(self, ctx, apikey: str):
        """Set the API key for PiShock"""
        #set variable for apikey
        self.apikey = apikey
        await ctx.send("API key set")
        
    @setup.command()
    async def username(self, ctx, username: str):
        """Set the username for PiShock"""
        self.username = username
        await ctx.send("Username set")
        
    @setup.command()
    async def sharecode(self, ctx, sharecode: str):
        """Set the user sharecode for PiShock"""
        self.sharecode = sharecode
        await ctx.send("Sharecode set")
        
    @setup.command()
    async def check(self, ctx):
        """Check current settings"""
        # print apikey, username and send as message)
        await ctx.send("API key: " + self.apikey + " Username: " + self.username + " Sharecode: " + self.sharecode)
    
    # the name variable for the POST request is set per each execution of the command
    
    @commands.group()
    async def ps(self, ctx):
        """Control PiShock"""
        if ctx.invoked_subcommand is None:
            await ctx.send("you need to specify a command")
            
    @ps.command()
    async def shock(self, ctx, duration: str, intensity: str):
        """Shock someone, set duration up to 15 seconds and intensity up to 100"""
        # throw an error if duration is over 15 seconds, or intensity is over 100
        if int(duration) > 15:
            await ctx.send("Duration must be 15 seconds or less")
        elif int(intensity) > 100:
            await ctx.send("Intensity must be 100 or less")
        else:
            # set the name variable for the POST request using the name of the bot followed by the user who passed the command
            self.name = ctx.message.author.name+"swissbot"
            # send post request to PiShock
            url = "https://do.pishock.com/api/apioperate"
            requestobject = {'Username': self.username, 'Name': self.name, 'Code': self.sharecode, 'Intensity': intensity, 'Duration': duration, 'apikey': self.apikey, 'Op': "0"}
            headers = CaseInsensitiveDict()
            returnvalue = requests.post(url, json = requestobject)
            # if the request is successful, equal to 300 send a message to the channel
            if returnvalue.status_code == 300:
                await ctx.send("operation successful")
            else:
                await ctx.send(returnvalue)
                await ctx.send("operation failed")
                
    