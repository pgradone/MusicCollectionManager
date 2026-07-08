"""
Global application configuration.
"""

from pathlib import Path

APP_NAME = "Music Collection Manager"
APP_VERSION = "1.0.0"

ROOT_DIR = Path(__file__).resolve().parent

DATABASE_FILE = ROOT_DIR / "Musi.db"

BACKUP_FOLDER = ROOT_DIR / "backups"

LOG_FOLDER = ROOT_DIR / "logs"

EXPORT_FOLDER = ROOT_DIR / "exports"

RESOURCE_FOLDER = ROOT_DIR / "resources"

ICON_FOLDER = RESOURCE_FOLDER / "icons"

THEME_FOLDER = RESOURCE_FOLDER / "themes"

SETTINGS_FILE = ROOT_DIR / "settings.json"

LOG_LEVEL = "INFO"

AUTO_BACKUP = True

MAX_BACKUPS = 30

WINDOW_WIDTH = 1600

WINDOW_HEIGHT = 900

ORGANIZATION = "Gradone Software"

APPLICATION = "MusicCollectionManager"