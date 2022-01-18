mkdir build
git clone https://github.com/opencv/opencv.git
cd build
sudo apt-get install ffmpeg
cmake -D WITH_FFMPEG=ON ../opencv
make
sudo make install