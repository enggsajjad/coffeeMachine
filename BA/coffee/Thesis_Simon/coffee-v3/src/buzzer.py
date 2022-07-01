import time
from gpiozero import Device, TonalBuzzer
from gpiozero.tones import Tone
import logging
import midi

from util import Msg, receive_cmd_block, receive_cmd

LOG = logging.getLogger(__name__)

BCM_PIN = 3
notes_r2d2 = ['A4', 'G4', 'E4', 'C4', 'D4', 'B4', 'F4', 'C5', 'A4', 'G4', 'E4', 'C4', 'D4', 'B4', 'F4', 'C5']

def hello():
    b = TonalBuzzer(BCM_PIN, mid_tone=Tone("A3"), octaves=3)
    LOG.debug("playing hello")
    b.play(Tone('C2'))
    time.sleep(0.2)
    b.play(Tone('C4'))
    time.sleep(0.2)
    b.stop()

def r2d2():
    b = TonalBuzzer(BCM_PIN, mid_tone=Tone("A3"), octaves=3)
    for note in notes_r2d2:
        b.play(Tone(note))
        time.sleep(0.1)

def buzz():
    b = TonalBuzzer(BCM_PIN, mid_tone=Tone("A3"), octaves=3)
    LOG.debug("playing buzz")
    b.play("A3")
    time.sleep(1)
    b.stop()


def bye():
    b = TonalBuzzer(BCM_PIN, mid_tone=Tone("A3"), octaves=3)
    b.play(Tone('C4'))
    time.sleep(0.2)
    b.play(Tone('C2'))
    time.sleep(0.2)
    b.stop()

def siren():
    b = TonalBuzzer(BCM_PIN, mid_tone=Tone("A3"), octaves=3)
    for _ in range(3):
        b.play(Tone('C5'))
        time.sleep(0.5)
        b.play(Tone('B3'))
        time.sleep(0.5)
    b.stop()

def swell():
    b = TonalBuzzer(BCM_PIN, mid_tone=Tone("A3"), octaves=3)
    b.value = -1
    while b.value < 0.7:
        b.value = b.value + 0.01
        time.sleep(0.005)

    time.sleep(0.2)
    b.stop()

def run(conn):
    """Setup buzzer, controlled by commands sent through connection"""
    bind = {
        Msg.CMD_UNLOCK: hello,
        Msg.CMD_LOCK: bye,
        Msg.CMD_BUZZ: lambda: play_from_midi("res/ThemeA.mid", 2)
    }

    LOG.debug("Buzzer started")
    swell()

    while True:
        receive_cmd_block(conn, bind=bind)

def play_from_midi(file, track):
    pattern = midi.read_midifile(file)

    second_per_tick = 0
    for event in pattern[0]:
        if type(event) == midi.SetTempoEvent:
            second_per_tick = event.get_mpqn() / event.get_bpm() / 1000000

    b = TonalBuzzer(BCM_PIN, mid_tone=Tone("A3"), octaves=3)
    for event in pattern[track]:
        print(event)
        if type(event) == midi.NoteOnEvent:
            time.sleep(event.tick * second_per_tick)
            if event.data[1] > 0:
                b.play(Tone.from_midi(event.data[0]))
            else:
                b.stop()
            


if __name__ == "__main__":
    play_from_midi("res/ThemeA.mid", 2)
    # play_from_midi("res/ThemeII.mid", 3)
    # buzz()
    # time.sleep(1)
    #     # hello()
    #     # time.sleep(1)
    #     # bye()
    #     # time.sleep(1)
    # r2d2()
    # time.sleep(1)
    # siren()
    # #    time.sleep(1)
    #    swell()
