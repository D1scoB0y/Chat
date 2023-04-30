import datetime as dt


def current_datetime() -> dt.datetime:
    '''Возвращает текущую дату и время'''
    return dt.datetime.utcnow().replace(microsecond=0)


def current_date() -> dt.date:
    '''Возвращает текущую дату без времени'''
    return dt.date.today()
