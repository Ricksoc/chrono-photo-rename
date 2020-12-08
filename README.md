# chrono-photo-rename
This script was created as yy cs50 final project is a python command line script which takes as input jpeg
photographs and renames them sequentially based on the date the photo was taken
as extracted from the jpeg exif meta data.

The script takes one or two command line arguments. The first is mandatory
specifying the directory containing the jpegs to be renamed. The second
is an optional prefix to be used for the file renaming in conjunction with a
counter. If this is not specified then the date and time the photo was taken is
used as the file name.

The script checks for valid input directory and that any supplied prefix
will not create invalid file names. If any unsupported files are in the
directory or any of the jpegs in there do not have the date_taken meta
data then these files are not processed and a list of them is given to the user
in a summary after the script has competed.

A YouTube video showing the script in action can be seen at https://youtu.be/QMswm5j0MNE
