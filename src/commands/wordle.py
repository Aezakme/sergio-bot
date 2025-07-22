from src.models.user import UserDB
import telegram


from telegram.ext import run_async
from src.utils.handlers_decorators import chat_guard, collect_stats, command_guard
from src.models.wordle import Wordle


@run_async
@chat_guard
@collect_stats
@command_guard
def send_wordle_stat_handler(bot: telegram.Bot, update: telegram.Update) -> None:
    send_wordle_stat(bot, update.message.chat_id)


def send_wordle_stat(bot: telegram.Bot, chat_id, date=None):

    msg = (
        f"<b>Стата по Вордли:</b>\n"
        + "Подряд - R\n"
        + "Кол-во побед - W\n"
        + "Попыток в среднем - A\n"
    )

    stats = Wordle.get_wordle_stats(chat_id, date)

    stats.sort(key=lambda x: x.total, reverse=True)
    count = 1
    for stat in stats:
        uid = stat.uid
        data = UserDB.get(uid)
        msg += f"\n<b> {count}. {data.fullname if data.fullname is not None else data.username}</b> (R:{stat.total}, W:{stat.totalWin / stat.total * 100}%, A:{round(stat.totalTries / stat.total, 2)})"
        count += 1

    bot.send_message(chat_id, msg, parse_mode=telegram.ParseMode.HTML)
