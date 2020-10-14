import argparse  # parse arguments via command line "python script.py -a 1 2"
import time  # for storing time
import uuid  # to generate UIDs

# import LSL's Stream Info and Outlet classes, data and sampling rate types
from pylsl import StreamInfo, StreamOutlet, IRREGULAR_RATE, cf_float32
from pynput import keyboard as kb  # for capturing the keyboard events

# instanciate command line argument parser
parser = argparse.ArgumentParser()
# by default `python script.py -h` or `python script --help` displays:
# usage: script.py [-h]
#
# optional arguments:
#   -h, --help  show this help message and exit

# we need to add the arguments we need
# documentation: https://docs.python.org/3.8/howto/argparse.html
parser.add_argument(
    "-e",  # short parameter
    "--event",  # long parameter
    type=str,  # value type
    choices=["press", "release"],  # option values (enforced)
    default="press",  # default parameter value if none specified
    help="key event to send triggers: press (default) or release",  # help text
)
parser.add_argument(
    "-o",
    "--opened",
    type=str,
    default="up",
    help="trigger key for eyes opened, e.g. up (default), down, space...",
)
parser.add_argument(
    "-c",
    "--closed",
    type=str,
    default="down",
    help="trigger key for eyes opened, e.g. up, down (default), space...)",
)

# parse added arguments/paramenters
args = parser.parse_args()
# get argument values passed
key_event = args.event
eyes_opened = args.opened
eyes_closed = args.closed
# display them
print("Parameters\n==========")
print(f"Keyboard event: {key_event}")
print(f"Eyes opened key: {eyes_opened}")
print(f"Eyes closed key: {eyes_closed}\n")

# generate UID and display it
UID = str(uuid.uuid1())
print(f"Session ID: {UID}\n")

# instanciate StreamInfo - more info:
# https://labstreaminglayer.readthedocs.io/projects/liblsl/ref/streaminfo.html
info = StreamInfo(
    name="KeyboardTriggers",  # name of the stream
    type="Markers",  # stream type
    channel_count=2,  # number of values to stream
    nominal_srate=IRREGULAR_RATE,  # sampling rate in Hz or IRREGULAR_RATE
    channel_format=cf_float32,  # data type sent (dobule, float, int, string)
    source_id=UID,  # unique identifier
)

# instanciate StreamOutlet - more info:
# https://labstreaminglayer.readthedocs.io/projects/liblsl/ref/outlet.html
outlet = StreamOutlet(info)
print("LSL stream ready to push samples...")


# push a sample into the stream
def send_trigger(eyes_state):
    # store UNIX timestamp (aka seconds since 01.01.1970 @ 00:00:00 UTC)
    timestamp = time.time()
    # send sample, always as a list/array, even if only 1 value is sent
    outlet.push_sample([timestamp, eyes_state])
    eyes_label = "👁 opened" if eyes_state == 1.0 else "❌ closed"
    print(f"Eyes status: {eyes_label}")
    print("Sample pushed!")


# check if key pressed/released is a char or others and return it
def check_key(key):
    checked = None
    try:
        checked = key.char
    except AttributeError:
        # not a char, then remove Key. from e.g. Key.up
        checked = key
        checked = str(checked).split(".")[1]
    if checked != "esc":
        return checked
    else:  # ESC key pressed, aka keyboard.Key.esc
        # stop listener, also stop pushing samples
        return False  # leave


# check if any of the keys pressed is one of the two targets (opened, closed)
# if so, send trigger
def check_target(target):
    if target == eyes_opened or target == eyes_closed:
        # since we cannot send bool values and our stream data type is float,
        # send 0.0 as eyes closed and 1.0 as eyes open
        to_send = 1.0 if target == eyes_opened else 0.0  # else -> eyes closed
        send_trigger(to_send)


# capture key pressed from key press event and push sample
def on_press(key):
    pressed = check_key(key)
    if pressed:
        print(f"Key pressed: {pressed}")
        check_target(pressed)
    else:  # ESC pressed
        print("Key pressed: ESC")
        print("Script terminated.")
        return False


# capture key released from key release event and push sample
def on_release(key):
    released = check_key(key)
    if released:
        print(f"Key pressed: {released}")
        check_target(released)
    else:  # ESC released
        print("Key released: ESC")
        print("Script terminated.")
        return False


if key_event == "press":
    # collect keyboard press events
    with kb.Listener(on_press=on_press, supress=True) as listener:
        listener.join()
else:  # or elif key_event == "release":
    # collect keyboard release events
    with kb.Listener(on_release=on_release) as listener:
        listener.join()
