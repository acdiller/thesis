# p5.js-style map function
def p5map(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2

# constrain value to range
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

