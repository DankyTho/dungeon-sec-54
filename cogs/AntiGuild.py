import discord
import json
from discord.ext import commands
import datetime

class AntiGuild(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_guild_update(ctx, self, guild):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.guild_update):
          if str(i.user.id) in whitelisted[str(guild.id)]:
            return
          await guild.ban(i.user, reason="zeon : Updating Guild as Non-Whitelist User")
          
          return


    @commands.Cog.listener()
    async def on_guild_update_recovery(ctx, guild, channel):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.guild_update):
          if str(i.user.id) in whitelisted[str(guild.id)]:
            return
          await channel.delete()
          
          return   

    @commands.Cog.listener()
    async def on_guild_update_recover(before, after, guild):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.guild_update):
          if str(i.user.id) in whitelisted[str(guild.id)]:
            return
          await guild.ban(i.user, reason="zeon : Updating Guild as Non-Whitelist User")
          await guild.edit(name=f"{before.name}")
          
          return          