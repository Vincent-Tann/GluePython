import serial

class Arduino:
    def __init__(self) -> None:
        self.port=serial.Serial(port='COM4')

    def detect_object_for_camera(self):
        return 1
    def quality_check(self):
        return 1