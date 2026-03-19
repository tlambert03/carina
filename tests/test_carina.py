import carina


def test_imports_with_version() -> None:
    assert isinstance(carina.__version__, str)
