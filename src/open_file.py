import sys


class Open:

    def __init__(self, path_to_file, mode):
        self.mode = mode
        self.file_path = path_to_file

    def __enter__(self):
        if self.file_path is not None:
            self.stream = open(self.file_path, self.mode)
        else:
            if self.mode == "w":
                self.stream = sys.stdout
            if self.mode == "r":
                self.stream = sys.stdin
        return self.stream

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_path is not None:
            self.stream.close()
