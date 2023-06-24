import numpy as np
import random as rd
import matplotlib.pyplot as plt
playerName = "myAgent"
nPercepts = 75  # This is the number of percepts
nActions = 5    # This is the number of actions
mChance = 1  # Mutation Chance(out of 100) for each gene
Elitism = 2  # How many of the old population will get carried over
P_parents = 6
fitness_over_time = []  # Recording the fitness over time, to plot a graph with.
# Train against random for 1000 generations, then against self for 1 generations
trainingSchedule = [("random", 1000), ("self", 1)]


# This is a tournament selection method that takes in the old population after it has been sorted.
# This old population is a list of tuples, with each tuple containing Fitness and the Creature.
#
# Selection is dependent upon the selector variable, which generates unique random variables using
# random's sample method. This lets it find 6 integers with no overlaps up to the length of our
# population. It then appends all the selected parents into a list, then sorts the list based upon
# their fitness in descending order using the reverse parameter. The first two parents in the list
# are the fittest parents, hence we return them.
#
# Note: This function can also return the entire list of
# potential parents, as selection is based upon the 0 and 1 index. For clarity's sake, we only return
# two parents.
def tournament_selection(old_pop_sort):
    potential_parents = []
    selector = rd.sample(range(0, len(old_pop_sort) - 1), P_parents)
    for i in selector:
        potential_parents.append(old_pop_sort[i])
    potential_parents.sort(key=lambda x: x[0], reverse=True)
    return potential_parents[0], potential_parents[1]


# The class that defines a creature.
class MyCreature:

    # The initialization of the creature. Values for chromosomes must be initialized here.
    def __init__(self):
        # The chromosome is initialized through using numpy's random uniform method, as the
        # method allows you to have integers of 0 and 1. The size is defined by how many possible
        # percepts and actions there are, and as such should be 75 (as percepts are 3 * 5 * 5) and 5
        # (as there are 5 actions), leading to 375 possible variables.

        # The reason for using uniform(integers) instead of random floats is due to percepts using 0's and 1's.
        # It is much easier in both understanding and interaction between chromosome and percepts
        # to use similar values.
        self.chromosome = np.random.uniform(0, 1, size=(nPercepts, nActions))

    # A function to generate out the five actions for the creature.
    def AgentFunction(self, percepts):
        # Actions must be a list of 5, and interact with our percepts. As such, we flatten our percepts to
        # make it easier for chromosome to interact with. We then use numpy's dot method to generate our
        # actions, giving us our list of 5 values.
        actions = np.dot(percepts.flatten(), self.chromosome)
        return actions


# A function to create a new generation based on the old one.
def newGeneration(old_population):
    # This records how big the population is, based upon a list.
    N = len(old_population)
    # We then initialize a numpy list of zeroes based on the size of the population, to contain their fitness.
    fitness = np.zeros(N)
    # Then we create an empty list, to hold tuples of a creature and their fitness.
    sorted_population = []
    # For every creature in the old population, we define their fitness through their current properties.
    # We then append them to our list above(sorted_population) as a tuple, in the order:
    # Fitness, Creature
    for n, creature in enumerate(old_population):
        # This equation can be altered depending on what you want the creature to do.
        # Each variable is multiplied by a weight so that a bigger variable means those creatures
        # are more fit.
        # We can also divide a variable to attach less importance to it, such as creature.turn.
        fitness[n] = (creature.turn - creature.bounces + creature.squares_visited*10)/10 + \
                     (creature.size*10) + (creature.strawb_eats*10) + (creature.enemy_eats*5)
        sorted_population.append([fitness[n], creature])
    # We now sort the population based upon their fitness. As the sort method normally goes in ascending order,
    # We can reverse it to have the fittest parents in the front.
    sorted_population.sort(key=lambda x: x[0], reverse=True)
    # We now define a list for our population to be created, based on the old one.
    new_population = []
    # We need to define their average fitness, both for a graph and the return statement.
    avg_fitness = np.mean(fitness)
    # Append average fitness to a global list, so we can generate a plot later.
    fitness_over_time.append(avg_fitness)
    # This generates a plot when fitness_over_time has a length of 50 or 100
    if len(fitness_over_time) == 500 or len(fitness_over_time) == 1000:
        plt.ylabel("AVG_Fitness")
        plt.plot(fitness_over_time)
        plt.show()
    # For integer 0-N, we generate a new Creature.
    # The new creature can be a completely randomized one if we do not alter any aspects.
    # However, to generate from old population, we alter the new Creature's chromosomes through
    # genetic algorithm.
    for n in range(N):
        # A newly created creature, with randomized variables.
        new_creature = MyCreature()
        # This is an implementation of elitism, based upon the sorted list of the old population.
        # if n is less than the specified Elitism variable, it will take the n creature in the
        # old population, meaning it will take 0(the best creature), 1(the second best), etc.
        if n < Elitism:
            # Note that n refers to location in the sorted population, and that sorted population is
            # a tuple of [Fitness, Creature], hence index of [n][1].
            new_creature = sorted_population[n][1]
        else:
            # Select parents based on tournament selection on the sorted population.
            parents = tournament_selection(sorted_population)
            # This is the crossover part, where mutation is included. I have tried using only the
            # 75 genes, and that leads to poor performance. Thus, I instead chose to alter every single
            # possible action in each gene, which lead to better performance. As such, we have to go over
            # every single percept and action.
            #
            # After trying multiple types of crossover including multi-point, uniform, fixed cut-off,
            # I decided on uniform as it seemed to have the best distribution.
            #
            # The mutation is located in the first if statement, where the creature has a chance to
            # get a randomly input 0 or 1 instead of inheriting from a parent.
            for i in range(0, nPercepts):
                for j in range(0, nActions):
                    if rd.randint(0, 100) <= mChance:
                        new_creature.chromosome[i][j] = rd.randint(0, 1)
                    else:
                        if rd.randint(0, 1):
                            new_creature.chromosome[i][j] = parents[0][1].chromosome[i][j]
                        else:
                            new_creature.chromosome[i][j] = parents[1][1].chromosome[i][j]
        new_population.append(new_creature)
    return new_population, avg_fitness


