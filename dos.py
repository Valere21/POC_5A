#!/usr/bin/env python3
import subprocess

xr = [s for s in subprocess.check_output("xrandr").decode("utf-8").split() if "+0+" in s]
scr = [int(n)/2 for n in xr[0].split("+")[0].split("x")]
subprocess.Popen(["xdotool", "mousemove", str(scr[0]), str(scr[1])])
