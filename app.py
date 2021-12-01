from pyrogram import Client, filters
import os
import time
import shutil
from progress import ShowProgress
from tinydb import TinyDB, Query
import json

api_id = 1848117
api_hash = '86e7152a80b430f838c83c7f9258b37c'
app = Client("my_account", api_id, api_hash,
             bot_token='1059263050:AAGGxs5Je7NNMYxf7DAIW6hbfw3JUsCoCPY')


db = TinyDB('db.json')
Tasks = Query()


def HandleCommands(command):
    # Check if BOT is Alive
    if(command == "/status"):
        return 'Yes Am Alive !'
    # To Get List of Already Downloaded Data
    elif(command == "/data"):
        arr = os.listdir('downloads')
        # First Check if our Downloaded Folder is Empty
        if not arr:
            return "No Data Available , send me a Telegram File"
        # Then Convert list to Better View
        AvailableData = f"Total : {len(arr)}"+"\n"
        count = 1
        for x in arr:
            AvailableData = AvailableData+"\n"+f"{count}. "+x
            count = count+1
        return AvailableData
    # To Get Disk Space of System
    elif(command == "/disk_space"):
        total, used, free = shutil.disk_usage("/")
        DiskSpace = "**Total**: %d GiB" % (total // (2**30))+"\n" + "**Used**: %d GiB" % (
            used // (2**30))+"\n"+"**Free**: %d GiB" % (free // (2**30))
        return DiskSpace
    # To Get Ongoing Current Tasks
    elif(command == "/ongoing"):
        OngoingTasks = ""
        for item in db:
            print(item)
            OngoingTasks = OngoingTasks+"\n"+json.dumps(item)
        if(OngoingTasks == ""):
            return "No Ongoing Task Currently"
        return OngoingTasks
    # admin Commands
    elif(command == "/reset"):
        db.truncate()
        return 'Database Reset'
    elif(command == "/stopall"):
        app.stop_transmission()
        return 'All Downloads Stopped'
    else:
        return "Unknown Command"


@app.on_message(filters.private)
async def download_file(client, message):
    try:
        # handle Commands here
        print(message.text)
        # First Handle All Commands
        if(message.text != None):
            if(message.text.startswith('/')):
                await message.reply_text(HandleCommands(message.text))
                return

        # First We will Check if Message contains a VideoFile or Not
        if(message.video == None):
            await message.reply_text(f"Hey {message.from_user.first_name}, This message doesn't contain any downloadable media")
        # if It Contains a Video Files , then we can Download It
        else:
            FileName = message.video.file_name
            FileSize = message.video.file_size

            # Wait For Starting Download
            sentm = await message.reply_text(f"Hold on !! Preparing For Download : {FileName}", quote=True)
            # Now Update Progress
            startTime = time.perf_counter()
            db.insert({'file': FileName})
            await app.download_media(message, progress=ShowProgress().progress, progress_args=(FileName, FileSize, sentm, startTime))
            await message.reply_text("File Downloaded Successfully , now you can send Another File", quote=True)
            db.remove(Tasks.file == FileName)
    except Exception as error:
        try:
            print(f"Error : {error}")
            if(message.video != None):
                db.remove(Tasks.file == FileName)
                await sentm.edit(f"Error : {error}")
                return
            await message.reply_text(f"Error : {error}", quote=True)
        except:
            await message.reply_text('Error : something went wrong !')
app.run()
