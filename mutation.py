from copy import deepcopy

import settings

def apply_mutation(ind, it):
    offspring = deepcopy(ind)
    offspring.id += f"_m{it}"

    # reset geometries, fitness, features, etc.
    for t in offspring.techniques:
        t.reset()
    offspring.features = None
    offspring.fitness = 0.0

    # choose random technique and mutate one of its parameters
    #t = offspring.rng.choice(offspring.techniques)
    #t.mutate()

    # slight chance to apply "coarse-grained" mutation (insert, delete, duplicate, or swap)
    if settings.rng.random() <= settings.mutation_rate:
        if offspring.techniques.length == 1:
            # can only insert or duplicate - not enough techniques to delete or swap
            offspring = insert(offspring) if settings.rng.random() < 0.5 else duplicate(offspring)
        elif offspring.techniques.length == settings.MAX_T:
            # can only delete or swap - too many techniques to insert or duplicate
            offspring = delete(offspring) if settings.rng.random() < 0.5 else swap(offspring)
        else:
            # all mutation types are valid - pick one at random
            m_types = [insert, delete, duplicate, swap]
            m = settings.rng.choice(m_types)
            offspring = m(offspring)

    # pick one (or two) of offspring's techniques and mutate a technique parameter
    for t in offspring.techniques:
        if settings.rng.random() <= 1/offspring.techniques.length:
            t.mutate()

    return offspring


def insert(ind):
    """
    Insert a new technique in a random position amongst the individual's existing techniques.
    """
    i = settings.rng.randrange(0, ind.techniques.length)
    new_t = settings.rng.choice(settings.ALL_TECHNIQUES)
    ind.techniques.insert(i, new_t(ind.rng, (0, 0, ind.dim[0], ind.dim[1])))

    return ind


def delete(ind):
    """
    Randomly select one of the individual's techniques and delete it.
    """
    i = settings.rng.randrange(0, ind.techniques.length)
    ind.techniques.pop(i)

    return ind


def duplicate(ind):
    """
    Randomly select one of the individual's techniques, duplicate it, and insert in a random position.
    """
    i = settings.rng.randrange(0, ind.techniques.length)
    t_copy = deepcopy(ind.techniques[i])
    j = settings.rng.randrange(0, ind.techniques.length)
    ind.techniques.insert(j, t_copy)
    return ind


def swap(ind):
    """
    Swap the positions of two of the individual's techniques, selected at random.
    """
    i1, i2 = settings.rng.sample(range(0, ind.techniques.length), 2)
    t1 = deepcopy(ind.techniques[i1])
    t2 = deepcopy(ind.techniques[i2])
    ind.techniques[i1] = t2
    ind.techniques[i2] = t1

    return ind

