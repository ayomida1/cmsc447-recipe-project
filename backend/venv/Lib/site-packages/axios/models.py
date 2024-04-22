from dataclasses import dataclass
from datetime import date


@dataclass
class Credentials:
    username: str
    password: str
    customer_id: str


@dataclass
class Profile(object):
    customer_id: str
    name: str
    customer_title: str
    customer_name: str


@dataclass
class Grade:
    date: date
    subject: str
    kind: str
    value: str
    teacher: str
    comment: str = ""
