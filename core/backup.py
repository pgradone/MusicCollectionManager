"""
Automatic database backup.
"""


import shutil

from datetime import datetime
from pathlib import Path

import config


def backup_database() -> Path | None:
    """
    Copy the database into the backup folder under a timestamped
    name and prune the oldest copies beyond config.MAX_BACKUPS.

    Returns the path of the new backup, or None when nothing was
    done (backups disabled, or there is no database file yet).
    """

    if not config.AUTO_BACKUP:

        return None

    config.BACKUP_FOLDER.mkdir(exist_ok=True)

    if not config.DATABASE_FILE.exists():

        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    destination = (
        config.BACKUP_FOLDER /
        f"Musi_{timestamp}.db"
    )

    shutil.copy2(
        config.DATABASE_FILE,
        destination
    )

    backups = sorted(
        config.BACKUP_FOLDER.glob("Musi_*.db"),
        reverse=True
    )

    for backup in backups[config.MAX_BACKUPS:]:

        backup.unlink()

    return destination
