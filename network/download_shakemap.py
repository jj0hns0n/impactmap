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

    print 'Opening %s' % url
    fid = urllib2.urlopen(url)

    print 'Reading %s' % url
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
        cmd = 'wget %s' % latest
        print cmd
        os.system(cmd)

        # Get inp.zip
        cmd = 'wget %s' % latest.replace('out', 'inp')
        print cmd
        os.system(cmd)

    return filename

def unpack(filename):
    """Extract shake map data from archive and move to $SHAKEDATA directory
    """

    # Get timestamp
    fields = filename.split('.')
    name = fields[0]

    # Unpack out.zip file
    cmd = 'unzip -o %s' % filename
    print cmd
    os.system(cmd)

    # Move to $SHAKEDATA
    cmd = 'cd usr/local/smap/data; mv %s %s' % (name, shakedata)
    print cmd
    os.system(cmd)

    # Unpack inp.zip file
    inpfilename = filename.replace('out', 'inp')
    cmd = 'unzip -o %s' % inpfilename
    print cmd
    os.system(cmd)

    # Move to $SHAKEDATA
    cmd = 'cd usr/local/smap/data/%s; mv input %s/%s' % (name, shakedata, name)
    print cmd
    os.system(cmd)

    # Copy grd file down
    cmd = 'cd %s; /bin/cp %s/%s/output/grid.xyz .' % (shakedata, shakedata, name)
    print cmd
    os.system(cmd)

    return name


def run_impact_map(name):
    """Run impact map
    """

    cmd = 'python PopExposureMap.py %s' % name
    print cmd
    os.system(cmd)

if __name__ == '__main__':

    filename = get_latest_shakemap(url)
    name = unpack(filename)
    run_impact_map(name)

