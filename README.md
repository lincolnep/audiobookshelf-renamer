# Audiobook Renaming Script
The Audiobook Renaming Script is a Python script that helps you organize and rename audiobook files within a specified root folder. This README provides instructions on how to use the script effectively.

## Prerequisites
Before using the Audiobook Renaming Script, make sure you have the following prerequisites in place:

- Python 3 installed on your system.
- "Store metadata with item" enabled in audiobookshelf metadata.json file needs to be in the audiobook folder other wise it will not rename the folder.
- Minimin version of audiobookshelf 2.5.0

## Disclaimer
Use at Your Own Risk, No Warranty: This script is provided as-is, without any warranties or guarantees. You are using it at your own risk. The authors and contributors of this script are not responsible for any potential data loss or issues that may arise from its usage. Always back up your data before running the script.

## Rename Examples
It's important to keep in mind that the effectiveness of this rename tool relies heavily on the accuracy of your metadata.

**Book Series Naming Convention:**
- Format: "{authors} - {series}, {title} {book_number}"

**Single Book Naming Convention:**
- Format: "{authors} - {title}"

These examples illustrate the naming conventions that should be followed when using the tool.

##### Output Example:
```
Current Folder: /data/audiobooks/Joshua Dalzelle - Vapor Trails Terran Scout Fleet, Book 3
New Folder: /data/audiobooks/Joshua Dalzelle - Terran Scout Fleet, Vapor Trails 3
Current Folder: /data/audiobooks/Joshua Dalzelle - Aftershock Terran Scout Fleet, Book 5
New Folder: /data/audiobooks/Joshua Dalzelle - Terran Scout Fleet, Aftershock 5
```

## Usage
To use the script, you need to run it from the command line with the specified command-line arguments. Here are the available arguments and their usage:

### '--root_folder' (required)
- Specifies the root folder where all your audiobook files are located.
- Required: You must provide a valid path to your audiobook files.

##### Example:
```bash
python audiobook_renamer.py --root_folder /path/to/audiobooks
```
### '--max_renames'
- Sets the maximum number of audiobooks to rename at once.
- Default value: 1
- You can specify an integer value for this argument. If you use -1, it means there is no limit, and the script will rename all audiobooks at once.

##### Example with custom limit:
```bash
python audiobook_renamer.py --root_folder /path/to/audiobooks --max_renames 5
```

##### Example with no limit:
```bash
python audiobook_renamer.py --root_folder /path/to/audiobooks --max_renames -1
```
### '--remove_empty_folders'
- When provided, this argument will remove any empty folders within the specified root folder.
- No value is required for this argument; it's a flag.
- If you include this argument, the script will remove empty folders during execution.

##### Example with the --remove_empty_folders flag:
```bash
python audiobook_renamer.py --root_folder /path/to/audiobooks --remove_empty_folders
```
### '--output_file'
Specifies the file where a copy of the script's output will be saved.
You can provide the path to the output file, and the script will write a copy of its results to that file.

##### Example with custom output file:
```bash
python audiobook_renamer.py --root_folder /path/to/audiobooks --output_file output.txt
```
## Running the Script
Once you have the necessary prerequisites in place and have a clear understanding of the available arguments, you can run the Audiobook Renaming Script by executing it from the command line, as demonstrated in the examples above. If you wish to keep a record of the script's output, you can specify the --output_file argument to save the results to a file for later reference.

The script will process the audiobook files within the specified root folder according to your provided arguments, renaming them and, if requested, removing empty folders. The output file will contain the results of the operation.
