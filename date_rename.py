import os, datetime, sys, re
from PIL import Image, ExifTags

''' Renames jpg / jpeg files based on date photo was taken
Accepts two command line arguments, the first being the file path
for the files to be renamed. The second being an optional prefix
for the renamed files. If this is not specificed they will be renamed with 
the date and time the photo was taken. 

This does require the cmaera time to have been set correctly when the photo was taken'''

print("\nThis program requires a file path to the photos to be renamed",
 "as the first command line argument, e.g. D\:photos\n")
print("An optional second command line argument can be supplied to set",
 "the renamed file prefix, otherwise the date and time the photo was",
 "taken will be used, e.g. D\:photos new_prefix\n")
 
 # Ask user to confirm photos have been backup up
confirm = input("Before beginning, have you backup up the photos to be renamed? (y/n): ")
print("")
if confirm.lower() == "n":
    exit("Ending program to allow file backup")

# Check a file path has been correctly specified
if len(sys.argv) < 2:
    exit("Please specify a file path to the photos")

path = sys.argv[1]

if not os.path.exists(path):
    exit("File path does not exist")

# Check for specified prefix and if so that it does not contain invalid characters
forbidden = ["*",".","\"","\\","\/", "[","]",":",";","|",","]
forbidden_list = "".join(forbidden)

if len(sys.argv) > 2:
    for char in forbidden:
        if char in sys.argv[2]:
            exit(f"Error: forbidden character in prefix, you cannot use: {forbidden_list} or a space")
            
# Specify allowed extensions
extensions = [".jpg", ".jpeg"]

# Get list of files in specified directory
directory = sys.argv[1]
files = os.listdir(directory)

# Initialize counters and stores
total_files = len(files)
counter = 0
files_failed = 0
invalid_files = []
no_exif = []
valid_files = []


for file in files:
    # Split file name and extension
    name, ext = os.path.splitext(file)
    
    # Remove non jpg / jpeg files from processing list
    if ext.lower() not in extensions:
        invalid_files.append(file)
        files_failed +=1
    
    else:
        img = Image.open("\\".join([directory,file]))
        img_data = img.getexif()
        img.close()
        
        # Check image has exif data
        if img_data is None:
            no_exif.append(file)
            files_failed += 1
            continue
        
        # Check exif date is available
        if 36867 in img_data.keys():
            
            # Check a correctly formatted time stamp is available
            if re.match(r"\d{4}:\d{2}:\d{2}",img_data[36867]):
                # Add tuple of name and date taken to file list
                valid_files.append(("\\".join([directory,file]), img_data[36867]))
            
            else:
                # Add file ot list of not processed
                no_exif.append(file)
                files_failed += 1
            
        else:
            # Add file ot list of not processed
            no_exif.append(file)
            files_failed += 1
            
# Sort pictures by date taken
sorted_list = sorted(valid_files,key = lambda x: x[1])

# Iterate through files with metadata
for item in sorted_list:
    if len(sys.argv) > 2:
        # Use supplied prefix if there was one
        prefix = sys.argv[2]
        
        # Calculate number of zeroes required for padding, make min of 3 digits
        max_pad = len(str(len(files)))
        padding = max(3, max_pad)
        
        # Count successfully extracted file and convert to file name
        counter += 1
        pad_counter = lambda num, zeros: f"{num:0{zeros}d}"
        fname = directory + "\\" + prefix + "_" + pad_counter(counter, padding)
        new_name = fname + ".jpeg"
        os.rename(item[0], new_name)
    
    else:
        # Otherwise use exif() data for when photo was created
        date_time_item = datetime.datetime.strptime(item[1], '%Y:%m:%d %H:%M:%S')
        formatted_date = date_time_item.strftime("%Y-%m-%d_%H-%M-%S")
        new_name = directory + "\\" + formatted_date + ".jpeg"
        os.rename(item[0], new_name)
        counter += 1

# Print program summary
print("*** PROGRAM COMPLETE ***")
print(f"\n{counter} of {total_files} files in specified directory successfully renamed")
print(f"\n{files_failed} files were not renamed")
       
if len(invalid_files) > 0:
    print("\n" + " ".join(invalid_files) + " unsupported file format")

if len(no_exif) > 0:
    print("\n" + " ".join(no_exif) + " no meta data available")