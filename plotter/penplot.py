import argparse

from pyaxidraw import axidraw

ad = axidraw.AxiDraw()

# simulate plotting
def simulate_plot(svg):
    ad.plot_setup(svg)

    ad.options.preview = True   # perform offline simulation of plot

    ad.plot_run(True)
    plot_stats = {
        "plot_time": ad.time_estimate,  # estimated plot time (seconds)
        "dist_drawn": ad.distance_pendown,  # distance traveled with pen down (meters)
        "pen_lifts": ad.pen_lifts   # number of pen lifts
    }
    
    return plot_stats

# actual plotting
def plot(svg, config):

    if not ad.connect():
        quit()
    
    ad.plot_setup(svg)
    ad.load_config(config)
    
    ad.plot_run()

if __name__ == "__main__":
    ad.plot_setup()
    ad.options.mode = "sysinfo"
    ad.plot_run()