import numpy as np
import random
import matplotlib.pyplot as plt

# N: Amount of influencers
# F = Amount of views per influencer
# R = Revenue per view


# The equation for calculating the yield
# after investing in influencer is
# Y = N(FR - c)


# To calculate the optimal ratio
# between these parameters
# a genetic algorithm will be used
#       The genetic algorithm will look
#       for maximum yield while
#       minimizing the amount of influencers
#       and cost per influencer


# The fitness function will simply calculate the
# yield (Y) after each generation
#       The genome will have the following format
#       0000000000 -> 2^10 => N (max. 1024)
#       0000000000000000 -> 2^16 => F (max. 65536)
#       0000000000 -> 2^10 / 4000 => R (max. 0.256)
# Genes -> Bits -> 10 + 16 + 10 = 36


def generate_genome():
    genome = np.empty(46, str)
    for i in range(46):
        # Generate a random gene (bit)
        genome[i] = round(random.random())
    return genome

def explode_genome(genome):
    N_bits = genome[0:10]
    F_bits = genome[10:26]
    R_bits = genome[26:36]

    # Calculate the values
    N = int("".join(map(str, N_bits.astype(int))), 2)
    F = int("".join(map(str, F_bits.astype(int))), 2)
    R = int("".join(map(str, R_bits.astype(int))), 2) / 4000

    # Calculate the investment
    I = coeffs[0]*F + coeffs[1]
    I *= N

    P = 0
    if I > max_investment:
        # The maximum investment amount
        # has been surpassed
        #       Introduce a penalty that is proportional
        #       to the difference between the investment
        #       and the maximum investment
        P = I ** I/max_investment

    return N, F, R, I, P


# Define the price of an influencer per amount of views
f = [1000, 100000, 50000, 500000]
c = [150, 400, 1650, 3500]
coeffs = np.polyfit(f, c, 1)


def fitness_function(genome):
    # Explode the genome
    N, F, R, I, P = explode_genome(genome)

    # Calculate the yield
    Y = N * F*R - I - P
        
    # Return the yield (fitness)
    return Y


# Set environment settings
max_investment = 100000


# Set simulation settings
organism_amount = 500
generation_amount = 100
reproduce_with_fit_chance = 0.5 
# Determines the chance that one of the fit organisms
# will reproduce with another fit organism
elitism = True
# Whenever "Elitism" is enabled, all of the top organisms
# get put into the next generation, after which the rest
# population is filled with offspring
random_crossover_point = True
# Determines whether a random crossover point should be calculated
# for every generation
attempts = 20
# Amount of simulation attempts


# Set the variables to check whether an equilibrium has been reached
consecutive_values_within_margin = 0
last_value_within_margin = None

# Register all attempts
# to plot them in a 3D plot
highest_scores = np.zeros(attempts)

for n in range(attempts):
    # Create arrays
    organisms = np.empty((organism_amount, 46), int)
    mean_fitness_scores = np.zeros(generation_amount)
    most_fit_organism = None
    most_fit_score = 0


    # Generate the first generation
    for o in range(organism_amount):
        organisms[o] = generate_genome()


    # Iterate over all generation
    for g in range(generation_amount):

        # Create array to register fitness of organisms
        fitnesses = np.empty(organism_amount, float)

        for o in range(organism_amount):
            # Calculate the fitness of every organism
            Y = fitness_function(organisms[o])
            fitnesses[o] = Y


        # Find maximum values
        # The "Elitism" approach is implemented
        selection_count = int(3/4 * organism_amount)

        positive_indices = np.where(fitnesses > 0)[0]
        sorted_indices = positive_indices[np.argsort(fitnesses[positive_indices])][::-1]
        max_indices = sorted_indices[:selection_count]

        # max_indices = np.argsort(fitnesses[fitnesses >= 0])
        selection_count = len(max_indices) if (len(max_indices) < selection_count) else selection_count

        # Show the fittest organisms
        if (attempts == 1):
            print(f"Fitness of top 3 organism of generation {g + 1}")
            print(f"1:  {fitnesses[max_indices[0]]}")
            print(f"2:  {fitnesses[max_indices[1]]}")
            print(f"3:  {fitnesses[max_indices[2]]}")
            print("\n")

        # Register the mean value of the top 3 fittest organisms
        mean_fitness_scores[g] = np.mean([
            fitnesses[max_indices[0]],
            fitnesses[max_indices[1]],
            fitnesses[max_indices[2]],
        ])

        # Check whether the fittest organism is
        # the overall fittest organism
        if fitnesses[max_indices[0]] > most_fit_score:
            most_fit_score = fitnesses[max_indices[0]]
            most_fit_organism = organisms[max_indices[0]]


        # Check whether the fitness of the generations
        # is stabilizing
        if (g > 0):
            if ((mean_fitness_scores[g] - mean_fitness_scores[g-1])/mean_fitness_scores[g-1] < 0.01):
                # Another value within the margins
                consecutive_values_within_margin += 1
                last_value_within_margin = mean_fitness_scores[g]
            else:
                # Not within the margins to reach stability
                consecutive_values_within_margin = 0

            if consecutive_values_within_margin == 10:
                # The fitness has reached a stable point

                # Shorten the `mean_fitness_scores` array
                temp_array = np.zeros(g)
                temp_array[:g] = mean_fitness_scores[:g]
                mean_fitness_scores = temp_array
                print("The generations have reached an equilibrium")
                break



        # Because "Elitism" is being used
        # all of the best organisms will be put into the next generation
        # and the rest of the generation will be filled by offset produced
        # by these fittest organisms.
            
        # Perform the genetic operation:
        #       "One-Point Crossover"
        # A "fit" organism will be selected and paired with a random organism
        #   Children will be produced until `organism_amount` of children are produced
        child_count = 0

        if (random_crossover_point):
            crossover_point = int(random.random() * 46)
        else:
            crossover_point = 20

        new_organisms = np.empty((organism_amount, 46), int)
        
        # Fill the array with the fittest organism
        if (elitism):
            new_organisms[:selection_count] = organisms[max_indices[:selection_count]]
            child_count += selection_count
            

        # Fill the rest of the array with offspring
        # produced by the fittest organisms
        while child_count < organism_amount:
            for o in organisms[max_indices]:
                # `o` represents the fit organism

                # Check whether enough children are produced
                if (child_count == organism_amount):
                    break

                # # Choose whether to reproduce with one of the fittest organisms
                # # or whether to reproduce with a less fit organism
                if random.random() <= reproduce_with_fit_chance:
                    # Reproduce with a fit organism
                    ro = organisms[max_indices[int(random.random() * (selection_count-1))]]
                else:
                    # Reproduce with a less fit organism
                    ro = organisms[int(random.random() * (organism_amount-1))]


                # Perform the genetic operation
                #       Fit organism
                o_first_bits = o[:crossover_point]
                o_second_bits = o[crossover_point:]
                #       Random organism
                ro_first_bits = ro[:crossover_point]
                ro_second_bits = ro[crossover_point:]

                new_organisms[child_count] = np.concatenate([o_first_bits, ro_second_bits])
                child_count += 1
                if (child_count == organism_amount):
                    break

                new_organisms[child_count] = np.concatenate([ro_first_bits, o_second_bits])
                child_count += 1

        # Update the `organisms` array
        organisms = new_organisms


    N, F, R, I, P = explode_genome(most_fit_organism)
    Y = N * F*R - I - P
    print("The most fit organism has the following properties:")
    print(f"(Amount of influencers) N =  {N}")
    print(f"(Amount of views per influencer) F =  {F}")
    print(f"(Revenue per view) R =  {R}")
    print(f"(Penalty) P =  {P}")
    print(f"(Yield) Y =  {Y}")
    print(f"(Investment) I =  {I}")
    print(f"(Return on investment) ROI = {Y/I * 100}%")
    print("\n")

    highest_scores[n] = Y/I

plt.plot(np.arange(1, attempts + 1, 1), highest_scores)
plt.show()