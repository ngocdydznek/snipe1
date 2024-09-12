import discord
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

sniped_messages = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    sniped_messages[message.channel.id] = {
        "content": message.content,
        "author": message.author,
        "time": message.created_at,
        "attachments": message.attachments
    }

@bot.command()
async def snipe(ctx):
    channel = ctx.channel
    try:
        sniped_message = sniped_messages[channel.id]
        embed = discord.Embed(
            description=sniped_message["content"] or "*No text content*",
            color=discord.Color.orange(),
            timestamp=sniped_message["time"]
        )
        embed.set_author(name=sniped_message["author"].name, icon_url=sniped_message["author"].avatar.url)
        embed.set_footer(text=f"Sniped by {ctx.author.name}")

        # Nếu tin nhắn có đính kèm (hình ảnh, video, etc.)
        if sniped_message["attachments"]:
            for attachment in sniped_message["attachments"]:
                if attachment.url.endswith(('png', 'jpg', 'jpeg', 'gif', 'webp')):
                    embed.set_image(url=attachment.url)
                else:
                    embed.add_field(name="Attachment", value=f"[{attachment.filename}]({attachment.url})", inline=False)

        await ctx.send(embed=embed)

    except KeyError:
        await ctx.send("There's nothing to snipe!")

bot.run('YOUR_BOT_TOKEN')
