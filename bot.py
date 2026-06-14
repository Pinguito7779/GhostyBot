import dotenv
import random
import re

import discord
from discord import app_commands

TOKEN = dotenv.dotenv_values()["TOKEN"]

# Create client with intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

GUILD_ID = discord.Object(id=1473332148491518098)

# ------------ON READY-----------------------
@client.event
async def on_ready():
    await tree.sync(guild=GUILD_ID)
    print(f"Logged in as {client.user}.")
# -------------------------------------------

# ============================================
@client.event
async def on_member_join(member):
    channel = member.channel
    await channel.send(f"WELCOME TO THE DEN {member.mention}!")
# ============================================

# =========== MESSAGES =======================
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # -------------- CHECK THE HI MESSAGE --------------
    # if "hi" in message.content.lower() or "hello" in message.content.lower():
    #     if message.author.id == 840878777945161738:
    #         memberclass = "Overseer"
    #         clearance = 5
    #     elif message.author.id == 1214071849848414228:
    #         memberclass = "Security"
    #         clearance = 4
    #     else:
    #         memberclass = "D"
    #         clearance = 1
    #     await message.channel.send(f"Hello there, Class {memberclass} and clearance {clearance} with ID {message.author.id} in channel {message.channel} with ID {message.channel.id}!")
    # --------------- CHECK FOR CODE ---------------
    if re.search("\d{6}", message.content):
        code = int(re.search("\d{6}", message.content)[0])
        guild_id = message.guild.id
        lobby_codes[guild_id] = code

    elif client.user.display_name.lower() in message.content.lower():
        await message.response.send_message(message.author.nick)
# ============================================

# ==================== COMMANDS =======================
@tree.command(name="spin_ghost", description="Spin the Ghost Wheel", guild=GUILD_ID)
async def spin_ghost(interaction: discord.Interaction):
    ghost = random.choice(ghosts)
    await interaction.response.send_message(f"The chosen ghost is: {ghost}")

@tree.command(name="spin_all_maps", description="Spin the Map Wheel", guild=GUILD_ID)
async def spin_all_maps(interaction: discord.Interaction):
    group = random.choice([small_maps, medium_maps, big_maps])
    map = random.choice(group)
    await interaction.response.send_message(f"The chosen map is: {map}")

@tree.command(name="spin_small_maps", description="Spin the Small Map Wheel", guild=GUILD_ID)
async def spin_small_maps(interaction: discord.Interaction):
    map = random.choice(small_maps)
    await interaction.response.send_message(f"The chosen map is: {map}")

@tree.command(name="spin_medium_maps", description="Spin the Medium Map Wheel", guild=GUILD_ID)
async def spin_medium_maps(interaction: discord.Interaction):
    map = random.choice(medium_maps)
    await interaction.response.send_message(f"The chosen map is: {map}")

@tree.command(name="spin_big_maps", description="Spin the Big Map Wheel", guild=GUILD_ID)
async def spin_big_maps(interaction: discord.Interaction):
    map = random.choice(big_maps)
    await interaction.response.send_message(f"The chosen map is: {map}")

@tree.command(name="assign_all_roles", description="Assign every user in the same vc a role (mention users to exclude them).", guild=GUILD_ID)
async def assign_all_roles(interaction: discord.Interaction, excluded: str=""):
    user = interaction.user

    if user.voice is None or user.voice.channel is None:
        await interaction.response.send_message("You need to be in a voice channel to use this command.")
        return
    
    channel = user.voice.channel

    excluded_ids = re.findall(r"<@!?(\d+)>", excluded)
    members = [member for member in user.voice.channel.members]
    for id in excluded_ids:
        for member in members:
            if int(id) == member.id:
                members.remove(member)

    members = [member.nick for member in members]
    
    random.shuffle(members)
    random.shuffle(roles_list)

    roles.clear()
    for member in members:
        roles[member] = []

    for i, role in enumerate(roles_list):
        member = members[i % len(members)]
        roles[member].append(role)
    
    message: str = "------- CURRENT ROLES -------\n"
    for player, player_roles in roles.items():
        message += f"{player}: {', '.join(player_roles)}\n"
    message += "---------------------------------"

    await interaction.response.send_message(message)

@tree.command(name="show_roles", description="Show all the current assigned roles.", guild=GUILD_ID)
async def show_roles(interaction: discord.Interaction):
    message: str = "------- CURRENT ROLES -------\n"
    for player in roles:
        message += player + ": " + roles[player] + "\n"
    message += "---------------------------------"
    
    await interaction.response.send_message(message, ephemeral=True)

@tree.command(name="my_roles", description="Show the description for your role.", guild=GUILD_ID)
async def my_role(interaction: discord.Interaction):
    member = interaction.user.nick
    player_roles = roles[member]
    names = ", ".join(player_roles)
    message = f"Your current roles are {names}:\n\n"
    for role in player_roles:
        message += role + ": " + role_descriptions[role] + "\n\n"

    await interaction.response.send_message(message, ephemeral=True)

@tree.command(name="show_role_descriptions", description="Show the descriptions for every role", guild=GUILD_ID)
async def show_role_descriptions(interaction: discord.Interaction):
    message = "------- ROLE DESCRIPTIONS -------\n"
    for role in roles_list:
        message += f"{role}: {role_descriptions[role]}\n\n"

    await interaction.response.send_message(message, ephemeral=True)

@tree.command(name="clear_roles", description="Clear the current assigned roles", guild=GUILD_ID)
async def clear_roles(interaction: discord.Interaction):
    roles.clear()
    await interaction.response.send_message("Cleared the current roles.")


@tree.command(name="show_code", description="Show the last lobby code typed in the server.", guild=GUILD_ID)
async def show_code(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    code = lobby_codes[guild_id]
    await interaction.response.send_message(f"Lobby code: {code}.")

# =========== GHOSTS, MAPS==================================
with open("assets/ghosts", "r") as g:
    ghosts = [line.strip() for line in g if line.strip()]

with open("assets/maps/small_maps", "r") as s:
    small_maps = [line.strip() for line in s if line.strip()]

with open("assets/maps/medium_maps", "r") as m:
    medium_maps = [line.strip() for line in m if line.strip()]

with open("assets/maps/big_maps", "r") as b:
    big_maps = [line.strip() for line in b if line.strip()]
# ===========================================================

# ========== ROLES =====================
roles = {}
roles_list = []
role_descriptions = {}

with open("assets/roles", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue

        role, description = line.split(",", 1)  # split only on first comma

        role = role.strip()
        description = description.strip()

        roles_list.append(role)
        role_descriptions[role] = description

# ============================================
lobby_codes = {}

# ============================================

# ============================================

# ============================================

# ============================================

# ============================================

# Run client
client.run(TOKEN)
