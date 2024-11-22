from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, \
    CallbackQueryHandler, CommandHandler, ContextTypes

from credentials import ChatGPT_TOKEN, TELEGRAM_TOKEN
from gpt import ChatGptService
from util import load_message, load_prompt, send_text_buttons, send_text, \
    send_image, show_main_menu, Dialog, default_callback_handler

"""echo the user message"""
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

"""main menu"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = 'main'
    text = load_message('main')
    await send_image(update, context, 'main')
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        'start': 'Главное меню',
        'random': 'Узнать случайный интересный факт 🧠',
        'gpt': 'Задать вопрос чату GPT 🤖',
        'talk': 'Поговорить с известной личностью 👤',
        'quiz': 'Поучаствовать в квизе ❓',
        'cook': 'Узнать что приготовить 🍅'
    })

"""get random fact"""
async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = load_prompt('random')
    await send_image(update, context, 'random')
    message = await send_text(update, context, 'Please wait...')
    answer = await chat_gpt.send_question(prompt, ' ')
    await message.edit_text(answer)

"""ask ChatGPT"""
async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = 'gpt'
    prompt = load_prompt('gpt')
    message = load_message('gpt')
    chat_gpt.set_prompt(prompt)
    await send_image(update, context, 'gpt')
    await send_text(update, context, message)
async def gpt_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    message = await send_text(update, context, 'Please wait...')
    answer = await chat_gpt.add_message(text)
    await message.edit_text(answer)

"""talk to a celeb"""

talk_data = {
        'talk_cobain': 'Курт Кобейн',
        'talk_hawking': 'Стивен Хокинг',
        'talk_nietzsche': 'Фридрих Ницше',
        'talk_queen': 'Елизавета II',
        'talk_tolkien': 'Джон Толкин'
}
async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = 'talk'
    text = load_message('talk')
    await send_image(update, context, 'talk')
    await send_text_buttons(update, context, text, talk_data)
async def talk_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query.data
    await update.callback_query.answer()
    await send_image(update, context, query)
    await send_text(update, context, "Hello! I'll be glad to talk to you!")
    prompt = load_prompt(query)
    chat_gpt.set_prompt(prompt)
async def talk_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    message = await send_text(update, context, 'Please wait...')
    answer = await chat_gpt.add_message(text)
    await message.edit_text(answer)

"""play a quiz"""
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = 'quiz'
    dialog.count = 0
    text = load_message('quiz')
    await send_image(update, context, 'quiz')
    await send_text_buttons(update, context, text, {
        "quiz_prog": "Программирование на Python 💻",
        "quiz_biology": "Биология 🔬",
        "quiz_math": "Математика 🧮"
    })
async def quiz_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = load_prompt('quiz')
    chat_gpt.set_prompt(prompt)
    query = update.callback_query.data
    await update.callback_query.answer()
    answer = await chat_gpt.add_message(query)
    await send_text(update, context, answer)
async def quiz_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    message = await send_text(update, context, 'Please wait...')
    answer = await chat_gpt.add_message(text)
    if ('Правильно' in answer):
        dialog.count += 1
    await message.edit_text(f'{answer}\nКол-во правильных ответов: {dialog.count}')

"""come up with a recipe"""
async def cook(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = 'cook'
    prompt = load_prompt('cook')
    message = load_message('cook')
    chat_gpt.set_prompt(prompt)
    await send_image(update, context, 'cook')
    await send_text(update, context, message)
async def cook_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    message = await send_text(update, context, 'Please wait...')
    answer = await chat_gpt.add_message(text)
    await message.edit_text(answer)
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if dialog.mode == 'main':
        await start(update, context)
    elif dialog.mode == 'gpt':
        await gpt_dialog(update, context)
    elif dialog.mode == 'talk':
        await talk_dialog(update, context)
    elif dialog.mode == 'quiz':
        await quiz_dialog(update, context)
    elif dialog.mode == 'cook':
        await cook_dialog(update, context)
    else:
        await echo(update, context)

dialog = Dialog()
dialog.mode = None

chat_gpt = ChatGptService(ChatGPT_TOKEN)
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

#to handle cmd (start with /)
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('random', random))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(CommandHandler('talk', talk))
app.add_handler(CommandHandler('quiz', quiz))
app.add_handler(CommandHandler('cook', cook))

#to handle msg (text, media or status update)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

#to handle Telegram callback query
app.add_handler(CallbackQueryHandler(talk_button, pattern='^talk_.*'))
app.add_handler(CallbackQueryHandler(quiz_button, pattern='^quiz_.*'))
app.add_handler(CallbackQueryHandler(default_callback_handler))
app.add_handler(CallbackQueryHandler(text_handler))
app.run_polling()
