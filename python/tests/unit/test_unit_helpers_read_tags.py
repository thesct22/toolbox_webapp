from pathlib import Path

import pytest
from toolbox.helpers.read_tags import read_tags_helper


@pytest.fixture
def root_folder(tmp_path: Path):
    """Returns a temporary folder for testing."""
    folder = tmp_path / "ansible" / "roles"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def test_install_read_tags():
    assert isinstance(read_tags_helper(True), list)
    assert len(read_tags_helper(True)) > 0
    assert isinstance(read_tags_helper(True)[0], dict)
    assert isinstance(read_tags_helper(True)[0]["title"], str)
    assert isinstance(read_tags_helper(True)[0]["tags"], list)
    assert isinstance(read_tags_helper(True)[0]["tags"][0], str)


def test_uninstall_read_tags():
    assert isinstance(read_tags_helper(False), list)
    assert len(read_tags_helper(False)) > 0
    assert isinstance(read_tags_helper(False)[0], dict)
    assert isinstance(read_tags_helper(False)[0]["title"], str)
    assert isinstance(read_tags_helper(False)[0]["tags"], list)
    assert isinstance(read_tags_helper(False)[0]["tags"][0], str)


def test_read_tags_helper_with_no_ansible_roles_dir(mocker):
    mocker.patch("toolbox.helpers.read_tags.Path.exists", return_value=False)
    with pytest.raises(ValueError):
        read_tags_helper(True)
