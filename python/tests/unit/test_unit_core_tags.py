import pytest
from toolbox.core.tags import InstallationTags, Tags, UninstallationTags


def test_tags():
    """Test the tags."""
    tags = Tags()
    assert tags.get_tags() == []


def test_get_instalation_tags():
    """Test the get tags."""
    tags = InstallationTags()
    assert tags.get_tags() == []


def test_get_uninstalation_tags():
    """Test the get tags."""
    tags = UninstallationTags()
    assert tags.get_tags() == []


def test_installation_read_tags_from_playbooks():
    """Test the read tags from installation."""
    tags = InstallationTags()
    tags.read_tags_from_playbooks()
    assert tags.get_tags() != []
    assert isinstance(tags.get_tags(), list)
    assert isinstance(tags.get_tags()[0], dict)
    assert isinstance(tags.get_tags()[0]["title"], str)
    assert isinstance(tags.get_tags()[0]["tags"], list)
    assert isinstance(tags.get_tags()[0]["tags"][0], str)


def test_uninstallation_read_tags_from_playbooks():
    """Test the read tags from uninstallation."""
    tags = UninstallationTags()
    tags.read_tags_from_playbooks()
    assert tags.get_tags() != []
    assert isinstance(tags.get_tags(), list)
    assert isinstance(tags.get_tags()[0], dict)
    assert isinstance(tags.get_tags()[0]["title"], str)
    assert isinstance(tags.get_tags()[0]["tags"], list)
    assert isinstance(tags.get_tags()[0]["tags"][0], str)


def test_tags_validation_tags_is_a_string():
    with pytest.raises(ValueError):
        Tags().validate_tags("tags")


def test_tags_validation_tags_without_title():
    with pytest.raises(ValueError):
        Tags().validate_tags(tags=[{"tags": ["tag1", "tag2"]}])


def test_tags_validation_tags_without_tags():
    with pytest.raises(ValueError):
        Tags().validate_tags(tags=[{"title": "title"}])


def test_tags_validation_tags_title_is_not_a_string():
    with pytest.raises(ValueError):
        Tags().validate_tags(tags=[{"title": 123, "tags": ["tag1", "tag2"]}])


def test_tags_validation_tags_tags_is_not_a_list():
    with pytest.raises(ValueError):
        Tags().validate_tags(tags=[{"title": "title", "tags": "tag1"}])


def test_tags_validation_tags_tags_is_not_a_string():
    with pytest.raises(ValueError):
        Tags().validate_tags(tags=[{"title": "title", "tags": [123]}])


def test_tags_validation_tags_tags_is_not_lowercase():
    with pytest.raises(ValueError):
        Tags().validate_tags(tags=[{"title": "title", "tags": ["Tag1"]}])


def test_tags_validation_tags_tags_is_not_alphanumeric():
    with pytest.raises(ValueError):
        Tags().validate_tags(tags=[{"title": "title", "tags": ["tag-1"]}])


def test_tags_validation_tags_title_is_not_alphanumeric():
    with pytest.raises(ValueError):
        Tags().validate_tags(tags=[{"title": "title$1", "tags": ["tag1"]}])
