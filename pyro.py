from logging import error
from pyrogram import Client, filters
import os

api_id = 1848117
api_hash = '86e7152a80b430f838c83c7f9258b37c'

app = Client("my_account", api_id, api_hash,
             bot_token='1059263050:AAGGxs5Je7NNMYxf7DAIW6hbfw3JUsCoCPY')

# Keep track of the progress while downloading


def progress(current, total):
    print(f"{current * 100 / total:.1f}%")


def HandleCommands(command):
    if(command == "/status"):
        return 'Yes Am Alive !'
    elif(command == "/get-data"):
        arr = os.listdir('downloads')
        if(arr == None):
            return "No Data Available"
        return arr
    elif(command == "/current-task"):
        return "Getting Current Tasks"
    else:
        return "Unknown Command"


@app.on_message(filters.private)
async def hello(client, message):
    try:
        # handle Commands here
        print(message.text)

        # First Handle All Commands
        if(message.text.startswith('/')):
            await message.reply_text(HandleCommands(message.text))
            return

        # First We will Check if Message contains a VideoFile or Not
        if(message.video == None):
            await message.reply_text(f"Hey {message.from_user.first_name}, This message doesn't contain any downloadable media")
        # if It Contains a Video Files , then we can Download It
        else:
            await message.reply_text(f"Downloading File : {message.video.file_name}")
            await app.download_media(message, progress=progress, progress_args={})
            await message.reply_text(f"File Downloaded Successfully to the System")
    except Exception as error:
        await message.reply_text(f"Error : {error}")

app.run()
