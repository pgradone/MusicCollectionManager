"""
Automatic database backup.
"""


import shutil

from datetime import datetime

import config


def backup_database():

    if not config.AUTO_BACKUP:

        return

    config.BACKUP_FOLDER.mkdir(exist_ok=True)

    if not config.DATABASE_FILE.exists():

        return

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