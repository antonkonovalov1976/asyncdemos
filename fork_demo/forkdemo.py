import os

PID = os.fork()

if PID > 0:
    print "I AM THE CHILD"
else:
    print "I AM THE PARENT"


