import discord
import dotenv

TOKEN = dotenv.dotenv_values()["TOKEN"]

# Create client with intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# ------------ON READY-----------------------
@client.event
async def on_ready():
    print(f"Logged in as {client.user}.")
# -------------------------------------------



# ============================================
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("Hi"):
        await message.channel.send("Hello!")



# ============================================

# Run client
client.run(TOKEN)