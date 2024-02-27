import sys
import time

def progress_bar(progress):
    bar_length = 100
    filled_length = int(round(bar_length * progress))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write('\r' + '[{}] {:.0%}'.format(bar, progress))
    sys.stdout.flush()

for i in range(101):
    progress = i / 100
    progress_bar(progress)
    time.sleep(0.05)
