import discord
import json
from discord.ext import commands
import datetime

class AntiChannel(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in channel.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.channel_create):
          if str(i.user.id) in whitelisted[str(channel.guild.id)]:
            return
          await channel.guild.ban(i.user, reason="zeon : Creating Channels as Non-Whitelist User")
          await channel.delete(reason=f"zeon : Deleting user created channels")
          await i.target.delete(reason=f"zeon : Deleting user created channels")
          return
        
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
      guild = channel.guild
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in channel.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.channel_delete):
          if str(i.user.id) in whitelisted[str(channel.guild.id)]:
            return
          await channel.guild.ban(i.user, reason="zeon : Deleting Channels as Non-Whitelist User")
          await guild.create_text_channel(name=f"{channel}")
          return

    @commands.Cog.listener()
    async def on_guild_channel_update(before, after, channel):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in channel.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.channel_update):
          if str(i.user.id) in whitelisted[str(channel.guild.id)]:
            return
          await after.edit(name=f"{before.name}")  
          await channel.guild.ban(i.user, reason="zeon : Updating Channels as Non-Whitelist User")
          return

    @commands.Cog.listener()
    async def on_guild_channel_overrights_create(self, channel):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in channel.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.overwrite_create):
          if str(i.user.id) in whitelisted[str(channel.guild.id)]:
            return
          await channel.guild.ban(i.user, reason="zeon : Updating Channels as Non-Whitelist User")
          return

    @commands.Cog.listener()
    async def on_guild_channel_overrights_update(before, after, channel):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in channel.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.overwrite_update):
          if str(i.user.id) in whitelisted[str(channel.guild.id)]:
            return
          await channel.guild.ban(i.user, reason="zeon : Updating Channels as Non-Whitelist User")
      return          
      
    
    
    @commands.Cog.listener()
    async def on_guild_channel_overrights_delete(self, channel):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in channel.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.overwrite_delete):
          if str(i.user.id) in whitelisted[str(channel.guild.id)]:
            return
          await channel.guild.ban(i.user, reason="zeon : Updating Channels as Non-Whitelist User")
          return          

    @commands.Cog.listener()
    async def on_guild_update(ctx, guild, channel):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.guild_update):
          if str(i.user.id) in whitelisted[str(guild.id)]:
            return
          await channel.delete()
          
          return             

        