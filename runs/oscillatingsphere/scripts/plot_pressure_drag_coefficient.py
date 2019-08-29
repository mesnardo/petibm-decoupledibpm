"""Plot the surface pressure coefficient from last probe record."""

import math
from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

from kinematics import dt, Am, f, D, nt_period, rho


def create_sphere(delta, R=0.5, center=(0.0, 0.0, 0.0)):
    xc, yc, zc = center
    # North pole.
    x, y, z = xc, yc, zc + R
    # Between poles.
    n_phi = math.ceil(numpy.pi * R / delta)
    phi_angles = numpy.linspace(0.0, numpy.pi, num=n_phi)[1:-1]
    for phi in phi_angles:
        rsinphi = R * math.sin(phi)
        rcosphi = R * math.cos(phi)
        n_theta = math.ceil(2 * numpy.pi * rsinphi / delta)
        theta = numpy.linspace(0.0, 2.0 * numpy.pi, num=n_theta + 1)[:-1]
        x = numpy.append(x, xc + rsinphi * numpy.cos(theta))
        y = numpy.append(y, yc + rsinphi * numpy.sin(theta))
        z = numpy.append(z, zc + rcosphi * numpy.ones(n_theta))
    # South pole.
    x = numpy.append(x, xc)
    y = numpy.append(y, yc)
    z = numpy.append(z, zc - R)
    return x, y, z


name = 'p'  # name of the field variable to load
show_figure = True  # if True, display the figure

# Set the simulation and data directories.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'solution'

nstart, nend = 2000, 2500
times = dt * numpy.arange(nstart, nend + 1, 10)

dx = 4.0 / 256
dA = dx**2
cpd = numpy.zeros_like(times)
for index, time in enumerate(times):
    print(time)
    # Load data from last record of the probe.
    filepath = datadir / 'probe-p.h5'
    (x, y, z), p = petibmpy.read_probe_volume_hdf5(filepath, name, time)
    # Generate a sphere outside the support region of the delta function.
    xc, yc, zc = Am * numpy.sin(2 * numpy.pi * f * time), 0.0, 0.0
    xb, yb, zb = create_sphere(dx, R=(D / 2 + 2 * dx), center=(xc, yc, zc))
    pb = numpy.empty_like(xb)
    for i, (xbi, ybi, zbi) in enumerate(zip(xb, yb, zb)):
        pi = petibmpy.linear_interpolation(p, z, zbi)
        pi = petibmpy.linear_interpolation(pi, y, ybi)
        pb[i] = petibmpy.linear_interpolation(pi, x, xbi)
        d = numpy.sqrt((xbi - xc)**2 + (ybi - yc)**2 + (zbi - zc)**2)
        n = numpy.array([xbi - xc, ybi - yc, zbi - zc]) / d
        cpd[index] -= pb[i] * n[0]
    cpd[index] *= dA / (0.5 * rho * D**3 * f**2)

# Plot the history of the pressure drag coefficient.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.set_xlabel(r'$t / T$')
ax.set_ylabel(r'$C_{PD}$')
ax.plot(f * times , cpd, color='black', marker='o')
# ax.set_xlim(0.0, 180.0)
ax.set_ylim(-4.0, 4.0)
fig.tight_layout()

# Save the figure.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'pressure_drag_coefficient.png'
fig.savefig(filepath, dpi=300)

if show_figure:
    pyplot.show()
