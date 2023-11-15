import json
import os
import re
import argparse

# Create an ArgumentParser object
parser = argparse.ArgumentParser()

# Add arguments to the parser
parser.add_argument(
    "--root_folder",
    required=True,
    help="Specify the root folder where all audiobooks are located.",
)
parser.add_argument(
    "--max_renames",
    default=1,
    type=int,
    help=(
        "Set the maximum number of audiobooks to rename at once. "
        "Use '-1' to allow an unlimited number of renames. The default value is 1."
    ),
)
parser.add_argument(
    "--remove_empty_folders",
    action="store_true",
    help=(
        "Remove empty folders within the specified root_folder. This option will delete"
        " any folders that do not contain any files or subfolders."
    ),
)
parser.add_argument(
    "--remove_abs_metadata",
    action="store_true",
    help=(
        "Remove metadata.abs files from the audiobook folder. This option is used to"
        " delete obsolete metadata.abs files that are no longer required."
    ),
)
parser.add_argument(
    "--dry_run",
    action="store_true",
    help=(
        "Performs a dry run, which means the script will simulate the process "
        "but will not make any actual changes to the data. This is useful for "
        "previewing the actions that would be taken without altering anything."
    ),
)
parser.add_argument(
    "--output_file",
    help=(
        "Specify the path to the log file where you want the script's output to be"
        " recorded. If provided, the script will capture and write output to this file."
        " If not provided, output will be displayed on the console."
    ),
)


# Parse the command-line arguments
args = parser.parse_args()

root_folder = args.root_folder
max_rename_count = int(args.max_renames)


def write_info_to_file_and_console(info):
    if args.output_file is not None:
        # Open the specified text file in write mode only on the first call
        if not hasattr(args, "file_initialized"):
            with open(args.output_file, "w") as file:
                file.write(info + "\n")
            args.file_initialized = True
        else:
            # Append the information to the file on subsequent calls
            with open(args.output_file, "a") as file:
                file.write(info + "\n")

    # Output the information to the console
    print(info)


def jsonHandler(file, mode="r", data=""):
    if mode == "w":
        # Serializing json
        json_object = json.dumps(data, indent=4)
        # Writing to sample.json
        with open(file, mode) as jfile:
            jfile.write(json_object)
    elif mode == "r":
        with open(file, mode) as jfile:
            # Reading from json file
            json_object = json.load(jfile)
        return json_object


def strip_invalid_file_name_characters(variable):
    invalid_file_name_characters = r'[\/:*"?<>|]'
    return re.sub(invalid_file_name_characters, "", variable)


def naming_convention(metadata):
    jsondata = jsonHandler(
        os.path.join(metadata, "metadata.json"),
        mode="r",
    )

    authors = strip_invalid_file_name_characters(", ".join(jsondata["authors"]))
    if jsondata["series"]:
        full_series = re.search(r"(.*) #(\d*)", jsondata["series"][0])
        if full_series:
            series = strip_invalid_file_name_characters(full_series.group(1))
            book_number = strip_invalid_file_name_characters(full_series.group(2))
        else:
            series = jsondata["series"][0]
            book_number = ""
    title = strip_invalid_file_name_characters(jsondata["title"])

    if jsondata["series"]:
        new_audio_book_path = f"{authors}/{series}"
        new_audio_book_folder = f"{title}, Book {book_number}"
        rename_of_folder_only = f"{authors} - {series}, {title} {book_number}"
    else:
        new_audio_book_path = f"{authors}"
        new_audio_book_folder = f"{title}"
        rename_of_folder_only = f"{authors} - {title}"
    return new_audio_book_path, new_audio_book_folder, rename_of_folder_only


def is_folder_empty(folder_path):
    list_of_items = os.listdir(folder_path)
    list_of_items = [item for item in list_of_items if item != ".DS_Store"]
    return len(list_of_items) == 0


def recursively_list_folders(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            yield os.path.join(root, dir)


duplicate_audiobooks = []
# Recursively list the folders in the folder
for folder in recursively_list_folders(root_folder):
    # Clean Up metadata
    if args.remove_abs_metadata:
        if os.path.exists(os.path.join(folder, "metadata.abs")):
            if args.dry_run:
                write_info_to_file_and_console(f"Will remove: {os.path.join(folder, 'metadata.abs')}")
            else:
                write_info_to_file_and_console(f"Will remove: {os.path.join(folder, 'metadata.abs')}")
                os.remove(os.path.join(folder, "metadata.abs"))
    # Move and rename the Audiobook into the correct folder structure
    if os.path.exists(os.path.join(folder, "metadata.json")):
        parent_folder_path = os.path.dirname(folder)
        new_audio_book_path, new_audio_book_folder, only_folder_name = (
            naming_convention(folder)
        )
        new_audio_book_path = os.path.join(root_folder, new_audio_book_path)
        new_folder = os.path.join(parent_folder_path, only_folder_name)
        if folder != new_folder:
            max_rename_count = max_rename_count - 1
            write_info_to_file_and_console(f"Current Folder: {folder}")
            write_info_to_file_and_console(f"New Folder: {new_folder}")
            if os.path.exists(new_folder):
                duplicate_audiobooks.append(f"{new_folder} - {folder}")
            else:
                if args.dry_run is False:
                    # Rename the folder as unable to move it yet without breaking the inode/library item
                    os.rename(folder, new_folder)
    elif is_folder_empty(folder):
        if args.remove_empty_folders:
            if args.dry_run is False:
                if os.path.exists(os.path.join(folder, ".DS_Store")):
                    os.remove(os.path.join(folder, ".DS_Store"))
                os.rmdir(folder)
            write_info_to_file_and_console(f"Removed empty folder: {folder}")
    if max_rename_count == 0:
        write_info_to_file_and_console("Hit Max Rename Limit")
        break

if duplicate_audiobooks:
    write_info_to_file_and_console("There are duplicate audiobooks:")
    for audiobook in duplicate_audiobooks:
        write_info_to_file_and_console(audiobook)
