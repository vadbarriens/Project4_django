from django.core.cache import cache

from config.settings import CACHE_ENABLED
from mailings.models import Mailing


def get_mailings_from_cache():
    """Получает данные по рассылкам из кэша, а если кэш пуст, то из БД"""
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    key = "mailing_list"
    mailings = cache.get(key)
    if mailings is not None:
        return mailings
    mailings = Mailing.objects.all()
    cache.set(key, mailings)
    return mailings
