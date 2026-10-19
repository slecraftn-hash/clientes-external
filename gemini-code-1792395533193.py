import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8657191025:AAFaZNt4IW-coJhQKbvgo4Uceu_BRNFSJHM"

# Tu ID de Administrador configurado
ADMIN_ID = 8046948909  

# Conjunto en memoria para almacenar los IDs de los usuarios
usuarios_registrados = set()

# Estado global del servidor (por defecto en Verde / Activo)
estado_servidor = {
    "activo": True,
    "mensaje": "🟢 **Estado del Servidor:** Operativo y funcionando al 100%."
}

async def registrar_usuario(user_id: int):
    """Guarda el ID del usuario para poder enviarle notificaciones globales."""
    usuarios_registrados.add(user_id)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await registrar_usuario(user_id)
    
    mensaje_publico = (
        "👋 **¡Bienvenido al Bot Oficial de CASAWA!**\n\n"
        "Usa el comando `/menu` para ver la lista de comandos disponibles."
    )
    
    if user_id == ADMIN_ID:
        mensaje_publico += (
            "\n\n👑 **Hola Administrador:**\n"
            "• Usa `/menu` para ver tus comandos de control.\n"
            "• Usa `/menugeneral` para ver el menú que ven los clientes."
        )
        
    await update.message.reply_text(mensaje_publico, parse_mode="Markdown")

# Comando /menu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await registrar_usuario(user_id)
    
    if user_id == ADMIN_ID:
        mensaje_admin = (
            "👑 **Menú Privado de Administrador:**\n\n"
            "• `/setestado verde` - Cambia el estado público a Verde.\n"
            "• `/setestado rojo` - Cambia el estado público a Rojo.\n"
            "• `/mensaje [texto]` - Envía un comunicado masivo a TODOS los usuarios.\n"
            "• `/say [texto]` - Envía un mensaje como si fuera el bot en el chat actual.\n"
            "• `/menugeneral` - Muestra el menú público de los clientes."
        )
        await update.message.reply_text(mensaje_admin, parse_mode="Markdown")
    else:
        await menu_general_texto(update)

# Comando /menugeneral
async def menu_general(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await registrar_usuario(update.effective_user.id)
    await menu_general_texto(update)

async def menu_general_texto(update: Update):
    mensaje_cliente = (
        "📌 **Menú General (Público):**\n\n"
        "• `/contacto` - Información de contacto.\n"
        "• `/tutorial` - Guía e instrucciones.\n"
        "• `/estado` - Consulta el estado del servidor."
    )
    await update.message.reply_text(mensaje_cliente, parse_mode="Markdown")

# Comando /contacto
async def contacto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await registrar_usuario(update.effective_user.id)
    mensaje = (
        "📩 **Contacto Oficial:**\n\n"
        "Puedes escribir directamente al administrador aquí:\n"
        "👉 @casawaxit"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# Comando /tutorial
async def tutorial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await registrar_usuario(update.effective_user.id)
    await update.message.reply_text(" ")

# Comando /estado (Consulta pública idéntica para todos)
async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await registrar_usuario(update.effective_user.id)
    await update.message.reply_text(estado_servidor["mensaje"], parse_mode="Markdown")

# Comando /setestado (Solo Admin) - Cambia el estado público (Verde/Rojo)
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
        await update.message.reply_text("✅ Estado público actualizado a **VERDE** (Operativo).", parse_mode="Markdown")
        
    elif opcion in ["rojo", "off", "mantenimiento"]:
        estado_servidor["activo"] = False
        estado_servidor["mensaje"] = "🔴 **Estado del Servidor:** En mantenimiento / Fuera de servicio."
        await update.message.reply_text("🔴 Estado público actualizado a **ROJO** (Mantenimiento).", parse_mode="Markdown")
        
    else:
        await update.message.reply_text("⚠️ Opción no válida. Usa `verde` o `rojo`.", parse_mode="Markdown")

# Comando /mensaje (Solo Admin) - Envío masivo a todos los usuarios
async def mensaje_masivo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("⚠️ Uso correcto: `/mensaje [tu comunicado o aviso]`", parse_mode="Markdown")
        return

    texto_difusion = " ".join(context.args)
    comunicado_completo = f"📢 **Aviso General:**\n\n{texto_difusion}"
    
    await update.message.reply_text(f"🚀 Enviando comunicado masivo a {len(usuarios_registrados)} usuario(s)...")
    
    enviados = 0
    for uid in list(usuarios_registrados):
        try:
            await context.bot.send_message(chat_id=uid, text=comunicado_completo, parse_mode="Markdown")
            enviados += 1
        except Exception:
            pass
            
    await update.message.reply_text(f"✅ Mensaje enviado con éxito a {enviados} usuario(s).")

# Comando /say (Solo Admin)
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
    app.add_handler(CommandHandler("mensaje", mensaje_masivo))
    app.add_handler(CommandHandler("say", say))
    
    print("🤖 Bot actualizado y listo...")
    app.run_polling()
