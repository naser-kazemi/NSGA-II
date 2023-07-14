from pymoo.problems import get_problem
from moop import MOOP

import matplotlib.pyplot as plt
from utils import *
from nsga2 import NSGA2
import math


def main():
    problem = get_problem("zdt2")
    lower_bound = problem.xl
    upper_bound = problem.xu

    # create a new NSGA2 instance
    # create two objectives
    f1 = lambda x: x[0]
    g = lambda x: 1 + 9 * sum(x[1:]) / (len(x) - 1)
    # f2 = lambda x: g(x) * (1 - np.sqrt(x[0] / g(x)))
    f2 = lambda x: g(x) * (1 - (x[0] / g(x)) ** 2)
    # f2 = lambda x: g(x) * (1 - math.sqrt(x[0] / g(x)) - (x[0] / g(x)) * math.sin(10 * math.pi * x[0]))
    objectives = [f1, f2]

    moop = MOOP(problem.n_var, objectives, problem.pareto_front(), lower_bound, upper_bound)

    nsga2 = NSGA2(moop, 100, 250, 0.9, 20, 20)

    # run the algorithm
    nsga2.run()

    front = np.array(nsga2.fast_non_dominated_sort(nsga2.population)[0])
    front = np.array([member.objective_values for member in front])
    distance_mean, distance_std = nsga2.evaluate_distance_metric()
    print("Distance metric mean: ", distance_mean)
    print("Distance metric std: ", distance_std)
    diversity = nsga2.evaluate_diversity_metric()
    print("Diversity metric: ", diversity)

    # plot the results and save the figure
    plt.scatter(problem.pareto_front()[:, 0], problem.pareto_front()[:, 1], color="red", label="Pareto Front")
    plt.scatter(front[:, 0], front[:, 1], color="blue", label="NSGA-II")

    plt.xlabel("$f_1(x)$")
    plt.ylabel("$f_2(x)$")
    plt.title("ZDT2")
    plt.legend()
    plt.savefig("zdt2.png")

    # create a GIF from the images in the images directory
    create_gif("images", "zdt2.gif")


if __name__ == "__main__":
    main()
