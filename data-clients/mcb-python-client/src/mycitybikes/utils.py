
# http://tomayko.com/writings/cleanest-python-find-in-list-function

## Python 2.6
#def index(seq, f):
#    """Return the index of the first item in seq where f(item) == True."""
#    return next((i for i in xrange(len(seq)) if f(seq[i])), None)

# Python 2.5 or 2.4
def index(seq, f):
    """Return the index of the first item in seq where f(item) == True."""
    for index in (i for i in xrange(len(seq)) if f(seq[i])):
        return index
