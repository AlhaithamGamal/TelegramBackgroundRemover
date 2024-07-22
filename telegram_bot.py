# import telegram

# import asyncio


# TOKEN="7145260815:AAGqK_QCqhwlZSDwljcQUdxXHRiY40mg-b0"


# async def main():
#     bot=telegram.Bot(TOKEN)

#     async with bot:
#         # Update(message=Message(channel_chat_created=False,
#         #                         chat=Chat(first_name='Haitham',
#         #                                   id=908484157, last_name='Moussa',
#         #                                   type=<ChatType.PRIVATE>, username='Haithamgamal96'),
#         #                                   date=datetime.datetime(2024, 7, 22, 0, 55, 56, tzinfo=<UTC>),
#         #                                     delete_chat_photo=False,
#         #                                       entities=(MessageEntity(length=6, offset=0, type=<MessageEntityType.BOT_COMMAND>),),
#         #                                       from_user=User(first_name='Haitham', id=908484157, is_bot=False, language_code='en', last_name='Moussa', username='Haithamgamal96'),
#         #                                         group_chat_created=False, message_id=8, supergroup_chat_created=False, text='/start'), update_id=553419168)


#         update=((await bot.get_updates())[-1])
#         chat_id=update.message.chat.id
#         user_name=update.message.from_user.first_name
#         await bot.send_message(text=f'Hi     {user_name}',chat_id=chat_id)
#         # chat_id=update.User.id
#         # user_name=update.User.first_name
#         #print(update)


# if __name__ == '__main__':
#     asyncio.run(main())


import os 

from rembg import remove


from PIL import Image
from telegram import Update # type: ignore

from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters # type: ignore

import asyncio


TOKEN = "7145260815:AAGqK_QCqhwlZSDwljcQUdxXHRiY40mg-b0"


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Hi, I\'m a background remover bot  ')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=' to remove a background from image please send me image ! ')



async def process_image(photo_name:str):
    name,_=os.path.splitext(photo_name)
    ouput_photo_path = f'./processed/{name}.png'
    Input = Image.open(f'./temp/{photo_name}')
    output=remove(Input)
    output.save(ouput_photo_path)
    os.remove(f'./temp/{photo_name}')
    return ouput_photo_path



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if filters.PHOTO.check_update(update):
        file_id = update.message.photo[-1].file_id #last size in the array of objs
        unique_file_id=update.message.photo[-1].file_unique_id
        photo_name=f"{unique_file_id}.jpg"
    elif filters.Document.IMAGE:
        file_id=update.message.document.file_id
        _,f_ext=os.path.splitext(update.message.document.file_name)
        unique_file_id=update.message.document.file_unique_id
        photo_name=f'{unique_file_id}.{f_ext}'


    photo_file = await context.bot.get_file(file_id)
    await photo_file.download_to_drive(custom_path=f'./temp/{photo_name}') 
    await context.bot.send_message(chat_id=update.effective_chat.id,text="we are processing your photo please wait...")
    processed_image = await process_image(photo_name)
    await context.bot.send_document(chat_id=update.effective_chat.id,document=processed_image)
    os.remove(processed_image)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()



    help_handler = CommandHandler('help', help)
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_message)
    application.add_handler(help_handler)
    application.add_handler(start_handler)
    application.add_handler(message_handler)

    application.run_polling()
