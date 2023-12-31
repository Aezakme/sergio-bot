import random
import re
from typing import List

import telegram
from telegram import ParseMode, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import run_async

from src.config import CHATRULES, CMDS, CONFIG
from src.commands.khaleesi.khaleesi_handler import check_base_khaleesi
from src.modules.last_word import get_last_word_cache_key
from src.modules.message_reactions import send_gdeleha, send_pidor
from src.models.leave_collector import LeaveCollector
from src.models.user import User
from src.commands.huificator import huificator
from src.utils.cache import cache
from src.utils.callback_helpers import get_callback_data
from src.utils.handlers_decorators import chat_guard, collect_stats, command_guard
from src.utils.handlers_helpers import is_command_enabled_for_chat, \
    check_admin
from src.utils.logger_helpers import get_logger

logger = get_logger(__name__)


@run_async
@chat_guard
@collect_stats
@command_guard
def huificator_handler(bot, update):
    send_huificator(bot, update.message, limit_chars=1000)


def send_huificator(bot: telegram.Bot, message: telegram.Message, limit_chars: int = 0) -> None:
    def get_new_msg(words: List[str]) -> str:
        new_msg = ''
        for word in words:
            new_msg += huificator(word)
            new_msg += ' '
        return new_msg

    result = check_base_khaleesi(bot, message, 'Хуй', 'Хуишком хуинное хуёобщение', limit_chars)
    if not result:
        return
    chat_id, text, reply_to_message_id = result
    new_msg = get_new_msg(text.split())
    bot.send_message(chat_id, new_msg, reply_to_message_id=reply_to_message_id)


@run_async
@chat_guard
@collect_stats
@command_guard
def expert(bot, update):
    expert_uid = CONFIG.get('expert_uid', None)
    if expert_uid is None:
        return
    chat_id = update.message.chat_id
    rand_num = random.randrange(1, 10)
    name = User.get(expert_uid).username
    last_msg_id, _ = cache.get(get_last_word_cache_key(chat_id, expert_uid))
    expert_phrases = [
        'иди сюда!',
        'Срочно нужен эксперт!',
        'ты тут нужен!',
        'твое мнение по этому вопросу?',
    ]
    # TODO: рефакторинг. сразу проверять last_msg_id и избавиться от проверки name (ссылку можно делать по uid)
    if rand_num < 5:
        if name:
            bot.sendMessage(chat_id, f'@{name}, {random.choice(expert_phrases)}')
    else:
        if last_msg_id:
            bot.sendMessage(chat_id, f'{random.choice(expert_phrases)}',
                            reply_to_message_id=last_msg_id)


@run_async
@chat_guard
@collect_stats
@command_guard
def papa(bot, update):
    phrases = [
        'Кек в кукарек',
        'Че кого сучары?',
        'Ночь в ночь',
        'Обед в обед',
        'Я на даче',
        'Крыса',
    ]
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id, random.choice(phrases))

@run_async
@chat_guard
@collect_stats
@command_guard
def kick(bot: telegram.Bot, update: telegram.Update) -> None:
    message = update.message
    chat_id = message.chat_id
    user_id = message.from_user.id
    text = 'Анус себе покикай.'
    bot.send_message(chat_id, text, reply_to_message_id=message.message_id)


@run_async
@chat_guard
@collect_stats
@command_guard
def changelog(bot: telegram.Bot, update):
    text = CONFIG.get('changelog', '')
    if len(text) == 0:
        return
    chat_id = update.message.chat_id
    bot.send_message(chat_id, text, parse_mode=telegram.ParseMode.HTML,
                     disable_web_page_preview=True)


@run_async
@chat_guard
@collect_stats
@command_guard
def love(bot, update):
    chat_id = update.message.chat_id
    stickers = [
        'BQADBQADoQADq2Y0AdG-PWaBAtQJAg',
        'BQADBQADmQADq2Y0AVCj5lMjk3x1Ag',
        'BQADBQADmwADq2Y0AdL-nlAYDZxoAg',
        'BQADBQADnwADq2Y0ARG1h2XKDTfUAg',
        'BQADBQADtwADq2Y0AULrTZbfPNGSAg',
        'BQADBQADwwADq2Y0AYNaGBjXfCaHAg',
        'BQADBQADIwEAAqtmNAEbknbN74qTvAI',
    ]
    bot.sendSticker(chat_id, random.choice(stickers))


@run_async
@chat_guard
@collect_stats
@command_guard
def rules(bot, update):
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id, CHATRULES, parse_mode=ParseMode.HTML)


@run_async
@chat_guard
@collect_stats
@command_guard
def anketa(bot, update):
    chat_id = update.message.chat_id
    with open('anketa.txt', 'r', encoding="utf-8") as file:
        content = file.read()
    if update.message.reply_to_message is not None:
        bot.sendMessage(chat_id, content,
                        reply_to_message_id=update.message.reply_to_message.message_id)
    else:
        bot.sendMessage(chat_id, content)


@run_async
@chat_guard
@collect_stats
@command_guard
def putin(bot: telegram.Bot, update: telegram.Update) -> None:
    chat_id = update.message.chat_id
    if update.message.reply_to_message is None:
        bot.sendMessage(chat_id, 'Кхе-кхе')
        return
    if update.message.reply_to_message.text.strip().endswith('?'):
        bot.sendMessage(chat_id, 'Она утонула',
                        reply_to_message_id=update.message.reply_to_message.message_id)
        return
    bot.sendMessage(chat_id, 'Кто вам это сказал?',
                    reply_to_message_id=update.message.reply_to_message.message_id)


@run_async
@chat_guard
@collect_stats
@command_guard
def pomogite(bot, update):
    def __get_commands(chat_id, section_name):
        return [
            f"/{cmd['name']} — {cmd['description']}\n"
            for key, cmd in CMDS[section_name].items()
            if is_command_enabled_for_chat(chat_id, cmd['name'])
        ]

    chat_id = update.message.chat_id
    msg = "Общие:\n"
    commands = __get_commands(chat_id, 'common')
    msg += ''.join(sorted(commands))
    user_id = update.message.from_user.id
    if check_admin(bot, chat_id, user_id):
        msg += "\nАдминские:\n"
        commands = __get_commands(chat_id, 'admins')
        msg += ''.join(sorted(commands))
    bot.sendMessage(chat_id, msg)


@run_async
@chat_guard
@collect_stats
@command_guard
def leave(bot, update):
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id, ChatAction.TYPING)

    leaves = LeaveCollector.get_leaves(chat_id, 3)
    joins = LeaveCollector.get_joins(chat_id, 3)

    reply_markup = None
    result = ""
    if len(leaves) > 0:
        leaves_text = "\n".join(leaves)
        result = "Убыло за 3 дня:\n\n{}".format(leaves_text)
        data = {"name": 'last_word',
                "leaves_uid": LeaveCollector.get_leaves(chat_id, 3, return_id=True)}
        keyboard = [[InlineKeyboardButton("Показать последние слова (нажмите там Start)",
                                          callback_data=(get_callback_data(data)))]]
        reply_markup = InlineKeyboardMarkup(keyboard)

    if len(joins) > 0:
        joins_text = "\n".join(joins)
        if not result:  # здесь это аналогично `if len(leaves) == 0:`
            result = "Прибыло за 3 дня:\n\n{}"
        else:
            result += "\n\nПрибыло:\n\n{}"
        result = result.format(joins_text)

    if not result:
        result = "За 3 дня ничего не произошло"

    bot.sendMessage(chat_id, result, parse_mode='HTML', reply_markup=reply_markup)


@run_async
@chat_guard
@collect_stats
@command_guard
def gdeleha(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    msg_id = update.message.message_id
    send_gdeleha(bot, chat_id, msg_id, user_id)


@chat_guard
@collect_stats
@command_guard
def pidor(bot, update):
    send_pidor(bot, update)


re_pipixel = re.compile(r"^(.*?[\w]+|_)[,\s]*(\W*)$", re.IGNORECASE | re.DOTALL)
re_ellipsis_at_end = re.compile(r"\.{3,}$", re.IGNORECASE | re.DOTALL)
re_chuvak_begin = re.compile(r"^(чувак|друг|подруг|друзья)", re.IGNORECASE | re.DOTALL)
re_objective_end = re.compile(r"объективно\W*$", re.IGNORECASE | re.DOTALL)
re_objective_bracket = re.compile(r"^>*\s*объективно\W*$", re.IGNORECASE | re.DOTALL)
re_puk = re.compile(r'^\w*\s*пук\s*\W*', re.IGNORECASE | re.DOTALL)
re_left_bracket = re.compile(r'^>', re.IGNORECASE | re.DOTALL)


def pipixel(text: str, drug: str) -> str:
    def _no_first_upper(s: str)-> str:
        words = s.split(' ')
        if not words:
            return s
        if words[0].isupper():
            return s
        return words[0].lower() + ' ' + ' '.join(words[1:])

    stripped = text.strip()

    if re_ellipsis_at_end.search(stripped) or \
            (re_chuvak_begin.search(stripped) and not re_objective_end.search(stripped)):
        return 'Объективно?'

    if re_objective_bracket.search(stripped):
        return '>пук'

    if re_puk.search(stripped) or re_left_bracket.search(stripped):
        return '>объективно'

    tail = re_pipixel.sub(r"\1, объективно\2", _no_first_upper(stripped))
    return f'{drug}, {tail}'


def pipixel_handler(bot: telegram.Bot, update: telegram.Update) -> None:
    drug = random.choice(('Друг', 'Чувак'))
    too_long = '>' + random.choice(('пук', 'норка', 'объективно', 'мышь'))

    result = check_base_khaleesi(bot, update.message, drug, too_long, 1000)
    if not result:
        return

    chat_id, text, reply_to_message_id = result
    new_msg = pipixel(text, drug)
    bot.send_message(chat_id, new_msg, reply_to_message_id=reply_to_message_id)
