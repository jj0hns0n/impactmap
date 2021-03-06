"""Generate variable components for LaTeX file
"""

from datetime import datetime
import locale
import pytz

# Why do I have to write this and why can't datetime understand 'JUN'?
# Anyway, this table will be hand for translating to Bahasa Indonesia
month2int = {'JAN': 1,
             'FEB': 2,
             'MAR': 3,
             'APR': 4,
             'MAY': 5,
             'JUN': 6,
             'JUL': 7,
             'AUG': 8,
             'SEP': 9,
             'OCT': 10,
             'NOV': 11,
             'DEC': 12}


def generate_event_header(event_info):
    """Generate header with event statistics

    Input
        event_info: Dictionary with event parameters

    Output
        filename: Name of generated LaTeX file with contents like

\begin{tabular}{@{}lr}
  {\Large \textbf{Mag: 7.8 SR 29-Jan-11 23:40:20 WIB}} & \large \flushright Versi 1\\
  {\Large \textbf{Lintang: 4.045$^\circ$ Garis bujur: 97.066$^\circ$ Kedalaman: 10.0 km}}&\\
  {\Large \textbf{115 km BaratDaya GUNUNGSITOLISUMUT}} &
  \scriptsize Dibuat 36 minggu, 2 hari setelah gempa\\
\end{tabular}

    """

    # Extract date and time info
    # FIXME (Ole): This ought to be done when first obtained)
    day = event_info['day']
    month_str = event_info['month'].title()  # FIXME: make translation table
    time_str = event_info['time']
    time_zone = event_info['time-zone']
    msg = ('Assumed GMT in shakemap data. If this has changed this '
           'code must change also.')
    assert time_zone == 'GMT', msg

    # Work out interval since earthquake (assume both are GMT)
    year = int(event_info['year'])
    month = month2int[month_str.upper()]
    day = int(event_info['day'])
    hour, minute, second = [int(x) for x in time_str.split(':')]

    eq_date = datetime(year, month, day, hour, minute, second)
    time_delta = datetime.utcnow() - eq_date

    # Hack - remove when ticket:10 has been resolved
    tz = pytz.timezone('Asia/Jakarta')  # Or 'Etc/GMT+7'
    now = datetime.utcnow()
    now_jakarta = now.replace(tzinfo=pytz.utc).astimezone(tz)
    eq_jakarta = eq_date.replace(tzinfo=tz).astimezone(tz)
    time_delta = now_jakarta - eq_jakarta

    # Work out string to report time elapsed after quake
    if time_delta.days == 0:
        # This is within the first day after the quake
        hours = int(time_delta.seconds / 3600)
        minutes = int((time_delta.seconds % 3600) / 60)

        if hours == 0:
            lapse_string = '%i menit' % minutes
        else:
            lapse_string = '%i jam %i menit' % (hours, minutes)
    else:
        # This at least one day after the quake

        weeks = int(time_delta.days / 7)
        days = int(time_delta.days % 7)

        if weeks == 0:
            lapse_string = '%i hari' % days
        else:
            lapse_string = '%i minggu %i hari' % (weeks, days)

    # Convert date to GMT+7
    # FIXME (Ole) Hack - Remove this as the shakemap data always
    # reports the time in GMT+7 but the timezone as GMT.
    # This is the topic of ticket:10
    #tz = pytz.timezone('Asia/Jakarta')  # Or 'Etc/GMT+7'
    #eq_date_jakarta = eq_date.replace(tzinfo=pytz.utc).astimezone(tz)
    eq_date_jakarta = eq_date

    # The character %b will use the local word for month
    # However, setting the locale explicitly to test, does not work.
    #locale.setlocale(locale.LC_TIME, 'id_ID')

    date_str = eq_date_jakarta.strftime('%d-%b-%y %H:%M:%S %Z')

    filename = 'event_statistics.tex'  # Must match main LaTeX file

    mag_str = 'M %s' % event_info['mag']
    version_str = 'Versi 1'  # FIXME (Ole): Still need to do this

    lat_str = 'Lintang: %s$^\circ$' % event_info['lat']
    lon_str = 'Bujur: %s$^\circ$' % event_info['lon']
    dep_str = 'Kedalaman: %s km' % event_info['depth']
    loc_str = '%s' % event_info['location_string']

    fid = open(filename, 'w')
    fid.write('\\begin{tabular}{@{}lr@{}}\n')
    fid.write('  {\Large \\textbf{%s %s}} & \large %s\\\\ \n' % (mag_str,
                                                                 date_str,
                                                                 version_str))
    fid.write('  {\Large \\textbf{%s %s %s}}&\\\\ \n' % (lat_str,
                                                         lon_str,
                                                         dep_str))
    fid.write('  {\Large \\textbf{%s}} & \n' % loc_str)
    fid.write('  \small Dibuat %s sesudah gempa\\\\ \n' % lapse_string)
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
  \multicolumn{9}{|c|}{\rule{0pt}{4mm} \Large \textbf{Perkiraan penduduk terpapar pada tingkat getaran yang berbeda}} \\
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
  \textbf{Penduduk (k = x1000)} &
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
        if x == 0:
            pop_str[key] = '$0$'
        elif x <= 1000:
            pop_str[key] = '$\le1$'
        else:
            pop_str[key] = '$%i$' % int(x/1000)


    # Generate LaTeX code
    filename = 'exposure_table.tex'  # Must match main LaTeX file

    fid = open(filename, 'w')
    fid.write('\\begin{tabular}{|l|c|c|c|c|c|c|c|c|} \n')
    fid.write('\\hline \n')
    fid.write('\\multicolumn{9}{|c|}{\\rule{0pt}{4mm} \\Large '
              '\\textbf{Perkiraan jumlah penduduk terpapar pada setiap tingkat '
              'getaran berbeda}} \\\\ \n')
    fid.write('\\hline \n')
    fid.write('\\hline \n')
    fid.write('\\textbf{Intensitas {\scriptsize (MMI)}} & \n')
    fid.write('\\cell{II}{II} & \n')
    fid.write('\\cell{III}{III} & \n')
    fid.write('\\cell{IV}{IV} & \n')
    fid.write('\\cell{V}{V} & \n')
    fid.write('\\cell{VI}{VI} & \n')
    fid.write('\\cell{VII}{VII} & \n')
    fid.write('\\cell{VIII}{VIII} & \n')
    fid.write('\\cell{IX}{IX}\\\\ \\hline \n')
    fid.write('\\textbf{Penduduk {\scriptsize (x1000)}} & \n')
    fid.write('%s & %s & %s & %s & %s & %s & %s & %s \\\\ \hline'
              '\n' % (pop_str['II'],
                      pop_str['III'],
                      pop_str['IV'],
                      pop_str['V'],
                      pop_str['VI'],
                      pop_str['VII'],
                      pop_str['VIII'],
                      pop_str['IX']))
    fid.write('\\textbf{Getaran Dirasakan} & \n')
    fid.write('Lemah & Lemah & Agak Lemah & Sedang & Kuat & Sangat Kuat & Keras & Sangat Keras  \\\\ \n')
    fid.write('\\noalign{\\hrule height 0.6pt} \n')
    fid.write('\\end{tabular} \n')

    fid.close()

    return filename
