from twisted.internet.defer import Deferred
from twisted.python.failure import Failure


def on_success_callback(res):
    res = "'SUCCESS RES: %s'" % str(res)
    print "   on_success_callback:", res
    return res


def final_sucess_callback(res):
    print " final_sucess_callback: < %s >" % str(res)


def on_error_callback(failure):
    #print "ERROR: ", str(failure)
    failure.trap(RuntimeError)
    return 0


def deferred_demo():
    d = Deferred()
    d.addCallback(on_success_callback)
    d.addCallback(final_sucess_callback)
    d.addErrback(on_error_callback)
    d.callback("FOO")

    #d.errback()
    d.errback(Failure(Exception("unknown error")))

if __name__ == "__main__":
    deferred_demo()
