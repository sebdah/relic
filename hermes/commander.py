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
        exec('self.%s("%s")' % (command, ", ".join(args)))
    
    def echo(self, *args):
        """
        Echo the message to the prompt
        
        args[0]:        message to print
        """
        print args[0]
        return True