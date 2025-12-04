# Simpsons TV

## Resources

Generally followed https://www.instructables.com/The-Simpsons-TV-35-Screen-Version/ as it's a newer update to the original post https://withrow.io/simpsons-tv-build-guide-waveshare

## Hardware

* Raspberry PI Zero
* Waveshare 4in HDMI display
  * https://www.waveshare.com/4inch-hdmi-lcd.htm
  * https://www.waveshare.com/wiki/4inch_HDMI_LCD

## Setup

### Raspian

Based setup on Step 16 in https://www.instructables.com/The-Simpsons-TV-35-Screen-Version/ with the following notes:

1. Chose “Operating System” -> “Raspberry Pi OS (other)” -> “Raspberry Pi OS Lite (Legacy)” but didn't get an option to pick a version. I ended up with **bookworm**
   1. 

### Media Player

omxplayer isn't included in bookworm and according to the internet, Raspian has moved to mplayer. Also according to the internet, mpv is also an option. After a very short experimentation, I opted to use mpv because I didn't have to change from text mode to GUI mode.

The prebuilt mpv doesn't appear to have hardware acceleration support, so I had to build it myself:

#### Building mpv

Remove prebuilt one to keep things clean:
1. sudo apt-get remove mpv

Starting guide: https://nwgat.ninja/quick-easy-compiling-mpv-for-raspberry-pi/

Also had to add these package:
1. sudo apt install meson ninja-build
1. sudo apt-get install libharfbuzz-dev
1. sudo apt-get install libx264-dev

Switched from --enable-mmal to --enable-x264 for ffmpeg

1. sudo apt-get install libcamera-apps-lite
   * Required for `--enable-mmal`




All of this is bullshit

Updated to latest raspian (Trixie)

`export DISPLAY=:0`
`vlc S02E03.mp4`
still rotated

magic command:
ffplay -codec:v h264_v4l2m2m -vf "transpose=2"  S02E03.mp4
Even better: 
 mpv --hwdec=v4l2m2m-copy --video-rotate=270 S02E03.mp4

cmdline attemps:
1. **working** video=HDMI-A-1:480x800M,rotate=90 console=serial0,115200 console=tty1 root=PARTUUID=e346e44a-02 rootfstype=ext4 fsck.repair=yes rootwait cfg80211.ieee80211_regdom=US
1. **panel_orientation** 
   1. https://github.com/raspberrypi/linux/blob/7c7adad3f457db10d347d5443a325d7c7a0a8253/drivers/gpu/drm/drm_modes.c#L2115