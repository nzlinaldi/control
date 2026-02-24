import asyncio
import discord
import sys
from discord.ext import commands
from datetime import datetime

# Dev inputs
token = input("Enter your bot token: ")
ticket_main_channel_id = int(input("Enter the main ticket channel ID: "))
ticket_open_category_id = int(input('Enter the open ticket category ID: '))
ticket_finish_category_id = int(input("Enter the finished ticket category ID: "))
ticket_emoji = "🎫"

# Prefix for commands and permissions
intents = discord.Intents.all()
intents.guilds = True
bot = commands.Bot(command_prefix='C.', intents=intents)

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    for guild in bot.guilds:
        await ticket_menu(guild)
    
    

# Latency command
@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000  # Convert to milliseconds
    await ctx.send(f'Pong! Latency: {latency:.2f} ms')

# Ticket System
async def ticket_menu(guild: discord.Guild):
    channel = guild.get_channel(ticket_main_channel_id)

    if channel is None:
        sys.exit('No ticket main channel ID has been found. Please start the bot and put the ID')
    print(f'Channel found: {channel.name}')

    embed = discord.Embed(
        title='🎫 Ticket System',
        description='Click the reaction below to create a new ticket.\n\n'
                    '📝 **How to use:**\n'
                    '1. Click the reaction 🎫\n'
                    '2. You will be asked for the reason (Please enable DMs messages)\n'
                    '3. A new private channel will be created\n'
                    '4. Only admins, technicians and you will be able to see it',
        color=discord.Color.red(),
        )
    embed.set_footer(text='Ticket System')

    try:
        await channel.purge(limit=None)
        print(f'Channel {channel.name} cleaned successfully')
    except Exception as e:
        print(f'Error cleaning channel: {e}')
    
    new_message = await channel.send(embed=embed)
    global ticket_message_id
    ticket_message_id = new_message.id
    await new_message.add_reaction(ticket_emoji)

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.id != ticket_message_id or str(reaction.emoji) != ticket_emoji:
        return

    if user.bot:
        return
    
    if reaction.message.id != ticket_message_id:
        return
    if reaction.emoji == ticket_emoji:
        await create_ticket(reaction, user)

async def create_ticket(reaction, user):
    guild = reaction.message.guild
    try:
        await reaction.remove(user)
    except:
        pass

    try:
        reason_embed = discord.Embed(
            title='🎫 Why are you opening a ticket?',
            description='Please describe the reason for your ticket in the next message. You have 2 minutes to respond.',
            color=discord.Color.red()
        )
        await user.send(embed=reason_embed)
    except Exception as e:
        print(f'Error creating reason embed: {e}')

    try:
        reason_msg = await bot.wait_for(
            'message',
            check=lambda m: m.author == user and isinstance(m.channel, discord.DMChannel),
            timeout=120.0
        )
        reason = reason_msg.content
    except asyncio.TimeoutError:
        await user.send('⏱️ Timeout! You took too long to respond. Please react again to create a new ticket.')
        return
    
    # Ticket channel name formatting
    ticket_number = f'ticket - {user.id}-{datetime.now()}'

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(view_channel=True)
    }

    # Creating Channel text
    try:
        ticket_channel = await guild.create_text_channel(
            name=ticket_number,
            category=guild.get_channel(ticket_open_category_id),
            overwrites=overwrites
        )

        embed = discord.Embed(
                title='📋 Ticket Details',
                description=f'**Who called:** {user.mention}\n'
                            f'**Date/Time:** {datetime.now()}\n'
                            f'**Status:** 🟢 Open\n\n'
                            f'**Reason:** {reason}',
                color=discord.Color.green()
        )
        embed.set_footer(text=f'Ticket ID: {ticket_channel.id}')
        await ticket_channel.send(embed=embed)

        confirm_embed = discord.Embed(
            title='✅ Ticket Created',
            description=f'Your ticket has been created in {ticket_channel.mention}\n\nReason: {reason}',
            color=discord.Color.green()
        )
        await user.send(embed=confirm_embed)

    except Exception as e:
        print(f'Error creating ticket channel: {e}')
        await user.send(f'❌ Error creating your ticket: {e}')
    
@bot.command()
async def close(ctx):
    if ctx.channel.category_id != ticket_open_category_id:
        await ctx.send('This command can only be used in an open ticket channel.')
        return
    try:
        await ctx.send('Enter if you are sure you want to close this ticket. (yes/no)')
        response = await bot.wait_for(
            'message',
            check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
            timeout=60.0
        )
        if response.content.lower() == 'yes':
            await ctx.channel.edit(category=ctx.guild.get_channel(ticket_finish_category_id))
            await ctx.send('Ticket closed successfully.')
        for member, overwrite in ctx.channel.overwrites.items():
            if isinstance(member, discord.Member):
                await ctx.channel.set_permissions(member, view_channel=False)
        else:
            await ctx.send('Ticket closing cancelled.')
    except asyncio.TimeoutError:
        await ctx.send('⏱️ Timeout! You took too long to respond. Please use the command again if you want to close the ticket.')
    except Exception as e:
        print(f'Error closing ticket: {e}')
        await ctx.send(f'❌ Error closing the ticket: {e}')

#Run Bot
bot.run(token)