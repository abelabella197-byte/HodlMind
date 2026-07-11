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

{'🏆 Great job! Keep learning!' if is_correct else '💪 Keep studying! You\'ll get it next time!'}
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
    
    message = """
🛡️ *Risk Management Golden Rules*

Essential rules for protecting your capital:

"""
    
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
    message = """
📊 *Trading Journal*

Track your trades to improve your decision-making:

*What to track in your journal:*

📅 *Date & Time:*
• When did you enter/exit?

💰 *Trade Details:*
• Asset traded
• Entry price
• Exit price
• Position size

🧠 *Psychology:*
• Why did you enter?
• Emotions at the time
• Any external influences?

📈 *Outcome:*
• Profit/Loss
• What went well?
• What could improve?

💡 *Journal Tips:*
• Write immediately after trades
• Be honest with yourself
• Review weekly to learn
• Identify patterns in your behavior

*Ready to start?* Use this template:
