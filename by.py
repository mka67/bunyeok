import discord
from google.cloud import translate_v2 as translate
import os
import signal
import sys


# Credentials in order to use the Google Cloud Translator API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r""

# Translator object
translate_client = translate.Client()
lang = translate_client.get_languages()
lang = [code["language"] for code in lang]
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
        return

    # Translate command
    if message.content.startswith("!"):
        content = message.content[1:].split(" ", 1)

        try:
            trg = content[0]
        except IndexError:
            await message.channel.send("Missing language code!")
            return

        if len(trg) != 2 or trg not in lang:
            await message.channel.send("Invalid language code!")
            return

        try:
            msg = content[1]
        except IndexError:
            await message.channel.send("Message missing!")
            return

        translate_client.detect_language(msg)
        translated_message = translate_client.translate(msg, target_language=f"{trg}")
        await message.channel.send(translated_message["translatedText"])

def signal_handler(_sig, _frame):
    print("Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Bot token
client.run("")