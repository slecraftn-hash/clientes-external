import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8657191025:AAFaZNt4IW-coJhQKbvgo4Uceu_BRNFSJHM"

# Tu ID de Administrador configurado
ADMIN_ID = 8046948909  

# Conjunto en memoria para almacenar los IDs de los usuarios
usuarios_registrados = set()

# Estados globales de los dos servicios
servicios_estado = {
    "external": {
        "activo": True,
        "nombre": "External"
    },
    "proxy": {
        "activo": True,
        "nombre": "Proxy"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # Notifica al Administrador únicamente si es la primera vez que inicia el bot
    if user_id not in usuarios_registrados:
        usuarios_registrados.add(user_id)
        
        # Si no eres tú mismo, te manda la alerta de nuevo registro
        if user_id != ADMIN_ID:
            username = f"@{user.username}" if user.username else "Sin username"
            nombre = user.full_name or "Usuario"

            mensaje_registro = (
                f"🎉 **¡Nuevo Usuario Registrado!**\n\n"
                f"👤 **Nombre:** {nombre}\n"
                f"🏷️ **User:** {username}\n"
                f"🆔 **ID:** `{user_id}`\n"
                f"📊 **Total registrados:** {len(usuarios_registrados)}"
            )
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=mensaje_registro,
                    parse_mode="Markdown"
                )
            except Exception:
                pass

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
    
    if user_id == ADMIN_ID:
        mensaje_admin = (
            "👑 **Menú Privado de Administrador:**\n\n"
            "• `/setexternal verde` / `/setexternal rojo` - Cambia estado de External y notifica.\n"
            "• `/setproxy verde` / `/setproxy rojo` - Cambia estado de Proxy y notifica.\n"
            "• `/mensaje [texto]` (o adjuntando foto/video) - Envía un comunicado masivo a TODOS.\n"
            "• `/say [texto]` - Envía un mensaje como el bot en este chat.\n"
            "• `/menugeneral` - Muestra el menú público de los clientes."
        )
        await update.message.reply_text(mensaje_admin, parse_mode="Markdown")
    else:
        await menu_general_texto(update)

# Comando /menugeneral
async def menu_general(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await menu_general_texto(update)

async def menu_general_texto(update: Update):
    mensaje_cliente = (
        "📌 **Menú General (Público):**\n\n"
        "• `/contacto` - Información de contacto.\n"
        "• `/tutorial` - Guía e instrucciones.\n"
        "• `/estado` - Consulta el estado del External y Proxy."
    )
    await update.message.reply_text(mensaje_cliente, parse_mode="Markdown")

# Comando /contacto
async def contacto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "📩 **Contacto Oficial:**\n\n"
        "Puedes escribir directamente al administrador aquí:\n"
        "👉 @casawaxit"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# Comando /tutorial
async def tutorial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" ")

# Comando /estado (Muestra el estado actual)
async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ext_icon = "🟢" if servicios_estado["external"]["activo"] else "🔴"
    ext_txt = "Operativo" if servicios_estado["external"]["activo"] else "En Mantenimiento"
    
    proxy_icon = "🟢" if servicios_estado["proxy"]["activo"] else "🔴"
    proxy_txt = "Operativo" if servicios_estado["proxy"]["activo"] else "En Mantenimiento"

    mensaje_estado = (
        "📊 **Estado Actual de los Servicios:**\n\n"
        f"{ext_icon} **External:** {ext_txt}\n"
        f"{proxy_icon} **Proxy:** {proxy_txt}"
    )
    await update.message.reply_text(mensaje_estado, parse_mode="Markdown")

# Función auxiliar para procesar cambio de estado
async def procesar_cambio_estado(update: Update, context: ContextTypes.DEFAULT_TYPE, servicio_key: str):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text(f"⚠️ Uso correcto: `/set{servicio_key} verde` o `/set{servicio_key} rojo`", parse_mode="Markdown")
        return

    opcion = context.args[0].lower()
    nombre_servicio = servicios_estado[servicio_key]["nombre"]
    notificacion = ""

    if opcion in ["verde", "on", "activo"]:
        servicios_estado[servicio_key]["activo"] = True
        notificacion = f"📢 **Actualización de Servicio:**\n\n🟢 El servicio **{nombre_servicio}** se encuentra **OPERATIVO** y funcionando al 100%."
    elif opcion in ["rojo", "off", "mantenimiento"]:
        servicios_estado[servicio_key]["activo"] = False
        notificacion = f"📢 **Actualización de Servicio:**\n\n🔴 El servicio **{nombre_servicio}** ha entrado en **MANTENIMIENTO**. Les avisaremos cuando esté activo nuevamente."
    else:
        await update.message.reply_text("⚠️ Opción no válida. Usa `verde` o `rojo`.", parse_mode="Markdown")
        return

    await update.message.reply_text(f"🚀 Estado de **{nombre_servicio}** actualizado. Enviando notificación masiva a {len(usuarios_registrados)} usuario(s)...", parse_mode="Markdown")
    
    enviados = 0
    for uid in list(usuarios_registrados):
        try:
            await context.bot.send_message(chat_id=uid, text=notificacion, parse_mode="Markdown")
            enviados += 1
        except Exception:
            pass

    await update.message.reply_text(f"✅ Notificación de **{nombre_servicio}** enviada con éxito a {enviados} usuario(s).")

# Comando /setexternal
async def set_external(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await procesar_cambio_estado(update, context, "external")

# Comando /setproxy
async def set_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await procesar_cambio_estado(update, context, "proxy")

# Comando /mensaje (Soporta texto y archivos multimedia con /mensaje en la descripción)
async def mensaje_masivo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    mensaje = update.message
    texto_difusion = " ".join(context.args) if context.args else ""
    if not texto_difusion and mensaje.caption:
        texto_difusion = mensaje.caption.replace("/mensaje", "").strip()

    if not texto_difusion and not mensaje.photo and not mensaje.video:
        await update.message.reply_text("⚠️ Escribe un texto o adjunta una foto/video con el comando `/mensaje`.", parse_mode="Markdown")
        return

    await update.message.reply_text(f"🚀 Enviando comunicado masivo a {len(usuarios_registrados)} usuario(s)...")
    
    enviados = 0
    for uid in list(usuarios_registrados):
        try:
            if mensaje.photo:
                photo_file = mensaje.photo[-1].file_id
                await context.bot.send_photo(chat_id=uid, photo=photo_file, caption=texto_difusion, parse_mode="Markdown")
            elif mensaje.video:
                video_file = mensaje.video.file_id
                await context.bot.send_video(chat_id=uid, video=video_file, caption=texto_difusion, parse_mode="Markdown")
            else:
                comunicado_completo = f"📢 **Aviso General:**\n\n{texto_difusion}"
                await context.bot.send_message(chat_id=uid, text=comunicado_completo, parse_mode="Markdown")
            enviados += 1
        except Exception as e:
            print(f"Error al enviar a {uid}: {e}")
            
    await update.message.reply_text(f"✅ Mensaje enviado con éxito a {enviados} usuario(s).")

# Comando /say
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
    app.add_handler(CommandHandler("setexternal", set_external))
    app.add_handler(CommandHandler("setproxy", set_proxy))
    app.add_handler(CommandHandler("mensaje", mensaje_masivo))
    app.add_handler(MessageHandler((filters.PHOTO | filters.VIDEO) & filters.CaptionRegex(r"^/mensaje"), mensaje_masivo))
    app.add_handler(CommandHandler("say", say))
    
    print("🤖 Bot listo con token limpio y soporte multimedia en /mensaje...")
    app.run_polling()
