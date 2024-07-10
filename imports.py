import asyncio
import logging

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode
import config
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router
from sqlite_db import*