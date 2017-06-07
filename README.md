# 231a-piano-music-identification
CS231a final project: Music Note Identification from Video
Project paper at: https://www.overleaf.com/read/zhdvfwgqwkpw

Data: Videos downloaded from Youtube using youtube-dl (usage: youtube-dl -f [format number] -o video_1 "https://www.youtube.com/watch?v=9Pk0R8OWg0k"), format number determined from running youtube-dl with flag -F and url.

Frame splitting: 

pip install ffmpy 

brew install ffmpeg --with-vpx --with-vorbis --with-libvorbis --with-vpx --with-vorbis --with-theora --with-libogg --with-libvorbis --with-gpl --with-version3 --with-nonfree --with-postproc --with-libaacplus --with-libass --with-libcelt --with-libfaac --with-libfdk-aac --with-libfreetype --with-libmp3lame --with-libopencore-amrnb --with-libopencore-amrwb --with-libopenjpeg --with-openssl --with-libopus --with-libschroedinger --with-libspeex --with-libtheora --with-libvo-aacenc --with-libvorbis --with-libvpx --with-libx264 --with-libxvid

#To manually split, given a video in command line: "ffmpeg  -r 30 -i ./videos/video_2.mp4 -qscale:v 2 -f image2 video_2-%04d.jpg"


Install OpenCV:
brew tap homebrew/science
brew install --with-contrib --with-ffmpeg --HEAD opencv

Later implementations for polishing after complete functionality achieved:
#def get_video -- let's just manually input urls for now when we want to extract a video
#If we need to include ffmpeg frame parsing in our code, here is how to do it in python: ff = ffmpy.FFmpeg(inputs={"ffmpeg -r 30 -i video_1.mp4 -f image2 video_1-%d.jpg"}, outputs={})
#We should definitely look into this to crop https://video.stackexchange.com/questions/4563/how-can-i-crop-a-video-with-ffmpeg -- Still relevant???
