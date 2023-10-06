import json
from pathlib import Path

import dateutil.parser
from django import template

from manager.kiwix_library import Book, catalog
from manager.models import Address, Order
from manager.utils import human_readable_size

register = template.Library()


def human_size(value):
    return human_readable_size(value).replace(" ", " ")  # noqa: RUF001


register.filter("human_size", human_size)


def raw_number(value):
    return str(value)


register.filter("raw_number", raw_number)


def fname(value):
    return Path(value).name.split("_")[-1]


register.filter("fname", fname)


def books_from_json(db_value: str) -> list[Book]:
    books = [catalog.get_or_none(ident) for ident in json.loads(db_value) or []]
    return [book for book in books if book]


register.filter("books_from_json", books_from_json)


def as_widget(field):
    if not hasattr(field, "as_widget"):
        return field
    our_classes = ["form-control"]
    if getattr(field, "errors", False):
        our_classes += ["alert-danger"]
    return field.as_widget(attrs={"class": field.css_classes(" ".join(our_classes))})


register.filter("as_widget", as_widget)


def country_name(country_code):
    return Address.country_name_for(country_code)


register.filter("country", country_name)


def get_id(mongo_data):
    return mongo_data.get("_id") if isinstance(mongo_data, dict) else None


register.filter("id", get_id)


def clean_statuses(items):
    if not isinstance(items, list):
        return []
    return sorted(
        [
            {
                "status": item.get("status"),
                "on": dateutil.parser.parse(item.get("on")),
                "payload": item.get("payload"),
            }
            for item in items
        ],
        key=lambda x: x["on"],
        reverse=True,
    )


register.filter("clean_statuses", clean_statuses)


def plus_one(number):
    return number + 1


register.filter("plus_one", plus_one)


def status_color(status):
    return {
        Order.COMPLETED: "message-success",
        Order.FAILED: "message-error",
        Order.NOT_CREATED: "message-error",
    }.get(status, "")


register.filter("status_color", status_color)


def clean_datetime(dt):
    return dateutil.parser.parse(dt) if dt else None


register.filter("datetime", clean_datetime)


def short_id(anid):
    if not anid:
        return None
    return anid[:8] + anid[-3:]


register.filter("short_id", short_id)


def yesno(value):
    """yes or no string from bool value"""
    return "yes" if bool(value) else "no"


register.filter("yesnoraw", yesno)
