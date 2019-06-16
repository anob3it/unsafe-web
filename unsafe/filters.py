from datetime import datetime
from typing import Union, Dict, Callable, Optional

from dateutil.relativedelta import relativedelta
from pyramid.config import Configurator


def abbrev_filter(value: str, maxlen=40):
    """Return the first line of a string abbreviated to ``maxlen`` characters.

    The result will have an ellipsis appended if truncated by leaving out lines
    or truncating the first line.
    """
    if not value:
        return value
    try:
        i = value.index('\n')
        clipped = i + 1 < len(value)
        value = value[:i]
    except ValueError:
        clipped = False

    if value.endswith(':'):
        value = value[:-1]
        clipped = True

    if len(value) > maxlen:
        value = value[0:maxlen]
        clipped = True

    return value + '\u2026' if clipped else value


def since_filter(value: Union[datetime, str], now: Optional[Union[datetime, str]] = None):
    if not value:
        return ''

    if isinstance(value, str):
        then = datetime.fromisoformat(value)
    else:
        then = value

    if now is None:
        now = datetime.now()
    elif isinstance(now, str):
        now = datetime.fromisoformat(now)

    delta = relativedelta(now, then)
    if delta.years:
        return f'{abs(delta.years)} år'
    elif delta.months:
        months = abs(delta.months)
        return f'{months} månader' if months > 1 else '1 månad'
    elif delta.days:
        days = abs(delta.days)
        return f'{days} dagar' if days > 1 else '1 dag'
    elif delta.hours:
        hours = abs(delta.hours)
        return f'{hours} timmar' if hours > 1 else '1 timme'
    elif delta.minutes:
        minutes = abs(delta.minutes)
        return f'{minutes} minuter' if minutes > 1 else '1 minut'
    else:
        seconds = abs(delta.seconds)
        return f'{seconds} sekunder' if seconds != 1 else '1 sekund'


def jinja2_filters() -> Dict[str, Callable]:
    import pyramid_jinja2.filters
    return dict(abbrev=abbrev_filter,
                since=since_filter,
                route_url=pyramid_jinja2.filters.route_url_filter,
                static_url=pyramid_jinja2.filters.static_url_filter,
                )


def includeme(config: Configurator):
    config.registry.settings['jinja2.filters'] = jinja2_filters()
