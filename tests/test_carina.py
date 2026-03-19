import carina


def test_imports_with_version():
    assert isinstance(carina.__version__, str)
