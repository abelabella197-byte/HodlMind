import os
import logging
import random
from datetime import datetime
from typing import Dict, List, Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.constants import ParseMode

# ===== CONFIGURATION =====
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===== DATA =====
class PsychologyData:
    """Crypto psychology and risk management content"""
    
    # Daily tips collection
    DAILY_TIPS = [
        "🧠 *Tip 1:* Fear and greed are your biggest enemies. Stick to your strategy.",
        "🧠 *Tip 2:* Never invest more than you can afford to lose. Risk management is key.",
        "🧠 *Tip 3:* The market is irrational. Don't let emotions drive your decisions.",
        "🧠 *Tip 4:* Take profits gradually. Nobody ever went broke taking profits.",
        "🧠 *Tip 5:* FOMO leads to bad decisions. Stick to your plan.",
        "🧠 *Tip 6:* Average in, don't go all in. Reduce your risk.",
        "🧠 *Tip 7:* Keep a trading journal. Learn from your mistakes.",
        "🧠 *Tip 8:* Diversify. Don't put all your eggs in one basket.",
        "🧠 *Tip 9:* Be patient. The best opportunities take time.",
        "🧠 *Tip 10:* When in doubt, zoom out. Look at the bigger picture.",
        "🧠 *Tip 11:* Buy the fear, sell the greed. Contrarian thinking works.",
        "🧠 *Tip 12:* Have an exit strategy before you enter a position.",
        "🧠 *Tip 13:* Don't chase pumps. What goes up must come down.",
        "🧠 *Tip 14:* Panic selling is usually the worst move. Stay calm.",
        "🧠 *Tip 15:* Research before you invest. Knowledge is power.",
        "🧠 *Tip 16:* Set stop-losses. Protect your capital.",
        "🧠 *Tip 17:* Remember 2022? Markets recover. Have faith.",
        "🧠 *Tip 18:* Your mental health is more important than any trade.",
        "🧠 *Tip 19:* Nobody can time the market perfectly. Accept it.",
        "🧠 *Tip 20:* The market rewards discipline, not emotion.",
    ]
    
    # Quiz questions
    QUIZZES = [
        {
            "question": "What is the biggest enemy of a trader?",
            "options": ["A) Bears", "B) FOMO & Greed", "C) Governments", "D) Whales"],
            "correct": "B",
            "explanation": "Fear of missing out (FOMO) and greed are the biggest psychological enemies. They lead to bad decisions."
        },
        {
            "question": "What should you do when the market crashes?",
            "options": ["A) Panic sell", "B) Buy the dip", "C) Do nothing", "D) All of the above"],
            "correct": "C",
            "explanation": "Sometimes doing nothing is the best strategy. Stay calm and stick to your plan."
        },
        {
            "question": "What is the 1% risk rule?",
            "options": ["A) Only invest 1%", "B) Risk 1% per trade", "C) 1% growth daily", "D) None"],
            "correct": "B",
            "explanation": "Never risk more than 1% of your portfolio on a single trade. This protects your capital."
        },
        {
            "question": "What causes most trading losses?",
            "options": ["A) Bad market", "B) Emotional decisions", "C) High fees", "D) Lack of capital"],
            "correct": "B",
            "explanation": "Emotional decisions like fear and greed cause more losses than market conditions."
        },
        {
            "question": "What is the best time to buy?",
            "options": ["A) When everyone is buying", "B) When everyone is selling", "C) At 3 AM", "D) Never"],
            "correct": "B",
            "explanation": "The best time to buy is when there's fear in the market (buy the fear)."
        },
    ]
    
    # Risk management rules
    RISK_RULES = [
        "🔴 *Golden Rule 1:* Never invest more than you can afford to lose completely.",
        "🔴 *Golden Rule 2:* Always use stop-loss orders. Protect your capital.",
        "🔴 *Golden Rule 3:* Diversify across different assets and sectors.",
        "🔴 *Golden Rule 4:* Never trade with money you need for bills or essentials.",
        "🔴 *Golden Rule 5:* Have a clear entry and exit strategy for every trade.",
        "🔴 *Golden Rule 6:* Don't let a small loss become a big loss. Cut losses early.",
        "🔴 *Golden Rule 7:* Take profits regularly. Don't get greedy.",
        "🔴 *Golden Rule 8:* Keep calm during volatility. Markets correct.",
        "🔴 *Golden Rule 9:* Educate yourself continuously. Knowledge compounds.",
        "🔴 *Golden Rule 10:* Your health is wealth. Take breaks from charts.",
    ]
    
    @staticmethod
    def get_daily_tip() -> str:
        """Get a random daily tip"""
        return random.choice(PsychologyData.DAILY_TIPS)
    
    @staticmethod
    def get_quiz() -> Dict:
        """Get a random quiz question"""
        return random.choice(PsychologyData.QUIZZES)
    
    @staticmethod
    def get_risk_rules() -> List[str]:
        """Get risk management rules"""
        return random.sample(PsychologyData.RISK_RULES, 5)

# ===== BOT HANDLERS =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Welcome message with /start"""
    user = update.effective_user
    welcome_message = f"""
🧠 *Welcome to HodlMind, {user.first_name}!*

Your crypto psychology and risk management coach. Learn to make better decisions.

*Quick Commands:*
💡 /tip - Daily mindset tip
🎯 /quiz - Test your knowledge
🛡️ /risk - Risk management rules
📊 /journal - Trading journal
📋 /menu - All commands
❓ /help - Help

*Master your mind, master the market.*
"""
    
    keyboard = [
        [InlineKeyboardButton("💡 Daily Tip", callback_data="tip"),
         InlineKeyboardButton("🎯 Quiz", callback_data="quiz")],
        [InlineKeyboardButton("🛡️ Risk Rules", callback_data="risk"),
         InlineKeyboardButton("📊 Journal", callback_data="journal")],
        [InlineKeyboardButton("📋 Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup,
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show main menu"""
    keyboard = [
        [InlineKeyboardButton("💡 Daily Tip", callback_data="tip"),
         InlineKeyboardButton("🎯 Quiz", callback_data="quiz")],
        [InlineKeyboardButton("🛡️ Risk Rules", callback_data="risk"),
         InlineKeyboardButton("📊 Journal", callback_data="journal")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
         InlineKeyboardButton("❓ Help", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """
🧠 *HodlMind Main Menu*

Choose a feature below:
"""
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

async def daily_tip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show a daily mindset tip"""
    tip = PsychologyData.get_daily_tip()
    
    today = datetime.now().strftime("%B %d, %Y")
    message = f"""
💡 *Daily Mindset Tip*
📅 {today}

{tip}

*Remember:*
• Stay disciplined
• Stick to your strategy
• Don't let emotions control you
• Patience pays off
"""
    
    keyboard = [
        [InlineKeyboardButton("🔄 New Tip", callback_data="tip"),
         InlineKeyboardButton("📊 Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start a quiz"""
    quiz_data = PsychologyData.get_quiz()
    
    # Store quiz in context for later
    context.user_data['current_quiz'] = quiz_data
    
    message = f"""
🎯 *Quiz Time!*

{quiz_data['question']}

{quiz_data['options'][0]}
{quiz_data['options'][1]}
{quiz_data['options'][2]}
{quiz_data['options'][3]}

Choose your answer by clicking below:
"""
    
    keyboard = [
        [
            InlineKeyboardButton("A", callback_data="quiz_a"),
            InlineKeyboardButton("B", callback_data="quiz_b"),
            InlineKeyboardButton("C", callback_data="quiz_c"),
            InlineKeyboardButton("D", callback_data="quiz_d"),
        ],
        [InlineKeyboardButton("📊 Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

async def quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle quiz answers"""
    query = update.callback_query
    await query.answer()
    
    # Get the answer
    answer = query.data.split('_')[1].upper()
    
    # Get the quiz data
    quiz_data = context.user_data.get('current_quiz')
    if not quiz_data:
        await query.edit_message_text(
            "❌ Quiz expired! Please start a new quiz with /quiz",
            parse_mode=ParseMode.MARKDOWN,
        )
        return
    
    correct = quiz_data['correct']
    is_correct = answer == correct
    
    message = f"""
🎯 *Quiz Result*

Question: {quiz_data['question']}
Your answer: {answer}
Correct answer: {correct}

{'✅ *Correct!*' if is_correct else '❌ *Incorrect!*'}

*Explanation:* {quiz_data['explanation']}

{'🏆 Great job! Keep learning!' if is_correct else '💪 Keep studying! You will get it next time!'}
"""
    
    keyboard = [
        [InlineKeyboardButton("🔄 Next Question", callback_data="quiz")],
        [InlineKeyboardButton("📊 Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup,
    )

async def risk_rules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show risk management rules"""
    rules = PsychologyData.get_risk_rules()
    
    message = "🛡️ *Risk Management Golden Rules*\n\nEssential rules for protecting your capital:\n\n"
    
    for i, rule in enumerate(rules, 1):
        message += f"{i}. {rule}\n\n"
    
    message += """
💡 *Remember:*
• Risk management is more important than profits
• Protect your capital first
• Never risk what you can't afford to lose
• Stay disciplined
"""
    
    keyboard = [
        [InlineKeyboardButton("🔄 New Rules", callback_data="risk"),
         InlineKeyboardButton("📊 Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

async def journal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Trading journal feature"""
    message = (
        "📊 *Trading Journal*\n\n"
        "Track your trades to improve your decision-making:\n\n"
        "*What to track in your journal:*\n\n"
        "📅 *Date & Time:*\n"
        "• When did you enter/exit?\n\n"
        "💰 *Trade Details:*\n"
        "• Asset traded\n"
        "• Entry price\n"
        "• Exit price\n"
        "• Position size\n\n"
        "🧠 *Psychology:*\n"
        "• Why did you enter?\n"
        "• Emotions at the time\n"
        "• Any external influences?\n\n"
        "📈 *Outcome:*\n"
        "• Profit/Loss\n"
        "• What went well?\n"
        "• What could improve?\n\n"
        "💡 *Journal Tips:*\n"
        "• Write immediately after trades\n"
        "• Be honest with yourself\n"
        "• Review weekly to learn\n"
        "• Identify patterns in your behavior\n\n"
        "*Ready to start?* Use the template below!"
    )
    
    keyboard = [
        [InlineKeyboardButton("📋 Get Template", callback_data="journal_template")],
        [InlineKeyboardButton("📊 Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

async def journal_template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show journal template"""
    template = (
        "📋 *Trading Journal Template*\n\n"
        "Copy this template to track your trades:\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "📅 DATE: [DD/MM/YYYY]\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "💰 ASSET: [BTC/ETH/etc]\n"
        "📊 POSITION: [Long/Short]\n\n"
        "📈 ENTRY PRICE: $\n"
        "📉 EXIT PRICE: $\n"
        "💼 POSITION SIZE: $\n\n"
        "🎯 RESULT: [+/- %]\n"
        "💵 PROFIT/LOSS: $\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🧠 EMOTIONAL STATE:\n"
        "[Before Entry]\n"
        "[During Trade]\n"
        "[After Exit]\n\n"
        "💡 LESSONS LEARNED:\n"
        "[What went well]\n"
        "[What to improve]\n\n"
        "📝 NOTES:\n"
        "[Additional thoughts]\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "💡 *Tips for effective journaling:*\n"
        "• Be honest about emotions\n"
        "• Write immediately after trading\n"
        "• Review at the end of each week\n"
        "• Look for patterns in your behavior"
    )
    
    keyboard = [
        [InlineKeyboardButton("📊 Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            template,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            template,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help message"""
    help_text = """
❓ *HodlMind Help*

*Available Commands:*
/start - Welcome message
/menu - Main menu
/tip - Daily mindset tip
/quiz - Test your knowledge
/risk - Risk management rules
/journal - Trading journal
/help - This message

*Features:*
• 🧠 Daily psychology tips
• 🎯 Educational quizzes
• 🛡️ Risk management education
• 📊 Trading journal guidance

*Philosophy:*
"Master your mind, master the market."

*Privacy:*
• No data stored
• Anonymous usage
• Educational focus only

*Support:* Coming soon!
"""
    
    keyboard = [[InlineKeyboardButton("📊 Menu", callback_data="menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show settings menu"""
    settings_text = """
⚙️ *Settings*

*Daily Tips:*
💡 Daily reminder: OFF
⏰ Time: 9:00 AM

*Quiz Preferences:*
📚 Difficulty: Beginner
🎯 Topics: General

*Notifications:*
🔔 Daily tip: ON
🧠 Quiz reminders: OFF

*Coming Soon:*
• Custom tip categories
• Progress tracking
• Achievement system
"""
    
    keyboard = [
        [InlineKeyboardButton("🔔 Toggle Tips", callback_data="toggle_tips")],
        [InlineKeyboardButton("📊 Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            settings_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            settings_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "tip":
        await daily_tip(update, context)
    elif query.data == "quiz":
        await quiz(update, context)
    elif query.data in ["quiz_a", "quiz_b", "quiz_c", "quiz_d"]:
        await quiz_answer(update, context)
    elif query.data == "risk":
        await risk_rules(update, context)
    elif query.data == "journal":
        await journal(update, context)
    elif query.data == "journal_template":
        await journal_template(update, context)
    elif query.data == "menu":
        await menu(update, context)
    elif query.data == "help":
        await help_command(update, context)
    elif query.data == "settings":
        await settings(update, context)
    elif query.data == "toggle_tips":
        await query.edit_message_text(
            "🔔 *Tip notifications coming soon!*\n\nStay tuned for daily reminders.",
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        await query.edit_message_text("Invalid option. Use /menu.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown messages"""
    await update.message.reply_text(
        "I'm not sure about that. Please use /menu to see available commands."
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ An error occurred. Please try again later or use /help."
        )

# ===== MAIN APPLICATION =====

def main() -> None:
    """Start the bot"""
    if not TOKEN:
        logger.error("No TELEGRAM_BOT_TOKEN found!")
        return
    
    logger.info("Starting HodlMind Bot...")
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("tip", daily_tip))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CommandHandler("risk", risk_rules))
    application.add_handler(CommandHandler("journal", journal))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("settings", settings))
    
    # Add button handler
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Add echo handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start polling
    logger.info("HodlMind Bot is now running! Waiting for messages...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
