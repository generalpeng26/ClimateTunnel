"""Polar plot of temperature"""

# pylint: disable=E1103

import os
import datetime

import numpy
import pandas

import matplotlib
matplotlib.use('Agg')

import matplotlib.animation as animation
import matplotlib.collections as collections
import matplotlib.pyplot as plt

plt.style.use('ggplot')

data_dir = 'data'

csv_filename = os.path.join(data_dir, 'nsidc_global_nt_final_and_nrt.txt')

data = pandas.read_csv(
    csv_filename,
    comment='#',
    infer_datetime_format=True,
    parse_dates=[0],
    skipinitialspace=True)

dates_without_year = [
    datetime.date(
        1980,
        x.month,
        x.day) for x in data.loc[:, 'date']]

years = [x.year for x in data.loc[:, 'date']]
unique_years = [
    years[i] for i in range(len(years)) if i == years.index(years[i])]
years = numpy.array(years)

days_from_1jan = [(x.date() - datetime.date(x.year, 1, 1)).days
                  for x in data.loc[:, 'date']]
thetas = numpy.array([float(x) / 365 * 2 * numpy.pi
                      for x in days_from_1jan])

areas = data['area'].values

fig = plt.figure(figsize=(9, 9))

ax = fig.add_subplot(1, 1, 1, projection='polar')

line = collections.LineCollection(
    [],
    linewidth=10,
    alpha=.2,
    cmap=plt.get_cmap('cool'),
    norm=plt.Normalize(
        12,
        30))

ax.add_collection(line)

title = ax.text(-0.11, 0.0, '', fontsize=50, transform=ax.transAxes)
caption1 = ax.text(-0.11,
                   1.1,
                   'Global sea ice area (M km2)',
                   fontsize=25,
                   transform=ax.transAxes)
caption2 = ax.text(-0.11,
                   1.025,
                   'data: https://sites.google.com/site/arctischepinguin/\n'
                   'code: https://github.com/wvangeit/ClimateTunnel',
                   fontsize=10,
                   transform=ax.transAxes)


ax.set_ylim([12, 24])
ax.set_xticks(2.0 * numpy.pi * numpy.linspace(0, 1, 12, endpoint=False))
ax.set_xticklabels(['Jan',
                    'Feb',
                    'Mar',
                    'Apr',
                    'May',
                    'Jun',
                    'Jul',
                    'Aug',
                    'Sep',
                    'Oct',
                    'Nov',
                    'Dec'], fontsize=20)

ax.set_yticks([12, 18, 24])
ax.set_yticklabels(['12', '18', '24 M Km2'], fontsize=20)


def init():
    """Init"""

    line.set_segments([])
    title.set_text('')
    return line, title


def animate(t):
    """Animate"""

    if t < len(unique_years):
        t_year = unique_years[t]

        print(t_year)

        t_thetas = thetas[numpy.where(years <= t_year)]
        t_rs = areas[numpy.where(years <= t_year)]

        points = numpy.array([t_thetas, t_rs]).T.reshape(-1, 1, 2)
        segments = numpy.concatenate([points[:-1], points[1:]], axis=1)

        title.set_text(str(t_year))
        line.set_segments(segments)
        line.set_array(t_rs)

    return line, title


ani = animation.FuncAnimation(
    fig,
    animate,
    frames=len(unique_years) + 30,
    init_func=init,
    blit=True,
    repeat=False)

print("Saving seaice gif ...")
ani.save('gifs/seaice.gif', dpi=60, writer='imagemagick')
