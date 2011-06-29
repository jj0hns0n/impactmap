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


def generate_exposure_table(event_info, pop_expo):
    """Generate table of people exposed to different MMI levels

    Input
        event_info: Dictionary with event parameters

    Output
        filename: Name of generated LaTeX file with contents like

\begin{tabular}{|c|c|c|c|c|c|c|c|c|}
  \hline
  \multicolumn{9}{|c|}{\rule{0pt}{4mm} \Large \textbf{Estimasi penduduk terexpos pada tingkat getaran yang berbeda}} \\
   \hline
  \hline
  \textbf{Intensitas (MMI)} &
  \cell{II}{II} &
  \cell{III}{III} &
  \cell{IV}{IV} &
  \cell{V}{V} &
  \cell{VI}{VI} &
  \cell{VII}{VII} &
  \cell{VIII}{VIII} &
  \cell{IX}{IX}\\ \hline
  \textbf{Populasi} &
  0 & 6921 & 8864 & 1367 & 472 & 16 & 0 & 0 \\ \hline
  \textbf{Persepsi Gemetar} &
  Lemah & Lemah & Cahaya & Moderat & Kuat & Sangat Kuat & Parah & Keras   \\
  \noalign{\hrule height 0.6pt}
\end{tabular}

    """

    # Convert absolute numbers to units of a thousand (k)
    pop_str = {}
    for key in pop_expo:
        x = pop_expo[key]
        if x > 1000:
            pop_str[key] = '%ik' % round(x/1000)
        else:
            pop_str[key] = '%i' % x


    # Generate LaTeX code
    filename = 'exposure_table.tex'  # Must match main LaTeX file

    fid = open(filename, 'w')
    fid.write('\\begin{tabular}{|c|c|c|c|c|c|c|c|c|} \n')
    fid.write('\\hline \n')
    fid.write('\\multicolumn{9}{|c|}{\\rule{0pt}{4mm} \\Large '
              '\\textbf{Estimasi penduduk terexpos pada tingkat '
              'getaran yang berbeda}} \\\\ \n')
    fid.write('\\hline \n')
    fid.write('\\hline \n')
    fid.write('\\textbf{Intensitas (MMI)} & \n')
    fid.write('\\cell{II}{II} & \n')
    fid.write('\\cell{III}{III} & \n')
    fid.write('\\cell{IV}{IV} & \n')
    fid.write('\\cell{V}{V} & \n')
    fid.write('\\cell{VI}{VI} & \n')
    fid.write('\\cell{VII}{VII} & \n')
    fid.write('\\cell{VIII}{VIII} & \n')
    fid.write('\\cell{IX}{IX}\\\\ \\hline \n')
    fid.write('\\textbf{Populasi} & \n')
    fid.write('%s & %s & %s & %s & %s & %s & %s & %s \\\\ \hline'
              '\n' % (pop_str['II'],
                      pop_str['III'],
                      pop_str['IV'],
                      pop_str['V'],
                      pop_str['VI'],
                      pop_str['VII'],
                      pop_str['VIII'],
                      pop_str['IX']))
    fid.write('\\textbf{Persepsi Gemetar} & \n')
    fid.write('Lemah & Lemah & Cahaya & Moderat & Kuat & Sangat Kuat & Parah & Keras   \\\\ \n')
    fid.write('\\noalign{\\hrule height 0.6pt} \n')
    fid.write('\\end{tabular} \n')

    fid.close()

    return filename
