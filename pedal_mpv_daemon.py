#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2025 23bipin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import socket
from evdev import InputDevice, ecodes, list_devices

MPV_SOCKET = "/tmp/mpvsocket"
DEVICE_NAME = "Your Pedal Device Name"  # change this to your pedal's device name (grep -A6 -B2 -i "input" /proc/bus/input/devices)


BACK_SEC = 0.5
FWD_SEC = 0.5
GRAB_DEVICE = True  # prevents the pedal clicks affecting other apps

LEFT = ecodes.BTN_LEFT
MIDDLE = ecodes.BTN_MIDDLE
RIGHT = ecodes.BTN_RIGHT


def mpv(cmd, *args):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(MPV_SOCKET)
    s.sendall((json.dumps({"command": [cmd, *args]}) + "\n").encode("utf-8"))
    s.close()


def find_pedal():
    for path in list_devices():
        dev = InputDevice(path)
        if dev.name == DEVICE_NAME:
            return dev
    return None


def main():
    dev = find_pedal()
    if not dev:
        raise SystemExit(f"Could not find device named: {DEVICE_NAME}\n"
                         f"Hint: check /proc/bus/input/devices for the Handlers=eventX line.")

    if GRAB_DEVICE:
        try:
            dev.grab()
        except Exception as e:
            print(f"[WARN] Could not grab device (continuing): {e}")

    print(f"[OK] Using: {dev.path} ({dev.name})")
    print(f"[OK] Left: -{BACK_SEC}s | Middle: play/pause | Right: +{FWD_SEC}s")

    for event in dev.read_loop():
        if event.type != ecodes.EV_KEY:
            continue
        if event.value != 1:  # act only on press-down
            continue

        try:
            if event.code == LEFT:
                mpv("seek", -BACK_SEC, "relative")
            elif event.code == RIGHT:
                mpv("seek", FWD_SEC, "relative")
            elif event.code == MIDDLE:
                mpv("cycle", "pause")
        except FileNotFoundError:
            print(f"[ERR] mpv socket not found at {MPV_SOCKET}. Start mpv with --input-ipc-server={MPV_SOCKET}")
        except ConnectionRefusedError:
            print("[ERR] Could not connect to mpv socket. Is mpv running?")


if __name__ == "__main__":
    main()
