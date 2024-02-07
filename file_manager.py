from typing import Any
from logger import LogMixin


class FileManager(LogMixin):
    def load_file_data(self, filename: str) -> str:
        try:
            with open(filename, encoding='utf-8') as file:
                return file.read()
        except OSError:
            self.logger.exception('File not found when trying to read data')
            return ''

    def save_file_data(self, filename: str, data: Any) -> None:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(data)
            self.logger.info(f'file with data {data} saved')
