import logging
from subprocess import call

logger = logging.getLogger(__name__)

class Switch:
    '''
    Switches have an on and off switch, with corresponding RF codes to send.
    Name is a display name for the switch, and a unique ID should be assigned.
    '''

    def __init__(self, id, name, oncode, offcode):
        self.id = id
        self.name = name
        self.oncode = oncode
        self.offcode = offcode

    def _sendcode(self, code):
        retcode = call(['/usr/local/bin/codesend', str(code)])
        logging.info('Sent code {} for switch {}'.format(code, self.name))
        if retcode != 0:
            raise Exception('Error sending code {}'.format(code))
    
    def on(self):
        self._sendcode(self.oncode)

    def off(self):
        self._sendcode(self.offcode)
        

