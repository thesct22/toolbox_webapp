from toolbox.helpers.find_free_port import find_free_port


def test_find_free_port():
    """Test the find free port."""
    assert find_free_port() != 0
    assert isinstance(find_free_port(), int)
    assert find_free_port() > 0
    assert find_free_port() < 65535
    assert isinstance(find_free_port("localhost"), int)
