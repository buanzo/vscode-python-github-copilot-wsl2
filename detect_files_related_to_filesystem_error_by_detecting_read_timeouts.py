# This script will, for each argument which is a filename:
# 1. Open the file for reading in binary mode
# 2. According to file size, determine a suitable chunk size
# 3. Read the file in chunks of that size
# 4. If the read() call blocks for more than 10 seconds,
#    print the filename in warning color.
# 5. If the read() call blocks for less than 10 seconds,
#    print the filename in success color.
# 6. Finally, close the file.
# This script attempts to determine which files are blocking for a
# long time when reading, either from logical or physical errors.

import sys
import os
import time

from pprint import pprint


def main():
    for filename in sys.argv[1:]:
        if not os.path.isfile(filename):
            print(f"Warning: {filename} is not a file",
                  file=sys.stderr)
            continue
        with open(filename, "rb") as f:
            chunk_size = 1024 * 1024
            if os.path.getsize(filename) > 1024 * 1024 * 1024:
                chunk_size = 1024 * 1024 * 1024
            elif os.path.getsize(filename) > 1024 * 1024 * 1024 * 10:
                chunk_size = 1024 * 1024 * 1024 * 10
            while True:
                start_time = time.time()
                try:
                    data = f.read(chunk_size)
                except Exception as e:
                    # Ignore errors, but print filename and
                    # the exception details:
                    print("\033[91m{}\033[0m".format(filename))
                    pprint(e)
                    pass
                end_time = time.time()
                if end_time - start_time > 10:
                    print("\033[93m{}\033[0m".format(filename))
                    break
                if len(data) < chunk_size:
                    print("\033[92m{}\033[0m".format(filename))
                    break


if __name__ == "__main__":
    main()
