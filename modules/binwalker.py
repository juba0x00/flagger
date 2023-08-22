from os import path
import subprocess


class BinWalker:
    """
    A class for extracting binary data using binwalk
    """
    def __init__(self, binary_file):
        """
        Initializes the BinaryExtractor object.

        Args:
            binary_file (str): The binary file to be extracted.
        """
        self.binary_file = binary_file

        if self.binwalk_installed and self.extract():
            self.extracted = True
        else:
            self.extracted = False

    @property
    def binwalk_installed(self):
        """
        Checks if binwalk is installed.

        Returns:
            bool: True if binwalk is installed, False otherwise.
        """
        if subprocess.run(['which', 'binwalk'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            return True
        else:
            return False

    def extract(self):
        """
        Extracts the binary data.

        Returns:
            bool: True if extraction was successful, False otherwise.
        """
        if not path.exists(self.binary_file):
            print('File does not exist')
            return False

        if path.exists(f'{self.binary_file}_extracted'):
            return True

        subprocess.run(['binwalk', '-e', self.binary_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if path.exists(f'{self.binary_file}_extracted'):
            return True
        else:
            return False