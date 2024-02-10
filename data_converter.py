import json
from tkinter import Label, Entry
from typing import Any
from logger import LogMixin
from entry_validator import EntryValidator


class DataConverter(LogMixin):
    def widget_to_json(self, raw_data: list[tuple[Label, Entry]]) -> str:
        try:
            raw = [{item[0].cget('text'): item[1].get()} for item in raw_data]
            raw = list(map(EntryValidator().clean_data, raw))
            return json.dumps(raw)
        except (IndexError, Exception):
            self.logger.exception('Invalid data in entry fields')

    def json_to_graph(self, json_str: str) -> tuple[list[tuple[Any, Any]], tuple[Any, ...]]:
        st = json.loads(json_str)
        keys = []
        values = []
        for d in st:
            for key, value in d.items():
                if isinstance(value, dict):
                    for k, v in value.items():
                        keys.append((key, k))
                        values.append(v)
        self.logger.info(f'Received data: {keys, tuple(values)}')
        return keys, tuple(values)
