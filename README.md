# OECCScheduler v. 2.5
A PyQt Surgery Scheduler for MEP


v. 2.5
- Fixed a bug where procedure update would not update blocks correctly when moving to 7:30

v. 2.0
- Added ability for names to be attached to procedure which can then be edited
- Added dynamic time displays for procedures that update automatically when moved
- Allowed for break slot to be able to be moved around accordingly

v. 1.0
- Developed scheduler where user can drag, drop, delete, and add between three different types of procedures
- User can save current schedule between sessions
- User can clear schedule except for a static break block


Known issues:
- There is currently an issue using PyInstaller with PyQt6 that causes a segmentation fault in the bundled app after packaging on MacOS Ventura
    - Remedied by using Pyinstaller 4.8 & PyQt6 6.3.0 on MacOS Catalina