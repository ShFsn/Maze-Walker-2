from pynput.keyboard import Key, Listener


class KBEventListener:
    def __init__(self):
        self._event = ''
        self._pressed = False
        # Collect events until released
        # noinspection PyTypeChecker
        self._listener = Listener(on_press=self._on_press, on_release=self._on_release)
        self._listener.start()

    def _on_press(self, key):
        # print('{0} pressed'.format(key))
        if not self._pressed:
            if type(key) == Key:
                self._event = key
            else:
                self._event = key.char
            self._pressed = True

    def _on_release(self, key):
        # print('{0} release'.format(key))
        if key == Key.esc:
            # Stop listener
            self._listener.stop()
        self._pressed = False

    def get_event(self):
        return self._event

    def clear_event(self):
        self._event = ''
