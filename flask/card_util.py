from datetime import datetime


def card_getdatestrnow():
    dt_now = datetime.now()
    return card_getdatestr(dt_now)


def card_getdatestr(dt):
    return dt.isoformat()


def card_getdatenow():
    return datetime.now()


def card_getdate(dt):
    return datetime.fromisoformat(dt)
