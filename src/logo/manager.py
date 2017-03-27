class Manager:
    """
    A manager object controls and initializes a server process in the client
    application.

    It is responsible for opening communication channels and initializing the
    connection between both processes.
    """

    def __init__(self, **kwargs):
        pass

    def start(self):
        """
        Starts manager.
        """

        self.start_server()

    def start_server(self):
        """
        Starts server process.
        """

        raise NotImplementedError


class InProcessManager(Manager):
    """
    Control servers that share same process as client.
    """

    def __init__(self, server, **kwargs):
        super().__init__()
        self.server = server

    def start_server(self):
        self.server.start()