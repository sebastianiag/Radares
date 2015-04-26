import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv
from argparser import ArgumentParser
from numpy import exp, sqrt


parser = ArgumentParser()
parser.add_argument("--Er", type=str, help="complex relative permitivity")
args = parser.parse_args()

Er = np.complex(args.Er)
x_axis = np.arange(0, 1000, 0.01)

for size in x_axis:
    rho = size*sqrt(Er)
    alpha01n = rho*
