import logging
from subprocess import call

logger = logging.getLogger(__name__)

PULSE_WIDTH = '189'

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
        retcode = call(['433Utils/RPi_utils/codesend', str(code), '0', PULSE_WIDTH])
        logging.info('Sent code {} for switch {}'.format(code, self.name))
        if retcode != 0:
            raise Exception('Error sending code {}'.format(code))
    
    def on(self):
        self._sendcode(self.oncode)

    def off(self):
        self._sendcode(self.offcode)
        

