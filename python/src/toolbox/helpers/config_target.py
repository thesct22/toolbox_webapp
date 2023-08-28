"""Configure the target machine to be accessed via ansible."""
from pathlib import Path
import subprocess


def config_target(host: str, user: str, password: str, operating_system: str) -> None:
    """
    Configure the target machine to be accessed via ansible.

    Args:
        host (str): The host to configure.
    """
    print(f"Configuring {operating_system} host: {host}...")
    if operating_system == "Linux":
        if not (Path.home() / ".ssh" / "id_rsa.pub").exists():
            print("Generating rsa key...")
            subprocess.run(
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
            )

        command = f"sshpass -p {password} ssh-copy-id -o StrictHostKeyChecking=no {user}@{host}"
        try:
            output = subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError:
            raise ValueError("Failed to configure target.")
        if output.returncode != 0:
            raise ValueError("Failed to configure target.")

    elif operating_system == "Windows":
        if not (Path.home() / ".ssh" / "id_rsa.pub").exists():
            print("Generating rsa key...")
            subprocess.run(
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
            )

        rsa_file_contents = (Path.home() / ".ssh" / "id_rsa.pub").read_text().strip()
        # run ssh user@machine powershell ni command to make .ssh/authoized_keys file if it doesn't exist
        command1 = [
            "sshpass",
            "-p",
            password,
            "ssh",
            f"{user}@{host}",
            "powershell",
            "-Command",
            "if (!(test-path ~/.ssh/authorized_keys)) {ni ~/.ssh/authorized_keys}",
        ]

        # run ssh user@machine powershell add-content command to add rsa key to authorized_keys file
        command2 = [
            "sshpass",
            "-p",
            password,
            "ssh",
            f"{user}@{host}",
            "powershell",
            "-Command",
            f"Add-Content -Path ~/.ssh/authorized_keys -Value '{rsa_file_contents}'",
        ]

        try:
            output = subprocess.run(command1, check=True)
            output2 = subprocess.run(command2, check=True)
        except subprocess.CalledProcessError:
            raise ValueError("Failed to configure target.")
        if output.returncode != 0 or output2.returncode != 0:
            raise ValueError("Failed to configure target.")

    else:
        raise ValueError("Unsupported operating system.")
