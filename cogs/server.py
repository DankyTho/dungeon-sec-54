from discord.ext import commands
import datetime
import discord
import random
import requests
import os

class server(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=['serverav', 'servericon'])
  async def serverpfp(self, ctx):
      icon_url = ctx.guild.icon_url
      embed = discord.Embed(
          timestamp=datetime.datetime.utcnow(),
          colour = 0xc57694,
          description=f"Requested by {ctx.author.mention}",
      )
      embed.set_author(name=f"Zeon", icon_url=icon_url)
      embed.set_image(url=icon_url)
      embed.set_footer(text=f"{ctx.guild.name}")

      await ctx.send(embed=embed)

  @commands.command(aliases=['av', 'pfp'])
  async def avatar(self, ctx, *, user: discord.Member=None):
      format = "gif"
      user = user or ctx.author

      if user.is_avatar_animated() != True:
	      format = "png"
      avatar = user.avatar_url_as(format = format if format != "gif" else None)

      embed = discord.Embed(
          timestamp=datetime.datetime.utcnow(),
          colour = 0x2f3136,
          description=f"Avatar requested by {ctx.author.mention}",
      )
      embed.set_author(name=str(user), url=f"{user.avatar_url}", icon_url=user.avatar_url)
      embed.set_image(url=avatar)
      embed.set_footer(text=f"{ctx.guild.name}")
    
      await ctx.send(embed=embed)

  @commands.command(pass_context=True, aliases=['ui'])
  async def whois(self, ctx, user: discord.Member = None):
      if user is None:
          user = ctx.author   
      embed = discord.Embed(color=0x2f3136)
      embed.set_author(name=str(user), icon_url=user.avatar_url)
      embed.set_thumbnail(url=user.avatar_url)
      embed.add_field(name="**Username:**", value=user, inline=True)
      embed.add_field(name="**ID:**", value=user.id, inline=True)
      embed.add_field(name="**Status:**", value=user.status, inline=True)
      embed.add_field(name="**Highest Role:**", value=user.top_role)

      userMade = user.created_at
      userMade2 = userMade.strftime("%B %d, %Y %I:%M %p")
      embed.add_field(name="**Registered:**", value="{}".format(userMade2))

      userJoin = user.joined_at
      userJoin2 = userJoin.strftime("%B %d, %Y %I:%M %p")
      embed.add_field(name="**Joined:**", value="{}".format(userJoin2))

      if len(user.roles) > 1:
          role_string = ' '.join([r.mention for r in user.roles][1:])
          embed.add_field(name="**Roles [{}]**".format(len(user.roles)-1), value=role_string, inline=False)
      perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
      embed.add_field(name="**Key permissions:**", value=perm_string, inline=False)

      embed.set_thumbnail(url=user.avatar_url)
      embed.set_footer(text="Requested by {}".format(ctx.message.author))
      await ctx.send(embed=embed)

  @commands.command(aliases=['ri'])
  async def roleinfo(self, ctx, *, role: discord.Role = None):
      if role is None:
          await ctx.send("You must provide a role to view info on!")
      guild = ctx.guild
      since_created = (ctx.message.created_at - role.created_at).days
      role_created = role.created_at.strftime("%d %b %Y %H:%M")
      created_on = "{} ({} days ago)".format(role_created, since_created)
      users = len([x for x in guild.members if role in x.roles])
      if str(role.colour) == "#000000":
          colour = "#000000"
          color = ("#%06x" % random.randint(0, 0xFFFFFF))
          color = int(colour[1:], 16)
      else:
          colour = str(role.colour).upper()
          color = role.colour
      embed = discord.Embed()
      embed.add_field(name='**Role Name:**', value=f"{role.name}", inline=False)
      embed.add_field(name='**Role ID:**', value=f"{role.id}", inline=False)
      embed.add_field(name="**Users In Role:**", value=f"{users}", inline=False)
      embed.add_field(name="**Mentionable:**", value=f"{role.mentionable}", inline=True)
      embed.add_field(name="**Hoisted:**", value=f"{role.hoist}", inline=True)
      embed.add_field(name="**Position:**", value=f"{role.position}", inline=False)
      embed.add_field(name="**Managed:**", value=f"{role.managed}", inline=True)
      embed.add_field(name="**Colour:**", value=f"{colour}", inline=True)
      embed.add_field(name='**Creation Date:**', value=f"{created_on}", inline=False)
      embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
      embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
      embed.set_footer(text="Requested by {}".format(ctx.message.author))
      await ctx.send(embed=embed)

  @commands.command(aliases=['guildinfo', 'si'])
  async def serverinfo(self, ctx):
      embed = discord.Embed(color=0x2f3136)
      embed.add_field(name='**Owner:**', value=f"{ctx.guild.owner}", inline=False)
      embed.add_field(name='**Region:**', value=f"{ctx.guild.region}", inline=False)
      embed.add_field(name='**Member Count:**', value=f"{ctx.guild.member_count}", inline=False)
      embed.add_field(name='**Creation Date:**', value=f"{ctx.guild.created_at.strftime('%d %b %Y %H:%M')}", inline=False)
      embed.add_field(name='**Roles:**', value="{}".format(len(ctx.guild.roles)-1), 	inline=False)
      embed.add_field(name='**Text Channels:**', value="{}".format(len(ctx.guild.text_channels)), 	inline=True)
      embed.add_field(name='**Voice Channels:**', value="{}".format(len(ctx.guild.voice_channels)), 	inline=True)
      if ctx.guild.system_channel:
          embed.add_field(name='**Standard Channel:**', value=f'#{ctx.guild.system_channel}', inline=False)
      embed.add_field(name='**AFK Voice Timeout:**', value=f'{int(ctx.guild.afk_timeout / 60)} minutes', inline=True)
      embed.add_field(name='**AFK Channel:**', value=f'#{ctx.guild.afk_channel}', inline=True)
      embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
      embed.set_thumbnail(url=ctx.guild.icon_url)
      embed.set_footer(text="Requested by {}".format(ctx.message.author))
      await ctx.send(embed=embed)
