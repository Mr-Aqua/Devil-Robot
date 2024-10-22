import time, re, psutil
from platform import python_version
from telegram import __version__ as ptbver

from sys import argv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import escape_markdown, mention_html
from Devil.Handlers.validation import is_user_admin

from telegram.error import (
    BadRequest,
    Unauthorized,
)

from Devil import (
    OWNER_ID,
    OWNER_USERNAME,
    dispatcher, 
    StartTime,
    LOGGER,
    SUPPORT_CHAT,
    WEBHOOK,
    CERT_PATH,
    PORT,
    URL,
    TOKEN,
    PHOTO,
    telethn,
    updater)

from Devil.Modules import ALL_MODULES
from Devil.__help__ import (
get_help, 
help_button, 
get_settings, 
settings_button, 
migrate_chats, 
send_help, 
send_settings,
HELP_STRINGS,
IMPORTED,
IMPORTED,
HELPABLE,)


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


PM_START_TEXT = """ 
Devil is sleeping.................

"""




def start(update: Update, context: CallbackContext):
    args = context.args
    bot = context.bot
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    first_name = update.effective_user.first_name
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="⬅️ BACK", callback_data="help_back")]]
                    ),
                )
                
                

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            update.effective_message.reply_text(
                PM_START_TEXT.format(
                        escape_markdown(first_name), escape_markdown(context.bot.first_name)),
                reply_markup=InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            text="➕️ Add me to your chat ➕️", url=f"https://t.me/{context.bot.username}?startgroup=true"),
    ],
    [
        
        InlineKeyboardButton(
            text="Bot Info", callback_data="Devil_"
        ),
    ],
    [
        InlineKeyboardButton(text="Helps & Commands❔", callback_data="help_back"),
    ],
]),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
            text = (
                f"Hello {mention_html(user.id, user.first_name)}, I'm {bot.first_name}\n\n"
                f"┏━━━━━━━━━━━━━━━━━━━\n"
                f"┣[• Uptime : {uptime} \n"
                f"┣[• Core : {psutil.cpu_percent()}%\n"
                f"┣[• P-T-B : Ver {str(ptbver)} \n"
                f"┣[• Python   : Ver {python_version()} \n"
                f"┗━━━━━━━━━━━━━━━━━━━")
        

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="SUPPORT", 
                        url=f"https://t.me/{SUPPORT_CHAT}"),
                    InlineKeyboardButton(
                        text="DEVLOPER", 
                        url=f"https://t.me/{OWNER_USERNAME}")
                    
                ],
                
                ])
            message.reply_photo(
                        PHOTO,
                        caption=(text),
                        reply_markup=keyboard,
                        parse_mode=ParseMode.HTML,
                        
                    )

                



def Devil_about_callback(update: Update, context: CallbackContext):
    first_name = update.effective_user.first_name
    query = update.callback_query
    if query.data == "Devil_":
        query.message.edit_text(
            text="""Hello *{}*, My name is *{}*. A Powerful Telegram Group Management Bot built to help you manage Group easily.
            \n ‣ I can Restrict Users.
            \n ‣ I can Greet Users with customizable welcome message and even set a group rules
            \n ‣ I have an advanced Anti-Flood System which will help you to safe group from Spammmer.
            \n ‣ I can Warn Users until they reach max Warns, with each predefined actions such as Ban, Mute and Kick etc.
            \n ‣ I have Note Keeping System, Blacklists, And even Predetermined replies on certain keywords.
            \n ‣ I check Admins Permissions before perform any Command and more Stuffs.
            \n ‣ I have an advanced Artificial Chatbot System, so can talk with users like humans.
            \n\n*If you have any Question, You can join Support Chat. My Developer Team will Answer. Check Link Below*""".format(
                        escape_markdown(first_name), escape_markdown(context.bot.first_name)),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                   [
                     InlineKeyboardButton(text="Support", url="t.me/Devil_Support"),
                     InlineKeyboardButton(text="News", url="t.me/Devil_Updates"),
                   ],
                   [
                    InlineKeyboardButton(text="Back", callback_data="Devil_back")
                   ]
                ]
            ),
        )
    elif query.data == "Devil_back":
        query.message.edit_text(
                PM_START_TEXT.format(
                        escape_markdown(first_name), escape_markdown(context.bot.first_name)),
                reply_markup=InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            text="➕️ Add me to your chat ➕️", url=f"https://t.me/{context.bot.username}?startgroup=true"),
    ],
    [
        
        InlineKeyboardButton(
            text="Bot Info", callback_data="Devil_"
        ),
    ],
    [
        InlineKeyboardButton(text="Helps & Commands❔", callback_data="help_back"),
    ],
]),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
        )


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            stringz = "My dear Owner , I'm Working Again. Thanks to make me live."
            dispatcher.bot.sendMessage(f"@{SUPPORT_CHAT}", stringz)
        except Unauthorized:
            LOGGER.warning(
                "Bot isnt able to send message to support_chat, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    start_handler = CommandHandler("start", start, pass_args=True, run_async=True)

    help_handler = CommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_.*", run_async=True)
    

    about_callback_handler = CallbackQueryHandler(Devil_about_callback, pattern=r"Devil_", run_async=True)

    settings_handler = CommandHandler("settings", get_settings, run_async=True)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_", run_async=True)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats, run_async=True)

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(allowed_updates=Update.ALL_TYPES, timeout=15, read_latency=4, drop_pending_updates=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()



if __name__ == "__main__":
    LOGGER.info("Successfully loaded Modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    main()
