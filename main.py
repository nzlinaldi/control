import discord
import asyncio
from discord.ext import commands

# Permissions for the bot, allowing it to access all intents
perm = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=perm)

@bot.event
async def on_ready():
    print('Bot is ready!')

@bot.command()
async def ping(ctx):
    await ctx.reply('Pong!')

@bot.command()
async def kick(ctx:commands.Context, member: discord.Member):
    # Verify permissions
    if not ctx.author.guild_permissions.kick_members:
        await ctx.reply('❌ You dont have permission to kick members.')
        return
    
    # Ask for confirmation and reason
    await ctx.reply(f'✅ Do you have sure you want to kick {member.mention}? Please type the reason for the kick or "cancel" to abort. You have 30 seconds.')
    
    try:
        # Wait for the user's response
        msg = await bot.wait_for('message', 
                                  check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                                  timeout=30.0)
        
        # If the user types "cancel", abort the action
        if msg.content.lower() == 'cancel':
            await ctx.send('❌ Action cancelled.')
            return
        
        # If the user provides a reason, kick the member and send a confirmation message
        reason = msg.content
        await member.kick(reason=reason)
        await ctx.send(f'✅ {member.mention} was kicked from the server. Reason: {reason}')
        
    except asyncio.TimeoutError:
        await ctx.send('⏱️ Timeout. Action cancelled.')

@bot.command()
async def ban(ctx:commands.Context, member: discord.Member):
    # Verify permissions
    if not ctx.author.guild_permissions.ban_members:
        await ctx.reply('❌ You dont have permission to ban members.')
        return
    
    # Ask for confirmation and reason
    await ctx.reply(f'✅ Do you have sure you want to ban {member.mention}? Please type the reason for the ban or "cancel" to abort. You have 30 seconds.')
    
    try:
        # Wait for the user's response
        msg = await bot.wait_for('message', 
                                  check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                                  timeout=30.0)
        
        # If the user types "cancel", abort the action
        if msg.content.lower() == 'cancel':
            await ctx.send('❌ Action cancelled.')
            return
        
        # If the user provides a reason, ban the member and send a confirmation message
        reason = msg.content
        await member.ban(reason=reason)
        await ctx.send(f'✅ {member.mention} was banned from the server. Reason: {reason}')
        
    except asyncio.TimeoutError:
        await ctx.send('⏱️ Timeout. Action cancelled.')

@bot.command()
async def unban(ctx:commands.Context, user_id: int):
    # Verify permissions
    if not ctx.author.guild_permissions.ban_members:
        await ctx.reply('❌ You dont have permission to unban members.')
        return
    
    # Ask for confirmation
    await ctx.reply(f'✅ Do you have sure you want to unban the user with ID {user_id}? Please type "yes" to confirm or "cancel" to abort. You have 30 seconds.')
    
    try:
        # Wait for the user's response
        msg = await bot.wait_for('message', 
                                  check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                                  timeout=30.0)
        
        # If the user types "cancel", abort the action
        if msg.content.lower() == 'cancel':
            await ctx.send('❌ Action cancelled.')
            return
        
        # If the user confirms, unban the member and send a confirmation message
        if msg.content.lower() == 'yes':
            user = await bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            await ctx.send(f'✅ The user {user} was unbanned from the server.')
        else:
            await ctx.send('❌ Action cancelled.')
        
    except asyncio.TimeoutError:
        await ctx.send('⏱️ Timeout. Action cancelled.')

@bot.command()
async def clear(ctx:commands.Context, amount: int):
    # Verify permissions
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.reply('❌ You dont have permission to manage messages.')
        return
    
    # Ask for confirmation
    await ctx.reply(f'✅ Do you have sure you want to clear {amount} messages? Please type "yes" to confirm or "cancel" to abort. You have 30 seconds.')
    
    try:
        # Wait for the user's response
        msg = await bot.wait_for('message', 
                                  check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                                  timeout=30.0)
        
        # If the user types "cancel", abort the action
        if msg.content.lower() == 'cancel':
            await ctx.send('❌ Ação cancelada.')
            return
        
        # If the user confirms, clear the messages and send a confirmation message
        if msg.content.lower() == 'yes':
            await ctx.channel.purge(limit=amount)
            await ctx.send(f'✅ {amount} mensagens foram limpas do canal.')
        else:
            await ctx.send('❌ Ação cancelada.')
        
    except asyncio.TimeoutError:
        await ctx.send('⏱️ Tempo expirou. Ação cancelada.')
    
@bot.command()
async def mute(ctx:commands.Context, member: discord.Member, duration: int):
    # Verify permissions
    if not ctx.author.guild_permissions.mute_members:
        await ctx.reply('❌ You dont have permission to mute members.')
        return
    
    # Ask for confirmation
    await ctx.reply(f'✅ Do you have sure you want to mute {member.mention} for {duration} minutes? Please type "yes" to confirm or "cancel" to abort. You have 30 seconds.')
    
    try:
        # Wait for the user's response
        msg = await bot.wait_for('message', 
                                  check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                                  timeout=30.0)
        
        # If the user types "cancel", abort the action
        if msg.content.lower() == 'cancel':
            await ctx.send('❌ Ação cancelada.')
            return
        
        # If the user confirms, mute the member and send a confirmation message
        if msg.content.lower() == 'yes':
            await member.edit(mute=True)
            await ctx.send(f'✅ {member.mention} was muted for {duration} minutes.')
            await asyncio.sleep(duration * 60)
            await member.edit(mute=False)
            await ctx.send(f'✅ {member.mention} was unmuted.')
        else:
            await ctx.send('❌ Action cancelled.')
        
    except asyncio.TimeoutError:
        await ctx.send('⏱️ Timeout. Action cancelled.')

@bot.command()
async def unmute(ctx:commands.Context, member: discord.Member):
    # Verify permissions
    if not ctx.author.guild_permissions.mute_members:
        await ctx.reply('❌ You dont have permission to unmute members.')
        return
    
    # Ask for confirmation
    await ctx.reply(f'✅ Do you have sure you want to unmute {member.mention}? Please type "yes" to confirm or "cancel" to abort. You have 30 seconds.')
    
    try:
        # Wait for the user's response
        msg = await bot.wait_for('message', 
                                  check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                                  timeout=30.0)
        
        # If the user types "cancel", abort the action
        if msg.content.lower() == 'cancel':
            await ctx.send('❌ Action cancelled.')
            return
        
        # If the user confirms, unmute the member and send a confirmation message
        if msg.content.lower() == 'yes':
            await member.edit(mute=False)
            await ctx.send(f'✅ {member.mention} was unmuted.')
        else:
            await ctx.send('❌ Action cancelled.')
        
    except asyncio.TimeoutError:
        await ctx.send('⏱️ Timeout. Action cancelled.')

@bot.command()
async def warn(ctx:commands.Context, member: discord.Member, *, reason: str):
    # Verify permissions
    if not ctx.author.guild_permissions.kick_members:
        await ctx.reply('❌ You dont have permission to warn members.')
        return
    
    # Send a warning message to the member
    await member.send(f'⚠️ You have been warned in {ctx.guild.name} for the following reason: {reason}')
    await ctx.send(f'✅ {member.mention} has been warned. Reason: {reason}')

    #If member has 1 warning, mute them for 10 minutes
    await member.edit(mute=True)
    await ctx.send(f'✅ {member.mention} was muted for 10 minutes.')
    await asyncio.sleep(600)  # 10 minutes in seconds
    await member.edit(mute=False)

    #If member has 3 warnings, mute for 3 days them
    if member.warns == 3:
        await member.edit(mute=True)
        await ctx.send(f'✅ {member.mention} was muted for 3 days.')
        await asyncio.sleep(259200)  # 3 days in seconds
        await member.edit(mute=False)

    #If member has 5 warnings, ban them
    if member.warns == 5:
        await member.ban(reason='5 warnings')
        await ctx.send(f'✅ {member.mention} was banned from the server for accumulating 5 warnings.')

@bot.command()
async def warns(ctx:commands.Context, member: discord.Member):
    # Verify permissions
    if not ctx.author.guild_permissions.kick_members:
        await ctx.reply('❌ You dont have permission to view warnings.')
        return
    
    # Send the number of warnings the member has
    await ctx.send(f'⚠️ {member.mention} has {member.warns} warnings.')

@bot.command()
async def clearwarns(ctx:commands.Context, member: discord.Member):
    # Verify permissions
    if not ctx.author.guild_permissions.kick_members:
        await ctx.reply('❌ You dont have permission to clear warnings.')
        return
    
    # Clear the member's warnings
    member.warns = 0
    await ctx.send(f'✅ {member.mention}\'s warnings have been cleared.')


# Run Bot
bot.run('')
