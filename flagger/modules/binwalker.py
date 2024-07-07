from os import path
from subprocess import Popen, run, PIPE, DEVNULL
from random import randint
from socket import socket, AF_INET, SOCK_STREAM
from flagger.modules.utils import COLORS


class BinWalker:
    """
    A class for extracting binary data using binwalk
    """

    def __init__(self, file_path: str) -> None:
        """
        Initializes the BinaryExtractor object.

        Args:
            file_path (str): The binary file to be extracted.
        """
        self.info: str  # ask
        self.extracted = False
        self.__file_path = file_path
        self.extract_dir = self.__get_result_dir()
        self.__extract() if self.__binwalk_installed and not self.__extracted_before() else None

    @property
    def __binwalk_installed(self) -> bool:
        """
        Checks if binwalk is installed.

        Returns:
            bool: True if binwalk is installed, False otherwise.
        """

        if run(['which', 'binwalk'], stdout=DEVNULL, stderr=DEVNULL).returncode == 0:
            return True
        else:
            self.info = "binwalk is not installed"
            print(self.info)
            return False

    def __extracted_before(self) -> bool:
        """
        Checks if the binary data has been extracted before.

        Returns:
            bool: True if the binary data has been extracted before, False otherwise.
        """
        if path.exists(self.extract_dir):
            self.extracted = True
            self.info = f"{COLORS['INFO']}{self.__file_path} extracted before, skip extracting{COLORS['RESET']}"
            print(self.info)  # TODO: change to logger
            return True
        else:
            return False

    def __extract(self) -> bool:
        """
        Extracts the binary data.

        Returns:
            bool: True if extraction was successful, False otherwise.
        """
        if not path.exists(self.__file_path):
            self.info = F"{COLORS['ERR']}File does not exist{COLORS['RESET']}"
            print(self.info)
            return False

        print(f"{COLORS['INFO']}Extracting {self.__file_path} using binwalk{COLORS['RESET']}")
        run(['binwalk', '-e', self.__file_path], stdout=DEVNULL, stderr=DEVNULL)
        # rand_port = randint(50000, 60000)
        # Popen(['binwalk', '-s', str(rand_port), '-e', self.__file_path], stdout=PIPE, stderr=PIPE)

        # while True:
        #     try:
        #         checker = socket(AF_INET, SOCK_STREAM)
        #         checker.connect(('localhost', rand_port))
        #         while data:=checker.recv(1024):
        #             print(f"{COLORS['INFO']}Binwalk Extracting: {data.decode()}\r", end=COLORS['RESET'])

        #         else:
        #             break

        #     except ConnectionRefusedError:
        #         continue
        #     except Exception as err:
        #         print(err)
        #         break

        if path.exists(self.extract_dir):
            self.info = f"{COLORS['INFO']}binwalk extracted {self.__file_path} successfully{COLORS['RESET']}"
            print(self.info)  # TODO: change to logger
            self.extracted = True

    def __get_result_dir(self) -> str:
        """
        Get Expected Extraction Directorys

        Returns:
            str: expected extraction path
        """
        return self.__file_path.replace(path.basename(self.__file_path),
                                        f"_{path.basename(self.__file_path)}.extracted")
