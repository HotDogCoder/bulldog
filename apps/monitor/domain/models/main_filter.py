from abc import ABC


class MainFilter(ABC):
    def __init__(self, date, text, number):
        self.date = date
        self.text = text
        self.number = number

