import discord
import json, requests
from discord.ext import commands
import datetime

class AntiWebhook(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_webhooks_update(self, channel):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
        entry = await channel.guild.audit_logs(limit=1).get()
        if str(entry.user.id) in whitelisted[str(channel.guild.id)]:
            return
        if entry.user!=self.client.user:
            user = await self.client.fetch_user(entry.user.id)
            try:
                await channel.guild.ban(user, reason="Zeon : Webhook upadte as a Non-Whitelist user")
            except:
                pass
    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after,emoji):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
        entry = await guild.audit_logs(limit=1).get()
        if str(entry.user.id) in whitelisted[str(guild.id)]:
            return
        if entry.user!=self.client.user:
            user = await self.client.fetch_user(entry.user.id)
            try:
                await guild.ban(user, reason="Zeon :update emoji")
                #requests.delete(emoji)
            except:
                pass
    @commands.Cog.listener()
    async def on_guild_stickers_update(self, guild, before, after):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
        entry = await guild.audit_logs(limit=1).get()
        if str(entry.user.id) in whitelisted[str(guild.id)]:
            return
        if entry.user!=self.client.user:
            user = await self.client.fetch_user(entry.user.id)
            try:
                await guild.ban(user, reason="Zeon :update sticker")
            except:
                pass