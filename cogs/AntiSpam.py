import asyncio
import discord
import json
import aiohttp
from discord.ext import commands
from datetime import datetime

antiSpam = False
antiLink = False
antiWord = True
punishment = "ban"

class onMessage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
        try:

                    try:
                        if antiSpam is True:
                            def check(message):
                                return(message.author == message.author and (datetime.utcnow() - message.created_at).seconds < 15)

                            if str(message.author.id) in whitelisted[str(message.guild.id)]:
                                return

                            if len(list(filter(lambda m: check(m), self.client.cached_messages))) >= 4 and len(list(filter(lambda m: check(m), self.client.cached_messages))) < 8:
                                pass
                            elif len(list(filter(lambda m: check(m), self.client.cached_messages))) >= 8:

                                if punishment == "ban":
                                    await message.author.kick(reason=f"Server Security Auto-Moderation | Spamming", delete_message_days=7)
                                  

                        if antiLink is True:
                            if str(message.author.id) in whitelisted[str(message.guild.id)]:
                                return
                            if "https://" in message.content:
                                await message.delete()

                                if punishment == "ban":
                                    await message.author.kick(reason=f"Server Security Auto-Moderation | Sending Links", delete_message_days=0)
                                


                        if message.mention_everyone:
                          if str(message.author.id) in whitelisted[str(message.guild.id)]:
                            return
                            await message.delete()
                            if punishment == "ban":
                                  await message.author.ban(reason=f"Mentioning Everyone")

                    except UnboundLocalError:
                        pass

        except discord.errors.NotFound:
            pass

