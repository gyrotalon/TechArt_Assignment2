"""
Filename: renamer_lib.py
Title: File Renamer Library
Author: Macy Chantharak
Date Created: 2025-02-18
Date Edited: 2025-02-19
Description:
    This library contains functions for renaming or copying files.
Python Version: 3.13
"""


import logger as logger
import os
import shutil


def get_logger(print_to_screen = False):
    """
    Uses the logger.py module to create a logger

    Args:
        print_to_screen: for printing to screen as well as file
    """

    return logger.initialize_logger(print_to_screen)

def get_renamed_file_path(existing_name, string_to_find, 
                          string_to_replace, prefix, suffix):
    """
    Returns the target file name given an existing file name and 
    string operations

    Args:
        logger: logger instance
        existing_name: the existing file's name
        string_to_find: a string to find and replace in the existing file name
        string_to_replace: the string you'd like to replace it with
        prefix: a string to insert at the beginning of the file name
        suffix: a string to append to the end of the file name
    """

    new_name = existing_name

    try:
        if (isinstance(string_to_find, str)):
            if string_to_find != '' and string_to_find in new_name:
                new_name = new_name.replace(string_to_find, string_to_replace)
        else:
            string_to_find = list(string_to_find)
            string_to_find.sort(reverse=True)
            for the_string in string_to_find:
                if the_string != '' and the_string in new_name:
                    new_name = new_name.replace(the_string, string_to_replace)
        if prefix != '':
            new_name = prefix + new_name
        if suffix != '':
            name_only, ext = os.path.splitext(new_name)
            new_name = name_only + suffix + ext
    except TypeError:
        return
    else:
        return new_name

def get_files_with_extension(folder_path, extension):
    """
    Returns a collection of files in a given folder with an extension that 
    matches the provided extension

    Args:
        folder_path: The path of the folder whose files you'd like to search
        extension: The extension of files you'd like to include in the return
    """

    files_with_extension_arr = []
    if extension[0] != '.':
        extension = '.' + extension
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        ext = os.path.splitext(file_name)[1]
        if (os.path.isfile(file_path) and ext == extension):
            files_with_extension_arr.append(file_name)
    return files_with_extension_arr

def rename_file(logger, existing_name, new_name, copy=False):
    """
    Renames a file if it exists
    By default, should move the file from its original path to its new path--
    removing the old file
    If copy is set to True, duplicate the file to the new path

    Args:
        logger: logger instance
        existing_name: full filepath a file that should already exist
        new_name: full filepath for new name
        copy: copy instead of rename
    """

    logger.info('Attempting to ' + ('copy ' if copy else 'rename ') + 
                f'{existing_name} to {new_name}')

    if os.path.isfile(existing_name):
        if not os.path.isfile(new_name):
            if copy:
                shutil.copy(existing_name, new_name)
                logger.info(f'Copied {existing_name} to {new_name}')
            else:
                shutil.move(existing_name, new_name)
                logger.info(f'Renamed {existing_name} to {new_name}')
        else:
            logger.error(f'{new_name} already exists ' +
                           'and cannot be used as a new file name.')
    else:
        logger.error(f'File {existing_name} does not exist, ' + 
                       'thus cannot be renamed.')

def rename_files_in_folder(logger, folder_path, extension, string_to_find,
                           string_to_replace, prefix, suffix, copy=False):
    """
    Renames all files in a folder with a given extension
    This should operate only on files with the provided extension
    Every instance of string_to_find in the filepath should be replaced
    with string_to_replace
    Prefix should be added to the front of the file name
    Suffix should be added to the end of the file name

    Args:
        logger: logger instance
        folder_path: the path to the folder the renamed files are in
        extension: the extension of the files you'd like renamed
        string_to_find: the string in the filename you'd like to replace
        string_to_replace: the string you'd like to replace it with
        prefix: a string to insert at the beginning of the file path
        suffix: a string to append to the end of the file path
        copy: whether to rename/move the file or duplicate/copy it
    """
    logger.info('START: rename_files_in_folder will attempt to ' +  
                ('copy ' if copy else 'rename ') + 
                'files based on provided arguments.')
    if not copy:
        logger.warning('Renaming files may cause existing links to break.')
    if(isinstance(extension, str)):
        if extension.count('.') >= 1 and extension[0] != '.':
            logger.warning('Multiple extensions are not supported. ABORTING.')
            return
    else:
        logger.warning('Extension input must be a string. ABORTING.')
        return

    if os.path.isdir(folder_path):
        logger.info(f'Opening {folder_path} to check for files.')
        existing_name_arr = get_files_with_extension(folder_path, extension)
        logger.info(f'Files with {extension} extension in {folder_path} ' + 
                    f'are: {existing_name_arr}')
        for existing_name in existing_name_arr:
            new_name = get_renamed_file_path(existing_name, string_to_find, 
                                             string_to_replace, prefix, suffix)
            try:
                new_name_path = os.path.join(folder_path, new_name)
            except TypeError:
                logger.error('string_to_replace, prefix, and suffix must ' + 
                             'be string type. string_to_find must be string' + 
                             ' or list/set/tuple of strings. ABORTING.')
                return
            existing_name_path = os.path.join(folder_path, existing_name)
            rename_file(logger, existing_name_path, new_name_path, copy)
    else:
        logger.error(f'The folder {folder_path} does not exist!')

    logger.info('END: rename_files_in_folder has finished running.')


def main():
    # Logger
    logger = get_logger(True)
    logger.info('Logger Initiated')

    #   Here are some examples of different logger messages
    logger.warning('This would be a logger warning')
    logger.error('This would be a logger error!!')
    logger.critical('This would be a critical log')


if __name__ == '__main__':
    main()
