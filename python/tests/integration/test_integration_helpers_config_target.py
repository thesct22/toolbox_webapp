from pathlib import Path
from unittest.mock import call, patch

import pytest
from toolbox.helpers.config_target import config_target


# create a temporary directory to store the ssh key
@pytest.fixture
def tmp_ssh_dir(tmp_path: Path):
    ssh_dir = tmp_path / ".ssh"
    ssh_dir.mkdir()
    return ssh_dir


@patch("subprocess.run")
@patch("pathlib.Path.home")
def test_config_target_linux(mock_pathlib_home, mock_subprocess_run, tmp_ssh_dir: Path):
    mock_subprocess_run.return_value.returncode = 0
    mock_subprocess_run.return_value.stdout = b"mocked_key"
    mock_pathlib_home.return_value = tmp_ssh_dir.parent
    config_target("example.com", "username", "password", "Linux")

    expected_calls = [
        call(
            [
                "ssh-keygen",
                "-t",
                "rsa",
                "-N",
                "",
                "-q",
                "-f",
                f"{Path.home()}/.ssh/id_rsa",
            ],
        ),
        call(
            "sshpass -p password ssh-copy-id -o StrictHostKeyChecking=no username@example.com",
            shell=True,
            check=True,
        ),
    ]
    mock_subprocess_run.assert_has_calls(expected_calls)


@patch("subprocess.run")
@patch("pathlib.Path.home")
def test_config_target_windows_with_rsa_file(
    mock_pathlib_home, mock_subprocess_run, tmp_ssh_dir: Path
):
    mock_subprocess_run.return_value.returncode = 0
    mock_subprocess_run.return_value.stdout = b"mocked_key"
    mock_pathlib_home.return_value = tmp_ssh_dir.parent
    (tmp_ssh_dir / "id_rsa.pub").write_text("mocked_key")

    config_target("example.com", "username", "password", "Windows")

    expected_calls = [
        call(
            [
                "sshpass",
                "-p",
                "password",
                "ssh",
                "username@example.com",
                "powershell",
                "-Command",
                "if (!(test-path ~/.ssh/authorized_keys)) {ni ~/.ssh/authorized_keys}",
            ],
            check=True,
        ),
        call(
            [
                "sshpass",
                "-p",
                "password",
                "ssh",
                "username@example.com",
                "powershell",
                "-Command",
                "Add-Content -Path ~/.ssh/authorized_keys -Value 'mocked_key'",
            ],
            check=True,
        ),
    ]
    mock_subprocess_run.assert_has_calls(expected_calls)


def test_config_target_unsupported_os():
    with pytest.raises(ValueError, match="Unsupported operating system."):
        config_target("example.com", "username", "password", "UnsupportedOS")
