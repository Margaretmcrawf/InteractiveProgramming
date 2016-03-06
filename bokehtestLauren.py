from bokeh.models import BoxSelectTool, BoxZoomTool, LassoSelectTool, HoverTool
from bokeh.plotting import figure, output_file, show, gridplot
from bokeh.models.widgets import Dropdown, Panel, Tabs, CheckboxButtonGroup
from bokeh.io import output_file, show, vform

# output to static HTML file
output_file("bokehlinetest.html")
TOOLS = 'box_zoom,box_select,crosshair,resize,reset,hover'

p1 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall First Floor")
selected_room = p1.quad(top=[2],bottom=[1], left=[1], right=[2], color="navy", alpha=0.8)
unselected_room = p1.quad(top=[2],bottom=[1], left=[1], right=[2], color="navy", alpha=0.2)
p1.segment(x0=[1, 1, 1, 6], y0=[1, 6, 1, 1], x1=[6, 6, 1, 6],
          y1=[1, 6, 6, 6], color="#F4A582", line_width=3, legend="West Hall")
p1.select_one(BoxZoomTool).overlay.line_color = "olive"
p1.select_one(BoxZoomTool).overlay.line_width = 8
p1.select_one(BoxZoomTool).overlay.line_dash = "solid"
p1.select_one(BoxZoomTool).overlay.fill_color = None
tab1 =  Panel(child=p1, title="WH1")

p2 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall Second Floor")
selected_room = p2.quad(top=[2],bottom=[1], left=[1], right=[2], color="navy", alpha=0.8)
unselected_room = p2.quad(top=[2],bottom=[1], left=[1], right=[2], color="navy", alpha=0.2)
p2.segment(x0=[1, 1, 1, 6], y0=[1, 6, 1, 1], x1=[6, 6, 1, 6],
          y1=[1, 6, 6, 6], color="#F4A582", line_width=3, legend="West Hall")
p2.select_one(BoxZoomTool).overlay.line_color = "olive"
p2.select_one(BoxZoomTool).overlay.line_width = 8
p2.select_one(BoxZoomTool).overlay.line_dash = "solid"
p2.select_one(BoxZoomTool).overlay.fill_color = None
tab2 = Panel(child=p2, title="WH2")


checkbox_button_group = CheckboxButtonGroup(
        labels=["Gender", "Same Roommates", "Other Selectable Shit"], active=[0, 1])
dropdown_choices = [("Item 1", "item_1"), ("Item 2", "item_2"), None, ("Item 3", "item_3")]
dropdown = Dropdown(label="Dropdown button", type="warning", menu=dropdown_choices)



tabs = Tabs(tabs=[ tab1, tab2 ])

# show the results
show(tabs)
#show(vform(dropdown))
#show(vform(checkbox_button_group))