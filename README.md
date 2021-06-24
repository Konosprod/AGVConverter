# AGVConverter
Convert AGV files to mp4 or gif, or just dump the frames

## Needed

* ffmpeg-python
* pillow

## How to use
```
usage: main.py [-h] [-a AUDIO] [-v | -g | -d] AGV

positional arguments:
  AGV                   AGV video filename

optional arguments:
  -h, --help            show this help message and exit
  -a AUDIO, --audio AUDIO
                        Audio filename
  -v, --video           Convert video to MP4
  -g, --gif             Convert video to gif
  -d, --dump            Dump all video frames
  ```` 
