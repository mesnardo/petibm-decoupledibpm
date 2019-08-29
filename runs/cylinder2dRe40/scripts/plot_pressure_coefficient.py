"""Plot the surface pressure coefficient at final time step."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


name = 'p'  # name of the field variable to load
timestep = 5000  # final time-step index
show_figure = True  # if True, display the figure

# Set the simulation and data directories.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'solution'

# Load the gridlines from file.
filepath = simudir / 'grid.h5'
x, y = petibmpy.read_grid_hdf5(filepath, name)
# Load the field from file.
filepath = datadir / '{:0>7}.h5'.format(timestep)
p = petibmpy.read_field_hdf5(filepath, name)

# Load boundary coordinates from file.
filepath = simudir / 'cylinder.body'
xb, yp = petibmpy.read_body(filepath, skiprows=1)
nb = xb.size

# Define circle outside support region of delta function.
dx = 1.5 / 90  # grid-spacing in the uniform region
R = 0.5 + 3 * dx  # radius 3 cells away from real boundary
theta = numpy.linspace(0.0, 2 * numpy.pi, num=nb + 1)[:-1]
xc, yc = 0.0, 0.0
xb_ext, yb_ext = xc + R * numpy.cos(theta), yc + R * numpy.sin(theta)

# Interpolate the field on extended boundary.
pb = numpy.empty_like(xb_ext)
for i, (xbi, ybi) in enumerate(zip(xb_ext, yb_ext)):
    pi = petibmpy.linear_interpolation(p, y, ybi)
    pb[i] = petibmpy.linear_interpolation(pi, x, xbi)

# Compute the pressure coefficient.
rho = 1.0  # fluid density
U_inf = 1.0  # freestream speed
p_inf = 0.0  # far-away pressure
cp = (pb - p_inf) / (0.5 * rho * U_inf**2)

# Re-arrange values to split apart lower and upper surfaces.
cp_lower = numpy.append(cp[nb // 2:], [cp[-1]])
theta_lower = numpy.linspace(0.0, 180.0, num=cp_lower.size)
cp_upper = cp[:nb // 2 + 1][::-1]
theta_upper = numpy.linspace(0.0, 180.0, num=cp_upper.size)

# Load digitized values from Li et al. (2016).
rootdir = pathlib.Path(__file__).absolute().parents[3]
filepath = rootdir / 'data' / 'li_et_al_2016_cylinder2dRe40_cp.csv'
with open(filepath, 'r') as infile:
    theta_li, cp_li = numpy.loadtxt(infile, delimiter=',', unpack=True)

# Plot the distribution of the surface pressure coefficient.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.grid()
ax.set_xlabel(r'$\theta$')
ax.set_ylabel('$C_p$')
ax.plot(theta_lower, cp_lower, label='PetIBM (lower surface)')
ax.plot(theta_upper, cp_upper, label='PetIBM (upper surface)', linestyle='--')
ax.scatter(theta_li, cp_li, label='Li et al. (2016)',
           c='black', marker='s', s=10)
ax.legend(prop={'size': 12})
ax.set_xlim(0.0, 180.0)
ax.set_ylim(-1.5, 1.5)
fig.tight_layout()

# Save the figure.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'pressure_coefficient.png'
fig.savefig(filepath, dpi=300, bbox_inches='tight')

if show_figure:
    pyplot.show()
