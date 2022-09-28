import random

# n is the number of men/women/couples
min_n = 4
max_n = 10

# monte_carlo is the number of simulations for each number of couples
monte_carlo = 1000

# Plotting how many iterations it takes the more n increases
plot_statistics = True
plot_2d = True
plot_3d = True

# Visualizing how the algorithm is doing the selection from the preference tables
visualize_iterations = True


# Print how iterations are distributed for each number of couples (monte carlo)
print_statistics = True
if visualize_iterations:
    import copy
    def print_preferences(iter=0):
        print(f'\nIteration {iter}')
        print('▮'*(n*2+7))
        for man in range(n):
            to_print = '|'
            for woman in init_preferences[str(man)]:
                if str(woman) not in men_preferences[str(man)]:
                    to_print += ' X'
                elif str(woman) in women_matches:
                    if women_matches[str(woman)] == str(man):
                        to_print += f' \033[31m{woman}\033[39m'
                    else:
                        to_print += f' {woman}'
                else:
                    to_print += f' {woman}'
            print('▮',man,to_print,'▮')    
        print('▮'*(n*2+7))
        for woman in range(n):
            to_print = '|'
            if str(woman) not in women_matches:
                to_print += ' '+' '.join(women_preferences[str(woman)])
            else:
                for man in women_preferences[str(woman)]:
                    if women_matches[str(woman)] == str(man):
                        to_print += f' \033[31m{man}\033[39m'
                    else:
                        to_print += f' {man}'
            print('▮',woman,to_print,'▮')
        print('▮'*(n*2+7))

# Initialize simulations
simulations = dict()

# Iterate over number of couples
for n in range(min_n,max_n+1):
    simulations[n] = dict()
    # Simulate algorithm monte_carlo times
    for _ in range(monte_carlo):
        # Create sequence from 0 to n-1 (these will represent the "names" of individuals)
        seq = [str(elem) for elem in list(range(n))]
        
        # Create men and women preferences by randomly permuting list from 0 to n-1
        men_preferences = {str(idx):random.sample(seq,n) for idx in range(n)}
        women_preferences = {str(idx):random.sample(seq,n) for idx in range(n)}

        women_matches = {}
        men_matches = {}
        iterations = 0

        # Keep a copy of the initial preferences for visualization
        if visualize_iterations:init_preferences = copy.deepcopy(men_preferences)

        # Iterate while there are still men not engaged in list
        while(len(seq)>0):
            # Choose man and remove him from list of engaged men
            man = seq.pop(0)

            # Choose woman candidate
            candidate_woman = men_preferences[man][0]

            # If woman is available, man and candidate_woman get matched
            if candidate_woman not in women_matches:
                women_matches[candidate_woman] = man
                men_matches[man] = candidate_woman

            # If man ranks higher in her preferences, break up and marry man
            elif man in women_preferences[candidate_woman][:women_preferences[candidate_woman].index(women_matches[candidate_woman])]:
                seq.append(women_matches[candidate_woman])
                men_preferences[women_matches[candidate_woman]].remove(candidate_woman)
                women_matches[candidate_woman] = man
                men_matches[man] = candidate_woman
            
            # Reject man (remove her from his preferences), add man back to list of unengaged men
            else:
                men_preferences[man].remove(candidate_woman)
                seq.append(man)

            iterations+=1
            if visualize_iterations:
                print_preferences(iterations)
                x = input('Press any key to continue...')
            
        # Count number of iterations for this instance of the algorithm
        if iterations in simulations[n]:
            simulations[n][iterations] +=1
        else:
            simulations[n][iterations] = 1

if print_statistics:
    import statistics
    import numpy as np
    mean = np.array([statistics.mean(simulations[elem]) for elem in range(min_n,max_n+1)])
    stdev = np.array([statistics.stdev(simulations[elem]) for elem in range(min_n,max_n+1)])
    print('\n'.join([f'{str(elem+min_n):{int(np.log10(max_n))+1}s} couples: mean={mean[elem]:.2f}, std={stdev[elem]:.2f}' for elem in range(len(mean))]))

if plot_statistics:
    import matplotlib.pyplot as plt
    import numpy as np
    
    if plot_2d:
        plt.figure()
        for n in simulations:
            x,y = zip(*sorted(zip(list(simulations[n].keys()),list(simulations[n].values()))))
            plt.plot(list(x),list(y), label=str(n))
        plt.xlabel('Number of iterations')
        plt.ylabel('Iteration Distribution')
        plt.legend()
        plt.show()

    if plot_3d:
        x_axis = []
        z_axis = []
        y_axis = []
        for n in simulations:
            x,z = zip(*sorted(zip(list(simulations[n].keys()),list(simulations[n].values()))))
            x_axis += list(x)
            z_axis += list(z)
            y_axis += [n]*len(x)
        plt.figure()
        ax = plt.axes(projection='3d')
        ax.scatter(x_axis, y_axis, z_axis, c=z_axis, cmap='viridis', linewidth=0.5);
        ax.set_xlabel('Number of iterations')
        ax.set_ylabel('Number of couples')
        ax.set_zlabel('Iteration Distribution')
        plt.show()