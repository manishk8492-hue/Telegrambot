import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

# ================= Configuration =================
API_ID = "32149732"          
API_HASH = "7dcf6b0608179fa120a9be12749404e2"      
BOT_TOKEN = "8601807064:AAE20vm4pGcyO0jn0A91MmJMrgt65lEKymw"    

# The channel users MUST join (Bot must be an admin in this channel)
# NOTE: Make sure the bot is an Admin in this exact channel!
FSUB_CHANNEL_ID = -1003767135679 

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
# =================================================

# --- Helper function to check if user joined the channel ---
async def is_subscribed(client, user_id):
    try:
        member = await client.get_chat_member(FSUB_CHANNEL_ID, user_id)
        # Using string matching here prevents crashes on newer Pyrogram versions
        status = str(member.status).lower()
        if "left" in status or "kicked" in status or "banned" in status:
            return False
        return True
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"Error checking sub: {e}")
        # If bot is not admin in channel or channel ID is wrong
        return False

# --- Start Command Handler ---
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    user_id = message.from_user.id
    
    # 1. Check Force Subscribe
    if not await is_subscribed(client, user_id):
        buttons = InlineKeyboardMarkup([[
                InlineKeyboardButton("Join Channel 1", url="https://t.me/silentcreations"),
                InlineKeyboardButton("Join Channel 2", url="https://t.me/Hunter_x_Anime")
            ],[
                InlineKeyboardButton("Join Channel 3", url="https://t.me/ongoinganime1"),
                InlineKeyboardButton("Join Channel 4", url="https://t.me/javersacapital")
            ],[
                InlineKeyboardButton("🔄 Try Again", callback_data="check_sub")
            ]
        ])
        
        await message.reply_text(
            f"Hello {message.from_user.first_name}\n"
            "You need to join in my Channel/Group to use me\n\n"
            "Kindly Please join Channel",
            reply_markup=buttons
        )
        return

    # 2. If subscribed, send the files
    await send_video_files(client, message.chat.id)


# --- "Try Again" Button Logic ---
@app.on_callback_query(filters.regex("check_sub"))
async def check_sub_button(client, callback_query):
    user_id = callback_query.from_user.id
    
    if await is_subscribed(client, user_id):
        # Delete the "Please join" message
        await callback_query.message.delete()
        # Send the files
        await send_video_files(client, callback_query.message.chat.id)
    else:
        # Show an alert if they still haven't joined
        await callback_query.answer("You still haven't joined the channels!", show_alert=True)


# --- File Sending and Auto-Delete Logic ---
async def send_video_files(client, chat_id):
    files_to_send =[
        "BQACAgUAAxkBAAMJacQpHJjITxhtFfLM1AqQWXFNfbUAAiEjAALGsAlWcJR0CVKlLcoeBA",
        "BQACAgUAAxkBAAMLacQpL8yJAoW2tZUGkCckzqjRFrQAAiIjAALGsAlWw-dHz_s_tIMeBA",
        "BQACAgUAAxkBAAMNacQpNPQQ4JLqVqekFGsSfYQ2gqsAAiMjAALGsAlWQCq02RJiQoIeBA",
        "BQACAgUAAxkBAAMPacQpOGyJHeNNbmMrPETkDFj3jQ4AAiUjAALGsAlWoVU_l3lny8seBA",
        "BQACAgUAAxkBAAMRacQpPVjA-pDOaZQUuJcz3x9o6tsAAiYjAALGsAlWpMpPDd-xA_IeBA",
        "BQACAgUAAxkBAAMTacQpTXvOW0MDApBMTbKwcs1OwhAAAigjAALGsAlWWfRks595S3keBA",
        "BQACAgUAAxkBAAMVacQpUVUrYy7qnS-kpQIKE9PWPT0AAikjAALGsAlW6brf0G3TmpweBA",
        "BQACAgUAAxkBAAMXacQpVpaG5oE3SY6cQNbxtozb230AAiojAALGsAlWs3InNj7aexQeBA",
        "BQACAgUAAxkBAAMZacQpWynqqlPvmUF7PwtNGEhvqMQAAisjAALGsAlWx75-F-wWKzweBA",
        "BQACAgUAAxkBAAMbacQpYNfzkxnXrEvvA5h-uP9epaEAAiwjAALGsAlWOJ0T2uKpCeweBA",
        "BQACAgUAAxkBAAMdacQpZMNlmSFIvpMD1m4r6ve7geoAAi0jAALGsAlWeafGdmswIq0eBA",
        "BQACAgUAAxkBAAMfacQpaKgeouYr5pOgTa3IBKlS7-wAAi4jAALGsAlWgRDos-B5N1seBA",
        "BQACAgUAAxkBAAMhacQpcOQ-6SMddElzMc2D8JgpVmkAAi8jAALGsAlW9c1y-VIPPJUeBA",
    ]
    
    sent_messages =[]
    
    # Send all files safely with Error Catching
    for file_id in files_to_send:
        try:
            msg = await client.send_document(
                chat_id=chat_id,
                document=file_id,
                caption="hells paradise season 1 [dual]"
            )
            sent_messages.append(msg)
            await asyncio.sleep(0.5) # Small delay to prevent flood waits
        except Exception as e:
            print(f"❌ ERROR SENDING FILE: {e}")
            await client.send_message(chat_id, f"❌ **Failed to send file!**\n\n**Error Details:** `{e}`\n\n_(If it says FILE_REFERENCE_EXPIRED or INVALID, please send the video to me directly to get a new File ID)_")
            return # Stop the process if sending fails
        
    # Send the auto-delete warning message
    warning_msg = await client.send_message(
        chat_id=chat_id,
        text="⚠️ **message**\nFile will be Auto Deleted in 15 minutes."
    )
    sent_messages.append(warning_msg)
    
    # Wait for 15 minutes (900 seconds)
    await asyncio.sleep(900)
    
    # Delete all sent messages
    for msg in sent_messages:
        try:
            await msg.delete()
        except Exception:
            pass # Ignore if user already deleted it themselves


# --- NEW TOOL: Get File IDs easily! ---
# If you send a video or document to the bot, it will give you the File ID
@app.on_message((filters.document | filters.video) & filters.private)
async def get_file_id(client, message):
    if message.document:
        file_id = message.document.file_id
    elif message.video:
        file_id = message.video.file_id
    
    await message.reply_text(f"**Here is your valid File ID:**\n`{file_id}`\n\nCopy this and paste it inside the `files_to_send` list in your code!")


if __name__ == "__main__":
    print("Bot is running...")
    app.run()
         
