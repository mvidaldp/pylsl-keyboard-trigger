# pylsl-keyboard-trigger
![keyboard-trigger](https://github.com/mvidaldp/pylsl-keyboard-trigger/raw/main/keyboard-trigger_demo.gif)

Python script that sends LSL markers (aka triggers) over the local network by pressing or releasing any of the two target keyboard keys.

In this specific script, since it's meant for an EEG eyes open/closed experimental task, one target key press/release is for indicating when the eyes are opened and the other for when they're closed. By default (no parameters specified), the selected event is `press` and the keys are `up` (eyes open) and `down` (eyes closed). 

The keyboard event to capture (press or release), and also the target keys can be customized by passing arguments on the script call:
```
usage: python keyboard-trigger.py [-h] [-e {press,release}] [-o OPENED] [-c CLOSED]

optional arguments:
  -h, --help            show this help message and exit
  -e {press,release}, --event {press,release}
                        key event to send triggers: press (default) or release
  -o OPENED, --opened OPENED
                        trigger key for eyes opened, e.g. up (default), down, space...
  -c CLOSED, --closed CLOSED
                        trigger key for eyes opened, e.g. up, down (default), space...
```

This repo also includes a 30-seconds streams recording example where UNIX epochs with eyes-closed/opened(0/1) samples were stored, simulatneously with EEG data streamed from an Android app. Moreover, a basic notebook for how to read the recording is included.

__Contents__
- `keyboard-trigger.py`: keyboard-trigger events via target key press/release event (non-target keys also captured).
- `howto_read_XDF_recordings.ipynb`: recording example with simultaneous streams from a mobile EEG Android App and a Python script sending keyboard triggers.
- `eeg_plus_triggers.xdf`: Jupyter notebook demonstrating how to read LSL streams from XDF recordings.

__How to run it:__

0. Install the LSL library: [liblsl](https://github.com/sccn/liblsl/releases/latest)
1. Install the Python dependencies: `pip install -r requirements.txt`
2. Download, install and run the [LSL LabRecorder](https://github.com/labstreaminglayer/App-LabRecorder/releases/latest)
3. Run the `keyboard-trigger.py` script by: `python keyboard-trigger.py` (run `stty -echo` before calling the script to avoid the keyboard input to be shown between the script output)

![LabRecorder](https://github.com/mvidaldp/pylsl-keyboard-trigger/raw/main/labrecorder.png)

4. Make sure the stream `KeyboardTrigger` appears on the LabRecorder (otherwise click `Update`), selected it (check it), and click `Start`.
5. Press any of the target keys to send a trigger. Press the ESC key to stop streaming and also to stop the script.
6. Click `Stop` on the LabRecorder.

__How to read XDF recordings (example)__ 
  - Offline: [howto_read_XDF_recordings.ipynb](https://github.com/mvidaldp/pylsl-keyboard-trigger/blob/main/howto_read_XDF_recordings.ipynb)
  - Online: Open `howto_read_XDF_recordings.ipynb` with your Jupyter notebook client to visualize or run the cells.
  
__Recorded data visualization__
![data-visualization](https://github.com/mvidaldp/pylsl-keyboard-trigger/raw/main/recording_visualization.png)
  
