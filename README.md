# Chicken Notes
This talon extension allows displaying notes through actions and commands. This can be useful for quickly looking things up and for having commands display relevant information, such as a voice command for defining an integer in C++ displaying a note on how many bytes an integer is. 

# Creating Notes
By default, compatible notes must be stored in the `note_files` subdirectory of the talon user directory. You can alternatively set the `user.chicken_notes_directory` setting to another directory path and then restart talon to use that instead. 

Notes should be stored as `.txt` files with the following format:

```
name: (name goes here. This is how you refer to the note)
tag: (Optionally, a tag name goes here. Tag names are used when searching your notes.)
link: (Optionally, a link can go here for a relevant webpage.)
-
Note text can go here.
The rest of the document is just notes. 
```

Example:
```
name: C plus plus int
tag: C plus plus
link: https://en.cppreference.com/w/cpp/language/types.html
-
int, short >= 2 bytes, long >= 4, long long >= 8
Processors cannot do arithmetic operations on types that are too small.
int as defined as the smallest type on the processor that it can do operations on.
Smaller types are implicitly converted to int for computations.
auto will consequently give int in those situations. 
```

Multiple tags and links go on separate lines prefixed with `tag: ` or `link: ` respectively.

If you make a mistake when defining a note file, an error will be output in the talon log. 

# Commands
## Managing the Display

`note show` allows seeing the current note. The display has to be turned on to see anything even if you use an action for showing a note.

`note hide` hides the display.

`note move` moves the display to the current cursor position.

## Using Notes

`note pick {user.chicken_notes_note_name}` shows the specified note.

`note expand` shows the full current note.

`note collapse` has the note only show text from the first line up to the maximum line length. 

`note tag search {user.chicken_notes_tag_name}` shows the notes with the specified tag name. 

`note copy link <number>` copies the link with the specified number.

`note open link <number>` opens the link with the specified number.

## Page Navigation

`note page <number>` go to the specified page number.

`note page next` advance the page number.

`note page (last|previous)` go back a page.

# Actions
`user.chicken_notes_display_brief_by_name` takes the name of the note as an argument and displays the text from the first line of the note up to the maximum line length.

`user.chicken_notes_display_by_name` takes the name of the note as an argument and displays the full note.

# Settings
`user.chicken_notes_max_line_length` is the maximum number of characters to display on a line. Make this 0 for no limit.

`user.chicken_notes_page_size` is the number of lines to show on each page. Make this 0 for no limit.

`user.chicken_notes_directory` is the directory to put the notes in. Changing this requires restarting talon or reloading this extension's python modules.

`user.chicken_notes_display_scale` is a floating point value that can be used to change the size of the display.

`user.chicken_notes_background_color` determines the display background color.

`user.chicken_notes_foreground_color` determines the display foreground color for the lines and text. 

# Dependencies
Chicken Notes depends on the following community actions:

`user.open_url` for opening links

