from pathlib import Path

from toolbox.core.ansible import Ansible


def test_get_ping_command():
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
    ansible_command = ansible.get_ping_command()
    assert ansible_command == [
        "ansible",
        "all",
        "-i",
        "inventory,",
        "-u",
        "user",
        "-e",
        "ansible_ssh_password=password",
        "-m",
        "ping",
        "-vv",
    ]


def test_get_ping_command_with_no_verbose():
    ansible = Ansible(
        user="user",
        password="password",
        inventory="inventory",
        run_folder=Path("/path/to/run/folder"),
        playbook="playbook.yml",
        tags=["tag1", "tag2"],
        extra_vars=[{"var1": "value1"}, {"var2": "value2"}],
        extra_args="--extra-arg",
    )
    ansible_command = ansible.get_ping_command()
    assert ansible_command == [
        "ansible",
        "all",
        "-i",
        "inventory,",
        "-u",
        "user",
        "-e",
        "ansible_ssh_password=password",
        "-m",
        "ping",
    ]


def test_get_ping_command_with_bare_minimum():
    ansible = Ansible(
        user="user",
        password="password",
        inventory="inventory",
    )
    ansible_command = ansible.get_ping_command()
    assert ansible_command == [
        "ansible",
        "all",
        "-i",
        "inventory,",
        "-u",
        "user",
        "-e",
        "ansible_ssh_password=password",
        "-m",
        "ping",
    ]
