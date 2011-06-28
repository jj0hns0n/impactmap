"""Get latest shakemap from server
"""

import os
import urllib2

url = 'ftp://geospasial.bnpb.go.id'
shakedata = os.environ['SHAKEDATA']

def read_contents(url):
    """Read contents of url

    Return contents as a list of urls
    """


    print 'Reading data from %s' % url
    fid = urllib2.urlopen(url)

    urls = []
    for line in fid.readlines():
        fields = line.strip().split()
        if fields[-1].endswith('out.zip'):
            urls.append(url + '/' + fields[-1])

    return urls

def get_latest_shakemap(url):
    """Get newest shakemap.
    If already downloaded, do nothing
    """

    urls = read_contents(url)

    # Assume they are sorted. FIXME (Ole): Test this assumption.
    latest = urls[-1]

    filename = latest.split('/')[-1]

    if os.path.isfile(filename):
        print 'Shakemap %s already exists' % filename
    else:
        print 'Downloading shakemap %s from %s' % (filename, url)

        # Get out.zip
        cmd = 'wget %s > logs/get_shakemap_output.log' % latest
        print cmd
        os.system(cmd)

        # Get inp.zip
        cmd = 'wget %s > logs/get_shakemap_input.log' % latest.replace('out', 'inp')
        print cmd
        os.system(cmd)

    return filename

def unpack(filename):
    """Extract shake map data from archive and move to $SHAKEDATA directory
    """

    # Get timestamp
    fields = filename.split('.')
    name = fields[0]

    print 'Unzipping shakemap data: %s' % name
    # Unpack out.zip file
    cmd = 'unzip -o %s > logs/unzip_shakemap_output.log' % filename
    os.system(cmd)

    # Unpack inp.zip file
    inpfilename = filename.replace('out', 'inp')
    cmd = 'unzip -o %s > logs/unzip_shakemap_input.log' % inpfilename
    os.system(cmd)

    # Move to $SHAKEDATA
    cmd = 'cd usr/local/smap/data; /bin/cp -rf %s %s' % (name, shakedata)
    print cmd
    os.system(cmd)

    return name
