from django.db import models
from subprocess import call

class Outlet(models.Model):
    # Constants for calling codesend
    _codesend = '433Utils/RPi_utils/codesend'
    _protocol = '0'
    _pulselength = '189'

    name = models.CharField(max_length=50)
    on_code = models.IntegerField()
    off_code = models.IntegerField()
    state = models.BooleanField(default=False)

    def _sendsignal(self, code, new_state):
        try:
            call([Outlet._codesend, str(code), Outlet._protocol, Outlet._pulselength])
            self.state = new_state
            self.save()
        except Exception as e:
            raise Exception('Error calling codesend!', e)

    def turn_on(self):
        self._sendsignal(self.on_code, True)

    def turn_off(self):
        self._sendsignal(self.off_code, False)

    def __str__(self):
        return self.name
