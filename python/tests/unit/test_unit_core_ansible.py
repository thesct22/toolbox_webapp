from pathlib import Path

from pydantic import ValidationError
import pytest
from toolbox.core.ansible import Ansible


def test_ansible_singleton():
    ansible1 = Ansible(user="user", password="password", inventory="inventory")
    ansible2 = Ansible(user="user", password="password", inventory="inventory")
    assert ansible1 is ansible2


def test_ansible_required_fields():
    with pytest.raises(ValidationError):
        Ansible()


def test_ansible_optional_fields():
    ansible = Ansible(
        user="user",
        password="password",
        inventory="inventory",
        run_folder=Path("/path/to/run/folder"),
        playbook="playbook.yml",
        tags=["tag1", "tag2"],
        extra_vars=[{"var1": "value1"}, {"var2": "value2"}],
        verbosity=2,
        extra_args="--extra-arg",
    )
    assert ansible.run_folder == Path("/path/to/run/folder")
    assert ansible.playbook == "playbook.yml"
    assert ansible.inventory == "inventory"
    assert ansible.tags == ["tag1", "tag2"]
    assert ansible.extra_vars == [{"var1": "value1"}, {"var2": "value2"}]
    assert ansible.user == "user"
    assert ansible.password == "password"
    assert ansible.verbosity == 2
    assert ansible.extra_args == "--extra-arg"


def test_ansible_with_missing_inventory():
    with pytest.raises(ValueError):
        Ansible(user="user", password="password")


def test_ansible_missing_user():
    with pytest.raises(ValidationError):
        Ansible(password="password", inventory="inventory")


def test_ansible_missing_password():
    with pytest.raises(ValidationError):
        Ansible(user="user", inventory="inventory")


def test_ansible_with_empty_user():
    with pytest.raises(ValidationError):
        Ansible(user="", password="password", inventory="inventory")


def test_ansible_with_root_user():
    with pytest.raises(ValidationError):
        Ansible(user="root", password="password", inventory="inventory")


def test_ansible_with_empty_password():
    with pytest.raises(ValidationError):
        Ansible(user="user", password="", inventory="inventory")


def test_ansible_with_empty_inventory():
    with pytest.raises(ValidationError):
        Ansible(user="user", password="password", inventory="")


def test_ansible_empty_playbook():
    with pytest.raises(ValidationError):
        Ansible(user="user", password="password", inventory="inventory", playbook="")


def test_ansible_invalid_verbosity_greater_than_4():
    with pytest.raises(ValidationError):
        Ansible(user="user", password="password", inventory="inventory", verbosity=5)


def test_ansible_invalid_verbosity_less_than_0():
    with pytest.raises(ValidationError):
        Ansible(user="user", password="password", inventory="inventory", verbosity=-1)


def test_ansible_default_playbook():
    ansible = Ansible(user="user", password="password", inventory="inventory")
    assert ansible.playbook == "install.yml"


def test_ansible_invalid_inventory():
    with pytest.raises(ValidationError):
        Ansible(user="user", password="password", inventory="")


def test_ansible_run_folder_default():
    ansible = Ansible(user="user", password="password", inventory="inventory")
    assert (
        ansible.run_folder.as_posix().lower()
        == (Path(__file__).parent.parent.parent / "src" / "toolbox" / "ansible")
        .as_posix()
        .lower()
    )


def test_ansible_run_folder():
    ansible = Ansible(
        user="user",
        password="password",
        inventory="inventory",
        run_folder=Path("/path/to/run/folder"),
    )
    assert ansible.run_folder == Path("/path/to/run/folder")


def test_ansible_tags():
    ansible = Ansible(
        user="user", password="password", inventory="inventory", tags=["tag1", "tag2"]
    )
    assert ansible.tags == ["tag1", "tag2"]


def test_ansible_extra_vars():
    ansible = Ansible(
        user="user",
        password="password",
        inventory="inventory",
        extra_vars=[{"var1": "value1"}, {"var2": "value2"}],
    )
    assert ansible.extra_vars == [{"var1": "value1"}, {"var2": "value2"}]


def test_ansible_verbosity():
    ansible = Ansible(
        user="user", password="password", inventory="inventory", verbosity=2
    )
    assert ansible.verbosity == 2


def test_ansible_extra_args():
    ansible = Ansible(
        user="user",
        password="password",
        inventory="inventory",
        extra_args="--extra-arg",
    )
    assert ansible.extra_args == "--extra-arg"
