# Simpsons TV

## Resources

Generally followed https://www.instructables.com/The-Simpsons-TV-35-Screen-Version/ as it's a newer update to the original post https://withrow.io/simpsons-tv-build-guide-waveshare

## Hardware

* Raspberry PI Zero
* Waveshare 4in HDMI display
  * https://www.waveshare.com/4inch-hdmi-lcd.htm
  * https://www.waveshare.com/wiki/4inch_HDMI_LCD

## Setup

### Raspian Installation

Based setup on Step 16 in https://www.instructables.com/The-Simpsons-TV-35-Screen-Version/ with the following notes:

1. Chose “Operating System” -> “Raspberry Pi OS (other)” -> “Raspberry Pi OS Lite (32-bit)” ("A port of Debian Trixie with no desktop environment")

### Raspian Setup

After installing the OS on the SD card, do the following (all of my versions of the files are in this github project):
1. Edit `cmdline.txt`:
  1. Add `video=HDMI-A-1:480x800m,margin_top=28,margin_bottom=-28,panel_orientation=left_side_up` to the beginning of the line.
    1. `panel_orientation` is the magic here to get the Waveshare display to rotate. (The relevant source code is https://github.com/raspberrypi/linux/blob/7c7adad3f457db10d347d5443a325d7c7a0a8253/drivers/gpu/drm/drm_modes.c#L2115)
    1. `margin_*` shifts the position of the display. The default position was too far to the right (toward the knobs), so after some trial and error, I found I could put in a negative offset as long as I did the same positive offset on the opposite side. **Note:** The top/bottom/left/right refers to the unrotated end of the display; in my case, `margin_top` is the right side and that's where I applied the offsets
1. No changes required for `config.txt`
  1. Compared [Brandon Winrow's Guide](http://www.withrow.io/simpsons-tv-build-guide), this Waveshare display doesn't use pin 18, so the remapping isn't required
  1. Changing the GPIO mode wasn't required to get sound to work **TODO* Actually, maybe it is since the latest copy had `dtoverlay=audremap,enable_jack,pins_18_19`

### First Boot and More Setup

1. `sudo apt-get update` and `sudo apt-get upgrade`
1. `sshd` fix if using Unifi access points:
  1. Add `IPQoS cs0` to end of `/etc/ssh/sshd_config` (https://forums.unraid.net/topic/189241-unraid-7-unable-to-add-sshd-settings-ipqos-0x00/)
    1. `sudo nano /etc/ssh/sshd_config`
    1. Verify syntax: `sudo ssdh -t` - you shouldn't see any output if everything is OK
    1. `sudo systemctl restart sshd`
1. Enable auto-login
  1. `sudo raspi-config` **TODO**
1. Install `mpv`
  1. `sudo apt-get install mpv`


### Media Player

`omxplayer` isn't available anymore, so after evaluating `vlc` and `mplayer`, I settled on `mpv` because I was able to get it to work.

#### Auto-play script

mpv extension

#### On-screen menu

TBD

### Touch Screen

Followed instruction from https://www.waveshare.com/wiki/4inch_HDMI_LCD where I copied over waveshare-ads7846.dtbo and added their line to config.txt, but couldn't get the x/y axis corrected. Switched to ads7846.dtbo since it appears to be built into the kernel and now I wonder if the waveshare-ads7846.dtbo is obsolete but waveshare hasn't updated their documentation.

1. Touch calibration
  1. `sudo apt-get install evtest`
  1. `sudo evtest`
  1. look for the x,y values and see if the axis are pointing the correct way with 0,0 being upper left
  1. Found that I needed to comment out the x,y min,max overrides in config.txt before doing the calibration

==> Didn't get to the point of being able to get mpv to recognize touch commands. Moved on.

### Read-Only FS

Enable:
1. Used raspi-config->

Disable:
1. Disable overlayfs: `sudo raspi-config nonint disable_overlayfs`, then reboot
1. Remount / as rw: 


### Boot splash

`sudo apt-get install rpd-plym-splash` (this installs the 'pix' theme that other posts refer to and that raspi-config is expecting when you try to enable the boot splash screen and it also runs the `update-initramfs` command)

https://www.raspberrypi.com/documentation/computers/configuration.html#custom-fullscreen-splash-image

# Other Tips or Useful Commands

* `killall mpv`



All of this is bullshit

Updated to latest raspian (Trixie)

`export DISPLAY=:0`
`vlc S02E03.mp4`
still rotated

magic command:
ffplay -codec:v h264_v4l2m2m -vf "transpose=2"  S02E03.mp4
Even better: 
 mpv --hwdec=v4l2m2m-copy --video-rotate=270 S02E03.mp4

cmdline attempts:
1. **working** video=HDMI-A-1:480x800M,rotate=90 console=serial0,115200 console=tty1 root=PARTUUID=e346e44a-02 rootfstype=ext4 fsck.repair=yes rootwait cfg80211.ieee80211_regdom=US
1. **panel_orientation** 
   1. https://github.com/raspberrypi/linux/blob/7c7adad3f457db10d347d5443a325d7c7a0a8253/drivers/gpu/drm/drm_modes.c#L2115

offset the screen: you can use negative offsets as long as you have the same positive offset on the opposite side
even though the screen is rotated, "top" still refers to the unrotated top of the display




# Configuring Certificate-based SSH