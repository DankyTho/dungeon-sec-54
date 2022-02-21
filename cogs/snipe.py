import discord
from discord.ext import commands
               
snipes = dict()

def snipe_embed(context_channel, message, user):
	if message.author not in message.guild.members or message.author.color == discord.Colour.default():
		embed = discord.Embed(title='Deleted message:',description = message.content, timestamp = message.created_at)
	else:
		embed = discord.Embed(color=0x2f3136,title='Deleted message:',description = message.content, timestamp = message.created_at)
	embed.set_author(name = str(message.author), icon_url = message.author.avatar_url)
	if message.attachments:
		embed.add_field(name = 'Attachment(s)', value = '\n'.join([attachment.filename for attachment in message.attachments]) + '\n\n__Attachment URLs are invalidated once the message is deleted.__')
	if message.channel != context_channel:
		embed.set_footer(text = 'Sniped by: ' + str(user) + ' | in channel: #' + message.channel.name)
	else: 
		embed.set_footer(text = 'Sniped by: ' + str(user))
	return embed

class snipe(commands.Cog):
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



