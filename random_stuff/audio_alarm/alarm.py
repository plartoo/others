"""
Description: Simple alarm script to play custom audio files periodically
for a pre-determined number of times. When time is up, the default
bell sound (audio) file, 'bell.m4a', is played. Important to make sure
that the audio file's length is not shorter than the interval ('-t')
time; otherwise, alarm file will be played at overlapping periods.

Created: Feb 5, 2021
"""
import argparse
import os
from random import randint
import time

DESC = """
Simple alarm script to play custom audio files periodically 
for a pre-determined number of times.
Usage:
> python alarm.py -t 300 -n 1
will trigger this alarm in the next five minutes once.
"""

T_FLAG_HELP_TEXT = """
Number of seconds to pause before the alarm sound file is played. 
For example, to play this alarm once a minute for five minutes, type:
> python alarm.py -t 60 -n 5
"""

N_FLAG_HELP_TEXT = """Number of times this alarm must be played (periodically). 
For example, if you want this alarm to be triggered every minute for an hour, 
you'd run the program like this:
> python alarm.py -t 60 -n 60
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=T_FLAG_HELP_TEXT,
        formatter_class=argparse.RawTextHelpFormatter,
        usage=argparse.SUPPRESS)
    parser.add_argument('-t', required=True, type=int,
                        help=T_FLAG_HELP_TEXT)
    parser.add_argument('-n', required=True, type=int,
                        help=N_FLAG_HELP_TEXT)
    args = parser.parse_args()

    if args.t:
        counter = 0
        while counter < args.n:
            counter += 1
            # audio_file_to_play = ''.join([str(randint(1, 3)), '.m4a'])
            audio_file_to_play = 'bell.m4a'
            time.sleep(args.t)
            os.system(audio_file_to_play)
            time.sleep(1)
            print(f"Alarm triggered this many times every {args.t} seconds: {counter}")

    else:
        print("Provide number of seconds to wait before triggering the alarm. Usage: python alarm -t 60")
