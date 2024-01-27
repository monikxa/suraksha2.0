# suraksha2.0


# Install dependencies first
------------------------

On Debian based Linux OS

Recommended Ubuntu 22.04

```console
sudo apt install pip
```

```console
pip install cmake

```
Add the executable path to PATH
```console
export PATH=$PATH:/home/mukhtar/.local/bin
```

```console
pip install numpy

pip install dlib

pip install face_recognition

pip install opencv-python


```

Stored in directory: /home/mukhtar/.cache/pip/wheels/9b/e2/80/888fdc098db86b463ff0c83ae5e5ca151889e901bc1e9a3a11


# Run the program

```console

python3 TeamSuraksha.py find_person --name "Taylor Swift"

```



To run this code, you need:

1. Python installed on your system.
2. Required libraries installed, including:
   - argparse: For parsing command-line arguments.
   - `face_recognition`: For facial recognition tasks.
   - cv2 (OpenCV): For handling video capture, processing, and displaying frames.
3. A video file named "vid.mp4" in the same directory as the script (or you can adjust the `video_path` variable to point to the correct location of your video file).
4. Facial data entries added to the FacialDatabase instance in the main function. You can modify this as needed for your application.
5. Proper usage of command-line arguments when executing the script, as described in the argparse configuration.
