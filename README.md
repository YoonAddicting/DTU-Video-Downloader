# DTU-Video-Downloader
Python script for downloading videos on video.dtu.dk

## Prerequisites
* Python 3.6+ (Tested on Python 3.8)
  * [Selenium](https://pypi.org/project/selenium/)
  * [youtube_dl](https://pypi.org/project/youtube_dl/)
* Login for DTU Video (DTU Inside)
* Chrome installed on your computer

## Initial setup
1. Download the latest release from the [releases tab](https://github.com/YoonAddicting/DTU-Video-Downloader/releases).
2. Download the corrosponding version of the chromedriver from https://chromedriver.chromium.org/downloads for your Chrome version and your operating system.
3. Place the above file in the same folder as the *main.py* file.

## Usage
Run the program by running the *main.py* file, enter your login details as described and paste the url of the video or the category you wish to download, and let the program do it's magic.

## Examples on links
Single video: 
```
https://video.dtu.dk/media/Matematik+1+-+Hold+B+Uge+1+Del+1/0_2pxlej2l/241155
```

Category of videos (Eg. entire course):
```
https://video.dtu.dk/category/Courses%3E01+Department+of+Applied+Mathematics+and+Computer+Science%3E01005+Matematik+1%3EE19_F20%3ESkema+B/241155
```
