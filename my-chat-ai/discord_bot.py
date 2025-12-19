import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")



API_URL = "http://localhost:8000/chat"


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is now online!')
    print(f'Nova AI Discord Bot is ready!')

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    
 
    is_mentioned = bot.user.mentioned_in(message)
    is_reply_to_bot = (message.reference and 
                       message.reference.resolved and 
                       message.reference.resolved.author == bot.user)
    is_dm = isinstance(message.channel, discord.DMChannel)
    

    if is_mentioned or is_reply_to_bot or is_dm:
       
        user_message = message.content.replace(f'<@{bot.user.id}>', '').strip()
        
        if not user_message:
            await message.channel.send("Hey! Ask me something!")
            return
        
   
        async with message.channel.typing():
            try:
          
                response = requests.post(
                    API_URL,
                    json={"message": user_message},
                    timeout=60
                )
                
                if response.status_code == 200:
                    nova_response = response.json()["response"]
                    await message.channel.send(nova_response)
                else:
                    await message.channel.send("Sorry, I'm having trouble thinking right now!")
            
            except Exception as e:
                await message.channel.send(f"Error: {str(e)}")
    
    await bot.process_commands(message)


bot.run(BOT_TOKEN)