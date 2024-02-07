from logger import LogMixin


class EntryValidator(LogMixin):

    def __try_validate_entry(self, key: str, data: str) -> bool:
        conditions = [
            key.lower() != 'z' and not data,
            key.lower() == 'o' and data == '',
            not any(item.isdigit() for item in data)
        ]
        self.logger.debug(f'Validated values: key = {key}, value = {data}, conditions = {conditions}')
        if key.lower() == 'z':
            return True
        return not any(conditions)

    def clean_data(self, data: dict):
        result_dict = {}
        for key, value in data.items():
            if not self.__try_validate_entry(key, value):
                raise Exception(f'Invalid data in label {key} and entry {value}')
            if '=' in value:
                pairs = (pair.strip() for pair in value.split(',') if pair)
                result_dict[key] = {k.strip(): int(v.strip()) if v.strip().isdigit() else v.strip() for k, v in
                                    (pair.split('=') for pair in pairs)}
            else:
                result_dict[key] = value
        return result_dict
