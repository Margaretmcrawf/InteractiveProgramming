from bokeh.models import BoxSelectTool, BoxZoomTool, LassoSelectTool
from bokeh.plotting import figure, output_file, show

# output to static HTML file
output_file("bokehlinetest.html")

p = figure(plot_width=400, plot_height=400)

# add a circle renderer with a size, color, and alpha
selected_room = p.quad(top=[2],bottom=[1], left=[1], right=[2], color="navy", alpha=0.8)
unselected_room = p.quad(top=[2],bottom=[1], left=[1], right=[2], color="navy", alpha=0.2)

p.segment(x0=[1, 1, 1, 6], y0=[1, 6, 1, 1], x1=[6, 6, 1, 6],
          y1=[1, 6, 6, 6], color="#F4A582", line_width=3, legend="West Hall")

p.select_one(BoxZoomTool).overlay.line_color = "olive"
p.select_one(BoxZoomTool).overlay.line_width = 8
p.select_one(BoxZoomTool).overlay.line_dash = "solid"
p.select_one(BoxZoomTool).overlay.fill_color = None


# show the results
show(p)