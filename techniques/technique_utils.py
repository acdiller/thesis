# p5.js-style map function
def p5map(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2

# constrain value to range
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


# helpers for drawsvg transforms since args have to be strings
def get_translate_str(tx=0, ty=0):
    return 'translate(' + str(tx) + ',' + str(ty) + ')'

def get_rotate_str(angle, cx=None, cy=None):
    rotate_args = ','.join(str(v) for v in locals().values() if v is not None)
    return 'rotate(' + rotate_args + ')'

def get_scale_str(x_mult, y_mult=None):
    scale_args = ','.join(str(v) for v in locals().values() if v is not None)
    return 'scale(' + scale_args + ')'