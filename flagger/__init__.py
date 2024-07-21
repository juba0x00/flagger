from concurrent.futures import ProcessPoolExecutor
from flagger.modules.banner import palestine
from flagger.flagger import Flagger
from flagger.modules import utils

import sys
def main():
    print(palestine)
    args = utils.parse_arguments()
    Flagger.flag_format = args.flag_format  # set the flag format for the class (all the instances)
    # I added the previous line here to be executed at the first instance only
    # , if it's in the constructor it will be executed in each instance initiation
    Flagger.verbose = args.verbose
    Flagger.silent = args.silent

    with ProcessPoolExecutor() as executor:
        executor.submit(Flagger, args.file_name, args.no_rot)

    # Process(target=Flagger, args=(args.file_name, args.no_rot)).start()  # create an instance of the class


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # kill all the child processes and threads
        #TODO
        ...
