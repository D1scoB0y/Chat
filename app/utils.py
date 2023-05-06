import datetime as dt


def current_datetime() -> dt.datetime:
    '''Возвращает текущую дату и время'''
    return dt.datetime.utcnow().replace(microsecond=0)

