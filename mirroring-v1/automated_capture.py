import subprocess
import time

# Start "scrcpy" in one subprocess
scrcpy_process = subprocess.Popen(["scrcpy", "--record", "myrecording.mp4"])

# Wait for "scrcpy" to initialize and start mirroring (you can adjust the delay as needed)
time.sleep(5)

# Start the OCR script in another subprocess
ocr_process = subprocess.Popen(["python", "extract-from-stream.py"])

# Wait for both processes to complete
scrcpy_process.wait()
ocr_process.wait()
