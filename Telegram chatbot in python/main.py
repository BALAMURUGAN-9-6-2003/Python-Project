from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import pprint
import google.generativeai as palm
import os
# bot api
t="AIzaSyCCPspemrQ7h66milbj4foyKIJXAC-Ki08"
palm.configure(api_key=t)
# bot api end 

# telegram API
Token: Final = ("6861281972:AAF-qsmqZwcw7vlb5PqAcjkdsuTI6Ryzxm0")
username: Final = "@Aibasebot"
# telegram API end
async def Start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Welcome to our AI assistant.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("How can I help you?")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command.")

async def handle(text: str):
    text = text.lower()
    prompt = text
    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name
    print(model)
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        # The maximum length of the response
        max_output_tokens=800,
    )
    if text.lower()=="exit":
            quit()
    return (completion.result)

async def handel_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.message.chat.type
        tex = update.message.text

        print(f"user ({update.message.chat.id}) in {message}: {tex}")
        if message == "group":
            if username in tex:
                new_text = tex.replace(username, "").split()
                response = await handle(new_text)
            else:
                return
        
        else:
            response = await handle(tex)
        print("bot:", response)
        await update.message.reply_text(response)
    except Exception as e:
        print(f"An error occurred: {e}")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused an error: {context.error}")

if __name__ == "__main__":
    print("Program start")
    app = Application.builder().token(Token).build()

    app.add_error_handler(CommandHandler("start", Start_command))
    app.add_error_handler(CommandHandler("help", help_command))
    app.add_error_handler(CommandHandler("custom", custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handel_msg))
    app.add_error_handler(error)
    
    app.run_polling(poll_interval=2)
