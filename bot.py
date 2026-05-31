import dotenv
import random

import discord
from discord import app_commands

TOKEN = dotenv.dotenv_values()["TOKEN"]

# Create client with intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ------------ON READY-----------------------
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1473332148491518098))
    print(f"Logged in as {client.user}.")
# -------------------------------------------

# ============================================
@client.event
async def on_member_join(member):
    channel = await client.fetch_channel(1473332149326446919)
    await channel.send(f"WELCOME TO THE DEN {member.mention}!")
# ============================================

# =========== MESSAGES =======================
@client.event
async def on_message(message):
    if message.author == client.user:
        return
# ============================================

# ==================== COMMANDS =======================
@tree.command(name="test", description="Test command", guild=discord.Object(id=1473332148491518098))
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("Test successful!")

@tree.command(name="spin_ghost", description="Spin the Ghost Wheel", guild=discord.Object(id=1473332148491518098))
async def test(interaction: discord.Interaction):
    ghost = random.choice(ghosts)
    await interaction.response.send_message(f"The chosen ghost is: {ghost}")

@tree.command(name="spin_all_maps", description="Spin the Map Wheel", guild=discord.Object(id=1473332148491518098))
async def test(interaction: discord.Interaction):
    group = random.choice([small_maps, medium_maps, big_maps])
    map = random.choice(group)
    await interaction.response.send_message(f"The chosen map is: {map}")

@tree.command(name="spin_small_maps", description="Spin the Small Map Wheel", guild=discord.Object(id=1473332148491518098))
async def test(interaction: discord.Interaction):
    map = random.choice(small_maps)
    await interaction.response.send_message(f"The chosen map is: {map}")

@tree.command(name="spin_medium_maps", description="Spin the Medium Map Wheel", guild=discord.Object(id=1473332148491518098))
async def test(interaction: discord.Interaction):
    map = random.choice(medium_maps)
    await interaction.response.send_message(f"The chosen map is: {map}")

@tree.command(name="spin_big_maps", description="Spin the Big Map Wheel", guild=discord.Object(id=1473332148491518098))
async def test(interaction: discord.Interaction):
    map = random.choice(big_maps)
    await interaction.response.send_message(f"The chosen map is: {map}")

# =========== GHOSTS, MAPS====================
with open("assets/ghosts", "r") as g:
    ghosts = [line.strip() for line in g if line.strip()]

with open("assets/maps/small_maps", "r") as s:
    small_maps = [line.strip() for line in s if line.strip()]

with open("assets/maps/medium_maps", "r") as m:
    medium_maps = [line.strip() for line in m if line.strip()]

with open("assets/maps/big_maps", "r") as b:
    big_maps = [line.strip() for line in b if line.strip()]
# ============================================

# ============================================

# ============================================

# ============================================

# Run client
client.run(TOKEN)