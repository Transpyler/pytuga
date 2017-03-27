class Connection:
    """
    Represents a connection between a server and client.
    """

    def start(self):
        """
        Initializes connection object.
        """

    def send(self, msg):
        """
        Sends a JSON-compatible message through connection.
        Returns the JSON response.

        This method is used at client side.
        """

        raise NotImplementedError

    def receive(self):
        """
        Receive a JSON-compatible message through connection.

        This method is used at server side.
        """

        raise NotImplementedError


class TCPConnection(Connection):
    """
    Connection over TCP/IP.
    """


class UDPConnection(Connection):
    """
    Communicate over UDP sockets.
    """


class PIPEConnection(Connection):
    """
    Communicate using unix pipes.
    """


class InProcessConnection(Connection):
    """
    A simple connetion for servers that runs in the same process as clients.

    It simply forwards messages to the server object.
    """

    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.server = manager.server

    def send(self, msg):
        response = self.server.dispatch_message(msg)
        if response is None:
            return {'status': 'ok'}
        else:
            return {'status': 'result', 'value': response}

    def receive(self):
        return {'status': 'error',
                'error': 'builtins.RuntimeError',
                'args': ['unexpected request']}