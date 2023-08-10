# OECCScheduler
A PyQt Surgery Scheduler for OECC

There is currently an issue using PyInstaller with PyQt6 that causes a segmentation fault in the bundled app after packaging on MacOS Ventura

Remedied by using Pyinstaller 4.8 & PyQt6 6.3.0 on MacOS Catalina