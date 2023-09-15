# OECCScheduler v. 2.5
A PyQt Surgery Scheduler for MVP

v. 3.5
- Added additional procedure categories
- Added total case number to top of schedule

v. 3.0
- Added ability for custom-length blocks to be added
- Added functionality for multi-select and movability of blocks
- Allowed for certain types of schedules to be opened in scheduler
- Added date to top of schedule
- Added additional time slots to schedule

v. 2.1
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
- Issue with multi movement up bugging out and not remapping correctly (Unknown how to reproduce)
- Names can overflow blocks