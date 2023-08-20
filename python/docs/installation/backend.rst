Toolbox Backend
===============

Installation
------------

Requirements
~~~~~~~~~~~~

Operating System
^^^^^^^^^^^^^^^^

- Linux (Ubuntu 20.04 LTS and up)

Python
^^^^^^

- Python 3.9 and up

Setup
~~~~~

Make sure you are in the `python` directory.

.. code-block:: bash

    cd python

Run the setup script.

.. code-block:: bash

    ./setup.sh

.. note::
    
    If you get a permission denied error, run `chmod +x setup.sh` and try again.
    
    Powershell equivalent: `.\setup.ps1` is also provided. However, it is limited in capacity due to ansible not supporting Windows host machines. Ansible does support Windows target machines though.
    
Install and build the frontend.

For more information on installing the frontend, please refer to 
:doc:`frontend installing <frontend>`.

Build the react static files and copy them and the ansible folder to the python source folder using this python script.

.. code-block:: bash

    python ./tools/build.py

.. note::
    
    Make sure you run this from the `python` directory.

Usage
-----

Make sure you are in the `python` directory, which is the folder containing this README file.

.. code-block:: bash

    cd python

Running the webapp
~~~~~~~~~~~~~~~~~~

Start uvicorn server.

.. code-block:: bash

    poetry run python -m toolbox.main

Enabling pre-commit hooks
~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
    
    Pre-commit is used for code quality and formatting. It is recommended to enable it.
    
    It runs code style checks and auto-formats code before committing and fails if there are any issues with the code, so you can fix them before committing.

.. code-block:: bash

    poetry run pre-commit install

Running pre-commit hooks manually
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    poetry run pre-commit run --all-files

.. note::
    
    This is automatically run when you commit changes.
