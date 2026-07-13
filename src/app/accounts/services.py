from datetime import timedelta, datetime
from typing import Optional, List
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings

UserModel = get_user_model()


class UserService:

    LAST_SEEN_CACHE_TIMEOUT = settings.LAST_SEEN_CACHE_TIMEOUT
    USER_ONLINE_TIMEOUT = settings.USER_ONLINE_TIMEOUT
    USERS_ONLINE_KEY = 'users_online_index'

    @classmethod
    def _get_cache_key(cls, user_id: int) -> str:
        return f'uls_{user_id}'

    @classmethod
    def _set_online_index_for_user(cls, user_id: int, timestamp: float):

        index = cache.get(cls.USERS_ONLINE_KEY) or {}
        index[user_id] = timestamp
        cache.set(
            key=cls.USERS_ONLINE_KEY,
            value=index,
            timeout=None
        )

    @classmethod
    def _set_online_index(cls, data: dict):
        cache.set(
            key=cls.USERS_ONLINE_KEY,
            value=data,
            timeout=None
        )

    @classmethod
    def _set_last_seen_cache(
        cls,
        user: UserModel,
        value: datetime
    ):

        cache_key = cls._get_cache_key(user.id)
        timestamp = value.timestamp()
        cache.set(
            key=cache_key,
            value=timestamp,
            timeout=cls.LAST_SEEN_CACHE_TIMEOUT
        )
        cls._set_online_index_for_user(user_id=user.id, timestamp=timestamp)

    @classmethod
    def set_last_seen_now(cls, user: UserModel):
        cls._set_last_seen_cache(
            user=user,
            value=timezone.now()
        )

    @classmethod
    def get_last_seen(cls, user: UserModel) -> Optional[datetime]:

        """ Для укзанного пользователя возрвращает
            дату последнего захода на сайт,
            если пользователь ни разу не входил возвращает None """

        cache_key = cls._get_cache_key(user.id)
        value = cache.get(cache_key)
        if value:
            value = datetime.fromtimestamp(value, tz=timezone.utc)
        elif value is None:
            if user.last_login:
                value = user.last_login
                cls._set_last_seen_cache(
                    user=user,
                    value=value
                )
        return value

    @classmethod
    def user_is_online(cls, user: UserModel) -> bool:
        last_seen = cls.get_last_seen(user)
        if last_seen is None:
            return False
        else:
            timeout = cls.USER_ONLINE_TIMEOUT
            return (
                last_seen + timedelta(seconds=timeout) >= timezone.now()
            )

    @classmethod
    def get_online_users_ids(cls) -> List[int]:
        index = cache.get(cls.USERS_ONLINE_KEY) or {}
        if not index:
            return frozenset()

        now = timezone.now()
        timeout = cls.USER_ONLINE_TIMEOUT
        online_ids = set()
        actual_index = {}

        for user_id, timestamp in index.items():
            last_seen = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            if last_seen + timedelta(seconds=timeout) >= now:
                actual_index[user_id] = timestamp

        cls._set_online_index(actual_index)
        return actual_index.keys()
