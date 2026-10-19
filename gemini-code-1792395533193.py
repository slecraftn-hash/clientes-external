import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Token de tu nuevo bot de consultas
TOKEN = "8657191025:AAFaZNt4IW-coJhQKbvgo4Uceu_BRNFSJHM"

# Diccionario o registro de permisos (puedes sincronizarlo o conectarlo con tu base de datos)
user_permissions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "👋 **¡Bienvenido al Bot de Consulta de Licencias de CASAWA!**\n\n"
        "Aquí puedes verificar el estado de tu acceso y cuánto tiempo te queda.\n\n"
        "📌 **Comandos disponibles:**\n"
        "• `/mi_tiempo` - Revisa el tiempo restante de tu cuenta actual.\n"
        "• `/check [usuario]` - Consulta el tiempo de un usuario específico."
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def mi_tiempo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    if not username:
        await update.message.reply_text("⚠️ Necesitas tener un nombre de usuario (@username) configurado en Telegram para consultar tu acceso.")
        return

    username = username.lower()
    
    if username in user_permissions:
        expiracion = user_permissions[username]
        ahora = datetime.datetime.now()
        
        if ahora < expiracion:
            restante = expiracion - ahora
            dias = restante.days
            horas, rem = divmod(restante.seconds, 3600)
            minutos, _ = divmod(rem, 60)
            
            await update.message.reply_text(
                f"✅ **Tu acceso está ACTIVO**\n\n"
                f"👤 Usuario: @{username}\n"
                f"⏳ Tiempo restante: **{dias} días, {horas} horas y {minutos} minutos**\n"
                f"📅 Expiración: `{expiracion.strftime('%Y-%m-%d %H:%M')}`",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(f"❌ Tu acceso para @{username} ha **expirado**.")
    else:
        await update.message.reply_text(f"❓ El usuario @{username} no tiene ninguna licencia activa registrada.")

async def check_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso correcto: `/check [username]`", parse_mode="Markdown")
        return

    target = context.args[0].replace("@", "").lower()

    if target in user_permissions:
        expiracion = user_permissions[target]
        ahora = datetime.datetime.now()
        
        if ahora < expiracion:
            restante = expiracion - ahora
            dias = restante.days
            horas, rem = divmod(restante.seconds, 3600)
            minutos, _ = divmod(rem, 60)
            
            await update.message.reply_text(
                f"🔎 **Estado de la licencia**\n\n"
                f"👤 Usuario: @{target}\n"
                f"🟢 Estado: **Activa**\n"
                f"⏳ Restante: **{dias}d {horas}h {minutos}m**",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(f"🔴 La licencia de @{target} está **expirada**.")
    else:
        await update.message.reply_text(f"⚠️ No se encontró registro para @{target}.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mi_tiempo", mi_tiempo))
    app.add_handler(CommandHandler("check", check_user))
    
    print("🤖 Bot de consultas de clientes iniciado...")
    app.run_polling()