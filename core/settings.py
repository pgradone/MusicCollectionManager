"""
Application settings.
"""

import json

import config


class Settings:

    def __init__(self):

        self.filename = config.SETTINGS_FILE

        self.data = {}

        self.load()

    def load(self):

        if self.filename.exists():

            with open(self.filename, "r", encoding="utf-8") as file:

                self.data = json.load(file)

        else:

            self.data = {

                "theme": "light",

                "window_width": config.WINDOW_WIDTH,

                "window_height": config.WINDOW_HEIGHT,

                "maximized": False

            }

            self.save()

    def save(self):

        with open(self.filename, "w", encoding="utf-8") as file:

            json.dump(
                self.data,
                file,
                indent=4
            )

    def get(self, key, default=None):

        return self.data.get(key, default)

    def set(self, key, value):

        self.data[key] = value

        self.save()