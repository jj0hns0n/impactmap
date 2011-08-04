import os


def makedir(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well

    Based on
    http://code.activestate.com/recipes/82465/

    Note os.makedirs does not silently pass if directory exists.
    """

    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        msg = 'a file with the same name as the desired ' \
            'dir, "%s", already exists.' % newdir
        raise OSError(msg)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            makedir(head)
        #print "_mkdir %s" % repr(newdir)
        if tail:
            os.mkdir(newdir)

    return newdir


def make_pdf_filename(event_name):
    """Make pdf filename based on event name
    """

    filename = 'eartquake_impact_map_%s.pdf' % event_name
    return filename
