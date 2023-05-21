### PMM - Personal Money Management

from ocr import perform_ocr
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()  # take environment variables from .env.
TOKEN = os.getenv('TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')
ID_USER = int(os.getenv('ID_USER'))


# commands
async def start_command(update, context):
    if update.message.chat.id == ID_USER:
        start_text = 'Hola Raul!!!'
    else:
        start_text = 'This is a private test bot, sorry!'
    await update.message.reply_text(start_text)


async def help_command(update, context):
    if update.message.chat.id == ID_USER:
        help_text = 'Raul, de verdad necesitas ayuda???'
    else:
        help_text = 'There is not help because, This is a private test bot, sorry!'
    await update.message.reply_text(help_text)


# Responses

def handle_responses(text: str) -> str:
    if 'hello' in text:
        return 'Hi, there!!!!'
    else:
        return 'no se...'


async def handle_message(update, context):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User: ({update.message.chat.id}) in {message_type}: {text}')

    if message_type == 'group':
        if BOT_USERNAME in text and update.message.chat.id == ID_USER:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_responses(new_text)
        else:
            return
    elif update.message.chat.id == ID_USER:
        response: str = handle_responses(text)

    else:
        return

    print('bot:', response)
    await update.message.reply_text(response)

async def handle_photo(update: Update, context):
    # Get the photo file ID
    message = update.effective_message
    photo_file_id = message.photo[-1].file_id
    new_file = await context.bot.get_file(photo_file_id)
    await new_file.download_to_drive('file_name.jpg')

    # Get the path to the image
    image_path = 'file_name.jpg'
    text = perform_ocr(image_path)

    await update.message.reply_text(text)

async def error(update, context):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting...')
    app = Application.builder().token(TOKEN).build()
    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)
