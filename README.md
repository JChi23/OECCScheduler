# OECCScheduler v. 4.3
A PyQt Surgery Scheduler for MVP

v. 4.3
- Added help guide that can be accessed via the help button on the main menu
- Changed MIGS procedures to display correctly
- Changed the way procedures are read in from files so that multi-procedures can be described correctly

v. 4.2
- Changed UI button layout for better readability
- Added icons to UI buttons for better readability
- Added better file-reading for excel files

v. 4.1
- Increased UI Scale for readibility
- Added functionality for downloading schedule as an image
- Time and names will now correctly scale for smaller custom blocks
- Added additional column with details regarding procedure type
- Fixed bug where you could not move blocks from columns other than the first

v. 4.0
- Completely overhauled procedure movement to now auto shift existing procedures upon drag and drop
- Added 'Squish' functionality to remove whitespace
- Increased robustness of file reading

v. 3.1
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

- Icon images taken from Google Fonts

Known issues:
- There is currently an issue using PyInstaller with PyQt6 that causes a segmentation fault in the bundled app after packaging on MacOS Ventura
    - Remedied by using Pyinstaller 4.8 & PyQt6 6.3.0 on MacOS Catalina
- Issue with multi movement up bugging out and not remapping correctly (Unknown how to reproduce)
- Names can overflow blocks
- Clicking between blocks may cause multiple blocks to be unintentionally selected

TODO:
- Package scheduler for windows
- Name auto-spacing/sizing
- Hovering over blocks to see a bigger description?
- Increased customizability for time
- Increased customizability for types of procedures inputed
- Ability to modify type