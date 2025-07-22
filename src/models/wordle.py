import random
import re
from datetime import datetime, timedelta
from threading import Lock

from telegram.ext import run_async

from src.models.user import UserDB
from src.models.user_stat import UserStat
from src.utils.cache import cache, YEAR
from src.utils.logger_helpers import get_logger

logger = get_logger(__name__)


class Wordle:
    lock = Lock()

    @classmethod
    def get_wordle_stats(cls, cid, date=None):
        monday = (
            cls.__get_current_monday() if date is None else cls.__get_date_monday(date)
        )
        
        return cls.__get_all_stats(monday, cid)

    @classmethod
    @run_async
    def parse_message(cls, message):
        msg = message.text
        if msg is None:
            return
        uid = message.from_user.id
        cid = message.chat_id

        if not cls.__has_wordle(msg):
            return

        arr = cls.__parse_stats(msg)

        cls.__add(uid, cid, arr)

    @classmethod
    def __has_wordle(cls, msg):
        msg_lower = msg.lower()
        if "вордли дня" in msg_lower:
            return True
        return False

    @classmethod
    def __parse_stats(cls, msg):
        arr = [0, 0]

        # round
        arr[0] = msg.split("#")[1].split(" ")[0]

        # tries
        arr[1] = msg.split("#")[1].split(" ")[1].split("/")[0]

        return arr

    @classmethod
    def __add(cls, uid, cid, arr, date=None):
        monday = (
            cls.__get_current_monday() if date is None else cls.__get_date_monday(date)
        )
        logger.debug(f"lock {cid}:{uid}")
        with cls.lock:
            stat = cls.__get_stat(monday, cid, uid)

            if stat.lastGameId == int(arr[0]):
                return

            if stat.lastGameId + 1 < int(arr[0]):
                stat = WordleRecord(uid=uid)

            stat.lastGameId = int(arr[0])
            stat.total += 1

            if "X" != arr[1]:
                stat.totalWin += 1
                stat.totalTries += int(arr[1])
            else:
                stat.totalTries += 6

            cls.__set_stat(stat, monday, cid, uid)

    @staticmethod
    def __get_user_cache_key(monday, cid, uid):
        return f'worlde:{monday.strftime("%Y%m%d")}:{cid}:{uid}'

    @staticmethod
    def __get_cache_key(monday, cid):
        return f'worlde:{monday.strftime("%Y%m%d")}:{cid}:*'

    @staticmethod
    def __get_date_monday(date):
        monday = date - timedelta(days=date.weekday())
        return monday.replace(hour=0, minute=0, second=0, microsecond=0)

    @classmethod
    def __get_current_monday(cls):
        return cls.__get_date_monday(datetime.today())

    @classmethod
    def __get_stat(cls, monday, cid, uid):
        cached = cache.get(cls.__get_user_cache_key(monday, cid, uid))
        if cached:
            return cached
        return WordleRecord(uid=uid)

    @classmethod
    def __get_all_stats(cls, monday, cid):
        key = cls.__get_cache_key(monday, cid)
        cached = cache.getByPattern(key)
        if cached:
            return cached
        return []

    @classmethod
    def __set_stat(cls, stat, monday, cid, uid):
        key = cls.__get_user_cache_key(monday, cid, uid)
        cache.set(key, stat, time=YEAR)


class WordleRecord:
    def __init__(self, uid=None, totalTries=0, lastGameId=0, total=0, totalWin=0):
        self.uid = uid
        self.totalTries = totalTries
        self.lastGameId = lastGameId
        self.total = total
        self.totalWin = totalWin
