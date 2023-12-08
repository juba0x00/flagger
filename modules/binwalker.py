from os import path
from subprocess import Popen, run, PIPE, DEVNULL
from random import randint
from socket import socket, AF_INET, SOCK_STREAM
from .utils import COLORS
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
        self.info: str  #ask
        self.extracted = False
        self.__file_path = file_path
        self.extract_dir = self.__get_result_dir()
        self.__extract() if self.__binwalk_installed else None

    @property
    def __binwalk_installed(self):
        """
        Checks if binwalk is installed.

        Returns:
            bool: True if binwalk is installed, False otherwise.
        """

        if run(['which', 'binwalk'], stdout=DEVNULL, stderr=DEVNULL).returncode == 0:
            return True
        else:
            self.info = "binwalk is not installed"
            return False


    def __extract(self):
        """
        Extracts the binary data.

        Returns:
            bool: True if extraction was successful, False otherwise.
        """
        if not path.exists(self.__file_path):
            self.info = F"{Colors.ERR}File does not exist{COLORS['RESET']}"
            return False


        if path.exists(self.extract_dir):  # already extracted
            self.info = f"{self.__file_path} extracted before, skip extracting"
            self.extracted = True
            return True
        # run(['binwalk', '-e', self.__file_path], stdout=DEVNULL, stderr=DEVNULL)
        rand_port = randint(50000, 60000)
        Popen(['binwalk', '-s', str(rand_port), '-e', self.__file_path], stdout=PIPE, stderr=PIPE)
        
        while True:
            try:
                checker = socket(AF_INET, SOCK_STREAM)
                checker.connect(('localhost', rand_port))
                while data:=checker.recv(1024):
                    print(f'{Fore.GREEN}Binwalk Extracting: {data.decode()}\r', end=Fore.RESET)
                
                else:
                    break

            except ConnectionRefusedError:
                continue
            except Exception as err:
                print(err)
                break
            
        if path.exists(self.extract_dir):
            self.info = f"{Fore.CYAN}binwalk extracted {self.__file_path} successfully{Fore.RESET}"
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
