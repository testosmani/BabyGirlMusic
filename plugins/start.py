from pyrogram import filters, Client
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from core.bot import Bot
from database.lang_utils import get_message as gm
from functions.youtube_utils import get_yt_details, download_yt_thumbnails

bot = Bot()


@Client.on_message(filters.command("start"))
async def pm_start(_, message: Message):
    bot_username = (await bot.get_me()).username
    bot_name = (await bot.get_me()).first_name
    chat_id = message.chat.id
    mention = message.from_user.mention
    user_id = message.from_user.id
    if message.chat.type == "private":
        if len(message.command) == 1:
            msg = START_TEXT.format(message.from_user.mention(), bot_name, bot_username)
            return await message.reply_text(text = msg,
                                            reply_markup = START_BUTTONS)


   START_TEXT = """💔 ʜᴇʏ {} !\n\nɪ ᴍ [{}](t.me/{}),\nɪ ᴄᴀɴ ᴘʟᴀʏ ᴀɴʏ ᴍᴇᴅɪᴀ ɪɴ ɢʀᴏᴜᴘ ᴛʜʀᴏᴜɢʜ ᴛʜᴇ ᴛᴇʟᴇɢʀᴀᴍ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ꜰᴇᴀᴛᴜʀᴇ !\nꜰɪɴᴅ ᴀʟʟ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ʙʏ ᴄʟɪᴄᴋɪɴɢ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ !\n━━━━━━━━━━━━━━━━━━━━━━
"""


   START_BUTTONS = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton( 
                   "😅 ᴀᴅᴅ ᴍᴇ ᴇʟsᴇ ʏᴏᴜ ɢᴇʏ ​😅", url=f"https://t.me/{bot_username}?startgroup=true"
                ),
            ],
            [
                InlineKeyboardButton("🤔 ʜᴇʟᴘ​ 🤔", callback_data="cbhelp"),
                InlineKeyboardButton(
                    "💕 ᴍᴀɪɴᴛᴀɪɴᴇʀ 💕​", url="https://t.me/anonymous_was_bot"
                ),
            ],
            [
                InlineKeyboardButton("😇 ᴄʜᴀɴɴᴇʟ​ 😇", url=config.CHANNEL_LINK),
                InlineKeyboardButton(
                    "💔 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ​💔", url="https://t.me/DevilsHeavenMF"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🙄 sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ 🙄​", url="https://t.me/DevilsHeavenMF",
                )
            ],
        ]
    )


        if len(message.command) >= 2:
            query = message.command[1]
            if query.startswith("ytinfo_"):
                link = query.split("ytinfo_")[1]
                details = get_yt_details(link)
                thumb_url = details["thumbnail"]
                thumb_file = download_yt_thumbnails(thumb_url, user_id)
                result_text = f"""
{gm(chat_id, 'track_info')}
📌 **{gm(chat_id, 'yt_title')}**: {details['title']}
🕰 **{gm(chat_id, 'duration')}**: {details['duration']}
👍 **{gm(chat_id, 'yt_likes')}**: {details['likes']}
👎 **{gm(chat_id, 'yt_dislikes')}**: {details['dislikes']}
⭐ **{gm(chat_id, 'yt_rating')}**: {details['rating']}
"""
                return await message.reply_photo(
                    thumb_file,
                    caption=result_text,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    f"🎥 {gm(chat_id, 'watch_on_yt')}",
                                    url=f"https://www.youtube.com/watch?v={details['link']}",
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    f"🗑 {gm(chat_id, 'close_btn_name')}",
                                    callback_data="close",
                                )
                            ],
                        ]
                    ),
                )
            if query.startswith("help"):
                return await message.reply(
                    gm(chat_id, "helpmusic"),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    f"{gm(chat_id, 'commands')}",
                                    url="https://telegra.ph/The-Bot-Command-11-14",
                                )
                            ]
                        ]
                    ),
                    disable_web_page_preview=True,
                )
    if message.chat.type in ["group", "supergroup"]:
        await message.reply(
            gm(chat_id, "chat_greet").format(mention, bot_name),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            gm(message.chat.id, "group_buttn"),
                            url=f"https://t.me/{bot_username}?start=help",
                        )
                    ]
                ],
            ),
            disable_web_page_preview=True,
        )


__cmds__ = ["start"]
__help__ = {
    "start": "help_start"
}
