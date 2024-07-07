import os
import subprocess
import random
import socket
from .utils import Colors, COLORS
from colorama import Fore

class BinWalker:
    """
    A class for extracting binary data using binwalk
    """

    def __init__(self, file_path):
        """
        Initializes the BinaryExtractor object.

        Args:
            file_path (str): The binary file to be extracted.
        """
        self.info = None
        self.extracted = False
        self.__file_path = file_path
        self.extract_dir = self.__get_result_dir()
        self.__extract() if self.__binwalk_installed else print("Binwalk is not installed.")

    @property
    def __binwalk_installed(self):
        """
        Checks if binwalk is installed.

        Returns:
            bool: True if binwalk is installed, False otherwise.
        """
        return subprocess.run(['which', 'binwalk'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

    def __extract(self):
        """
        Extracts the binary data.

        Returns:
            bool: True if extraction was successful, False otherwise.
        """
        if not os.path.exists(self.__file_path):
            self.info = f"{Colors.ERR}File does not exist{COLORS['RESET']}"
            return False

        if os.path.exists(self.extract_dir):
            self.info = f"{self.__file_path} has been previously extracted, skipping extraction."
            self.extracted = True
            return True

        rand_port = random.randint(50000, 60000)
        subprocess.Popen(['binwalk', '-s', str(rand_port), '-e', self.__file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        while True:
            try:
                checker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                checker.connect(('localhost', rand_port))
                while data := checker.recv(1024):
                    print(f'{Fore.GREEN}Binwalk Extracting: {data.decode()}\r', end=Fore.RESET)
                else:
                    break
            except ConnectionRefusedError:
                continue
            except Exception as err:
                print(err)
                break
            
        if os.path.exists(self.extract_dir):
            self.info = f"{Fore.CYAN}Binwalk successfully extracted {self.__file_path}{Fore.RESET}"
            self.extracted = True

    def __get_result_dir(self) -> str:
        """
        Get Expected Extraction Directorys

        Returns: 
            str: expected extraction path
        """
        path_dirs = self.__file_path.split('/')
        path_dirs[-1] = f"_{path_dirs[-1]}.extracted"
        return '/'.join(path_dirs)
