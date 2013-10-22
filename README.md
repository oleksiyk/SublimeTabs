Sublime Text 3 Tabs plugin
==========================

Some useful additions to ST3 tabs:
  * show filename in status bar
  * automatically close unused tabs
  * autocomplete within all opened files

Installation
------------
Clone this repo into Sublime Text 3 `Packages` folder

Settings
------------
```json
{

  // enable auto closing of tabs
  "close_tabs": true,

  // Do not close files that were modified in last N seconds
  "keep_modified_in": 1800,

  // Do not close files that were accessed in last N seconds
  "keep_accessed_in": 60,

  // Do not close any files if the are less the N tabs open
  "keep_tabs" : 8,

  // Autocomplete within all currently open files
  "autocomplete_open_files": true,

  // show current filename in status bar
  "filename_in_statusbar": true,
}
```

