from discord.ext import commands
import datetime
import discord
import os
start_time = datetime.datetime.utcnow()



class extra(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

 
  @commands.group(invoke_without_command=True)
  async def help(self, ctx):
      embed = discord.Embed(description="",color=0x2f3136)

      embed.add_field(name="HELP MENU", value=f"• Prefix for this server is .\n• Type .help <command> for more info. \n• [Invite Me](https://discord.com/api/oauth2/authorize?client_id=938388484884488483&permissions=8&scope=bot%20applications.commands) ", inline=False)      
      embed.add_field(name="**__General Commands__**", value=f"\n<a:z_arrow:936618068724051978> **`Utility`** \n<a:z_arrow:936618068724051978> **`Security`** \n<a:z_arrow:936618068724051978> **`Music`**\n<a:z_arrow:936618068724051978> **`Moderation`**\n<a:z_arrow:936618068724051978> **`Features`**", inline=False)
      await ctx.reply(embed=embed)
  
  @help.command()
  async def moderation(self, ctx):
      embed = discord.Embed(description=f"**Zeon Help**",color=0x2f3136)

      embed.add_field(name=f"**__Moderation Commands__**", value=f" Kick \n```Kick's a member``` \n\n Unbanall \n```Unban's all banned user's in the guild``` \n\n Mute \n```Mute's a member``` \n\n Unmute \n```Unmute's a member``` \n\nLockall \n```lock all server``` \nunlockall \n```Unlock all server```", inline=False)
      embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024')
      await ctx.send(embed=embed)   

  @help.command()
  async def utility(self, ctx):
      embed = discord.Embed(description=f"**Zeon Help**",color=0x2f3136)

      embed.add_field(name=f"**__Utility Commands__**", value=f"avatar \n```Show's avatar of member```\n\nserverinfo \n```Show's Serverinfo``` \n\nuserinfo \n```Show's info of a user``` \n\nmembercount \n```Show's member's in a server``` \n\nnuke \n```Delete the channel and recreate it``` \npruneest \n```Show's estimate prune members in your server (with roles 1day)``` \n\n<a:processing:887677851824979988>pruneestr \n```Show's estimate prune members in your server (without roles 1day)```", inline=False)
      embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024')
      await ctx.send(embed=embed)        
  @help.command()
  async def security(self, ctx):
      embed = discord.Embed(description=f"**Zeon Help**",color=0x2f3136)

      embed.add_field(name=f"**__Security Information__**", value=f" ```The Bot has Pre-Setup that helps to protect a server from getting nuked/wizzed. Just Simply drag my role to top```  \n\n ```Get More Information >features``` \n  ```Limit =1``` \n  ```Punishment =Ban``` \n```RECOVER = TRUE```", inline=False)
      embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024')
      await ctx.reply(embed=embed)

