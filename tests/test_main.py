from core.database import DatabaseManager
from main import DatabaseInfo, collect_database_info


def test_collect_database_info_returns_connected_state_and_tables() -> None:
    db = DatabaseManager()

    info: DatabaseInfo = collect_database_info(db)

    assert info["connected"] is True
    assert isinstance(info["tables"], list)
    assert len(info["tables"]) > 0
