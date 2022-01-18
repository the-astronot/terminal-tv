#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/opencv_modules.hpp>
#include <opencv2/video.hpp>
#include <opencv2/videoio.hpp>
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;
using namespace cv;
using namespace std;

int main(int argc, char** argv) 
{
	string pwd = fs::current_path();
	string filename =  pwd + "/videos/Scooby_Doo_S01E01.mkv";
	cout << filename << endl;

	if (fs::exists(filename)) {
		cout << "FILE EXISTS" << endl;
	}

	// Read the video 
  VideoCapture cap(filename); 

  // if not success, exit program
  if (cap.isOpened() == false)  {
    cout << "Cannot open the video file" << endl;
    return 1;
  }

  //Uncomment the following line if you want to start the video in the middle
  //cap.set(CAP_PROP_POS_MSEC, 300); 

  //get the frames rate of the video
  double fps = cap.get(CAP_PROP_FPS); 
  cout << "Frames per seconds : " << fps << endl;

  return 0; 
}