import pathlib
import numpy
from matplotlib import pyplot


def read_drag_coefficient(filepath):
    """Read the forces from file and returns the drag coefficient.

    Arguments
    ---------
    filepath: str or pathlib.Path object
        The path of the file with the forces.

    Returns
    -------
    data: dict
        History of the drag coefficient.
    """
    data = {}
    with open(filepath, 'r') as infile:
        t, fx = numpy.loadtxt(infile, dtype=numpy.float64,
                              unpack=True, usecols=(0, 1))
    KC = 5.0
    D = 1.0
    f = 0.2
    w = 2 * numpy.pi * f
    Am = KC * D / (2 * numpy.pi)
    rho = 1.0
    Um = w * Am
    V = numpy.pi * D**2 / 4
    ax = w**2 * Am * numpy.sin(w * t)
    fx += rho * V * ax
    cd = fx / (0.5 * rho * Um**2 * D)
    data['t'], data['cd'] = f * t, cd
    return data


root_dir = pathlib.Path(__file__).parents[1]

simus = {}

# Get drag coefficient obtained with algo 1 and scheme 3.
label = 'Algo 1'
filepath = root_dir / 'algo1_scheme3' / 'forces-0.txt'
simus[label] = read_drag_coefficient(filepath)

# Get drag coefficient obtained with algo 2 and scheme 3.
label = 'Algo 2'
filepath = root_dir / 'algo2_scheme3' / 'forces-0.txt'
simus[label] = read_drag_coefficient(filepath)

# Get drag coefficient obtained with algo 3 and scheme 3.
label = 'Algo 3'
filepath = root_dir / 'algo3_scheme3' / 'forces-0.txt'
simus[label] = read_drag_coefficient(filepath)

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0))
ax.grid()
ax.set_xlabel('$t / T$')
ax.set_ylabel('$C_D$')
for label, simu in simus.items():
    ax.plot(simu['t'], simu['cd'], label=label)
ax.legend(ncol=3)
ax.axis((0.0, 4.0, -6.0, 6.0))
fig.tight_layout()

# Save the figure.
fig_dir = root_dir / 'figures'
fig_dir.mkdir(parents=True, exist_ok=True)
filepath = fig_dir / 'dragCoefficient.png'
fig.savefig(str(filepath), dpi=300)

pyplot.show()
