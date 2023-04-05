from pynput.keyboard import Key
import bin.KeyboardMgr as Kb
import bin.Sequencer as Seq

kb = Kb.KBEventListener()
seq = Seq.Sequencer()

# main loop
while True:
    kb_event = kb.get_event()
    if type(kb_event) == Key and kb_event == Key.esc:
        break
    kb.clear_event()
    seq.call(kb_event)
