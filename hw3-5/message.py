import datetime
from dataclasses import dataclass


@dataclass
class Message:
	type: str
	username: str
	date: datetime.datetime
	text: str
	destination_username: str | None = None