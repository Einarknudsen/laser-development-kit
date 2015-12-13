from .kclient import reference_dict

# --------------------------------------------
# Decorators
# --------------------------------------------

def command(func):
    """ Decorate commands
    
    If the name of the command is CMD_NAME, 
    then the name of the function must be cmd_name.
    
    /!\ The order of kwargs matters.
    """
    def decorator(self, *args, **kwargs):
        self.client.send_command(self.ref['id'], self.ref[func.__name__], 
                                 *(args + tuple(kwargs.values())))
        return func(self, *args, **kwargs)
    return decorator

# --------------------------------------------
# Base class
# --------------------------------------------

class Device(object):
    def __init__(self, client):
        self.client = client
        self.ref = reference_dict(self)
        self.is_failed = False
