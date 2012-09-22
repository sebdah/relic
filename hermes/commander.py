"""
Defines all commands supported by Hermes
"""

class Commander():
    """
    Class for executing commands
    """
    def __init__(self, command, args):
        """
        Constructor
        """
        exec('self.%s("%s")' % (command, args))
    
    def echo(self, message):
        """
        Echo the message to the prompt
        """
        print message
        return True
