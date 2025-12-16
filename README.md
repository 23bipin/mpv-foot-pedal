# Linux Foot Pedal Controller for mpv

Control mpv playback using a USB foot pedal on Linux.
Works on GNOME / Wayland and does not require mpv to be focused.

This project is designed to be **hardware-agnostic** and works with
any USB foot pedal that appears as a Linux input device
(keyboard, mouse buttons, or HID).

---

## Features
- Left pedal: rewind audio/video by 0.5 seconds
- Middle pedal: play / pause
- Right pedal: forward audio/video by 0.5 seconds
- Works even when mpv is not the active window
- Wayland-safe (no global key injection)
- Simple, single-file Python daemon

---

## Requirements
- Linux
- Python 3
- mpv
- python-evdev

### Debian / Ubuntu
```bash
apt install mpv python3-evdev

---

## Usage

Start mpv with IPC enabled:
```bash
mpv --no-input-terminal --force-window=yes \
    --input-ipc-server=/tmp/mpvsocket mediafile.mp3

Run the daemon:
```bash
python3 pedal_mpv_daemon.py
