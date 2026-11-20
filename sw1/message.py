import datetime
from dataclasses import dataclass


@dataclass
class Message:
    type:str
    sender_id:int
    sender_name:str
    recipient:int|None
    text:str
    time: datetime.datetime
    room:str|None
