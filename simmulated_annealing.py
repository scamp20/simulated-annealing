def simulated_annealing( self,time_allowance=60.0 ):
    results = {}
    count = 0
    bssf = None
    start_time = time.time()

    # Give self.defaultRandomTour 2 seconds to find a path
    bssf = self.defaultRandomTour(2)['soln']
    time_allowance -= 2
    last = bssf

    # Set hyperparameters
    temperature = 1000
    cooling_rate = .98

    while temperature > 1e-3 and time.time()-start_time < time_allowance:
        route = bssf.route
        # Swap two cities
        curr = self.swap(route)
        count += 1
        # Calculate error
        error = last.cost - curr.cost
        if curr.cost < bssf.cost:
            # Update bssf and use this solution as 'last'
            bssf = curr
            last = bssf
        elif curr.cost < last.cost:
            # Use this better solution as 'last'
            last = curr
        elif curr.cost > last.cost:
            # Give it a chance to escape local minima
            p = np.exp(((error/2)/temperature))
            if np.random.rand() < p:
                last = curr
        else:
            # Don't use that solution
            pass
        temperature *= cooling_rate

    end_time = time.time()
    results['cost'] = bssf.cost
    results['time'] = end_time - start_time
    results['count'] = count
    results['soln'] = bssf
    results['max'] = None
    results['total'] = None
    results['pruned'] = None
    return results

def swap(self, route):
    while(True):
        swap_indexes = random.sample(range(len(route)), 2)
        i, j = swap_indexes
        edges = self._scenario._edge_exists
        if edges[i][j]:
            temp_route = route.copy()
            temp_route[i], temp_route[j] = temp_route[j], temp_route[i]
            temp_bssf = TSPSolution(temp_route)
            if temp_bssf.cost < np.inf:
                return temp_bssf