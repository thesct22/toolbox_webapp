from pathlib import Path
from unittest.mock import Mock

import pytest
from toolbox.core.ansible import Ansible


@pytest.fixture
def ansible_instance(mocker):
    # Mock the subprocess.run function
    mocker.patch("subprocess.run")

    # Create an instance of Ansible with some default data
    return Ansible(
        inventory="remote_host1,remote_host2",
        user="test_user",
        password="test_password",
        run_folder=Path("/path/to/run_folder"),
        verbosity=2,
        tags=["tag1", "tag2"],
        extra_vars=[{"var1": "value1"}, {"var2": "value2"}],
        extra_args="--extra-arg",
        playbook="playbook.yml",
    )


def test_run_command(ansible_instance: Ansible, mocker):
    # Mock subprocess.run to return a successful result
    mocker.patch(
        "subprocess.run",
        return_value=Mock(returncode=0, stdout=b"success\n", stderr=b""),
    )

    command_to_run = ansible_instance.get_command()

    assert ansible_instance.run_command(command_to_run) == "success\n"


def test_run_command_failure(ansible_instance: Ansible, mocker):
    # Mock subprocess.run to return a non-zero return code for localhost
    mocker.patch(
        "subprocess.run",
        return_value=Mock(returncode=1, stdout=b"failure\n", stderr=b""),
    )

    command_to_run = ansible_instance.get_command()

    with pytest.raises(ValueError, match="Failed to run ansible. failure\n"):
        ansible_instance.run_command(command_to_run)
