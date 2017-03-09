from django.db import models
from subprocess import call
import logging

logger = logging.getLogger(__name__)

class Outlet(models.Model):
    # Constants for calling codesend
    _protocol = '0'
    _pulselength = '189'

    name = models.CharField(max_length=50)
    on_code = models.IntegerField()
    off_code = models.IntegerField()
    state = models.BooleanField(default=False)

    def _sendsignal(self, code, new_state):
        try:
            call(['codesend', str(code), Outlet._protocol, Outlet._pulselength])
            self.state = new_state
            self.save()
            logger.info('Sent code {} successfully'.format(code))
        except Exception as e:
            logger.exception(e)
            raise Exception('Error calling codesend!', e)

    def turn_on(self):
        self._sendsignal(self.on_code, True)

    def turn_off(self):
        self._sendsignal(self.off_code, False)

    def __str__(self):
        return self.name
