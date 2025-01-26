#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from typing import Optional, Self


class Tree:
    message_subdirectory_line: str = '{prefix}└── {path}'
    message_tabulation: str = '{prefix}    '
    message_current_directory_line: str = '{prefix}├── {path}'
    message_subdirectory_tabulation: str = '{prefix}│   '

    def __init__(
        self: Self,
    ) -> None:
        self.count_dirs: int = 0
        self.count_files: int = 0

    def register(
        self: Self,
        absolute_path: str,
    ) -> None:
        """
        Registers occurrences of files and directories.

        :param absolute_path: Absolute path to the current directory or file.
        :type absolute_path: str
        """
        if os.path.isdir(absolute_path):
            self.count_dirs += 1
        else:
            self.count_files += 1

    def summary_message(
        self: Self,
    ) -> str:
        """
        Creates a message report.

        :return: Message with number of directories and files.
        :rtype: str
        """
        message = '{directories_count} directories, {files_count} files'

        return message.format(
            directories_count=self.count_dirs,
            files_count=self.count_files,
        )

    def say(
        self: Self,
        message: str,
        new_line: Optional[bool] = False,
    ) -> None:
        """
        Displays a message to the user.

        :param message: Message for user.
        :type message: str

        :param new_line: Start message on a new line, defaults to False
        :type new_line: bool, optional
        """
        if new_line:
            msg = '\n{message}\n'
        else:
            msg = '{message}\n'

        sys.stderr.write(
            msg.format(
                message=message,
            )
        )

    def walk(
        self: Self,
        directory: str,
        prefix: Optional[str] = '',
    ) -> None:
        """
        View all files and directories relative to the starting position.

        :param directory: Start directory.
        :type directory: str

        :param prefix: Prefix for message, defaults to ''
        :type prefix: str, optional
        """
        filepaths: list[str] = sorted([filepath for filepath in os.listdir(directory)])

        for idx, path in enumerate(filepaths):
            if self._is_dot_file(path):
                continue

            absolute_path = os.path.join(directory, path)
            self.register(absolute_path)

            if idx == len(filepaths) - 1:
                self.say(
                    self.message_subdirectory_line.format(
                        prefix=prefix,
                        path=path,
                    ),
                )
                if os.path.isdir(absolute_path):
                    self.walk(
                        absolute_path,
                        self.message_tabulation.format(
                            prefix=prefix,
                        ),
                    )

            else:
                self.say(
                    self.message_current_directory_line.format(
                        prefix=prefix,
                        path=path,
                    ),
                )
                if os.path.isdir(absolute_path):
                    self.walk(
                        absolute_path,
                        self.message_subdirectory_tabulation.format(
                            prefix=prefix,
                        ),
                    )

    def _is_dot_file(
        self: Self,
        path: str,
    ) -> bool:
        """
        Checking whether it is a dot file.

        :param path: Path to check.
        :type path: str

        :return: True if `path` is dot file. Otherwise False.
        :rtype: bool
        """
        if path.startswith('.'):
            return True

        return False


if __name__ == '__main__':
    tree = Tree()
    directory = '.'

    if len(sys.argv) > 1:
        directory = sys.argv[1]
    tree.say(directory)

    tree.walk(directory)
    tree.say(tree.summary_message(), new_line=True)
