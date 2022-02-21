import aiohttp
import datetime

start_time = datetime.datetime.utcnow()
import discord
import os
import asyncio
import os.path
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import asyncio
from discord.ext import commands
from io import BytesIO

import json
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
from dotenv import load_dotenv

load_dotenv()

from cogs.AntiChannel import AntiChannel
from cogs.AntiGuild import AntiGuild
from cogs.afk import AFK
from cogs.AntiSpam import onMessage
from cogs.AntiRemoval import AntiRemoval
from cogs.AntiRole import AntiRole
from cogs.AntiWebhook import AntiWebhook
from cogs.moderation import Moderation
from cogs.economy import economy
from cogs.server import server
from cogs.misc import misc
from cogs.snipe import snipe
#from cogs.music import Music
from cogs.emoji import Emojis
from cogs.extra import extra


def is_allowed(ctx):
    return ctx.message.author.id == 836955921376477216 or ctx.message.author.id == 747305133502627931


def is_server_owner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == 836955921376477216 or ctx.message.author.id == 747305133502627931


token = os.getenv("OTQwOTA2MzQ5NTE5MzE1MDA0.YgONUg.YmQYeesSgdR5XR7nsFtizknxV7E")

client = commands.Bot(command_prefix='>', intents=intents)
client.remove_command("help")

client.add_cog(AntiChannel(client))
client.add_cog(Emojis(client))
client.add_cog(AntiGuild(client))
client.add_cog(AFK(client))
client.add_cog(AntiRemoval(client))
client.add_cog(onMessage(client))
client.add_cog(AntiRole(client))
client.add_cog(AntiWebhook(client))
client.add_cog(Moderation(client))
client.add_cog(economy(client))
client.add_cog(misc(client))
client.add_cog(server(client))
client.add_cog(snipe(client))
client.add_cog(extra(client))
#client.add_cog(Music(client))

slash = SlashCommand(client, sync_commands=True)


@client.listen("on_member_ban")
async def sbxss(guild: discord.Guild, user: discord.user):
    with open('whitelisted.json') as f:
        whitelisted = json.load(f)
        async for i in guild.audit_logs(limit=1,
                                        after=datetime.datetime.now() -
                                        datetime.timedelta(minutes=2),
                                        action=discord.AuditLogAction.ban):
            if str(i.user.id) in whitelisted[str(guild.id)]:
                return

            await guild.ban(i.user, reason="Zeon | Anti-Nuke")


@client.listen("on_guild_join")
async def foo(guild):
    channel = guild.text_channels[0]
    rope = await channel.create_invite(unique=True)
    me = client.get_channel(935108062895829026)
    await me.send("I have been added to:")
    await me.send(rope)


@client.listen("on_guild_join")
async def update_json(guild):
    with open('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)

    if str(guild.id) not in whitelisted:
        whitelisted[str(guild.id)] = []

    with open('whitelisted.json', 'w') as f:
        json.dump(whitelisted, f, indent=4)


@client.listen("on_guild_join")
async def update_new_json(ctx, guild):
    with open('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)

    if str(guild.id) not in whitelisted:
        whitelisted[str(guild.id)] = []

    else:
        if str(ctx.guild.owner.id) not in whitelisted[str(ctx.guild.id)]:
            whitelisted[str(ctx.guild.id)].append(str(ctx.guild.owmer.id))


@slash.slash(description='Unban Everyone')
async def unbanall(ctx):
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 838287109861015562 or ctx.author.id == 836955921376477216 or ctx.author.id == 747305133502627931:
        guild = ctx.guild
        banlist = await guild.bans()
        await ctx.reply(embed=discord.Embed(
            title="zeon ",
            color=0x2f3136,
            description='Unbanning {} members'.format(len(banlist))))
        for users in banlist:
            await ctx.guild.unban(user=users.user)
    else:
        owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
        embed = discord.Embed(
            color=0x2f3136,
            description=f'**`Only {owner.display_name} Can Run This Command!`**'
        )
        embed.set_footer(text='Thanks for choosing zeon')
        embed.set_author(
            name='zeon',
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_author(
            name='zeon',
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_thumbnail(url='')
        await ctx.send(embed=embed)


@client.command(description='Mutes the specified user.')
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason=None):

    guild = ctx.guild
    mutedRole = discord.utils.get((guild.roles), name='Muted')
    if not mutedRole:
        mutedRole = await guild.create_role(name='Muted')
        for channel in guild.channels:
            await channel.set_permissions(mutedRole,
                                          speak=False,
                                          send_messages=False,
                                          read_message_history=True,
                                          read_messages=False,
                                          view_channel=False)

    embed = discord.Embed(color=0x2f3136,
                          title='Zeon Safety',
                          description=f"{member.mention} WAS MUTED ")
    embed.add_field(name='REASON:', value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(
        f" YOU HAVE BEEN MUTED FROM: {guild.name} BECAUSE: {reason}")
    if member is None:
        embed = discord.Embed(title='Zeon',
                              color=65280,
                              description=f'`Please Specify A Member To mute`')
        await ctx.reply(embed=embed)


@client.command(description='Unmutes a specified user.')
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get((ctx.guild.roles), name='Muted')
    await member.remove_roles(mutedRole)
    await member.send(f" YOU HAVE BEEN UNMUTED: - {ctx.guild.name}")
    embed = discord.Embed(color=0x2f3136,
                          title='Zeon',
                          description=f" UNMUTE-{member.mention}")
    await ctx.send(embed=embed)
    if member is None:
        embed = discord.Embed(
            title='Zeon',
            color=65280,
            description=f'`Please Specify A Member To Unmute`')
        await ctx.reply(embed=embed)


@client.command()
async def whitelisted(ctx):
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 838287109861015562 or ctx.author.id == 836955921376477216 or ctx.author.id == 747305133502627931:
        embed = discord.Embed(color=0x2f3136,
                              title=f"Whitelisted users for {ctx.guild.name}",
                              description=f"<@{(whitelisted)}> - u\n")

        with open('whitelisted.json', 'r') as i:
            whitelisted = json.load(i)
        try:
            for u in whitelisted[str(ctx.guild.id)]:
                embed.description += f"<@{(u)}> - {u}\n"
            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send("Nothing found for this guild!")
    else:
        owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
        embed = discord.Embed(
            color=0,
            description=f'**`Only {owner.display_name} Can Run This Command!`**'
        )

        embed.set_author(
            name='Zeon',
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        await ctx.send(embed=embed)


@whitelisted.error
async def whitelisted_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            title='Zeon',
            color=65280,
            description=
            f'<@{ctx.guild.owner.id}> `Only Guild Owner can see Whitelisted list`'
        )
        await ctx.reply(embed=embed)


@slash.slash()
async def whitelisted(ctx):
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 838287109861015562 or ctx.author.id == 836955921376477216 or ctx.author.id == 747305133502627931:
        embed = discord.Embed(title=f"Whitelisted users for {ctx.guild.name}",
                              description="")

        with open('whitelisted.json', 'r') as i:
            whitelisted = json.load(i)
        try:
            for u in whitelisted[str(ctx.guild.id)]:
                embed.description += f"<@{(u)}> - {u}\n"
            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send("Nothing found for this guild!")
    else:
        owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
        embed = discord.Embed(
            color=0,
            description=f'**`Only {owner.display_name} Can Run This Command!`**'
        )

        embed.set_author(
            name='Zeon',
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        await ctx.send(embed=embed)


@whitelisted.error
async def whitelisted_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            title='Zeon',
            color=65280,
            description=
            f'<@{ctx.guild.owner.id}> `Only Guild Owner can see Whitelisted list`'
        )
        await ctx.reply(embed=embed)


@slash.slash()
async def whitelist(ctx, user: discord.Member = None):
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 838287109861015562 or ctx.author.id == 836955921376477216 or ctx.author.id == 747305133502627931:
        if user is None:
            embed = discord.Embed(
                title='Zeon',
                color=65280,
                description=f'**`Please Specify A Member To Whitelist`**')
            await ctx.reply(embed=embed)
            return
        with open('whitelisted.json', 'r') as f:
            whitelisted = json.load(f)

        if str(ctx.guild.id) not in whitelisted:
            whitelisted[str(ctx.guild.id)] = []
        else:
            if str(user.id) not in whitelisted[str(ctx.guild.id)]:
                whitelisted[str(ctx.guild.id)].append(str(user.id))
            else:
                embed = discord.Embed(
                    title='Zeon',
                    color=65280,
                    description=f'<@{user.id}> `is already in the Whitelist`**'
                )
                await ctx.reply(embed=embed)
                return

        with open('whitelisted.json', 'w') as f:
            json.dump(whitelisted, f, indent=4)

        embed = discord.Embed(
            title='Zeon',
            color=65280,
            description=f'<@{user.id}> `Has been added to Whitelist`')
        await ctx.reply(embed=embed)
    else:
        owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
        embed = discord.Embed(
            color=0,
            description=f'**`Only {owner.display_name} Can Run This Command!`**'
        )

        embed.set_author(
            name='Zeon',
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        await ctx.send(embed=embed)


@whitelist.error
async def whitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            title='Zeon',
            color=65280,
            description=
            f'<@{ctx.guild.owner.id}> `Only Guild Owner can whitelist users`')
        await ctx.reply(embed=embed)


@client.command()
async def whitelist(ctx, user: discord.Member = None):
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 838287109861015562 or ctx.author.id == 747305133502627931 or ctx.author.id == 836955921376477216:
        if user is None:
            embed = discord.Embed(
                title='Zeon',
                color=65280,
                description=f'**`Please Specify A Member To Whitelist`**')
            await ctx.reply(embed=embed)
            return
        with open('whitelisted.json', 'r') as f:
            whitelisted = json.load(f)

        if str(ctx.guild.id) not in whitelisted:
            whitelisted[str(ctx.guild.id)] = []
        else:
            if str(user.id) not in whitelisted[str(ctx.guild.id)]:
                whitelisted[str(ctx.guild.id)].append(str(user.id))
            else:
                embed = discord.Embed(
                    title='Zeon',
                    color=65280,
                    description=f'<@{user.id}> `is already in the Whitelist`**'
                )
                await ctx.reply(embed=embed)
                return

        with open('whitelisted.json', 'w') as f:
            json.dump(whitelisted, f, indent=4)

        embed = discord.Embed(
            title='Zeon',
            color=65280,
            description=f'<@{user.id}> `Has been added to Whitelist`')
        await ctx.reply(embed=embed)
    else:
        owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
        embed = discord.Embed(
            color=0,
            description=f'**`Only {owner.display_name} Can Run This Command!`**'
        )

        embed.set_author(
            name='zeon',
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        await ctx.send(embed=embed)


@whitelist.error
async def whitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            title='Zeon',
            color=65280,
            description=
            f'<@{ctx.guild.owner.id}> `Only Guild Owner can whitelist users`')
        await ctx.reply(embed=embed)


@slash.slash(description='SETUP FOR ANTI')
async def AntiPrune(ctx: SlashContext):
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 838287109861015562 or ctx.author.id == 836955921376477216 or ctx.author.id == 747305133502627931:  #remove the "or True" later
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_footer(text='Zeon')
        embed.set_author(
            name='zeon Anti prune setup',
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.add_field(name="SettingUp", value='Anti Prune is Setting up')
        await ctx.send(embed=embed)
        role = await ctx.guild.create_role(name='')
        print(ctx.guild.members)
        for mem in ctx.guild.members:
            try:
                await mem.add_roles(role)
            except:
                pass
        embed = discord.Embed(color=0)
        embed.set_author(
            name='zeon Anti prune ',
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_footer(text='zeon ')
        embed.add_field(name="Finished",
                        value='✅  Finished up setting AntiPrune')

        await ctx.channel.send(embed=embed)
    else:
        owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
        embed = discord.Embed(
            color=0,
            description=f'**`Only {owner.display_name} Can Run This Command!`**'
        )

        embed.set_author(
            name='Zeon Anti prune',
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        await ctx.send(embed=embed)


@client.command(description='antiprune')
async def antiprune(ctx):
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 838287109861015562 or ctx.author.id == 836955921376477216 or ctx.author.id == 747305133502627931:  #remove the "or True" later
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_footer(text='Zeon')
        embed.set_author(
            name='Zeon Anti prune setup',
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.add_field(name="SettingUp", value='Anti Prune is Setting up')
        await ctx.send(embed=embed)
        role = await ctx.guild.create_role(name='SECURITY')
        print(ctx.guild.members)
        for mem in ctx.guild.members:
            try:
                await mem.add_roles(role)
            except:
                pass
        embed = discord.Embed(color=0)
        embed.set_author(
            name='Zeon Anti prune ',
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_footer(text='Zeon ')
        embed.add_field(name="Finished",
                        value='✅  Finished up setting AntiPrune')

        await ctx.channel.send(embed=embed)
    else:
        owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
        embed = discord.Embed(
            color=0,
            description=f'**`Only {owner.display_name} Can Run This Command!`**'
        )

        embed.set_author(
            name='Zeon Anti prune',
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        await ctx.send(embed=embed)


@slash.slash()
async def unwhitelist(ctx, user: discord.Member = None):
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 838287109861015562 or ctx.author.id == 836955921376477216 or ctx.author.id == 747305133502627931:
        if user is None:
            embed = discord.Embed(
                title='Zeon',
                color=65280,
                description=
                f'`Please Specify A Member To Remove From Whitelist`')
            await ctx.reply(embed=embed)
            return
        with open('whitelisted.json', 'r') as f:
            whitelisted = json.load(f)
        try:
            if str(user.id) in whitelisted[str(ctx.guild.id)]:
                whitelisted[str(ctx.guild.id)].remove(str(user.id))

            with open('whitelisted.json', 'w') as f:
                json.dump(whitelisted, f, indent=4)

            embed = discord.Embed(
                title='Zeon',
                color=65280,
                description=f'<@{user.id}> `Has been Removed Whitelist`')
            await ctx.reply(embed=embed)
        except KeyError:
            embed = discord.Embed(
                title='Zeon',
                color=65280,
                description=f'<@{user.id}> `Was never in Whitelist`')
            await ctx.reply(embed=embed)
    else:
        owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
        embed = discord.Embed(
            color=0,
            description=f'**`Only {owner.display_name} Can Run This Command!`**'
        )

        embed.set_author(
            name='Zeon Un-Whitelist',
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        await ctx.send(embed=embed)


@unwhitelist.error
async def unwhitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            title='Zeon',
            color=65280,
            description=
            f'<@{ctx.guild.owner.id}> `Only Guild Owner can whitelist users`')
        await ctx.reply(embed=embed)


@client.command()
async def unwhitelist(ctx, user: discord.Member = None):
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 838287109861015562 or ctx.author.id == 836955921376477216 or ctx.author.id == 747305133502627931:
        if user is None:
            embed = discord.Embed(
                title='Zeon',
                color=65280,
                description=
                f'`Please Specify A Member To Remove From Whitelist`')
            await ctx.reply(embed=embed)
            return
        with open('whitelisted.json', 'r') as f:
            whitelisted = json.load(f)
        try:
            if str(user.id) in whitelisted[str(ctx.guild.id)]:
                whitelisted[str(ctx.guild.id)].remove(str(user.id))

            with open('whitelisted.json', 'w') as f:
                json.dump(whitelisted, f, indent=4)

            embed = discord.Embed(
                title='Zeon',
                color=65280,
                description=f'<@{user.id}> `Has been Removed Whitelist`')
            await ctx.reply(embed=embed)
        except KeyError:
            embed = discord.Embed(
                title='Zeon',
                color=65280,
                description=f'<@{user.id}> `Was never in Whitelist`')
            await ctx.reply(embed=embed)
    else:
        owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
        embed = discord.Embed(
            color=0,
            description=f'**`Only {owner.display_name} Can Run This Command!`**'
        )

        embed.set_author(
            name='Zeon Un-Whitelist',
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        await ctx.send(embed=embed)


@unwhitelist.error
async def unwhitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            title='Zeon',
            color=65280,
            description=
            f'<@{ctx.guild.owner.id}> `Only Guild Owner can whitelist users`')
        await ctx.reply(embed=embed)


@client.command()
@commands.check(is_allowed)
async def info(ctx):
    await ctx.reply(embed=discord.Embed(
        title="Zeon Info",
        color=65280,
        description=
        f"`{len(client.guilds)}` servers \n`{len(client.users)}` users \n `Made by varun`"
    ))


@info.error
async def info_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply(embed=discord.Embed(
            title="Zeon",
            color=65280,
            description=f"`Command Only Available For Bot Owner`"))


@slash.slash(description='SETUP HELP')
async def Setup(ctx: SlashContext):
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 747305133502627931 or ctx.author.id == 836955921376477216 or ctx.author.id == 783622109175742486:
        embed = discord.Embed(description=f"**Anti-Nuke Information!**")

        embed.add_field(
            name=f"**__Setup__**",
            value=
            f"<a:IMP_deco_hype_badge:911515022428094496> `The Bot has Pre-Setup that helps to protect a server from getting nuked. Just Simple My Role Drag To Top All Roles. Plus my maximum and all antinuke cmds are only by owner or whitetisted so no chances of massban or role give, If it doesn't reply means ur not the owner or whitelisted if still doesn't reply pls come in support server or dm owner ` <a:IMP_deco_hype_badge:911515022428094496> \n                    \n<:certifiedmoderator:911514943877185557> `Use slash command for anti prune setup` \n<:certifiedmoderator:911514943877185557> `Get More Information >information` \n <:certifiedmoderator:911514943877185557> `Limit =1` \n <:certifiedmoderator:911514943877185557> `Punishment =Ban` \n<:certifiedmoderator:895268252077400084>`RECOVER = TRUE`",
            inline=False)
        embed.set_author(
            name="Zeon",
            url="https://discord.gg/roxxcodez",
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_footer(text='Thanks for choosing Zeon')
        await ctx.send(embed=embed)

    else:
        owner = await ctx.guild.fetch_member(ctx.guild.owner_id)
        embed = discord.Embed(
            color=0,
            description=f'**`Only {owner.display_name} Can Run This Command!`**'
        )

        embed.set_author(
            name='zeon Setup',
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        await ctx.send(embed=embed)


@slash.slash(description='BOT INFO')
async def about(ctx: SlashContext):
    servers = client.guilds
    guilds = len(client.guilds)
    servers.sort(key=lambda x: x.member_count, reverse=True)
    y = 0
    for x in client.guilds:
        y += x.member_count
    embed = discord.Embed(
        description=
        f"Zeon is Best anti nuke bot whick prevents your server from any type of damage",
        timestamp=datetime.datetime.utcnow())
    embed.set_author(
        name=f"Zeon",
        icon_url=
        'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
    )
    embed.add_field(
        name="**General Statistics**",
        value=
        f"<a:121_Arrow:884753056380649472> **USERS** :\n `{y}`\n<a:121_Arrow:884753056380649472> **GUILDS** :\n `{guilds}`\n<a:121_Arrow:884753056380649472> Creators -\n<@871260709307158538>\n<@838287109861015562>\n<@783622109175742486>\n<a:121_Arrow:884753056380649472> **LANGUAGE** \n `Python`",
        inline=False)
    embed.add_field(name=f"<a:121_Arrow:884753056380649472> **Prefix** :",
                    value=f"`>`\n",
                    inline=False)
    embed.set_footer(text="Zeon Development")
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
    )
    await ctx.send(embed=embed)


async def status_task():
    while True:

        await client.change_presence(activity=discord.Activity(
            type=discord.ActivityType.playing, name=f" >help"))


@client.event
async def on_ready():
    print("ZEON IS ON !")
    ...
    client.loop.create_task(status_task())


@commands.cooldown(3, 300, commands.BucketType.user)
@client.command(aliases=["massunban"])
@commands.has_permissions(administrator=True)
async def unbanall(ctx):
    guild = ctx.guild
    banlist = await guild.bans()
    await ctx.reply(embed=discord.Embed(
        title="Zeon ",
        color=65280,
        description='Unbanning {} members'.format(len(banlist))))
    for users in banlist:
        await ctx.guild.unban(user=users.user)


@unbanall.error
async def unbanall_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply(embed=discord.Embed(
            title="Zeon ",
            color=65280,
            description=
            f"`Must Have Adminstration Permissions To run this command`"))


@client.command()
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.reply(embed=discord.Embed(
        title="Zeon",
        color=65280,
        description=f"Set Channel to `{seconds}` Seconds Slowmode"))


@slowmode.error
async def slowmode(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply(embed=discord.Embed(
            title="Zeon",
            color=65280,
            description=
            f"`Must Have Adminstration Permissions To run this command`"))


status = '<:enabled:911153577437851688>'


@client.command()
async def features(ctx, member: discord.Member = None):
    embed = discord.Embed(color=65280)
    embed.set_author(
        name='Zeon',
        icon_url=
        'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
    )
    embed.set_thumbnail(
        url=
        "https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024"
        "")
    embed.add_field(
        name=f"<a:IMP_deco_hype_badge:896268546697486366>**__Features__**",
        value=
        f" <a:xyz:904270829091713024> `Anti Guild Update` \n<a:xyz:904270829091713024> `Anti Channel Create` \n<a:xyz:904270829091713024> `Anti Channel Delete` \n<a:xyz:904270829091713024> `Anti Channel Update` \n<a:xyz:904270829091713024> `Anti Role Create` \n<a:xyz:904270829091713024> `Anti Role Delete` \n<a:xyz:904270829091713024> `Anti Role Update` \n<a:xyz:904270829091713024> `Anti Ban` \n<a:xyz:904270829091713024> `Anti Kick` \n<a:xyz:904270829091713024> `Anti Webhook [Creation],   [Update], [Delete]`\n<a:xyz:904270829091713024> `Anti Emoji [Creation],\n[Update], [Delete]` \n<a:xyz:904270829091713024> `Anti Sticker [Creation],   [Update], [Delete]`\n \n <a:121_moderation:884753029759397939> **__SETTINGS__** \n <a:xyz:904270829091713024> `LIMITS =1` \n <a:xyz:904270829091713024> `PUNISHMENT =BAN` \n<a:xyz:904270829091713024> `RECOVER = TRUE`",
        inline=True)

    await ctx.reply(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def recover(ctx):
    for channel in ctx.guild.channels:
        if channel.name in ('rules', 'moderator-only'):
            try:
                await channel.delete()
            except:
                pass


@client.command(name='purge',
                description='Mass delete messages (default = 15)',
                aliases=['clea'],
                usage="purge <amount>")
@commands.has_permissions(administrator=True)
async def purgeee(ctx, amount=15):
    await ctx.channel.send(f"purging wait bemti")
    await ctx.channel.purge(limit=amount + 2)
    await ctx.send(f"krdia purge bemti")


@client.command()
@commands.has_permissions(administrator=True)
async def lockall(ctx, server: discord.Guild = None, *, reason=None):
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 747305133502627931 or ctx.author.id == 836955921376477216:
        await ctx.message.delete()
        if server is None: server = ctx.guild
        try:
            for channel in server.channels:
                await channel.set_permissions(
                    ctx.guild.default_role,
                    overwrite=discord.PermissionOverwrite(send_messages=False),
                    reason=reason)
                await ctx.send(
                    f"**{server}** has been locked.\nReason: `{reason}`")
        except:
            await ctx.send(f"**Failed to lockdown, {server}.**")
    else:
        pass


@client.command()
@commands.has_permissions(administrator=True)
async def unlockall(ctx, server: discord.Guild = None, *, reason=None):
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 747305133502627931 or ctx.author.id == 836955921376477216:
        await ctx.message.delete()
        if server is None: server = ctx.guild
        try:
            for channel in server.channels:
                await channel.set_permissions(
                    ctx.guild.default_role,
                    overwrite=discord.PermissionOverwrite(send_messages=True),
                    reason=reason)
                await ctx.send(
                    f"**{server}** has been unlocked.\nReason: `{reason}`")
        except:
            await ctx.send(f"**Failed to unlock, {server}**")
    else:
        pass


@client.command()
@commands.has_permissions(administrator=True)
async def mmoodon(ctx, server: discord.Guild = None, *, reason=None):
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 747305133502627931 or ctx.author.id == 836955921376477216:
        await ctx.message.delete()
        if server is None: server = ctx.guild
        try:
            for channel in server.channels:
                await channel.set_permissions(
                    ctx.guild.default_role,
                    overwrite=discord.PermissionOverwrite(view_channel=False),
                    reason=reason)
                await ctx.send(
                    f"**{server}** has been locked.\nReason: `{reason}`")

        except:
            await ctx.send(f"**Failed to lock, {server}**")
    else:
        await ctx.send(f"**Beta Tu Owner Kabse Bn Gya**")


@client.command()
@commands.has_permissions(administrator=True)
async def mmoodoff(ctx, server: discord.Guild = None, *, reason=None):
    if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 747305133502627931 or ctx.author.id == 836955921376477216:
        await ctx.message.delete()
        if server is None: server = ctx.guild
        try:
            for channel in server.channels:
                await channel.set_permissions(
                    ctx.guild.default_role,
                    overwrite=discord.PermissionOverwrite(view_channel=True),
                    reason=reason)
                await ctx.send(f" has been unlocked.\nReason: `{reason}`")
        except:
            await ctx.send(f"**Failed to unlock**")
    else:
        await ctx.send(f"**Beta Tu Owner Kabse Bn Gya**")


@mmoodoff.error
async def mmoodoff_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply(embed=discord.Embed(
            title="zeon ", color=65280, description=f"`Must Be Owner`"))


snipe_message_author = {}
snipe_message_content = {}


@client.event
async def on_message_delete(message):
    snipe_message_author[message.channel.id] = message.author.id
    snipe_message_content[message.channel.id] = message.content
    await asyncio.sleep(60)
    del snipe_message_author[message.channel.id]
    del snipe_message_content[message.channel.id]


@client.command(name='snipe')
async def snipe(ctx):
    channel = ctx.channel
    try:
        em = discord.Embed(color=65280)
        em.set_author(
            name='Zeon',
            icon_url=
            'https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024'
        )
        em.set_thumbnail(
            url=
            "https://cdn.discordapp.com/avatars/911149764438016101/ca5f0f018dea0fd65f875958d3e50a3b.png?size=1024"
        )
        em.add_field(
            name=f"Snipe",
            value=
            f"**Sent By** : <@{snipe_message_author[channel.id]}>\n**Message** : {snipe_message_content[channel.id]}",
            inline=True)
        em.set_footer(text=f"Safety ++")
        await ctx.reply(embed=em)
    except:
        await ctx.send(f"Nothing to snipe in <#{channel.id}>")


def guildcheck(ctx):
    with open("db.json", "r") as foo:
        db = json.loads(foo.read())
    if str(ctx.guild.id) in db.keys():
        return True
    else:
        raise commands.CheckFailure(
            message=
            "Add a default role for this guild first, using `>autorole [role]`"
        )


@client.command()
@commands.has_permissions(administrator=True)
async def autorole(self, ctx: commands.Context, *, role: discord.Role):
    self.db[str(ctx.guild.id)] = role.id
    with open("db.json", "w") as foo:
        foo.write(json.dumps(self.db, indent=2))
    await ctx.send(embed=discord.Embed(
        description=f"Auto role set to {role.mention}", color=0x00FF77))


@client.command(pass_context=True)
@commands.has_permissions(manage_nicknames=True)
@commands.bot_has_permissions(manage_nicknames=True)
async def nick(ctx, user: discord.Member, nick):
    old_name = user.display_name
    await user.edit(nick=nick)
    new_name = user.display_name
    embed = discord.Embed(
        title="Changed Nickname",
        description=f"{ctx.author.mention}, {user.mention}'s nickname changed "
        f"from `{old_name}` to `{new_name}`",
        color=discord.Color.blue())
    return await ctx.channel.reply(embed=embed)


@client.command()
async def pruneestr(ctx):
    guild = ctx.guild
    try:
        po = await ctx.guild.estimate_pruned_members(days=1, roles=guild.roles)
        await ctx.channel.reply(f"Here s your result {po}")
    except:
        pass


@client.command()
async def pruneest(ctx):
    try:
        po = await ctx.guild.estimate_pruned_members(days=1)
        await ctx.channel.reply(f"Here s your result {po}")
    except:
        pass


@client.event
async def on_command_error(ctx, error):
    error = getattr(error, 'original', error)
    await ctx.reply(embed=discord.Embed(color=0x2f3136,
                                        timestamp=ctx.message.created_at,
                                        description=f'`{error}`'))


@client.command()
async def help2(ctx):
    embed = discord.Embed(color=0x7289DA)

    embed.set_description(name="loda", value="hi", inline=True)


#server.py dekh ramdike

#beer = 836955921376477216
#ritik = 747305133502627931
#sam = 818052886642032670
#@client.event
#async def on_message(message):
#if str(beer) in str(message.content):
#embed = discord.Embed(color=0x0ce885)
#embed.set_thumbnail(url="https://media.discordapp.net/attachments/892757875473133578/908954902062051368/ab5f57525e5c94c600a06e33fe039388.png?width=325&height=325")
# embed.add_field(name="<:_mafia_jhappi:871603117966368779> REAL OWNER", value="That's my owner!", inline=False)
#  await message.channel.send(embed=embed)
#if message.author.id == ritik:
# await message.add_reaction("<a:PN_GoldenCrown:936619745124421665>")
#  elif message.author.id == beer:
#      await message.add_reaction("<a:PN_GoldenCrown:936619745124421665>")
#  elif message.author.id == sam:
#   await message.add_reaction("<a:ag_queen_crown:936621647216123914>")

#@client.event
#async def on_message(message):
#msg = message.content
#with open('antiwords.txt') as BadWords:
#if msg in BadWords.read():
#await message.delete()
#await message.author.ban()
#await message.channel.send("Don´t use this word here!")

client.run(token, bot=True)
