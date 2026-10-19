import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8657191025:AAFaZNt4IW-coJhQKbvgo4Uceu_BRNFSJHM"
API_BASE = "http://155.117.40.185:10068/Wen0PWx!loa"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "👋 **¡Bienvenido al Bot de Verificación!**\n\n"
        "Usa el siguiente comando para comprobar tu key:\n"
        "• `/check [tu_key]`"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def check_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Uso correcto: `/check [tu_key]`", parse_mode="Markdown")
        return

    user_key = context.args[0]
    url = f"{API_BASE}/check?key={user_key}"

    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Comprobamos si la API responde con éxito (key válida)
            if data.get("success") is True:
                await update.message.reply_text(
                    f"✅ La key `{user_key}` **está activa y funciona correctamente**.",
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    f"❌ La key `{user_key}` **no es válida o ha expirado**.",
                    parse_mode="Markdown"
                )
        else:
            await update.message.reply_text(
                f"❌ La key `{user_key}` no existe en el sistema.",
                parse_mode="Markdown"
            )
            
    except Exception as e:
        await update.message.reply_text("⚠️ Ocurrió un error al conectar con el servidor de licencias.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_key))
    
    print("🤖 Bot de verificación iniciado...")
    app.run_polling()
