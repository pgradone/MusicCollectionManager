from main import build_table_query


def test_build_table_query_uses_expected_columns() -> None:
    query = build_table_query("Artists")

    assert "SELECT" in query
    assert "FROM [Artists]" in query
    assert "ORDER BY [ArtistID]" in query
