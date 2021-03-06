"""Get latest shakemap from server
"""

import os
import urllib2


class Shakemap_url:
    """Class to abstract url pairs for shakemap data

    Shakemap data urls come in pairs of the form with input and
    output data separate

    ftp://geospasial.bnpb.go.id/20110627235226.inp.zip
    ftp://geospasial.bnpb.go.id/20110627235226.out.zip

    This class represents these two urls along with the event name itself
    event_name: Name common to the two urls, e.g. '20110627235226'
     """

    def __init__(self, event_name, inputdata_url, outputdata_url):
        self.event_name = event_name
        self.inputdata_url = inputdata_url
        self.outputdata_url = outputdata_url

        assert self.event_name in self.inputdata_url
        assert self.event_name in self.outputdata_url

    def download_data(self, shakedata_dir):
        """Download input and output shakemap data
        """

        for url in [self.inputdata_url, self.outputdata_url]:
            filename = url.split('/')[-1]

            if os.path.isfile(filename):
                print 'Using existing shakemap file %s' % filename
            else:
                print 'Downloading shakemap file %s from %s' % (filename, url)

                # Get it
                cmd = 'wget %s > logs/get_%s.log' % (url, filename)
                print cmd
                os.system(cmd)

            # Unpack and move zip archives
            cmd = 'unzip -o %s > logs/unzip_%s.log' % (filename, filename)
            os.system(cmd)

            # Move to $SHAKEDATA
            cmd = ('cd usr/local/smap/data; '
                   '/bin/cp -rf %s %s' % (self.event_name,
                                          shakedata_dir))
            os.system(cmd)

            # Clean up
            cmd = '/bin/rm -rf %s; /bin/rm -rf usr' % filename
            os.system(cmd)

        print ('Shakemap data available in:'
               '%s' % (os.path.join(shakedata_dir, self.event_name)))
        return self.event_name


def get_shakemap_urls(url, name=None):
    """Get URLs for one shakemap

    Inputs
        url: URL where shakemap data is published.
        name: Optional parameter to select one event.
              If omitted, latest event will be used.

    Output
        Instance of class Shakemap_url containing
        event_name
    """

    print 'Reading shakemap data from %s' % url
    urls = _read_contents(url)

    if name is None:
        # Use the last one
        # Assume they are sorted. FIXME (Ole): Test this assumption.
        name = urls[-1].split('/')[-1].split('.')[0]
        print 'Getting urls for latest event, which is %s' % name
    else:
        print 'Getting urls for selected event %s' % name

    # Find the url pair for selected name
    inputdata_url = None
    outputdata_url = None
    for u in urls:
        if name in u:
            msg = ('Expected zip file for event %s. '
                   'Instead I got "%s"' % (name, u))
            assert u.endswith('.zip'), msg

            if u.endswith('inp.zip'):
                inputdata_url = u

            if u.endswith('out.zip'):
                outputdata_url = u

    if inputdata_url is None:
        msg = ('Expected input data url for event %s at %s but found '
               'nothing.' % (name, url))
        raise Exception(msg)

    if outputdata_url is None:
        msg = ('Expected output data url for event %s at %s but found '
               'nothing.' % (name, url))
        raise Exception(msg)

    print 'Found event %s in %s' % (name, url)
    return Shakemap_url(name, inputdata_url, outputdata_url)


def _get_shakemap_data(url, name=None, shakedata_dir=None):
    """Get shakemap from website

    Input
        url: URL where shakemap data is located
        name: Optional argument specifying which one is requested.
              If omitted, the latest will be used.

    If shakemap has already been downloaded, use local copy

    Shakemap data for one event are assumed to come in pairs:

    06-28-11  04:58PM                 1397 20110628165827.inp.zip
    06-28-11  04:58PM               759222 20110628165827.out.zip

    """

    S = get_shakemap_urls(url, name)
    S.download_data(shakedata_dir)
    return S.event_name


def get_shakemap_data(url, name=None, shakedata_dir=None):
    """Get shakemap from website unless already downloaded

    Input
        url: URL where shakemap data is located
        name: Optional argument specifying which one is requested.
              If omitted, the latest will be used.
        shakedata_dir: Optional argument specifying where to store shakedata
                       Default is './shakedata'

    If shakemap has already been downloaded, use local copy
    """

    if name is None:
        # Get latest shakemap (in case no event was specified)
        S = get_shakemap_urls(url, name)
        event_name = S.event_name
    else:
        if name.startswith(url):
            # Extract event name from URL if that is the case
            msg = 'Expected event name %s to end with .zip' % name
            assert name.endswith('.zip'), msg

            event_name = name.split('/')[-1]
            event_name = event_name.split('.')[0]
        else:
            # Else use name as provided
            event_name = name

    # Clean event_name just in case someone pasted a dirname
    if event_name.endswith('/'):
        event_name = event_name[:-1]

    if shakedata_dir is None:
        shakedata_dir = './shakedata'

    # If it doesn't already exist, try to get it from web site
    if os.path.isdir((os.path.join(shakedata_dir, event_name))):
        print ('Event %s already exists in %s, no need to download'
               % (event_name, shakedata_dir))
    else:
        print ('Downloading event %s from %s to %s'
               % (event_name, url, shakedata_dir))
        event_name = _get_shakemap_data(url,
                                        name=event_name,
                                        shakedata_dir=shakedata_dir)

    return event_name


def _read_contents(url):
    """Read contents of url

    Auxiliary function to read and return shakemap urls.
    Shakemap data comes in pairs of the form

    06-28-11  04:58PM                 1397 20110628165827.inp.zip
    06-28-11  04:58PM               759222 20110628165827.out.zip

    Input
        url: URL where shakemap data is published.
    Output:
        list of urls that can be used directly, e.g. with wget.

    """


    fid = urllib2.urlopen(url)

    urls = []
    for line in fid.readlines():
        fields = line.strip().split()
        if fields[-1].endswith('.zip'):
            urls.append(url + '/' + fields[-1])

    return urls


