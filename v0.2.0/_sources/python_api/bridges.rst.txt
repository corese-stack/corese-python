Java bridge packages
====================

Corese is a stack of Java libraries that implement the standards of the Semantic Web.
To run and access Java libraries we tested two off-the-shelf packages:

- `py4j <https://www.py4j.org/>`_ - this package establishes a bridge between Python and Java using sockets (IPC). The
**corese-python** Java library implements the listener and wrapper for ``corese-core`` library and is built with ``gradle`` specifically for **pycorese**.

- `jpype <https://jpype.readthedocs.io/en/latest/>`_ - this package utilizes a single shared memory space by embedding the JVM directly into the Python process. The actual ``corese-core`` Java library is downloaded from the Maven repository.

At first we tried both packages to decide which one is better for our purposes. We found that both `py4j` and `jpype` have their pros and cons. See the comparison table below:

.. list-table:: Compare Python- Java bridge packages
  :widths: 24 38 38
  :header-rows: 1

  * -
    - JPype
    - Py4J

  * - Core Technology
    - JNI (direct JVM embedding)
    - Reflection & Socket IPC

  * - Communication
    - Shared memory (in-process)
    - Socket based (out-of-process)

  * - Performance
    - High (no serialization)
    - Moderate (due to IPC overhead)

  * - Setup
    - Requires JVM in-process
    - *Requires a GatewayServer*

  * - Use case
    - High-performance scenarios
    - Lightweight, flexible usage

  * - Crash Tolearnce
    - *Low: JVM crash affects Python (shared process) and cannot be restarted on its own*
    - High: JVM and Python are separate processes, so a JVM crash won't take down Python.

  * - Distribution
    - Download ``corese-core-{version}.jar``
    - Build ``corese-python-{version}.jar``

Although ``jpype`` is more performant and does not require an extra wrapper library, we decided to use ``py4j`` as a default because it is more crash tolerant. The main reason is that ``jpype`` requires the JVM to be embedded in the Python process and prohibits the restart of this subprocess in case of a crash (by design). This could be a critical issue for long-running applications or services.

However we decided to leave both bridges in the package and let the user choose the one that fits their needs better.

Both Java Libraries are installed with the package and can be used interchangeably. See the `User Guide <../user_guide.html>`_.
