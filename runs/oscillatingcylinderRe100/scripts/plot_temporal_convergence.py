"""Plot the temporal convergence for the streamwise velocity components."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


rootdir = pathlib.Path(__file__).absolute().parents[1]

name = 'u'  # name of the variable for the x-velocity
f = 0.2  # oscillation frequency
T = 1 / f  # oscillation period
t = 0.4 * T  # time value to monitor

u = []
folders = ['algo1-dt=0.01', 'algo1-dt=0.005', 'algo1',
           'algo1-dt=0.001', 'algo1-dt=0.0005']
dt = [0.01, 0.005, 0.002, 0.001, 0.0005]
for d, folder in zip(dt, folders):
    timestep = int(t / d)
    print(timestep)
    simudir = rootdir / folder
    filepath = simudir / 'solution' / '{:0>7}.h5'.format(timestep)
    u.append(petibmpy.read_field_hdf5(filepath, name))

l2_errors, linf_errors = [], []
for i in range(len(u) - 1):
    l2 = numpy.sqrt(numpy.sum((u[i] - u[-1])**2))
    l2_errors.append(l2)
    linf = numpy.max(numpy.abs(u[i] - u[-1]))
    linf_errors.append(linf)

pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.grid()
ax.set_xlabel(r'$\Delta t$')
ax.set_ylabel('Temporal error ($u$)')
ax.loglog(dt[:-1], linf_errors, label=r'$L_\infty$',
          color='black', marker='s')
ax.loglog(dt[:-1], l2_errors, label='$L_2$',
          color='black', marker='s', markerfacecolor='none')
first = linf_errors[0] / dt[0] * numpy.array(dt[:-1])
second = l2_errors[0] / dt[0]**2 * numpy.array(dt[:-1])**2
ax.loglog(dt[:-1], first, label=r'$1^{st}$-order',
          color='black', linestyle='--')
ax.loglog(dt[:-1], second, label=r'$2^{st}$-order',
          color='black', linestyle=':')
ax.legend(prop={'size': 12})
ax.axis('scaled', adjustable='box')
ax.set_xlim(5e-4, 5e-2)
fig.tight_layout()

# Save the figure.
figdir = rootdir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'temporal_error.png'
fig.savefig(filepath, dpi=300)

pyplot.show()
