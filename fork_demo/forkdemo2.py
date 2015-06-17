import os
import sys

PROCESSES_COUNT = 10


def do_children_work(num):
    print "CHILDREN #%d IN WORK..." % num


children = []


for process_num in range(PROCESSES_COUNT):
    PID = os.fork()
    if PID:
        children.append(PID)
    else:
        do_children_work(process_num)
        os._exit(0)

for child in children:
    os.waitpid(child, 0)

print "ALL CHILDREN PROCESSES IS OVER"