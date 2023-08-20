Executable
==========

.. note::
    The executable is only available for Linux x86_64 and differnt from the above docker container.

This can be used if you wish to not use docker.

Build
-----

To build the executable, run the following command:

.. code-block:: bash

    cd toolbox-webapp/python
    ./build_standalone.sh

This will create a folder called `toolbox` in the `python` directory.

Run
---

To run the executable, run the following command:

.. code-block:: bash

    cd toolbox
    ./main.bin

Note: The executable is only available for Linux x86_64.

To open the webapp go to: `http://localhost:8000`

To stop the webapp, press `Ctrl+C` (multiple times if needed).
