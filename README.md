# Control Discord Ticket Bot

This repository contains a Discord bot developed in Python using the `discord.py` library.  
The bot provides a complete ticket system for servers, allowing users to create private support tickets through reactions and manage them with commands.

## Overview

This project is a Discord support ticket bot designed to streamline communication between users and staff.  
Users can open tickets by reacting to a message, describe their issue via DM, and automatically receive a private channel accessible only to them and administrators.

The bot also includes ticket closing functionality and latency monitoring.

## Features

- Reaction-based ticket creation  
- Private ticket channels with permissions  
- Ticket reason collection via DM  
- Automatic ticket embed with details  
- Ticket closing command  
- Ticket category organization (open / closed)  
- Latency (`ping`) command  
- Auto-clean ticket menu channel on startup  
- Error handling and timeout protection  

## Technologies

- Python 3
- discord.py
- asyncio

## How It Works

1. The bot sends a **Ticket System** embed in the configured channel.
2. Users react with 🎫 to open a ticket.
3. The bot asks the user (via DM) for the ticket reason.
4. A private ticket channel is created in the **open tickets** category.
5. Staff and the user can communicate inside the ticket.
6. Staff can close the ticket with the `C.close` command.
7. The channel is moved to the **finished tickets** category.

## Setup

1. Install dependencies:

```bash
pip install discord.py
```
2. Run the bot
```bash
python bot.py
```
3. Enter the required IDs when prompted:

- Bot token
- Ticket main channel ID
- Open tickets category ID
- Closed tickets category ID

## Commands
- C.ping -> Shows bot latency
- C.close -> Closes the current ticket

## Requirements

- Python 3.8+
- Discord bot token
- Server with:
- - Ticket channel
- - Open tickets category
- - Closed tickets category
- - Administrator permissions for the bot

## Author

- GitHub: https://github.com/nzlinaldi  
- LinkedIn: https://www.linkedin.com/in/enzo-linaldi-315204389/