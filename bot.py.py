import discord
from discord.ext import commands
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Cargar el valor del contador desde un archivo de texto
try:
    with open("contador.txt", "r") as file:
        contador_negro = int(file.read())
except FileNotFoundError:
    contador_negro = 0

@bot.event
async def on_ready(): 
    print(f'{bot.user} has connected to Discord!')
    print(f'Guilds: {bot.guilds}')

@bot.event
async def on_command_error(ctx, error):
    logger.error(error)
    await ctx.send('Ha ocurrido un error ejecutando el comando')

@bot.event
async def on_message(message):
    global contador_negro
    
    # Si el mensaje no proviene del bot mismo
    if message.author != bot.user:
        # Si el mensaje contiene la palabra "negro"
        if "negro" in message.content.lower():
            contador_negro += 1
            await message.channel.send("Juanfra es negro.")
            await message.channel.send(f"Se le ha dicho a Juanfra que es negro {contador_negro} veces.")
            guardar_contador()

    await bot.process_commands(message)


def guardar_contador():
    with open("contador.txt", "w") as file:
        file.write(str(contador_negro))

# Guardar el valor del contador en un archivo de texto antes de apagar el bot
@bot.event
async def on_disconnect():
    with open("contador.txt", "w") as file:
        file.write(str(contador_negro))

# Comando !veces para mostrar la cantidad de veces que se ha mencionado "negro"
@bot.command()
async def veces(ctx):
    await ctx.send(f"La palabra 'negro' se ha mencionado {contador_negro} veces.")
      
@bot.command()
async def hello(ctx):
    await ctx.send('Hola! Estoy conectado.') 

@bot.command()  
async def goodbye(ctx):
    await ctx.send('Adiós!')

bot.run('MTIwNzAwNzQ1Mzg3NTc5ODAyNg.GPLrK0.ydSOdyUlonF_GTIALfuxp-lpELWnABxSAsg3OY')
