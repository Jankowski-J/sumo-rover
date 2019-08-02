import threading
import time

NOOP_LAMBDA = (lambda: None)


class InputThread(threading.Thread):
    last_user_input = None
    input_callback = None
    input_prompt = ""

    def __init__(self, input_callback=None, input_prompt=""):
        threading.Thread.__init__(self)
        if input_callback is None:
            input_callback = NOOP_LAMBDA

        self.input_callback = input_callback
        self.input_prompt = input_prompt

    def run(self):
        while True:
            self.last_user_input = input(self.input_prompt)
            self.input_callback(self.last_user_input)

    def stop(self):
        self.stop()


class WasdController:
    w_callback = None
    s_callback = None
    a_callback = None
    d_callback = None
    input_thread = None

    def __init__(self, w=NOOP_LAMBDA, s=NOOP_LAMBDA, a=NOOP_LAMBDA, d=NOOP_LAMBDA):
        self.w_callback = w
        self.s_callback = s
        self.a_callback = a
        self.d_callback = d

        self.callback_dict = {
            "w": self.w_callback,
            "s": self.s_callback,
            "a": self.a_callback,
            "d": self.d_callback
        }

        self.keys = self.callback_dict.keys()

        self.input_thread = InputThread(input_callback=(lambda x: self._handle_input(x)))

    def _handle_input(self, input_string):
        first_letter = input_string.lower()
        if first_letter in self.keys:
            callback = self.callback_dict[first_letter]
            callback()

    def stop(self):
        self.input_thread.stop()

    def start(self):
        self.input_thread.start()

ctrl = WasdController()
ctrl.start()

while True:
   time.sleep(1)


