import logging, argparse, os, re
from functools import wraps
from datetime import datetime, timedelta
from collections import namedtuple

FORMAT = "%(levelname)s: %(asctime)s - %(message)s"
logging.basicConfig(level="INFO", format=FORMAT, filemode='w')
logger = logging.getLogger(__name__)

handler_error = logging.FileHandler("../../error.log", encoding="utf-8")
handler_error.setFormatter(logging.Formatter(FORMAT))

logger.addHandler(handler_error)


def log_decorator(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            result = func(*args, *kwargs)
        except Exception as e:
            logger.critical(e)
            raise e
        return result

    return wrap


@log_decorator
def div(a, b):
    return a / b


# -----------------------------------------------

months = {'января': 1, 'февраля': 2, 'марта': 3,
          'апреля': 4, 'мая': 5, 'июня': 6,
          'июля': 7, 'августа': 8, 'сентября': 9,
          'октября': 10, 'ноября': 11, 'декабря': 12}

weekdays = {'понедельник': 0, 'вторник': 1, 'среда': 2,
            'четверг': 3, 'пятница': 4, 'суббота': 5, 'воскресенье': 6}


@log_decorator
def date_from_text(date_str: str):
    day, weekday, month = date_str.split()
    weeks = int(day.split('-')[0])
    month = months[month]
    weekday = weekdays[weekday]
    date = datetime(year=datetime.now().year, month=month, day=1)
    while date.weekday() != weekday:
        date += timedelta(days=1)
    result = date + timedelta(weeks=weeks - 1)
    if result.month != month:
        raise ValueError('Такой даты не существует')
    return result


def date_parser():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument('-d', '--date')
    return parser.parse_args()


# --------------------------------------------------


Dir = namedtuple("Dir", ['parent_dir', 'dir', 'file', 'expansion'])


def dir_parser():
    parser = argparse.ArgumentParser(description="Dir_parser")
    parser.add_argument('-d', '--dir')
    path = parser.parse_args().dir

    logger_dir = logging.getLogger('dir_logger')
    logger_dir.setLevel(logging.INFO)

    handler_dir = logging.FileHandler("dir_log.log", "w", encoding='utf-8')
    format_dir = logging.Formatter("%(asctime)s - %(message)s: ")
    handler_dir.setFormatter(format_dir)
    logger_dir.addHandler(handler_dir)

    for dir_path, dir_name, file in os.walk(path):
        parent_dir = dir_path.split('\\')[-1]
        if dir_name:
            for d in dir_name:
                dir_out = Dir(parent_dir, dir=d, file=None, expansion=None)
                logger_dir.info(f"Parent_dir: {dir_out.parent_dir} -> "
                                f"dir: {dir_out.dir}")
        if file:
            for f in file:
                list_f = f.split(".")
                file_name = list_f[0]
                expansion = list_f[-1]
                dir_out = Dir(parent_dir, None, file=file_name, expansion=expansion)
                logger_dir.info(f"Parent_dir: {dir_out.parent_dir} -> "
                                f"file: {dir_out.file} with "
                                f"expansion: {dir_out.expansion}")

def text_parser():
    parser = argparse.ArgumentParser(description="Text_parser")
    parser.add_argument('-t', '--text')
    text = parser.parse_args().text

    logger_text = logging.getLogger('text_logger')
    logger_text.setLevel(logging.INFO)

    handler_text = logging.FileHandler("text_log.log", "w", encoding='utf-8')
    format_text = logging.Formatter("%(asctime)s - %(message)s: ")
    handler_text.setFormatter(format_text)
    logger_text.addHandler(handler_text)

    text = text.lower()
    list_text = re.split(" |,|'|!", text)
    for i in range(len(list_text)):
        list_text[i] = list_text[i].strip(".")

    dict_words = {}
    list_words = []
    for i in list_text:
        if i.isalpha():
            if i in dict_words:
                dict_words[i] = dict_words[i] + 1
            else:
                dict_words.setdefault(i, 1)

    for i,k in dict_words.items():
        list_words.append((i,k))

    logger_text.info(list_words)


if __name__ == '__main__':
    # try:
    #     print(div(5,0))
    # except ZeroDivisionError as e:
    #     print(e)

    # print(date_from_text("1-й четверг ноября"))

    # dir_parser() # py seminar_log_arg.py -d "C:\parent_dir\dirs"
    text_parser() # py seminar_log_arg.py -t "Hello world. Hello Python, Hello again."

