import nextcord, datetime, json, asyncio, time, random, humanfriendly, re, pytz, os
from nextcord import Integration, Interaction, slash_command, SlashOption, ChannelType
from nextcord.ext import commands, tasks
from nextcord.utils import format_dt
from nextcord.ext.commands import Bot, Context
from nextcord.ui import View
import sqlite3
from datetime import datetime, timezone, timedelta
from typing import List, Tuple
