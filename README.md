# pylsl-keyboard-trigger
Very simple Python script to send LSL markers (aka triggers) over the local network by pressing any keyboard key. It also includes a recording example, and how to read the recording.

__Contents__
- `keyboard-trigger.py`: keyboard-trigger events via key press event (key release also captured).
- `recording_test.xdf`: XDF recording of LSL streams. 
- `read_XDF_example.ipynb`: Jupyter notebook demonstrating how to read LSL streams from XDF recordings.

__How to run it:__
0. Install the LSL library: [liblsl](https://github.com/sccn/liblsl/releases/latest)
1. Install the Python dependencies: `pip install -r requirements.txt`
2. Download, install and run the [LSL LabRecorder](https://github.com/labstreaminglayer/App-LabRecorder/releases/latest)
3. Run the `keyboard-trigger.py` script by: `python keyboard-trigger.py`

![LabRecorder](https://github.com/mvidaldp/pylsl-keyboard-trigger/raw/main/labrecorder.png)

4. Make sure the stream `KeyboardTrigger` appears on the LabRecorder (otherwise click `Update`), selected it (check it), and click `Start`.
5. Press any key to send a trigger. Press the ESC key to stop streaming and also to stop the script.
6. Click `Stop` on the LabRecorder.

__How to read XDF recordings (example)__ 
  - Offline: [read_XDF_example.ipynb](https://github.com/mvidaldp/pylsl-keyboard-trigger/blob/main/read_XDF_example.ipynb)
  - Online: Open `read_XDF_example.ipynb` with your Jupyter notebook client to visualize or run the cells.
  
