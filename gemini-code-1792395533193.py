import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8657191025:AAFaZNt4IW-coJhQKbvgo4Uceu_BRNFSJHM"

# Tu ID de Administrador configurado
ADMIN_ID = 8046948909  

# Estado global del servidor (por defecto en Verde / Activo)
estado_servidor = {
    "activo": True,
    "mensaje": "🟢 **Estado del Servidor:** Operativo y funcionando al 100%."
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    mensaje_publico = (
        "👋 **¡Bienvenido al Bot Oficial de CASAWA!**\n\n"
        "Usa el comando `/menu` para ver la lista de comandos disponibles."
    )
    
    # Si eres el Administrador, incluye también la nota especial
    if user_id == ADMIN_ID:
        mensaje_publico += (
            "\n\n👑 **Hola Administrador:**\n"
            "• Usa `/menu` para ver tus comandos de control.\n"
            "• Usa `/menugeneral` para ver el menú que ven los clientes."
        )
        
    await update.message.reply_text(mensaje_publico, parse_mode="Markdown")

# Comando /menu (Privado para el Admin, Público para los clientes)
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id == ADMIN_ID:
        # Menú exclusivo para ti
        mensaje_admin = (
            "👑 **Menú Privado de Administrador:**\n\n"
            "• `/setestado verde` - Cambia el estado del servidor a Verde (Operativo).\n"
            "• `/setestado rojo` - Cambia el estado del servidor a Rojo (Mantenimiento).\n"
            "• `/say [mensaje]` - Envía un mensaje a través del bot.\n"
            "• `/menugeneral` - Muestra el menú público de los clientes."
        )
        await update.message.reply_text(mensaje_admin, parse_mode="Markdown")
    else:
        # Menú para todos los usuarios clientes
        await menu_general_texto(update)

# Comando /menugeneral (Ver el menú público de los usuarios)
async def menu_general(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await menu_general_texto(update)

# Función auxiliar para enviar el menú público
async def menu_general_texto(update: Update):
    mensaje_cliente = (
        "📌 **Menú General (Público):**\n\n"
        "• `/contacto` - Información de contacto.\n"
        "• `/tutorial` - Guía e instrucciones.\n"
        "• `/estado` - Consulta el estado del servidor."
    )
    await update.message.reply_text(mensaje_cliente, parse_mode="Markdown")

# 1. Comando /contacto
async def contacto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "📩 **Contacto Oficial:**\n\n"
        "Puedes escribir directamente al administrador aquí:\n"
        "👉 @casawaxit"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# 2. Comando /tutorial (en blanco)
async def tutorial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" ")

# 3. Comando /estado (Público)
async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(estado_servidor["mensaje"], parse_mode="Markdown")

# 4. Comando /setestado (Solo tú puedes usarlo)
async def set_estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("⚠️ Uso correcto: `/setestado verde` o `/setestado rojo`", parse_mode="Markdown")
        return

    opcion = context.args[0].lower()

    if opcion in ["verde", "on", "activo"]:
        estado_servidor["activo"] = True
        estado_servidor["mensaje"] = "🟢 **Estado del Servidor:** Operativo y funcionando al 100%."
        await update.message.reply_text("✅ Estado cambiado a **VERDE** (Operativo).", parse_mode="Markdown")
        
    elif opcion in ["rojo", "off", "mantenimiento"]:
        estado_servidor["activo"] = False
        estado_servidor["mensaje"] = "🔴 **Estado del Servidor:** En mantenimiento / Fuera de servicio."
        await update.message.reply_text("🔴 Estado cambiado a **ROJO** (Mantenimiento).", parse_mode="Markdown")
        
    else:
        await update.message.reply_text("⚠️ Opción no válida. Usa `verde` o `rojo`.", parse_mode="Markdown")

# 5. Comando /say para enviar mensajes mediante el bot (Solo tú)
async def say(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("⚠️ Uso: `/say [mensaje]`", parse_mode="Markdown")
        return

    mensaje_a_enviar = " ".join(context.args)
    
    try:
        await update.message.delete()
    except Exception:
        pass

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=mensaje_a_enviar,
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers públicos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("menugeneral", menu_general))
    app.add_handler(CommandHandler("contacto", contacto))
    app.add_handler(CommandHandler("tutorial", tutorial))
    app.add_handler(CommandHandler("estado", estado))
    
    # Handlers privados para el Administrador
    app.add_handler(CommandHandler("setestado", set_estado))
    app.add_handler(CommandHandler("say", say))
    
    print("🤖 Bot cliente iniciado con menú general...")
    app.run_polling()
