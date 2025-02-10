from pyaxidraw import axidraw

ad = axidraw.AxiDraw()

# simulate plotting
def simulate_plot(svg):
    ad.plot_setup(svg)

    ad.options.preview = True
    ad.options.report_time = True

    # must call plot_run to get report_time
    ad.plot_run(True)
    dist_drawn = ad.distance_pendown
    plot_time = ad.time_estimate
    
    return dist_drawn, plot_time

# actual plotting
def plot(svg, config):

    if not ad.connect():
        quit()
    
    ad.plot_setup(svg)
    ad.load_config(config)
    
    ad.plot_run()
