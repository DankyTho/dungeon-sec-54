import discord
import json
from discord.ext import commands
import datetime

class AntiRemoval(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.ban):
      
          if str(i.user.id) in whitelisted[str(guild.id)]:
            return
          await guild.ban(i.user, reason="Zeon: Banning Members")
          await guild.kick(i.user, reason="Zeon: Banning Members")
          return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
      
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in member.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.kick):
      
          if str(i.user.id) in whitelisted[str(i.guild.id)]:
            return
          if i.target.id == member.id:
             await i.user.ban()
             return

    @commands.Cog.listener()
    async def on_member_prune(self, member):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in member.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.member_prune):
      
          if str(i.user.id) in whitelisted[str(i.guild.id)]:
            return
          if i.target.id == member.id:
             await i.user.ban()
             return

    @commands.Cog.listener()
    async def on_member_join(self, member):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in member.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.bot_add):
      
          if str(i.user.id) in whitelisted[str(member.guild.id)]:
            return
          
          if member.bot:
             await member.ban(reason="zeon : Unknown Bot as Non-Whitelist User")
             await i.user.ban(reason="zeon : Added Unknown Bot as Non-Whitelist User")
             return
          
    @commands.Cog.listener()
    async def on_member_role_update(before, after ,member, user):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in member.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.member_role_update):
          if i.user.bot:
              return
      
          if str(i.user.id) in whitelisted[str(member.guild.id)]:
              return
          await member.guild.ban(i.user, reason="zeon : Updating Roles as Non-Whitelist User")
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
