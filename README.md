# 231a-piano-music-identification
CS231a final project: Music Note Identification from Video

Data: Videos downloaded from Youtube using youtube-dl (usage: youtube-dl -f [format number] -o video_1 "https://www.youtube.com/watch?v=9Pk0R8OWg0k"), format number determined from running youtube-dl with flag -F and url.

Frame splitting: 

pip install ffmpy 

brew install ffmpeg --with-vpx --with-vorbis --with-libvorbis --with-vpx --with-vorbis --with-theora --with-libogg --with-libvorbis --with-gpl --with-version3 --with-nonfree --with-postproc --with-libaacplus --with-libass --with-libcelt --with-libfaac --with-libfdk-aac --with-libfreetype --with-libmp3lame --with-libopencore-amrnb --with-libopencore-amrwb --with-libopenjpeg --with-openssl --with-libopus --with-libschroedinger --with-libspeex --with-libtheora --with-libvo-aacenc --with-libvorbis --with-libvpx --with-libx264 --with-libxvid

Install OpenCV:
brew tap homebrew/science
brew install --with-contrib --with-ffmpeg --HEAD opencv