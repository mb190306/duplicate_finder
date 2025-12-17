#!/usr/bin/env python3
import sys
import hashlib
import os
from tempfile import TemporaryDirectory


def list_files(path: str) -> list[str]:
    """
    Recursively lists all file paths in the specified directory.

    Args:
        path (str): The root directory to search for files.

    Returns:
        list[str]: A list of file paths found in the directory and its subdirectories.
    """
    # Run "pytest find_duplicates_solo.py -k list_files" to test your implementation
    raise NotImplementedError()


def hash_file(file_path: str) -> str:
    """
    Computes the SHA-1 hash of the entire file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The hexadecimal SHA-1 hash of the file.
    """
    # Run "pytest find_duplicates_solo.py -k hash_file" to test your implementation
    raise NotImplementedError()


def group_files_by_full_hash(file_paths: list[str]) -> list[list[str]]:
    """
    Groups files by their full content hash and identifies duplicate groups.

    Args:
        file_paths (list[str]): A list of file paths to analyze.

    Returns:
        list[list[str]]: A list of groups where each group contains file paths of identical files.
    """
    files_by_hash = {}
    for file_path in file_paths:
        hash = hash_file(file_path)
        if hash in files_by_hash:
            files_by_hash[hash].append(file_path)
        else:
            files_by_hash[hash] = [file_path]
    duplicates = []
    for hash, paths in files_by_hash.items():
        if len(paths) > 1:
            duplicates.append(paths)
    return duplicates


def print_duplicates(duplicates: list[list[str]]):
    """
    Prints details of duplicate files, including their sizes and paths.

    Args:
        duplicates (list[list[str]]): A list of duplicate file groups.
                                      Each group contains file paths of identical files.

    Returns:
        None
    """
    for files in duplicates:
        print("Found duplicate files:")
        for file in files:
            print(file)


def check_for_duplicates(paths: list[str]):
    """
    Checks for duplicate files in the given paths and prints the results.

    Args:
        paths (list[str]): A list of directory paths to search for duplicates.

    Returns:
        None
    """
    files = []
    for path in paths:
        files.extend(list_files(path))
    duplicates = group_files_by_full_hash(files)
    print_duplicates(duplicates)


def main():
    """
    The main entry point of the script. Checks for duplicate files in the directories
    provided as command-line arguments.

    Returns:
        None
    """
    if len(sys.argv) < 2:
        print("Usage: find_duplicates_solo.py <path> [<path> ...]")
        sys.exit(1)
    check_for_duplicates(sys.argv[1:])


if __name__ == "__main__":
    main()


# Pytest Tests
# Use pytest find_duplicates_solo.py to run these tests.


def create_file(directory, name, content):
    """Helper function to create a file with the given content."""
    file_path = os.path.join(directory, name)
    with open(file_path, "w") as f:
        f.write(content)
    return file_path


def test_list_files():
    """Test if list_files correctly lists all files."""
    with TemporaryDirectory() as temp_dir:
        file1 = create_file(temp_dir, "file1.txt", "Hello World")
        file2 = create_file(temp_dir, "file2.txt", "Hello World")
        file3 = create_file(temp_dir, "file3.txt", "Different Content")

        files = list_files(temp_dir)
        assert set(files) == {file1, file2, file3}


def test_list_files_recursive():
    """Test if list_files correctly lists all files recursively."""
    with TemporaryDirectory() as temp_dir:
        file1 = create_file(temp_dir, "file1.txt", "Hello World")
        subdir = os.path.join(temp_dir, "subdir")
        os.mkdir(subdir)
        file2 = create_file(subdir, "file2.txt", "Different Content")

        files = list_files(temp_dir)
        assert set(files) == {file1, file2}


def test_hash_file():
    """Test if hash_file computes the correct full file hash."""
    with TemporaryDirectory() as temp_dir:
        file1 = create_file(temp_dir, "file1.txt", "Hello World")
        file2 = create_file(temp_dir, "file2.txt", "Hello World")
        file3 = create_file(temp_dir, "file3.txt", "Different Content")

        hash1 = hash_file(file1)
        hash2 = hash_file(file2)
        hash3 = hash_file(file3)

        assert hash1 == "0a4d55a8d778e5022fab701977c5d840bbc486d0"
        assert hash1 == hash2
        assert hash1 != hash3


def test_group_files_by_full_hash():
    """Test if group_files_by_full_hash identifies files with identical content."""
    with TemporaryDirectory() as temp_dir:
        file1 = create_file(temp_dir, "file1.txt", "Hello World")
        file2 = create_file(temp_dir, "file2.txt", "Hello World")
        file3 = create_file(temp_dir, "file3.txt", "Different Content")
        file4 = create_file(temp_dir, "file4.txt", "A" * 1024 + "B" * 24)
        file5 = create_file(temp_dir, "file5.txt", "A" * 1024 + "C" * 24)

        groups = group_files_by_full_hash([file1, file2, file3, file4, file5])

        assert len(groups) == 1  # Only one group of duplicates
        assert set(groups[0]) == {file1, file2}
