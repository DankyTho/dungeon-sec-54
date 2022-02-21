import discord
import json
from discord.ext import commands
import datetime

class AntiRole(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in role.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.role_create):
        if i.user.bot:
            return
      
        if str(i.user.id) in whitelisted[str(role.guild.id)]:
            return
        await role.guild.ban(i.user, reason="zeon : Creating Roles")
        await role.delete()
        return
        
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in role.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.role_delete):
          if i.user.bot:
              return
      
          if str(i.user.id) in whitelisted[str(role.guild.id)]:
              return
          await role.guild.ban(i.user, reason="zeon : Deleting Roles as Non-Whitelist User")
          await i.target.clone()
          return

    
    @commands.Cog.listener()
    async def on_guild_role_update(before, after, role):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in role.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.role_update):
          if str(i.user.id) in whitelisted[str(role.guild.id)]:
            return
          await role.guild.ban(i.user, reason="zeon : Updating roles as Non-Whitelist User")
          return

          if not before.permissions.ban_members and after.permissions.ban_members:
                await after.guild.kick(i.user, reason=f"zeon : Gave the role ({after.name}) Ban perms")
          permissions = after.permissions
          permissions.update(ban_members=False)
          await after.edit(permissions=permissions)

          if not before.permissions.administrator and after.permissions.administrator:
                await after.guild.kick(i.user, reason=f"zeon : Gave the role ({after.name}) Admin perms")
          permissions = after.permissions
          permissions.update(administrator=False)
          await after.edit(permissions=permissions)

          if not before.permissions.kick_members and after.permissions.kick_members:
                await after.guild.kick(i.user, reason=f"zeon : Gave the role ({after.name}) Kick perms")
          permissions = after.permissions
          permissions.update(kick_members=False)
          await after.edit(permissions=permissions)

          if not before.permissions.manage_channels and after.permissions.manage_channels:
                await after.guild.kick(i.user, reason=f"zeon : Gave the role ({after.name}) Channel perms")
          permissions = after.permissions
          permissions.update(manage_guild=False)
          await after.edit(permissions=permissions)
          return

          if not before.permissions.manage_roles and after.permissions.manage_roles:
                await after.guild.kick(i.user, reason=f"Zeon : Gave the role ({after.name}) Channel perms")
          permissions = after.permissions
          permissions.update(manage_roles=False)
          await after.edit(permissions=permissions)
          return

    @commands.Cog.listener()
    async def on_guild_role_update_recovery(before, after):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      role = after.guild  
      async for i in role.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.role_update):
          if str(i.user.id) in whitelisted[str(role.guild.id)]:
            return
          await after.edit(name=f"{before.name}")  
          await role.guild.ban(i.user, reason="zeon : Updating roles as Non-Whitelist User")         