from random import randrange

import discord
import os
from discord.app_commands import commands
from dotenv import load_dotenv
from discord.ext import commands
from PIL import Image
import io
import subprocess

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

load_dotenv()

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

@bot.command()
async def gifthis(ctx):
    # Check if this message is a reply
    if ctx.message.reference:
        # Fetch the original message
        replied_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)

        # Check if the replied message has attachments
        if replied_msg.attachments:
            attachment = replied_msg.attachments[0]  # take first attachment
            img_bytes = await attachment.read()  # download the file as bytes

            # Open image with PIL
            image = Image.open(io.BytesIO(img_bytes))

            # Convert to GIF
            gif_bytes_io = io.BytesIO()
            image.save(gif_bytes_io, format="GIF")
            gif_bytes_io.seek(0)

            # Save to storage (example: local folder)
            randomnum = randrange(1000000, 9999999)
            filename = f"{randomnum}_{attachment.filename.split('.')[0]}.gif"
            with open(filename, "wb") as f:
                f.write(gif_bytes_io.read())

            subprocess.run(["git", "add", filename])
            subprocess.run(["git", "commit", "-m", f"Add {filename}"])
            subprocess.run(["git", "push", "origin", "main"])

            await ctx.send(f"{filename}")
        else:
            await ctx.send("The replied message has no image attachment.")
    else:
        await ctx.send("You need to reply to a message with an image.")

if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))