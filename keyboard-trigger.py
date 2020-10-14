# import LSL's Stream Info and Outlet classes, data and sampling rate types
from pylsl import StreamInfo, StreamOutlet, IRREGULAR_RATE, cf_float32
from pynput import keyboard  # for capturing the keyboard events
import time  # for storing time
import uuid  # to generate UIDs

# generate UID and display it
UID = str(uuid.uuid1())
print(f"Session ID: {UID}")

# instanciate StreamInfo - more info:
# https://labstreaminglayer.readthedocs.io/projects/liblsl/ref/streaminfo.html
info = StreamInfo(
    name="KeyboardTriggers",  # name of the stream
    type="Markers",  # stream type
    channel_count=1,  # number of values
    nominal_srate=IRREGULAR_RATE,  # sampling rate in Hz or IRREGULAR_RATE
    channel_format=cf_float32,  # data type sent (dobule, float, int, string)
    source_id=UID,  # unique identifier
)

# instanciate StreamOutlet - more info:
# https://labstreaminglayer.readthedocs.io/projects/liblsl/ref/outlet.html
outlet = StreamOutlet(info)
print("LSL stream ready to push samples...")


# push a sample into the stream
def send_trigger():
    # store UNIX timestamp (aka seconds since 01.01.1970 @ 00:00 UTC)
    timestamp = time.time()
    outlet.push_sample([timestamp])  # send sample, always as a list/array
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
    return checked


# capture key pressed from key press event and push sample
def on_press(key):
    pressed = check_key(key)
    print(f"Key pressed: {pressed}")
    send_trigger()


# capture key released from key release event and push sample
def on_release(key):
    released = check_key(key)
    print(f"Key released: {released}")
    if released == "esc":  # on ESC key pressed, aka keyboard.Key.esc
        # stop listener, also stop pushing samples
        return False  # leave


# collect keyboard press and release events
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
