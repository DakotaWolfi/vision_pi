"""Client boundary between VisionPi and CollarPet.

Keep CollarPet's behaviour/runtime in the CollarPet repository. VisionPi
should only read state and send high-level commands through this interface.
"""


class CollarClient:
    def get_status(self):
        raise NotImplementedError

    def get_battery(self):
        raise NotImplementedError

    def set_led_mode(self, mode):
        raise NotImplementedError

    def set_expression(self, expression):
        raise NotImplementedError

    def vibrate(self, pattern=None):
        raise NotImplementedError

    def get_music_state(self):
        raise NotImplementedError
