"""Generate variable components for LaTeX file
"""


def generate_event_header(event_info):
    """Generate header with event statistics

    Input
        event_info: Dictionary with event parameters

    Output
        filename: Name of generated LaTeX file with contents like

\begin{tabular}{@{}lr}
  {\Large \textbf{Mag: 7.8 SR 29-Jan-11 23:40:20 WIB}} & \large Versi 1\\
  {\Large \textbf{Lintang: 4.045$^\circ$ Garis bujur: 97.066$^\circ$ Kedalaman: 10.0km}}&\\
  {\Large \textbf{115 km BaratDaya GUNUNGSITOLISUMUT}} &
  \scriptsize Dibuat 36 minggu, 2 hari setelah gempa\\
\end{tabular}

    """

    filename = 'event_statistics.tex'  # Must match main LaTeX file

    mag_str = 'M %s SR' % event_info['mag']
    date_str = '%s-%s-%s %s %s' % (event_info['day'],
                                   event_info['month'].title(),
                                   event_info['year'][2:],
                                   event_info['time'],
                                   event_info['time-zone'])

    version_str = 'Versi 1'  # FIXME (Ole): Still need to do this

    lat_str = 'Lintang: %s$^\circ$' % event_info['lat']
    lon_str = 'Garis bujur: %s$^\circ$' % event_info['lon']
    dep_str = 'Kedalaman: %skm' % event_info['depth']
    loc_str = '%s' % event_info['location']
    # FIXME: We want: 115 km BaratDaya Bandung

    fid = open(filename, 'w')
    fid.write('\\begin{tabular}{@{}lr}\n')
    fid.write('  {\Large \\textbf{%s %s}} & \large %s\\\\ \n' % (mag_str,
                                                                 date_str,
                                                                 version_str))
    fid.write('  {\Large \\textbf{%s %s %s}}&\\\\ \n' % (lat_str,
                                                         lon_str,
                                                         dep_str))
    fid.write('  {\Large \\textbf{%s}} & \n' % loc_str)

    # FIXME: Still need to calculate time after earthquake (easy, though)
    fid.write('  \scriptsize Dibuat X minggu, Y hari setelah gempa\\\\ \n')

    fid.write('\\end{tabular}')
    fid.close()

    return filename
