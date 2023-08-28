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
    )


def test_verify_auth_remote_hosts(ansible_instance: Ansible, mocker):
    # Mock subprocess.run to return a successful result
    mocker.patch(
        "subprocess.run",
        return_value=Mock(returncode=0, stdout=b"success\n", stderr=b""),
    )

    assert ansible_instance.verify_auth() is True


def test_verify_auth_local_host(ansible_instance: Ansible, mocker):
    # Mock subprocess.run to return a successful result for localhost
    mocker.patch(
        "subprocess.run",
        return_value=Mock(returncode=0, stdout=b"success\n", stderr=b""),
    )

    ansible_instance.inventory = "localhost"

    assert ansible_instance.verify_auth() is True


def test_verify_auth_remote_host_failure(ansible_instance: Ansible, mocker):
    # Mock subprocess.run to return a non-zero return code for remote host
    mocker.patch(
        "subprocess.run",
        return_value=Mock(returncode=1, stdout=b"failure\n", stderr=b""),
    )

    with pytest.raises(ValueError, match="Failed to verify ansible credentials"):
        ansible_instance.verify_auth()


def test_verify_auth_local_host_failure(ansible_instance: Ansible, mocker):
    # Mock subprocess.run to return a non-zero return code for localhost
    mocker.patch(
        "subprocess.run",
        return_value=Mock(returncode=1, stdout=b"failure\n", stderr=b""),
    )

    with pytest.raises(
        ValueError, match="Failed to verify ansible credentials for host: localhost"
    ):
        ansible_instance.inventory = "localhost"
        ansible_instance.verify_auth()
