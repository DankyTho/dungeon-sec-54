import discord, praw
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv
import os

load_dotenv()
REDDIT_ID = os.getenv('REDDIT_ID')
REDDIT_SECRET = os.getenv('REDDIT_SECRET')
PREFIX = os.getenv('PREFIX')

r = praw.Reddit(user_agent='For fetching reddit submissions',  
                client_id=REDDIT_ID,
                client_secret=REDDIT_SECRET)
 
class image(commands.Cog, name = 'Reddit'):
    '''Reddit Posts'''
 
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(f'{PREFIX}r/'):
            ErrEmbed = discord.Embed(title='ERR', description='No such subreddit', color=discord.Color.red())
            NSFWEmbed = discord.Embed(title='ERR', description='NSFW content is not allowed in this channel', color=discord.Color.red())
            try:
                submission = r.subreddit(str(message.content).replace(f'{PREFIX}r/', '')).random()
            except:
                await message.channel.send(embed=ErrEmbed)
                
            Embed = discord.Embed(title=submission.title, description=submission.selftext)
            Embed.set_image(url=submission.url)
            if not submission.over_18 or message.channel.is_nsfw():
                await message.channel.send(embed=Embed)
            else:
                await message.channel.send(embed=NSFWEmbed)

                
    @commands.command(name='r/')
    async def reddit(self, ctx, arg):
        '''Sends a random hot submission from a specified subreddit. Example: &r/redditdev'''
        # Placeholder. The actual code is at lines 22 to 37
 

    @commands.command(name='memes')
    async def memes(self, ctx):
        '''Sends random a hot meme from r/memes'''
        submission = r.subreddit('memes').random()
 
        Embed = discord.Embed(title=submission.title)
        Embed.set_image(url=submission.url)
        await ctx.send(embed=Embed)

      
    @commands.command(name='dankmemes')
    async def dankmemes(self, ctx):
        '''Sends a random hot meme from r/dankmemes'''
        submission = r.subreddit("dankmemes").random()
 
        Embed = discord.Embed(title=submission.title)
        Embed.set_image(url=submission.url)
        await ctx.send(embed=Embed)

      
    @commands.command(name='caveposts')
    async def caveposts(self, ctx):
        '''Sends a random hot submission from r/chatcave'''
        submission = r.subreddit("chatcave").random()
 
        Embed = discord.Embed(title=submission.title)
        Embed.set_image(url=submission.url)
        await ctx.send(embed=Embed)
    
    
    @commands.command(name='foodporn')
    async def foodporn(self, ctx):
        '''Sends a random hot submission from r/FoodPorn'''
        submission = r.subreddit('foodporn').random()
 
        Embed = discord.Embed(title=submission.title)
        Embed.set_image(url=submission.url)
        await ctx.send(embed=Embed)
    
    
    @commands.command(name='webcomics')
    async def webcomics(self, ctx):
        '''Sends a random hot webcomic from r/webcomics'''
        submission = r.subreddit('webcomics').random()
 
        Embed = discord.Embed(title=submission.title)
        Embed.set_image(url=submission.url)
        await ctx.send(embed=Embed)
    
    
    @commands.command(name='showerthoughts')
    async def showerthoughts(self, ctx):
        '''Sends a random hot submission from r/showerthoughts'''
        submission = r.subreddit('showerthoughts').random()
 
        Embed = discord.Embed(title=submission.title)
        Embed.set_image(url=submission.url)
        await ctx.send(embed=Embed)
