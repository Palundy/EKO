import numpy as np
import random
import matplotlib.pyplot as plt


#       The genome will have the following format
# 
#  Chance of growing to TOP direction
#       0000 -> 2^4 => GT (max. 16)
#  Chance of growing to RIGHT direction
#       0000 -> 2^4 => GR (max. 16)
#  Chance of growing to BOTTOM direction
#       0000 -> 2^4 => GB (max. 16)
#  Chance of growing to LEFT direction
#       0000 -> 2^4 => GL (max. 16)
# These values will be divided by 16
# 
# 
#  Irradiance boost factor:
#   gives a boost whenever a cell
#   is directly under sunlight.
#  Boost chance in TOP direction
#       000000 -> 2^6 => IBFT (max. 64) 
#  Boost chance in RIGHT direction
#       000000 -> 2^6 => IBFR (max. 64) 
#  Boost chance in BOTTOM direction
#       000000 -> 2^6 => IBFB (max. 64) 
#  Boost chance in LEFT direction
#       000000 -> 2^6 => IBFL (max. 64) 
#   This will be divided by 64, then the boost
#   will be applied by dividing the chances by the boost factor
 






def generate_genome():
    genome = np.empty(46, str)
    for i in range(46):
        # Generate a random gene (bit)
        genome[i] = round(random.random())
    return genome

def convert_chromosome(chromosome):
    return int("".join(map(str, chromosome.astype(int))), 2)

def explode_genome(genome):
    GT = convert_chromosome(genome[0:4]) / 16
    GR = convert_chromosome(genome[4:8]) / 16
    GB = convert_chromosome(genome[8:12]) / 16
    GL = convert_chromosome(genome[12:16]) / 16
    IBFT = convert_chromosome(genome[16:22]) / 64
    IBFR = convert_chromosome(genome[28:34]) / 64
    IBFB = convert_chromosome(genome[34:40]) / 64
    IBFL = convert_chromosome(genome[40:46]) / 64

    IBFT = 0.0001 if IBFT == 0 else IBFT
    IBFR = 0.0001 if IBFR == 0 else IBFR
    IBFB = 0.0001 if IBFB == 0 else IBFB
    IBFL = 0.0001 if IBFL == 0 else IBFL

    return [
        GT, GR, GB, GL,
        IBFT, IBFR, IBFB, IBFL
    ]

def perform_action(genome):
    return

def evaluate_organisms(organisms, cells, t):
    for x in range(x_range):
        for y in range(y_range):
            organism = organisms[t][x][y]
            organisms[t + 1][x][y] = organism
            GT, GR, GB, GL, IBFT, IBFR, IBFB, IBFL = explode_genome(organisms[t][x][y])

            # Calculate chance to grow TOP
            if (GT / IBFT > random.random()):
                # Grow TOP
                if (y != y_range-1):
                    organisms[t][x][y+1] = organism

            # Calculate chance to grow RIGHT
            if (GR / IBFR > 1):
                # Grow RIGHT
                if (x != x_range-1):
                    organisms[t][x+1][y] = organism

            # Calculate chance to grow BOTTOM
            if (GB / IBFB > 1):
                # Grow BOTTOM
                if (y != 0):
                    organisms[t][x][y-1] = organism

            # Calculate chance to grow LEFT
            if (GL / IBFL > 1):
                # Grow LEFT
                if (x != 0):
                    organisms[t][x-1][y] = organism

    return organisms, cells





def fitness_function(genome):
    # The fitness wil simply be determined by calculating
    # the total amount of cells with the given genome
    return None



# Set simulation settings
organism_amount = 5
generation_amount = 100
reproduce_with_fit_chance = 0.5
# Determines the chance that one of the fit organisms
# will reproduce with another fit organism
elitism = True
# Whenever "Elitism" is enabled, all of the top organisms
# get put into the next generation, after which the rest
# population is filled  with offspring
random_crossover_point = True
# Determines whether a random crossover point should be calculated
# for every generation
simulation_steps = 100
# Amount of steps per generation simulation
x_range = 100
y_range = 100


# Set the variables to check whether an equilibrium has been reached
consecutive_values_within_margin = 0
last_value_within_margin = None


# Create arrays
organisms = np.zeros((simulation_steps, x_range, y_range, 46))
cells = np.zeros((simulation_steps, x_range, y_range))
mean_fitness_scores = np.zeros(generation_amount)
most_fit_organism = None
most_fit_score = 0


# Generate the first generation
fraction = 12
spacing = (x_range * (fraction-2)/fraction) / (organism_amount)
for i in range(organism_amount):
    # Spread the organisms around on the 'floor' of the grid
    organisms[0][0][int(x_range/fraction + i*spacing + x_range/fraction)] = generate_genome()
    cells[0][0][int(x_range/fraction + i*spacing + x_range/fraction)] = 1

fig, ax = plt.subplots()
im = ax.imshow(cells[0], cmap='viridis')


# Iterate over all generation
for g in range(generation_amount):

    # Create array to register fitness of organisms
    fitnesses = np.empty(organism_amount, float)

    # Run the whole simulation
    for t in range(simulation_steps - 1):
        # For each organism in the grid
        # the genome will be evaluated
        # then action will be taken
        organisms, cells = evaluate_organisms(organisms, cells, t)

        im.set_data(cells[t])
        fig.canvas.draw_idle()
        plt.show()

    exit()



    for o in range(organism_amount):
        # Calculate the fitness of every organism
        Y = fitness_function(organisms[o])
        fitnesses[o] = Y



    # Find maximum values
    selection_count = int(3/4 * organism_amount)
    positive_indices = np.where(fitnesses > 0)[0]
    sorted_indices = positive_indices[np.argsort(fitnesses[positive_indices])][::-1]
    max_indices = sorted_indices[:selection_count]

    # max_indices = np.argsort(fitnesses[fitnesses >= 0])
    selection_count = len(max_indices) if (len(max_indices) < selection_count) else selection_count

    # Show the fittest organisms
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

