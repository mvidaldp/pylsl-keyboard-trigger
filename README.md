# pylsl-keyboard-trigger

![keyboard-trigger](https://github.com/mvidaldp/pylsl-keyboard-trigger/raw/main/keyboard-trigger_demo.gif)

Python script that sends LSL markers (aka triggers) over the local network by pressing or releasing any of the two target keyboard keys.

In this specific script, meant for EEG eyes open/closed experimental tasks, one target key press/release indicates when the eyes are opened and the other for when they're closed. By default (no parameters specified), the selected event is `press`, the keys are `up` (eyes open) and `down` (eyes closed), and the LSL stream name is `KeyboardTriggers`.

The keyboard event to capture (press or release), the target keys, and the stream name can be customized by passing arguments on the script call:

```man
usage: python keyboard-trigger.py [-h] [-e {press,release}] [-o OPENED] [-c CLOSED] [-n NAME]

optional arguments:
  -h, --help            show this help message and exit
  -e {press,release}, --event {press,release}
                        key event to send triggers: press (default) or release
  -o OPENED, --opened OPENED
                        trigger key for eyes opened, e.g. up (default), down, space...
  -c CLOSED, --closed CLOSED
                        trigger key for eyes opened, e.g. up, down (default), space...
  -n NAME, --name NAME  LSL outlet stream name: KeyboardTriggers (default)
```

This repo also includes a 30-seconds stream recording example where UNIX epochs with eyes-closed/opened(0/1) samples were stored, simultaneously with EEG data streamed from an Android app. Moreover, a basic notebook for how to read the recording is included.

## Contents

- `keyboard-trigger.py`: keyboard-trigger events via target key press/release event (non-target keys also captured).
- `howto_read_XDF_recordings.ipynb`: recording example with simultaneous streams from a mobile EEG Android App and a Python script sending keyboard triggers.
- `eeg_plus_triggers.xdf`: Jupyter notebook demonstrating how to read LSL streams from XDF recordings.

## How to run it

![LabRecorder](https://github.com/mvidaldp/pylsl-keyboard-trigger/raw/main/labrecorder.png)

0. Install the LSL library: [liblsl](https://github.com/sccn/liblsl/releases/latest)
1. Install the Python dependencies: `pip install -r requirements.txt`
2. Download, install and run the [LSL LabRecorder](https://github.com/labstreaminglayer/App-LabRecorder/releases/latest)
3. Run the `keyboard-trigger.py` script by: `python keyboard-trigger.py` (run `stty -echo` before calling the script to avoid the keyboard input shown between the script output)

4. Make sure the stream `KeyboardTrigger` appears on the LabRecorder (otherwise click `Update`), selected it (check it), and click `Start`.
5. Press any of the target keys to send a trigger. Press the ESC key to stop streaming and also to stop the script.
6. Click `Stop` on the LabRecorder.

## How to read XDF recordings (example)

- Offline: [howto_read_XDF_recordings.ipynb](https://github.com/mvidaldp/pylsl-keyboard-trigger/blob/main/howto_read_XDF_recordings.ipynb)
- Online: Open `howto_read_XDF_recordings.ipynb` with your Jupyter notebook client to visualize or run the cells.
  
__Recorded data visualization (EEG data + triggers)__
![data-visualization](https://github.com/mvidaldp/pylsl-keyboard-trigger/raw/main/recording_visualization.png)
