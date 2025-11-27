import heapq

class Archive:
    def __init__(self, fd_bins):
        self.fd_bins = fd_bins

        self.archive = {}
        self.cells = self.archive.values()
    

    def add_to_archive(self, ind):
        """
        Place an individual in its corresponding cell in the archive.

        Determine what cell an individual belongs to according to its features
        and place it there if the cell is empty, or if the individual outperforms
        the current occupant of the cell.
        """
        coordinates = []
        # get index for bin corresponding to individual's features, for each set of bins
        for b, bins in enumerate(self.fd_bins.values()):
            for i in range(len(bins)-1):
                if bins[i] <= ind.features[b] and ind.features[b] < bins[i+1]:
                    coordinates.append(i)
                    break
        coordinates = tuple(coordinates)  # make hashable for archive key

        self.archive.setdefault(coordinates, [])
        heapq.heappush(self.archive[coordinates], (ind.fitness, ind.id, ind))
        print(f"{ind.id} with fitness {ind.fitness} placed at {coordinates}")


        # place individual in cell if cell is empty, or it outperforms current occupant
        #if coordinates not in self.archive: 
        #    print(f"{ind.id}, {ind.fitness} placed at {coordinates}")
        #    self.archive[coordinates] = ind
        #elif self.archive[coordinates].fitness < ind.fitness:
        #    print(f"{ind.id}, {ind.fitness} replaced {self.archive[coordinates].id}, "
        #          f"{self.archive[coordinates].fitness} at {coordinates}")
        #    self.archive[coordinates] = ind
        #else:
        #    print(f"{ind.id}, {ind.fitness} rejected at {coordinates} over "
        #          f"{self.archive[coordinates].id}, {self.archive[coordinates].fitness}")
    

    #TODO: need to do coverage in a way that shows what cells are occupied, keep track over time
    def qd_scores(self):
        """Compute coverage and mean fitness for the map."""
        mapsize = 1
        for b in self.bins.values():
            mapsize *= len(b)
        coverage = len(self.archive.values()) / mapsize

        fitnesses = [ind.fitness for ind in list(self.archive.values())]
        mean = sum(fitnesses) / mapsize
        return coverage, mean
    

    # TODO: heatmaps