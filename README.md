CS231a final project: Music Note Identification from Video

Authors: Sarah Radzihovsky and Natalie Muenster

Our project paper can be found here: (https://www.overleaf.com/read/gfnnvjzbckrp)

This project is a tool that enables a user to extract notes from a chosen video of someone playing piano. This process is done in three steps: 1) Preprocessing the video, 2) locating the visible keys, and 3) mapping the pressed keys to their corresponding notes.

##Preprocessing

1. Submit your video
...* In order to use this tool, your chosen video must be downloaded and placed in the video folder of the provided data directory. If you would like to use a video from Youtube, you should download it from Youtube using youtube-dl (usage: youtube-dl -f [format number] -o video_1 "link"), format number determined from running youtube-dl with flag -F and url.

...* The closer the view in the video is to being directly overhead and parallel to the piano's keyboard, the more accurate the results will be.

NOTE: We require all submitted videos to begin with a bare keyboard of all unpressed keys and no hand occlusion. This is necessary for the keys to be located. Additionally, our tool works under the assumption that the camera is stationary for the entirety of the video.


2. Frame splitting
In order to detect the notes played, you must split the video into frames.

...* Once you have ffmpeg downloaded, to manually split a given a video (e.g. video_2.mp4), type the following into the command line: "ffmpeg  -r 30 -i ./videos/video_2.mp4 -qscale:v 2 -f image2 video_2-%04d.jpg"

3. Provide user input

The console will prompt the user to select the corners of the keyboard from the first frame in order to rectify and crop the keyboard out of the video. It will also request for the user to identify the left-most visible white-key in the video.

## Key Detection
The second step of our pipeline locates all visible white and black keys on the keyboard using images produced during preprocessing. We used the user's input of the note associated with the left-most white key to link the location of each key to its corresponding note.

## Note Detection
The played notes are determined by finding key differences in consecutive frames and mapping the locations of the detected differences in pixel intensity to the known locations of all the keys, thereby indicating which key was pressed and obtaining its corresponding note.  


## Installation

* Install Homebrew
download from [here] (https://brew.sh/)

* Install OpenCV:
brew tap homebrew/science
brew install --with-contrib --with-ffmpeg --HEAD opencv

* Install ffmpy
brew install ffmpeg --with-vpx --with-vorbis --with-libvorbis --with-vpx --with-vorbis --with-theora --with-libogg --with-libvorbis --with-g        pl --with-version3 --with-nonfree --with-postproc --with-libaacplus --with-libass --with-libcelt --with-libfaac --with-libfdk-aac --with    -lib    freetype --with-libmp3lame --with-libopencore-amrnb --with-libopencore-amrwb --with-libopenjpeg --with-openssl --with-libopus --with    -libschr    oedinger --with-libspeex --with-libtheora --with-libvo-aacenc --with-libvorbis --with-libvpx --with-libx264 --with-libxvid
