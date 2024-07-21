from concurrent.futures import ProcessPoolExecutor
from flagger.modules.banner import palestine
from flagger.flagger import Flagger
from flagger.modules import utils
from signal import signal, SIGINT, SIGTERM
from os import getpid, killpg


def main():
    executor = ProcessPoolExecutor()
    print(palestine)
    args = utils.parse_arguments()
    Flagger.flag_format = args.flag_format  # set the flag format for the class (all the instances)
    # I added the previous line here to be executed at the first instance only
    # , if it's in the constructor it will be executed in each instance initiation
    Flagger.verbose = args.verbose
    Flagger.silent = args.silent
    with ProcessPoolExecutor(max_workers=15) as executor:
        executor.submit(Flagger, args.file_name, args.no_rot)


def terminate_all_processes(sig, frame):
    killpg(getpid(), SIGTERM)


if __name__ == '__main__':
    signal(SIGINT, terminate_all_processes)
    main()


