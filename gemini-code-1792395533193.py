import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8657191025:AAFaZNt4IW-coJhQKbvgo4Uceu_BRNFSJHM"
API_BASE = "http://155.117.40.185:10068/Wen0PWx!loa"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "👋 **¡Bienvenido al Bot de Consulta de Licencias de CASAWA!**\n\n"
        "Aquí puedes verificar el estado de tus accesos o llaves.\n\n"
        "📌 **Comando disponible:**\n"
        "• `/check [tu_key]` - Consulta el tiempo y estado de tu key."
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
            # Puedes personalizar este mensaje según lo que devuelva exactamente tu API
            await update.message.reply_text(
                f"✅ **Estado de la Key**\n\n"
                f"🔑 Key: `{user_key}`\n"
                f"📄 Respuesta del servidor:\n```json\n{data}\n```",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(f"❌ La key `{user_key}` no existe o es inválida.", parse_mode="Markdown")
            
    except Exception as e:
        await update.message.reply_text("⚠️ Ocurrió un error al conectar con el servidor de licencias.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_key))
    
    print("🤖 Bot de consultas conectado a la API iniciado...")
    app.run_polling()
