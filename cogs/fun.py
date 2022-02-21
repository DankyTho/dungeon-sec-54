from discord.ext import commands
import discord
import requests
import aiohttp
import datetime
from random import randint
from time import sleep
import random
import os

snipes = dict()

def snipe_embed(context_channel, message, user):
	if message.author not in message.guild.members or message.author.color == discord.Colour.default():
		embed = discord.Embed(title='Deleted message:',description = message.content, timestamp = message.created_at)
	else:
		embed = discord.Embed(title='Deleted message:',description = message.content, timestamp = message.created_at)
	embed.set_author(name = str(message.author), icon_url = message.author.avatar_url)
	if message.attachments:
		embed.add_field(name = 'Attachment(s)', value = '\n'.join([attachment.filename for attachment in message.attachments]) + '\n\n__Attachment URLs are invalidated once the message is deleted.__')
	if message.channel != context_channel:
		embed.set_footer(text = 'Sniped by: ' + str(user) + ' | in channel: #' + message.channel.name)
	else: 
		embed.set_footer(text = 'Sniped by: ' + str(user))
	return embed

def RandomColor(): 
    randcolor = discord.Color(random.randint(0x000000, 0xFFFFFF))
    return randcolor

class fun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.snipes = {}
    self.editsniped = {}

  @commands.Cog.listener()
  async def on_guild_remove(self, guild):
      try:
          del snipes[guild.id]
      except KeyError:
          pass

  @commands.Cog.listener()
  async def on_guild_channel_delete(self, channel):
      try:
          del snipes[channel.guild.id][channel.id]
      except KeyError:
          pass

  @commands.Cog.listener()
  async def on_message_delete(self, message):
      if message.guild and not message.author.bot:
          try:
              snipes[message.guild.id][message.channel.id] = message
          except KeyError:
              snipes[message.guild.id] = {message.channel.id: message}

  @commands.Cog.listener()
  async def on_message_edit(self, before, after):
      try:
          if not before.author.bot:
              srvid = before.guild.id
              chid = before.channel.id
              author = before.author
              author_mention = before.author.mention
              msg_before = before.content
              msg_after = after.content
              #print(f"server:{srvid}, channel:{chid}, author:{author}, before:{msg_before}, after:{msg_after}")
              self.editsniped.update({
                  srvid : {
                      chid : {
                          'Sender':author,
                          'Mention':author_mention,
                          'Before':msg_before,
                          'After':msg_after
                      }
                  }
              })
      except:
          pass
                

  @commands.command()
  async def kiss(self, ctx, user: discord.Member = None):
      if user is None:
          await ctx.send(f"`{ctx.author}` you must mention a user to do that!")
      else:
          r = requests.get("https://nekos.life/api/v2/img/kiss")
          res = r.json()
          embed = discord.Embed(
              timestamp=datetime.datetime.utcnow(),
              description=f"{ctx.author.mention} kisses {user.mention}",
          )
          embed.set_image(url=res['url'])
          embed.set_footer(text=f"{ctx.guild.name}")
    
          await ctx.send(embed=embed)

  @commands.command()
  async def tickle(self, ctx, user: discord.Member = None):
      if user is None:
          await ctx.send(f"`{ctx.author}` you must mention a user to do that!")
      else:
          r = requests.get("https://nekos.life/api/v2/img/tickle")
          res = r.json()
          embed = discord.Embed(
              timestamp=datetime.datetime.utcnow(),
              description=f"{ctx.author.mention} tickle {user.mention}",
          )
          embed.set_image(url=res['url'])
          embed.set_footer(text=f"{ctx.guild.name}")
    
          await ctx.send(embed=embed)

  @commands.command()
  async def hug(self, ctx, user: discord.Member = None):
      if user is None:
          await ctx.send(f"`{ctx.author}` you must mention a user to do that!")
      else:
          r = requests.get("https://nekos.life/api/v2/img/hug")
          res = r.json()
          embed = discord.Embed(
              timestamp=datetime.datetime.utcnow(),
              description=f"{ctx.author.mention} hugs {user.mention}",
          )
          embed.set_image(url=res['url'])
          embed.set_footer(text=f"{ctx.guild.name}")
    
          await ctx.send(embed=embed)

  @commands.command()
  async def slap(self, ctx, user: discord.Member = None):
      if user is None:
          await ctx.send(f"`{ctx.author}` you must mention a user to do that!")
      else:
          r = requests.get("https://nekos.life/api/v2/img/slap")
          res = r.json()
          embed = discord.Embed(
              timestamp=datetime.datetime.utcnow(),
              description=f"{ctx.author.mention} slapped {user.mention}",
          )
          embed.set_image(url=res['url'])
          embed.set_footer(text=f"{ctx.guild.name}")
    
          await ctx.send(embed=embed)

  @commands.command()
  async def pat(self, ctx, user: discord.Member = None):
      if user is None:
          await ctx.send(f"`{ctx.author}` you must mention a user to do that!")
      else:
          r = requests.get("https://nekos.life/api/v2/img/pat")
          res = r.json()
          embed = discord.Embed(
              timestamp=datetime.datetime.utcnow(),
              description=f"{ctx.author.mention} pats {user.mention}",
          )
          embed.set_image(url=res['url'])
          embed.set_footer(text=f"{ctx.guild.name}")
    
          await ctx.send(embed=embed)

  @commands.command()
  async def feed(self, ctx, user: discord.Member = None):
      if user is None:
          await ctx.send(f"`{ctx.author}` you must mention a user to do that!")
      else:
          r = requests.get("https://nekos.life/api/v2/img/feed")
          res = r.json()
          embed = discord.Embed(
              timestamp=datetime.datetime.utcnow(),
              description=f"{ctx.author.mention} feeds {user.mention}",
          )
          embed.set_image(url=res['url'])
          embed.set_footer(text=f"{ctx.guild.name}")
    
          await ctx.send(embed=embed)

  @commands.command()
  async def pet(self, ctx, user: discord.Member = None):
      if user is None:
          await ctx.send(f"`{ctx.author}` you must mention a user to do that!")
      else:
          r = requests.get("https://nekos.life/api/v2/img/pat")
          res = r.json()
          embed = discord.Embed(
              timestamp=datetime.datetime.utcnow(),
              description=f"{ctx.author.mention} pets {user.mention}",
          )
          embed.set_image(url=res['url'])
          embed.set_footer(text=f"{ctx.guild.name}")
    
          await ctx.send(embed=embed)

  @commands.command(aliases=['gay'])
  async def howgay(self, ctx, *, person):
      embed = discord.Embed()
      responses = ['50',
                  '75',
                  '25',
                  '1',
                  '3',
                  '5',
                  '10',
                  '65',
                  '60',
                  '85',
                  '30',
                  '40',
                  '45',
                  '80',
                  '100',
                  '150',
                  '1000']
      embed.description = f'**{person} is {random.choice(responses)}% Gay** :rainbow:'
      embed.set_footer(text=f'How gay are you? - {ctx.author.name}')

      await ctx.send(embed = embed)
  @howgay.error 
  async def howgay_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
          embed = discord.Embed(title="*You must mention someone to howgay!*")
          await ctx.send(embed=embed)

  @commands.command()
  async def slots(self, ctx):
      emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
      a = random.choice(emojis)
      b = random.choice(emojis)
      c = random.choice(emojis)
      slotmachine = f"[ {a} {b} {c} ]\n{ctx.author.mention}"
      if (a == b == c):
          await ctx.send(embed=discord.Embed(title="Slot machine", description=f"{slotmachine} All Matching! You Won!"))
      elif (a == b) or (a == c) or (b == c):
          await ctx.send(embed=discord.Embed(title="Slot machine", description=f"{slotmachine} 2 Matching! You Won!"))
      else:
          await ctx.send(embed=discord.Embed(title="Slot machine", description=f"{slotmachine} No Matches! You Lost!"))

  @commands.command(aliases = ['dick'])
  async def penis(self, ctx, user: discord.Member = None):
      if user is None:
          user = ctx.author
      size = random.randint(1, 15)
      dong = ""
      for _i in range(0, size):
          dong += "="
      em = discord.Embed(title=f"**{user}'s** Dick size", description=f"8{dong}D")
      em.set_footer(text=f'whats {user} dick size?')
      await ctx.send(embed=em)

  @commands.command()
  async def meme(self, ctx):
      embed = discord.Embed(title="""Take some memes""")

      async with aiohttp.ClientSession() as cs:
          async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
              res = await r.json()
              embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
              embed.set_footer(text=f'Random Meme:')
              await ctx.send(embed=embed)

  @commands.command()
  async def cat(self, ctx):
      embed = discord.Embed(title="""Here's a cat""")

      async with aiohttp.ClientSession() as cs:
          async with cs.get('http://aws.random.cat/meow') as r:
              res = await r.json()
              embed.set_image(url=res['file'])
              embed.set_footer(text=f'Random Cats:')

              await ctx.send(embed=embed)

  @commands.command(aliases=['8ball'])
  async def eightball(self, ctx, *, question: str = None):
      '''Ask the 8 ball a question'''
      if not question:
          return await ctx.send("**Inform a question!**")
      elif not question.endswith('?'):
          return await ctx.send('**You must ask a question!**')

      responses = ["https://thumb-p4.xhcdn.com/a/tMP48vfoim2voZrfZ7hZVA/000/473/075/594_1000.gif"]

      num = randint(0, len(responses) - 1)
      if num < 10:
          em = discord.Embed()
      elif num < 15:
          em = discord.Embed()
      else:
          em = discord.Embed()

      response = responses[num]

      em.title = f"🎱**{question}**"
      em.set_image = response
      await ctx.send(embed=em)

  @commands.command()
  @commands.has_permissions(send_messages=True)
  @commands.guild_only()
  async def snipe(self, ctx, channel: discord.TextChannel = None):
      if not channel:
          channel = ctx.channel

      if not ctx.author.guild_permissions.send_messages or not ctx.author.permissions_in(channel).read_messages or not ctx.author.permissions_in(channel).read_message_history:
          return
      try:
          sniped_message = snipes[ctx.guild.id][channel.id]
      except KeyError:
          await ctx.send("There's nothing to snipe!")
      else:
          await ctx.send(embed = snipe_embed(ctx.channel, sniped_message, ctx.author))
    
  @commands.command()
  @commands.guild_only()
  async def esnipe(self, ctx, message):
      """
      Similar to deletesnipe, this command allows you to see edited message.
      Please do not spam this command as well!
      """
      try:
          author = self.editsniped[ctx.guild.id][ctx.channel.id]["Sender"]
          before = self.editsniped[ctx.guild.id][ctx.channel.id]["Before"]
          after = self.editsniped[ctx.guild.id][ctx.channel.id]["After"]

          if before and after:
              emb = discord.Embed(timestamp = message.created_at)
              emb.set_author(name="Edited Message:", icon_url=ctx.message.author.avatar_url)
              emb.add_field(name="Before:", value=before)
              emb.add_field(name="After:", value=after)
              emb.set_footer(text=f"Sniped by: {ctx.message.author}")
              await ctx.send(embed=emb)
          else:
              emb = discord.Embed(title="Sniped!")
              emb.add_field(name="Author:", value=author, inline=False)
              emb.add_field(name="Before:", value="Empty Message.")
              emb.add_field(name="After:", value="Empty Message.")
              emb.set_footer(text=f"Sniped by: {ctx.message.author}")
              await ctx.send(embed=emb)
          self.editsniped.popitem()
      except KeyError:
          await ctx.send("There's nothing to esnipe!")
          return
      except discord.NotFound:
          pass
