from reprint import output
from inputs import get_gamepad
import math
import threading
import time


class ControllerState(object):
    def __init__(self):
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

    def __str__(self) -> str:
        return (
            f"Left.X: {round(self.LeftJoystickX, 4)} Left.Y: {round(self.LeftJoystickY, 4)}\n"
            f"Right.X: {round(self.RightJoystickX, 4)} Right.Y: {round(self.RightJoystickY, 4)}\n"
            f"L Trigger: {round(self.LeftTrigger, 4)} R Trigger: {round(self.RightTrigger, 4)}"
        )


class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):
        self.state = ControllerState()

        self._monitor_thread = threading.Thread(
            target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def read(self):  # return the buttons/triggers that you care about in this method
        return self.state

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.state.LeftJoystickY = event.state / \
                        XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.state.LeftJoystickX = event.state / \
                        XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.state.RightJoystickY = event.state / \
                        XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.state.RightJoystickX = event.state / \
                        XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.state.LeftTrigger = event.state / \
                        XboxController.MAX_TRIG_VAL  # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.state.RightTrigger = event.state / \
                        XboxController.MAX_TRIG_VAL  # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.state.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.state.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.state.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.state.X = event.state
                elif event.code == 'BTN_WEST':
                    self.state.Y = event.state
                elif event.code == 'BTN_EAST':
                    self.state.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.state.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.state.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.state.Back = event.state
                elif event.code == 'BTN_START':
                    self.state.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.state.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.state.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.state.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.state.DownDPad = event.state


TICK_DELAY = 0.05

if __name__ == '__main__':
    joy = XboxController()
    print("Hello world?")
    with output(output_type='list', initial_len=3) as output_lines:
        while True:
            time.sleep(TICK_DELAY)
            controller_state = joy.read()
            output_lines[0] = f"Left.X: {round(controller_state.LeftJoystickX, 4)} Left.Y: {round(controller_state.LeftJoystickY, 4)}"
            output_lines[1] = f"Right.X: {round(controller_state.RightJoystickX, 4)} Right.Y: {round(controller_state.RightJoystickY, 4)}"
            output_lines[2] = f"L Trigger: {round(controller_state.LeftTrigger, 4)} R Trigger: {round(controller_state.RightTrigger, 4)}"
