import discord
from google.cloud import translate_v2 as translate
import os

# Credentials in order to use the Google Cloud Translator API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r""

# Translator object
translate_client = translate.Client()

# Initiate Discord client
client = discord.Client()


# Console message to let the user know bot is now online
@client.event
async def on_ready():
    print("Bunyeok has awoken!")

# Bot commands
@client.event
async def on_message(message):
    # Checks that the bot is not the one who sent a message
    if message.author == client.user:
        return

    # Help command
    if message.content.startswith("!bunyeok"):
        await message.channel.send("https://cloud.google.com/translate/docs/languages")
        await message.channel.send("!(targetLanguage) (message)\nex: !fr hello")

    # Translate command
    if message.content.lower().startswith("!"):
        msg = message.content[4:]
        trg = message.content[1:3]
        translate_client.detect_language(msg)
        translated_message = translate_client.translate(msg, target_language=f"{trg}")
        await message.channel.send(translated_message["translatedText"])

# Bot token
client.run("")