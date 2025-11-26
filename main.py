import logging
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ContextTypes, ConversationHandler
)

# Configuração
import os
TOKEN = os.environ.get("TOKEN")
ADMIN_GROUP_ID = -1003068867391
CHANNEL_ID = -1002803201198
DIOR_CHANNEL_LINK = "https://t.me/DiorEventos"

# Estados da conversação
MENU, ANONIMO, MENSAGEM, DESTINATARIO, ELEGANTE_ANONIMO, ELEGANTE_MENSAGEM, ELEGANTE_DESTINATARIO, AMIZADE_ANONIMO, AMIZADE_MENSAGEM, AMIZADE_DESTINATARIO = range(10)

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📢 Canal", url=DIOR_CHANNEL_LINK),
            InlineKeyboardButton("🔥 Farpa", callback_data="menu_farpa")
        ],
        [
            InlineKeyboardButton("💌 Elegante", callback_data="menu_elegante"),
            InlineKeyboardButton("🤝 Amizade", callback_data="menu_amizade")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎯 *Escolha uma opção:*\n\n"
        "• 📢 *Canal* - Nosso canal principal\n"
        "• 🔥 *Farpa* - Envie uma farpa\n"
        "• 💌 *Elegante* - Mensagem elegante\n" 
        "• 🤝 *Amizade* - Mensagem de amizade\n\n"
        "Use /menu para ver este menu novamente.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return MENU

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📢 Canal", url=DIOR_CHANNEL_LINK),
            InlineKeyboardButton("🔥 Farpa", callback_data="menu_farpa")
        ],
        [
            InlineKeyboardButton("💌 Elegante", callback_data="menu_elegante"),
            InlineKeyboardButton("🤝 Amizade", callback_data="menu_amizade")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎯 *Menu Principal*\n\n"
        "• 📢 *Canal* - Nosso canal principal\n"
        "• 🔥 *Farpa* - Envie uma farpa\n"
        "• 💌 *Elegante* - Mensagem elegante\n"
        "• 🤝 *Amizade* - Mensagem de amizade",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return MENU

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "menu_farpa":
        keyboard = [
            [
                InlineKeyboardButton("🙈 Anônimo", callback_data="farpa_anonimo_sim"),
                InlineKeyboardButton("👤 Revelar", callback_data="farpa_anonimo_nao")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🔥 *Enviar Farpa*\n\nVocê quer enviar anônimo?",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return ANONIMO
        
    elif query.data == "menu_elegante":
        keyboard = [
            [
                InlineKeyboardButton("🙈 Anônimo", callback_data="elegante_anonimo_sim"),
                InlineKeyboardButton("👤 Revelar", callback_data="elegante_anonimo_nao")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "💌 *Correio Elegante*\n\nVocê quer enviar anônimo?",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return ELEGANTE_ANONIMO
        
    elif query.data == "menu_amizade":
        keyboard = [
            [
                InlineKeyboardButton("🙈 Anônimo", callback_data="amizade_anonimo_sim"),
                InlineKeyboardButton("👤 Revelar", callback_data="amizade_anonimo_nao")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🤝 *Correio Amizade*\n\nVocê quer enviar anônimo?",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return AMIZADE_ANONIMO

# Funções para Farpa
async def farpa_anonimo_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    choice = query.data
    context.user_data['tipo'] = 'farpa'
    context.user_data['anonimo'] = ("anonimo_sim" in choice)
    
    if not context.user_data['anonimo']:
        try:
            user = update.effective_user
            username = user.username
            if username:
                context.user_data['remetente'] = f"@{username}"
            else:
                await query.edit_message_text(
                    "❌ Sem @username.\nSua farpa será anônima."
                )
                context.user_data['anonimo'] = True
                context.user_data['remetente'] = "anônimo"
        except Exception as e:
            logger.error(f"Erro ao obter username: {e}")
            context.user_data['anonimo'] = True
            context.user_data['remetente'] = "anônimo"
    else:
        context.user_data['remetente'] = "anônimo"
    
    await query.edit_message_text("💬 Digite a farpa:")
    return MENSAGEM

# Funções para Correio Elegante
async def elegante_anonimo_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    choice = query.data
    context.user_data['tipo'] = 'correio_elegante'
    context.user_data['anonimo'] = ("anonimo_sim" in choice)
    
    if not context.user_data['anonimo']:
        try:
            user = update.effective_user
            username = user.username
            if username:
                context.user_data['remetente'] = f"@{username}"
            else:
                await query.edit_message_text(
                    "❌ Sem @username.\nSua mensagem será anônima."
                )
                context.user_data['anonimo'] = True
                context.user_data['remetente'] = "anônimo"
        except Exception as e:
            logger.error(f"Erro ao obter username: {e}")
            context.user_data['anonimo'] = True
            context.user_data['remetente'] = "anônimo"
    else:
        context.user_data['remetente'] = "anônimo"
    
    await query.edit_message_text("💬 Digite a mensagem:")
    return ELEGANTE_MENSAGEM

# Funções para Correio da Amizade
async def amizade_anonimo_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    choice = query.data
    context.user_data['tipo'] = 'correio_amizade'
    context.user_data['anonimo'] = ("anonimo_sim" in choice)
    
    if not context.user_data['anonimo']:
        try:
            user = update.effective_user
            username = user.username
            if username:
                context.user_data['remetente'] = f"@{username}"
            else:
                await query.edit_message_text(
                    "❌ Sem @username.\nSua mensagem será anônima."
                )
                context.user_data['anonimo'] = True
                context.user_data['remetente'] = "anônimo"
        except Exception as e:
            logger.error(f"Erro ao obter username: {e}")
            context.user_data['anonimo'] = True
            context.user_data['remetente'] = "anônimo"
    else:
        context.user_data['remetente'] = "anônimo"
    
    await query.edit_message_text("💬 Digite a mensagem:")
    return AMIZADE_MENSAGEM

async def receber_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mensagem'] = update.message.text
    await update.message.reply_text("📧 Digite o @ do destinatário:")
    
    tipo = context.user_data.get('tipo', 'farpa')
    if tipo == 'farpa':
        return DESTINATARIO
    elif tipo == 'correio_elegante':
        return ELEGANTE_DESTINATARIO
    elif tipo == 'correio_amizade':
        return AMIZADE_DESTINATARIO

async def receber_destinatario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    destinatario = update.message.text
    
    if not destinatario.startswith('@'):
        destinatario = f"@{destinatario}"
    
    destinatario = re.sub(r'[^a-zA-Z0-9_@]', '', destinatario)
    context.user_data['destinatario'] = destinatario
    
    mensagem = context.user_data['mensagem']
    remetente = context.user_data['remetente']
    tipo = context.user_data.get('tipo', 'farpa')
    
    if tipo == 'farpa':
        texto = (
            f"🔥 *FARPA NOVA*\n\n"
            f"📩 *Mensagem:*\n{mensagem}\n\n"
            f"👤 *Remetente:* {remetente}\n"
            f"🎯 *Destinatário:* {destinatario}"
        )
    elif tipo == 'correio_elegante':
        texto = (
            f"💌 *Elegante*\n\n"
            f"📩 *Mensagem:*\n{mensagem}\n\n"
            f"👤 *Remetente:* {remetente}\n"
            f"🎯 *Destinatário:* {destinatario}"
        )
    else:
        texto = (
            f"🤝 *AMIZADE NOVA*\n\n"
            f"📩 *Mensagem:*\n{mensagem}\n\n"
            f"👤 *Remetente:* {remetente}\n"
            f"🎯 *Destinatário:* {destinatario}"
        )
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Aceitar", callback_data=f"aceitar_{update.effective_user.id}_{tipo}"),
            InlineKeyboardButton("❌ Rejeitar", callback_data=f"rejeitar_{update.effective_user.id}_{tipo}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await context.bot.send_message(
            chat_id=ADMIN_GROUP_ID,
            text=texto,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
        await update.message.reply_text(
            f"✅ Enviado para aprovação!\n"
            "Aguarde a publicação."
        )
    except Exception as e:
        logger.error(f"Erro ao enviar para admin: {e}")
        error_msg = f"❌ Erro: {str(e)}"
        await update.message.reply_text(error_msg)
    
    await mostrar_menu(update, context)
    return MENU

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    parts = data.split('_')
    user_id = parts[1] if len(parts) > 1 else None
    action = parts[0]
    tipo = parts[2] if len(parts) > 2 else 'farpa'
    
    if action == "aceitar":
        try:
            await query.edit_message_reply_markup(reply_markup=None)
            
            original_text = query.message.text
            lines = original_text.split('\n')
            
            # Extrai informações
            mensagem = ""
            remetente = ""
            destinatario = ""
            
            for i, line in enumerate(lines):
                if "Mensagem:" in line:
                    # Pega as linhas seguintes até encontrar uma linha vazia ou próximo campo
                    msg_lines = []
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip() == "" or "Remetente:" in lines[j] or "Destinatário:" in lines[j]:
                            break
                        msg_lines.append(lines[j])
                    mensagem = "\n".join(msg_lines).strip()
                elif "Remetente:" in line:
                    remetente = line.split("Remetente:")[1].replace("*", "").strip()
                elif "Destinatário:" in line:
                    destinatario = line.split("Destinatário:")[1].replace("*", "").strip()
            
            # Formatação SIMPLES sem Markdown para evitar problemas
            if tipo == 'farpa':
                texto_canal = (
                    f"FARPA 🔥\n\n"
                    f"Mensagem:\n{mensagem}\n\n"
                    f"Remetente: {remetente}\n"
                    f"Destinatário: {destinatario}\n\n"
                    f"Use o bot: @DiorEventosBot"
                )
            elif tipo == 'correio_elegante':
                texto_canal = (
                    f"CORREIO ELEGANTE 💌\n\n"
                    f"Mensagem:\n{mensagem}\n\n"
                    f"Remetente: {remetente}\n"
                    f"Destinatário: {destinatario}\n\n"
                    f"Use o bot: @DiorEventosBot"
                )
            else:
                texto_canal = (
                    f"CORREIO DA AMIZADE 🤝\n\n"
                    f"Mensagem:\n{mensagem}\n\n"
                    f"Remetente: {remetente}\n"
                    f"Destinatário: {destinatario}\n\n"
                    f"Use o bot: @DiorEventosBot"
                )
            
            try:
                # Envia SEM formatação Markdown para evitar problemas
                message = await context.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=texto_canal
                )
                
                # Verifica se a mensagem foi realmente enviada
                if message.message_id:
                    await query.message.reply_text("✅ Publicado no canal com sucesso!")
                else:
                    await query.message.reply_text("⚠️ Mensagem enviada, mas pode estar invisível")
                
            except Exception as e:
                logger.error(f"Erro ao publicar: {e}")
                await query.message.reply_text(f"❌ Erro ao publicar: {str(e)}")
        
        except Exception as e:
            logger.error(f"Erro geral: {e}")
            await query.message.reply_text(f"❌ Erro interno: {str(e)}")
    
    elif action == "rejeitar":
        await query.edit_message_text(
            f"{query.message.text}\n\n❌ REJEITADO POR ADMIN"
        )
        await query.message.reply_text("❌ Mensagem rejeitada.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operação cancelada.")
    await mostrar_menu(update, context)
    return MENU

async def mostrar_menu(update, context):
    keyboard = [
        [
            InlineKeyboardButton("📢 Canal", url=DIOR_CHANNEL_LINK),
            InlineKeyboardButton("🔥 Farpa", callback_data="menu_farpa")
        ],
        [
            InlineKeyboardButton("💌 Elegante", callback_data="menu_elegante"),
            InlineKeyboardButton("🤝 Amizade", callback_data="menu_amizade")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if hasattr(update, 'message') and update.message:
        await update.message.reply_text(
            "🎯 Menu Principal\n\nEscolha uma opção:",
            reply_markup=reply_markup
        )
    elif hasattr(update, 'callback_query') and update.callback_query:
        await update.callback_query.message.reply_text(
            "🎯 Menu Principal\n\nEscolha uma opção:",
            reply_markup=reply_markup
        )

# Comando para verificar permissões do canal
async def check_permissions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Tenta obter informações do canal
        chat = await context.bot.get_chat(CHANNEL_ID)
        await update.message.reply_text(f"📋 Informações do canal:\nNome: {chat.title}\nID: {chat.id}")
        
        # Tenta enviar uma mensagem de teste
        test_msg = await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text="🔍 Teste de visibilidade\nSe você está vendo esta mensagem, está funcionando!"
        )
        
        if test_msg.message_id:
            await update.message.reply_text("✅ Teste enviado! Verifique se está visível no canal.")
        else:
            await update.message.reply_text("⚠️ Mensagem enviada, mas pode estar invisível")
            
    except Exception as e:
        error_msg = f"❌ Erro ao acessar canal: {str(e)}"
        if "chat not found" in str(e).lower():
            error_msg += "\n• Canal não encontrado"
        elif "not enough rights" in str(e).lower():
            error_msg += "\n• Bot não é administrador"
        elif "forbidden" in str(e).lower():
            error_msg += "\n• Bot foi bloqueado"
        
        await update.message.reply_text(error_msg)

# Comando para verificar se o bot é admin
async def check_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, context.bot.id)
        if member.status in ['administrator', 'creator']:
            await update.message.reply_text("✅ Bot é administrador do canal!")
        else:
            await update.message.reply_text("❌ Bot NÃO é administrador do canal!")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao verificar admin: {str(e)}")

def main():
    application = Application.builder().token(TOKEN).build()
    
    # Conversation handlers
    farpa_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(farpa_anonimo_choice, pattern="^farpa_anonimo_")],
        states={
            MENSAGEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_mensagem)],
            DESTINATARIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_destinatario)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        map_to_parent={MENU: MENU}
    )
    
    elegante_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(elegante_anonimo_choice, pattern="^elegante_anonimo_")],
        states={
            ELEGANTE_MENSAGEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_mensagem)],
            ELEGANTE_DESTINATARIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_destinatario)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        map_to_parent={MENU: MENU}
    )
    
    amizade_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(amizade_anonimo_choice, pattern="^amizade_anonimo_")],
        states={
            AMIZADE_MENSAGEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_mensagem)],
            AMIZADE_DESTINATARIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_destinatario)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        map_to_parent={MENU: MENU}
    )
    
    # Conversation handler principal
    main_conv = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('menu', menu_command)],
        states={
            MENU: [
                CallbackQueryHandler(menu_handler, pattern="^menu_"),
                farpa_conv,
                elegante_conv,
                amizade_conv
            ],
            ANONIMO: [farpa_conv],
            ELEGANTE_ANONIMO: [elegante_conv],
            AMIZADE_ANONIMO: [amizade_conv]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    application.add_handler(main_conv)
    application.add_handler(CallbackQueryHandler(button_handler, pattern="^(aceitar|rejeitar)_"))
    
    # Comandos de diagnóstico
    application.add_handler(CommandHandler("checkchannel", check_permissions))
    application.add_handler(CommandHandler("checkadmin", check_admin))
    
    logger.info("Bot iniciado...")
    print("Bot está rodando! Use Ctrl+C para parar.")
    application.run_polling()

if __name__ == '__main__':
    main()
