"""Configure the target machine to be accessed via ansible."""
from pathlib import Path
import subprocess


def config_target(host: str, user: str, password: str) -> None:
    """
    Configure the target machine to be accessed via ansible.

    Args:
        host (str): The host to configure.
    """
    print(f"Configuring {host}...")

    # check if rsa key exists
    if not (Path.home() / ".ssh" / "id_rsa.pub").exists():
        print("Generating rsa key...")
        # use ssh-keygen -t rsa -N '' -f id_rsa
        subprocess.run(
            ["ssh-keygen", "-t", "rsa", "-N", "''", "-f", "id_rsa"], check=True
        )

    command = (
        f"sshpass -p {password} ssh-copy-id -o StrictHostKeyChecking=no {user}@{host}"
    )
    output = subprocess.run(command, shell=True, check=True)
    if output.returncode != 0:
        raise ValueError("Failed to configure target.")
