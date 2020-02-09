"""Plot the surface pressure coefficient at final time step."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

import rodney


def get_pressure(simudir, timestep):
    name = 'p'  # name of the field variable to load
    datadir = simudir / 'output'
    # Load the gridlines from file.
    filepath = datadir / 'grid.h5'
    x, y = petibmpy.read_grid_hdf5(filepath, name)
    # Load the field from file.
    filepath = datadir / f'{timestep:0>7}.h5'
    p = petibmpy.read_field_hdf5(filepath, name)
    return (x, y), p


def compute_surface_pressure_coefficient(p, x, y):
    # Define circle outside support region of delta function.
    N = 500
    dx = 1.5 / 90  # grid-spacing size in the uniform region
    R = 0.5 + 3 * dx  # radius 3 cells away from real boundary
    theta = numpy.linspace(0.0, 2 * numpy.pi, num=N + 1)[:-1]
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
    return theta, cp


def split_lower_upper(theta, cp):
    mask = numpy.where((theta >= numpy.pi) & (theta < 2 * numpy.pi))[0]
    theta_lower = theta[mask] % numpy.pi
    cp_lower = cp[mask]
    mask = numpy.where((theta >= 0.0) & (theta < numpy.pi))[0]
    theta_upper = numpy.flip(numpy.pi - theta[mask])
    cp_upper = numpy.flip(cp[mask])
    return (dict(theta=theta_lower, cp=cp_lower),
            dict(theta=theta_upper, cp=cp_upper))


args = rodney.parse_command_line()
maindir = pathlib.Path(__file__).absolute().parents[1]
timestep = 5000  # final time-step index

label1 = r'500 markers ($\Delta s \approx 0.38 \Delta x$)'
simudir1 = maindir / '500_markers'
grid, p = get_pressure(simudir1, timestep)
theta, cp = compute_surface_pressure_coefficient(p, *grid)
lower1, upper1 = split_lower_upper(theta, cp)

label2 = r'189 markers ($\Delta s \approx \Delta x$)'
simudir2 = maindir / '189_markers'
grid, p = get_pressure(simudir2, timestep)
theta, cp = compute_surface_pressure_coefficient(p, *grid)
lower2, upper2 = split_lower_upper(theta, cp)

# Plot the distribution of the surface pressure coefficient.
pyplot.rc('font', family='serif', size=14)
fig, (ax1, ax2) = pyplot.subplots(ncols=2, figsize=(10.0, 4.0))
ax1.set_title(label1, fontsize=14)
ax1.set_xlabel(r'$\theta$')
ax1.set_ylabel('$C_p$')
ax1.plot(numpy.degrees(lower1['theta']), lower1['cp'],
         label='lower surface')
ax1.plot(numpy.degrees(upper1['theta']), upper1['cp'],
         label='upper surface', linestyle='--')

ax2.set_title(label2, fontsize=14)
ax2.set_xlabel(r'$\theta$')
ax2.set_ylabel('$C_p$')
ax2.plot(numpy.degrees(lower2['theta']), lower2['cp'],
         label='lower surface')
ax2.plot(numpy.degrees(upper2['theta']), upper2['cp'],
         label='upper surface', linestyle='--')

if args.extra_data:
    # Load digitized values from Li et al. (2016).
    theta_li, cp_li = rodney.lietal2016_load_cp(40)
    ax1.scatter(theta_li, cp_li, label='Li et al. (2016)',
                c='black', marker='s', s=10)
    ax2.scatter(theta_li, cp_li, label='Li et al. (2016)',
                c='black', marker='s', s=10)

for ax in (ax1, ax2):
    ax.set_xlim(0.0, 180.0)
    ax.set_ylim(-1.5, 1.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

ax2.legend(frameon=False)
fig.tight_layout()

if args.save_figures:
    # Save the figure.
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / f'cp_{timestep:0>7}.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
