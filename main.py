from random import randrange

import discord
import os
from discord.app_commands import commands
from dotenv import load_dotenv
from discord.ext import commands
from PIL import Image
import io
import asyncio
import subprocess

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

load_dotenv()

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

async def run_git_command(cmd):
    result = await asyncio.to_thread(
        subprocess.run,
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

@bot.command()
async def gt(ctx):
    if not ctx.message.reference:
        await ctx.send("Reply to a message containing an image.")
        return

    replied_msg = await ctx.channel.fetch_message(
        ctx.message.reference.message_id
    )

    if not replied_msg.attachments:
        await ctx.send("That message has no image attachment.")
        return

    attachment = replied_msg.attachments[0]
    img_bytes = await attachment.read()

    image = Image.open(io.BytesIO(img_bytes))

    gif_bytes_io = io.BytesIO()
    image.save(gif_bytes_io, format="GIF")
    gif_bytes_io.seek(0)

    randomnum = randrange(1000000, 9999999)
    filename = f"{randomnum}.gif"

    with open(filename, "wb") as f:
        f.write(gif_bytes_io.read())

    await run_git_command(["git", "add", filename])
    await run_git_command(["git", "commit", "-m", f"Add {filename}"])
    await run_git_command(["git", "push", "origin", "master"])

    await ctx.send(f"Dělám tvůj úžasnej gif, ale počkej mi minutku.\n-# čekám než si github rozhodne tam dát ten gif")

    await asyncio.sleep(60)

    await ctx.message.delete()

    await ctx.send(
        f"https://pixousek.github.io/kaja.github.io/{filename}"
    )


if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))