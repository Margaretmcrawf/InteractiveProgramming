from bokeh.models import BoxSelectTool, BoxZoomTool, LassoSelectTool, HoverTool, Quad
from bokeh.plotting import figure, output_file, show, gridplot, ColumnDataSource
from bokeh.models.widgets import Dropdown, Panel, Tabs, CheckboxButtonGroup, RadioGroup
from bokeh.io import output_file, show, vform

#PROJECT OVERVIEW:
#Create an interactive map of West Hall showing hallway culture via gender distribution, sleeping habit, etc.
#(If we hear back from STAR, we'll also have data on how people move from year to year, which will be awesome to implement)

#PROGRESS:
#currently outputs to an html file which has 2 tabs - one for WH1 and one for WH2
#rooms are currently blue squares, some with click and hover functionality, which is being modified and will be implemented in all once we figure out how to do it properly
#Also have buttons that are currently disfunctional but are planned to be able to display different color coordinations for each room.
#Will be initializing Room objects from a .csv file in this folder, but have not implemented yet.


# output to static HTML file
output_file("bokehlinetest.html")

class Room(object):
	def __init__(self, roomNum, roommates, gender, bedtime, top, bottom, left, right):
		self.roomNum = roomNum
		self.roommates = roommates
		self.gender = gender
		self.bedtime = bedtime
		self.top = top
		self.bottom = bottom
		self.left = left
		self.right = right

	def __str__(self):
		return 'Room Number: %s; Current Inhabitants: %s; Gender: %s; Average Bedtime: %s' %(self.roomNum, self.roommates, self.gender, self.bedtime)


# This was our previous Way of setting data (now we'll be using a csv file and pulling data from there to initialize each Room object)
''' 
#setting dictionary values for things on the first floor
source1 = ColumnDataSource(
        data=dict(
			roomates = ['Uma and Lauren', 'Margo and Nicole'],
			gender = ['female', 'female'],
			top=[2, 2],
			bottom=[1, 1], 
			left=[1, 3], 
			right=[2, 4],
		)
	)
'''

#setting what goes in the hover box (currently dysfunctional)
hover = HoverTool(
        tooltips=[
        	("index", "@index"),
			("roomates", "@roomates"),
			("gender", "@gender")
			]
		)

TOOLS = "box_zoom,box_select,resize,reset,hover,tap"

p1 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall First Floor")
rooms1 = p1.quad('top','bottom', 'left', 'right',
					
					#visual choices for when the room isn't selected, doesn't really work.
					#also maybe not necessary to click to select rooms, but could
					#be useful framework for changing color based on which button is selected
					nonselection_fill_alpha=0.01,
					nonselection_fill_color=None,
					nonselection_line_color="firebrick",
					nonselection_line_alpha=1.0,

					#visual choices for when the room is selected, actually works
					selection_color="blue",
					selection_fill_alpha=.5,

					#source for all of the room data
					source=source1
					)

p1.segment(x0=[1, 1, 1, 6], y0=[1, 6, 1, 1], x1=[6, 6, 1, 6],
          y1=[1, 6, 6, 6], color="#F4A582", line_width=3, legend="West Hall")
p1.select_one(BoxZoomTool).overlay.line_color = "olive"
p1.select_one(BoxZoomTool).overlay.line_width = 8
p1.select_one(BoxZoomTool).overlay.line_dash = "solid"
p1.select_one(BoxZoomTool).overlay.fill_color = None
tab1 =  Panel(child=p1, title="WH1")

p2 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall Second Floor")

rooms2 = p2.quad(top=[2],bottom=[1], left=[1], right=[2], 
					
					nonselection_fill_alpha=0.01,
					nonselection_fill_color=None,
					nonselection_line_color="firebrick",
					nonselection_line_alpha=1.0,

					selection_color="blue",
					selection_fill_alpha=.5)
					
p2.segment(x0=[1, 1, 1, 6], y0=[1, 6, 1, 1], x1=[6, 6, 1, 6],
          y1=[1, 6, 6, 6], color="#F4A582", line_width=3, legend="West Hall")

p2.select_one(BoxZoomTool).overlay.line_color = "olive"
p2.select_one(BoxZoomTool).overlay.line_width = 8
p2.select_one(BoxZoomTool).overlay.line_dash = "solid"
p2.select_one(BoxZoomTool).overlay.fill_color = None
tab2 = Panel(child=p2, title="WH2")


radio_group = RadioGroup(
        labels=["Gender", "Bedtime", "Some other shit"], active=0)

#dropdown_choices = [("Item 1", "item_1"), ("Item 2", "item_2"), ("Item 3", "item_3")]
#dropdown = Dropdown(label="Dropdown button", type="warning", menu=dropdown_choices)



tabs = Tabs(tabs=[ tab1, tab2 ])
layout = vform(dropdown, radio_group, tabs)

# show the results
show(tabs)
show(layout)
#show(vform(checkbox_button_group))