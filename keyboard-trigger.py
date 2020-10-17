import argparse  # parse arguments via command line `python script.py -a 1 -b`
import time  # time manipulation
import uuid  # UIDs manipulation
import sys  # interpreter objects

# import LSL's Stream Info and Outlet classes, data and sampling rate types
from pylsl import StreamInfo, StreamOutlet, IRREGULAR_RATE, cf_float32
from pynput import keyboard as kb  # for capturing the keyboard events


def add_arguments_get_values():
    """
    Add arguments to the command line and get the values passed.

    Returns:
        argparse.Namespace: Argument values passed.
    """
    # instanciate command line argument parser
    # also define the program as `python script.py` instead of just `script.py`
    # to improve usage description, sys.argv[0] gives you the script called
    parser = argparse.ArgumentParser(prog=f"python {sys.argv[0]}")
    # by default `python script.py -h` or `python script --help` displays:
    # usage: script.py [-h]
    #
    # optional arguments:
    #   -h, --help  show this help message and exit

    # we need to add the arguments
    # documentation: https://docs.python.org/3.8/howto/argparse.html
    parser.add_argument(
        "-e",  # short parameter
        "--event",  # long parameter
        type=str,  # value type
        choices=["press", "release"],  # define and restrict option values
        default="press",  # default parameter value if none specified
        # help text to display
        help="key event to send triggers: press (default) or release",
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
        help="trigger key for eyes opened, e.g. up, down (default), space...",
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        default="KeyboardTriggers",
        help="LSL outlet stream name: KeyboardTriggers (default)",
    )
    return parser.parse_args()


def check_key(key):
    """
    Check if key pressed/released is a char, others or ESC key.

    Parameters:
        key (pynput.keyboard.KeyCode): Key code captured.

    Returns:
        str: The key code as string if not ESC, otherwise False.
    """
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


def send_trigger(eyes_state):
    """
    Send a trigger (sample) using the LSL outlet stream created.

    The sample is a float list with the current UNIX epoch and a
    float-represented boolean (0.0 for eyes closed, 1.0 for eyes opened).

    Parameters:
        eyes_state (float): Trigger value to send (0.0 or 1.0).
    """
    # UNIX epoch (aka seconds since 01.01.1970 @ 00:00:00 UTC)
    timestamp = time.time()
    # send sample, always as a list/array, even if only 1 value is sent
    outlet.push_sample([timestamp, eyes_state])
    eyes_label = "👁 opened" if eyes_state == 1.0 else "❌ closed"
    print(f"=> Eyes status: {eyes_label}")
    print("=> Sample pushed!")


def check_target(kcode):
    """
    Check if the key code matches with one of the two key targets.
    If it matches, send the trigger.

    Parameters:
        kcode (str): Key code captured.
    """
    if kcode == eyes_opened or kcode == eyes_closed:
        # since we cannot send bool values and our stream data type is float,
        # send 0.0 as eyes closed and 1.0 as eyes open
        to_send = 1.0 if kcode == eyes_opened else 0.0  # else -> eyes closed
        send_trigger(to_send)


def key_event_answer(key):
    """
    If a key code is given, check if it is target, otherwise (ESC) quit.

    Parameters:
        key (str): Key code captured.

    Returns:
        bool: False only if key pressed/released was ESC.
    """
    if key:
        print(f"Key {action}: {key}")
        check_target(key)
    else:  # ESC pressed/released
        print(f"Key {action}: ESC")
        print("Script terminated.")
        return False


def on_press(key):
    """
    Capture key code from key press event. Then check key and give feedback.

    Parameters:
        key (pynput.keyboard.KeyCode): Key code captured.

    Returns:
        bool: False only if key pressed was ESC.
    """
    pressed = check_key(key)
    return key_event_answer(pressed)


def on_release(key):
    """
    Capture key code from key release event. Then check key and give feedback.

    Parameters:
        key (pynput.keyboard.KeyCode): Key code captured.

    Returns:
        bool: False only if key released was ESC.
    """
    released = check_key(key)
    return key_event_answer(released)


if __name__ == "__main__":
    """Flow of the script."""

    # add command line arguments and get all values passed
    args = add_arguments_get_values()
    # store each argument values
    key_event = args.event
    eyes_opened = args.opened
    eyes_closed = args.closed
    stream_name = args.name

    # display parameters
    print("Setup\n=====")
    print(f"Keyboard event: {key_event}")
    print(f"Eyes opened key: {eyes_opened}")
    print(f"Eyes closed key: {eyes_closed}\n")

    # create pressed or released label from "press" or "release"
    action = f"{key_event}ed" if key_event == "press" else f"{key_event}d"
    # generate stream UID
    UID = str(uuid.uuid4())

    # instanciate StreamInfo - more info:
    # https://labstreaminglayer.readthedocs.io/projects/liblsl/ref/streaminfo.html
    info = StreamInfo(
        name=stream_name,  # name of the stream
        type="Markers",  # stream type
        channel_count=2,  # number of values to stream
        nominal_srate=IRREGULAR_RATE,  # sampling rate in Hz or IRREGULAR_RATE
        channel_format=cf_float32,  # data type sent (dobule, float, int, str)
        source_id=UID,  # unique identifier
    )

    # display LSL outlet stream information
    print("LSL stream\n==========")
    print(f"ID: {UID}")
    print(f"Name: {stream_name}\n")

    # instanciate StreamOutlet - more info:
    # https://labstreaminglayer.readthedocs.io/projects/liblsl/ref/outlet.html
    outlet = StreamOutlet(info)
    print("LSL stream ready to push samples...\n")

    # event selected als variable
    press = on_press if key_event == "press" else None
    release = on_release if key_event == "release" else None
    # collect keyboard press/relese events
    with kb.Listener(on_press=press, on_release=release) as listener:
        listener.join()
