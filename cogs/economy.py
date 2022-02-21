from discord.ext import commands
import discord
import datetime
import os
import praw
import random
import requests
from requests.exceptions import HTTPError

r = praw.Reddit(client_id="7oE7yB5GJJua2Q", client_secret="ooidPB-ETJxbRflpja6a65KX03g", user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36', username="PhantomVipermon")

class economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hentai(self, ctx):

        if hasattr(ctx.message.channel, "nsfw"):
            channel_nsfw = ctx.message.channel.nsfw
        else:
            channel_nsfw = str(ctx.message.channel.type) == "private"

        if channel_nsfw:
            sub = r.subreddit("hentai")
            #posts = [post for post in sub.hot(limit=50)]
            #random_post_number = random.randint(0, 50)
            #random_post = posts[random_post_number]
            await ctx.send(sub.random().url)
            #await ctx.send(random_post.url)
        else:
            await ctx.send("U can't use that command here!")

    @commands.command()
    async def porngif(self, ctx):

        if hasattr(ctx.message.channel, "nsfw"):
            channel_nsfw = ctx.message.channel.nsfw
        else:
            channel_nsfw = str(ctx.message.channel.type) == "private"

        if channel_nsfw:
            sub = r.subreddit('porngifs')
            await ctx.send(sub.random().url)
        else:
            await ctx.send("U can't use that command here!")
