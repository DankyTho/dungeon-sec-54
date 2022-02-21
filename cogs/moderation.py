import json

import discord
import time
from discord.ext import commands



class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
    


    @commands.command(usage="[#channel/id]")
    @commands.has_permissions(manage_messages=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 838287109861015562 or ctx.author.id == 783622109175742486:
         channel = channel or ctx.channel
         overwrite = channel.overwrites_for(ctx.guild.default_role)
         overwrite.send_messages = False
         await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
         await ctx.send(f"{channel.mention} locked!")

    @commands.command(usage="[#channel/id]")
    @commands.has_permissions(manage_messages=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 838287109861015562 or ctx.author.id == 783622109175742486:
          channel = channel or ctx.channel
          overwrite = channel.overwrites_for(ctx.guild.default_role)
          overwrite.send_messages = True
          await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
          await ctx.send(f"{channel.mention} unlocked!")

    @commands.command(name="kick",
                      usage="<member> [reason]")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if member.id == ctx.author.id:
            await ctx.send("You cannot kick yourself!")
            return
        if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 838287109861015562 or ctx.author.id == 783622109175742486:
         await member.kick(reason=reason)

         await ctx.message.delete()
         kick = discord.Embed(description=f"**A member has been kicked.**\n\n"
                                          f"Moderator: {ctx.author.mention}\n"
                                          f"Member: {member.mention}", colour=discord.Colour.blue())
         kick.add_field(name="Reason", value=reason, inline=False)
         await ctx.send(embed=kick)

    @commands.command(usage="<member> [reason]")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if member.id == ctx.author.id:
            await ctx.send("You cannot ban yourself!")
            return
            if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 838287109861015562 or ctx.author.id == 783622109175742486:
              await member.ban(reason=reason, delete_message_days=0)
              ban = discord.Embed(description=f"**A member has been banned.**\n\n"
                                        f"Moderator: {ctx.author.mention}\n"
                                        f"Member: {member.mention}", colour=discord.Colour.blue())
              ban.add_field(name="Reason", value=reason, inline=False)
              await ctx.send(embed=ban)


    @commands.command(usage="number")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=0):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"I have cleared **{amount}** messages.", delete_after=3)

    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def nuke(self, ctx):
        if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 838287109861015562 or ctx.author.id == 783622109175742486:
          channelthings = [ctx.channel.category, ctx.channel.position]
          await ctx.channel.clone()
          await ctx.channel.delete()
          nukedchannel = channelthings[0].text_channels[-1]
          await nukedchannel.edit(position=channelthings[1])
          await nukedchannel.send(f"Channel was nuked by {ctx.author.mention}")

    @commands.command(usage="add/remove <member> <role>")
    @commands.has_permissions(administrator=True)
    async def role(self, ctx, addORremove, member: discord.Member, role: discord.Role):

        addORremove = addORremove.lower()

        if addORremove == 'add':

            if role == ctx.author.top_role:
                return await ctx.send("That role has the same position as your top role!")

            if role in member.roles:
                return await ctx.send("The member already has this role assigned!")

            if role.position >= ctx.guild.me.top_role.position:
                return await ctx.send(f"This role is higher than my role, move it to the top!")
            if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 838287109861015562 or ctx.author.id == 783622109175742486:
              await member.add_roles(role)
              await ctx.send(f"I have added {member.mention} the role {role.mention}")

        if addORremove == 'remove':
           

            if role == ctx.author.top_role:
                return await ctx.send("That role has the same position as your top role!")

            if role not in member.roles:
                return await ctx.send("The member does not have this role!")

            if role.position >= ctx.guild.me.top_role.position:
                return await ctx.send(f"This role is higher than my role, move it to the top!")
            if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 838287109861015562 or ctx.author.id == 783622109175742486:
              await member.remove_roles(role)
              await ctx.send(f"I have removed {member.mention} the role {role.mention}")