from pathlib import Path

from toolbox.core.ansible import Ansible


def test_get_command():
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

    ansible_command = ansible.get_command()

    assert ansible_command == [
        "ansible-playbook",
        "playbook.yml",
        "-i",
        "inventory,",
        "-u",
        "user",
        "-e",
        "ansible_password=password",
        "-e",
        "ansible_become_password=password",
        "-e",
        "ansible_ssh_password=password",
        "-vv",
        "--tags",
        "tag1,tag2",
        "-e",
        "var1=value1",
        "-e",
        "var2=value2",
        "--extra-arg",
    ]


def test_get_command_with_no_verbose():
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

    ansible_command = ansible.get_command()

    assert ansible_command == [
        "ansible-playbook",
        "playbook.yml",
        "-i",
        "inventory,",
        "-u",
        "user",
        "-e",
        "ansible_password=password",
        "-e",
        "ansible_become_password=password",
        "-e",
        "ansible_ssh_password=password",
        "--tags",
        "tag1,tag2",
        "-e",
        "var1=value1",
        "-e",
        "var2=value2",
        "--extra-arg",
    ]


def test_get_command_with_no_tags():
    ansible = Ansible(
        user="user",
        password="password",
        inventory="inventory",
        run_folder=Path("/path/to/run/folder"),
        playbook="playbook.yml",
        extra_vars=[{"var1": "value1"}, {"var2": "value2"}],
        verbosity=2,
        extra_args="--extra-arg",
    )

    ansible_command = ansible.get_command()

    assert ansible_command == [
        "ansible-playbook",
        "playbook.yml",
        "-i",
        "inventory,",
        "-u",
        "user",
        "-e",
        "ansible_password=password",
        "-e",
        "ansible_become_password=password",
        "-e",
        "ansible_ssh_password=password",
        "-vv",
        "-e",
        "var1=value1",
        "-e",
        "var2=value2",
        "--extra-arg",
    ]


def test_get_command_with_no_extra_vars():
    ansible = Ansible(
        user="user",
        password="password",
        inventory="inventory",
        run_folder=Path("/path/to/run/folder"),
        playbook="playbook.yml",
        tags=["tag1", "tag2"],
        verbosity=2,
        extra_args="--extra-arg",
    )

    ansible_command = ansible.get_command()

    assert ansible_command == [
        "ansible-playbook",
        "playbook.yml",
        "-i",
        "inventory,",
        "-u",
        "user",
        "-e",
        "ansible_password=password",
        "-e",
        "ansible_become_password=password",
        "-e",
        "ansible_ssh_password=password",
        "-vv",
        "--tags",
        "tag1,tag2",
        "--extra-arg",
    ]


def test_get_command_with_no_extra_args():
    ansible = Ansible(
        user="user",
        password="password",
        inventory="inventory",
        run_folder=Path("/path/to/run/folder"),
        playbook="playbook.yml",
        tags=["tag1", "tag2"],
        extra_vars=[{"var1": "value1"}, {"var2": "value2"}],
        verbosity=2,
    )

    ansible_command = ansible.get_command()

    assert ansible_command == [
        "ansible-playbook",
        "playbook.yml",
        "-i",
        "inventory,",
        "-u",
        "user",
        "-e",
        "ansible_password=password",
        "-e",
        "ansible_become_password=password",
        "-e",
        "ansible_ssh_password=password",
        "-vv",
        "--tags",
        "tag1,tag2",
        "-e",
        "var1=value1",
        "-e",
        "var2=value2",
    ]


def test_get_command_with_bare_minimum():
    ansible = Ansible(
        user="user",
        password="password",
        inventory="inventory",
        playbook="playbook.yml",
    )

    ansible_command = ansible.get_command()

    assert ansible_command == [
        "ansible-playbook",
        "playbook.yml",
        "-i",
        "inventory,",
        "-u",
        "user",
        "-e",
        "ansible_password=password",
        "-e",
        "ansible_become_password=password",
        "-e",
        "ansible_ssh_password=password",
    ]
