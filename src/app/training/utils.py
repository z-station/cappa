from typing import List
import hashlib


def get_md5_hash_from_list(value: List[str]) -> str:
    str_value = ','.join(value)
    return hashlib.md5(
        str_value.encode('UTF-8')
    ).hexdigest()
