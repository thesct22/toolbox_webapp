Docker Container
================

Toolbox Container
-----------------

To execute the docker container, run the following command:

.. code-block:: bash

    docker run -d -p 8000:8000 -p 8765:8765 ghcr.io/thesct22/toolbox:lastest --name toolbox

To open the webapp go to: `http://localhost:8000`

.. note::
    The container will be running in the background.

The username and password to use for this container are:

+----------+-----------------+
| Username | Password        |
+==========+=================+
| ansible  | ansible-password|
+----------+-----------------+

To find the IP address of the container, run the following command:

.. code-block:: bash

    docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' toolbox

To stop the container, run the following command:

.. code-block:: bash

    docker stop toolbox

To delete the container, run the following command:

.. code-block:: bash

    docker rm toolbox

Toolbox Tester Container
------------------------

To execute the docker container for testing the toolbox, run the following command:

.. code-block:: bash

    docker run -d ghcr.io/thesct22/toolbox-tester:lastest --name test1

If you wish to run 1 more testing container, run the following command:

.. code-block:: bash

    docker run -d ghcr.io/thesct22/toolbox-tester:lastest --name test2

To find the IP address of the container, run the following command:

.. code-block:: bash

    docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name>

For example, the IP address of the tester containers can be found by running the following commands:

.. code-block:: bash

    docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' test1
    docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' test2

Use these IP addresses to test the toolbox.

The username and password to use for these containers are:

+----------+-----------------+
| Username | Password        |
+==========+=================+
| ansible  | ansible-password|
+----------+-----------------+

To stop the containers, run the following command:

.. code-block:: bash

    docker stop test1
    docker stop test2

To delete the containers, run the following command:

.. code-block:: bash

    docker rm test1
    docker rm test2

Test the toolbox
----------------

First Configure these targets using the `configure target` page (click on the gear icon on the navbar).

Once successfully configured, you can return to home page and select the tools you wish to install and provide the above username and password and IP address(es) and click on `Install` or `Uninstall` button.

The `Ping` button can be used to check if the target(s) are reachable.

To stop the containers, run the following command:

.. code-block:: bash

    docker stop toolbox
    docker stop test1
    docker stop test2

.. note::
    Stop the container you wish to remove before deleting, delete it and create a new one.

To delete the containers, run the following command:

.. code-block:: bash

    docker rm toolbox
    docker rm test1
    docker rm test2

.. note::
    Delete the container you wish to remove and create a new one.

To open the webapp go to: `http://localhost:8000`
