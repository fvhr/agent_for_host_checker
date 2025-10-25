import logging
import logging.handlers
import json
import os
import sys
import traceback
from datetime import datetime

import pytz


def convert_to_moscow_time(value=None):
    moscow_tz = pytz.timezone('Europe/Moscow')
    if not value:
        value = datetime.now()
    if value is not None:
        if value.tzinfo is None:
            value = value.replace(tzinfo=pytz.utc)
        value = value.astimezone(moscow_tz)
        return value.replace(tzinfo=None)
    return None


class LoggingRotate:
    """Класс логирования с ротацией лог файла по
    10 МБ и вывода в консоль с цветами."""

    def __init__(
            self,
            log_file: str,
            level=logging.CRITICAL,
            max_bytes: int = 10 * 1024 * 1024,
            backup_count: int = 5,
    ):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)

        # Создаем обработчик для файла с ротацией
        handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
        )
        handler.setLevel(level)

        # Форматируем сообщения лога
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        )
        handler.setFormatter(formatter)

        # Добавляем обработчик к логгеру
        self.logger.addHandler(handler)

    def prepear_text(self, text=None):
        result = ''
        if text is not None:
            if isinstance(text, dict):
                result += (
                        json.dumps(
                            self.convert_dict_to_str(text),
                            ensure_ascii=False,
                            indent=4,
                        )
                        + '\n'
                )
            else:
                result += str(text)
        return result

    def message_print(self, text=None):  # Message
        if text is not None:
            print('\033[37m\033[1m{}\033[0m'.format(self.prepear_text(text)))

    def debug(self, msg: str, console_log: bool = True):
        self._log_message(
            msg,
            self.logger.debug,
            console_log,
            self.message_print,
        )

    def info(self, msg: str, console_log: bool = True):
        self._log_message(msg, self.logger.info, console_log, self.green_print)

    def warning(self, msg: str, console_log: bool = True):
        self._log_message(
            msg,
            self.logger.warning,
            console_log,
            self.warning_print,
        )

    def error(self, msg: str, console_log: bool = True):
        self._log_message(msg, self.logger.error, console_log, self.red_print)

    def critical(self, msg: str, console_log: bool = True):
        self._log_message(
            msg,
            self.logger.critical,
            console_log,
            self.blackonred_print,
        )

    def _log_message(
            self,
            msg: str,
            log_func: callable,
            console_log: bool,
            print_func: callable,
    ):
        """Общая функция для логирования сообщений."""
        date = str(convert_to_moscow_time(datetime.now()))
        msg = date + ' ' + msg
        if isinstance(msg, str):
            txt = self.prepare_text(msg)
            if console_log:
                print_func(txt)
            log_func(txt)

    def red_print(self, text=None):
        if text is not None:
            print('\033[31m\033[1m{}\033[0m'.format(self.prepare_text(text)))

    def green_print(self, text=None):
        if text is not None:
            print('\033[32m\033[1m{}\033[0m'.format(self.prepare_text(text)))

    def warning_print(self, text=None):
        if text is not None:
            print('\033[35m\033[1m{}\033[0m'.format(self.prepare_text(text)))

    def blackonred_print(self, text=None):  # Черный на красном фоне
        if text is not None:
            print(
                '\033[31m\033[1m\033[7m{}\033[0m'.format(
                    self.prepare_text(text),
                ),
            )

    def prepare_text(self, text=None) -> str:
        """Подготовка текста для логирования."""
        if text is None:
            return ''

        if isinstance(text, dict):
            return (
                    json.dumps(
                        self.convert_dict_to_str(text),
                        ensure_ascii=False,
                        indent=4,
                    )
                    + '\n'
            )

        return str(text)

    def convert_dict_to_str(self, data) -> dict:
        """Преобразование словаря в строку."""
        if isinstance(data, dict):
            return {
                key: (
                    self.convert_dict_to_str(value)
                    if isinstance(value, dict)
                    else str(value)
                )
                for key, value in data.items()
            }

        return data

    def print_exception(self) -> None:
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_frames = traceback.extract_tb(exc_tb)
        project_root = os.path.abspath(os.path.dirname(__file__))
        your_frame = None
        for frame in reversed(tb_frames):
            frame_path = os.path.abspath(frame.filename)
            if frame_path.startswith(project_root):
                your_frame = frame
                break
        if your_frame is None:
            your_frame = tb_frames[-1]

        filename = your_frame.filename
        line_number = your_frame.lineno

        self.critical(f'{filename}:{line_number} - {str(exc_value)}')


logger = LoggingRotate('app.log', level=logging.CRITICAL)
