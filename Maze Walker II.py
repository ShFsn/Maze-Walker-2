from pynput.keyboard import Key
from bin.KeyboardMgr import KBEventListener
from bin.Sequencer import Sequencer

kb = KBEventListener()
seq = Sequencer()

# main loop
while True:
    kb_event = kb.get_event()
    if type(kb_event) == Key and kb_event == Key.esc:
        break
    kb.clear_event()
    seq.call(kb_event)
