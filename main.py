import sys
import io
from PIL import Image
import ffmpeg
from pathlib import Path
import argparse

def saveToGif(images, framerate, filename):
    frames = []

    for image in images:
        frame = Image.open(io.BytesIO(image))
        frames.append(frame)

    print("Generating gif")
    frames[0].save(filename+".gif", save_all=True, append_images=frames[1:], optimize=False, duration=len(images)/framerate, loop=0)

def dumpFrames(images):
    for i in range(0, len(images)):
        print("Dumping frame n°" + str(i))
        with open("frame" + str(i) + ".jpg", "wb") as fileout:
            fileout.write(images[i])

def saveToMp4(images, framerate, filename, sound=None):

    process = None
    if sound is not None:
        audio = ffmpeg.input(sound)
        process = ffmpeg.input("pipe:", r=framerate, f="jpeg_pipe").filter("pad", "ceil(iw/2)*2", "ceil(ih/2)*2").output(audio, filename + ".mp4", vcodec="libx265", acodec="mp3").overwrite_output().run_async(pipe_stdin=True)
    else:
        process = ffmpeg.input("pipe:", r=framerate, f="jpeg_pipe").filter("pad", "ceil(iw/2)*2","ceil(ih/2)*2").output(filename + ".mp4", vcodec="libx265").overwrite_output().run_async(pipe_stdin=True)

    for image in images:
        process.stdin.write(image)

    process.stdin.close()
    process.wait()

    return

def main(args):

    file = open(sys.argv[1], "rb")

    filename = Path(sys.argv[1]).stem

    file.seek(0x0D)

    framerate = int.from_bytes(file.read(0x01), "little")
    nb_file = int.from_bytes(file.read(0x04), "little")
    print("NB Frames : " + str(nb_file))
    print("Framerate : " + str(framerate) + "fps")

    frames = []

    for i in range(0, nb_file):
        size = int.from_bytes(file.read(0x04), "little")
        data = file.read(size)
        frames.append(data)

    if args.video:
        saveToMp4(frames, framerate, filename, args.audio)
    elif args.gif:  
        saveToGif(frames, framerate, filename)
    else:
        dumpFrames(frames)


    file.close()

    return

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("AGV", help="AGV video filename")
    parser.add_argument("-a", "--audio", help="Audio filename")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--video", help="Convert video to MP4", action="store_true")
    group.add_argument("-g", "--gif", help="Convert video to gif", action="store_true")
    group.add_argument("-d", "--dump", help="Dump all video frames", action="store_true")

    args = parser.parse_args()
    main(args)