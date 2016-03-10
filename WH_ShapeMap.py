from bokeh.models import BoxSelectTool, BoxZoomTool, LassoSelectTool, HoverTool, Quad
from bokeh.plotting import figure, output_file, show, gridplot, ColumnDataSource
from bokeh.models.widgets import Dropdown, Panel, Tabs, CheckboxButtonGroup, RadioGroup
from bokeh.io import output_file, show, vform, save
import csv

#PROJECT OVERVIEW:
#Create an interactive map of West Hall showing hallway culture via gender distribution, sleeping habits, time spent in hallways, etc.
#(If we hear back from STAR, we'll also have data on how people move from year to year, which will be awesome to implement)

#PROGRESS:
#currently outputs to an html file which has 3 tabs - WH1, WH2, and WH3
#rooms are currently blue squares, have hover functionality with correct labels but no data
#Also have buttons that are currently nonfunctional but are planned to be able to display different color coordinations for each room.
#Initializes and draws all rooms from a .csv file with data from survey sent to first years.

#NEXT STEPS:
#Get more room data from people (keep collecting survey responses)
#Draw rooms in correct places
#Make import for roommate names work correctly
#Make hover display room number and inhabitant names instead of '???'
#Make buttons functional
	#figure out how to make buttons active
	#make metric for color changing and coordination


# output to static HTML file
output_file("WH_Firstyears.html")

class Room(object):
	def __init__(self, roomNum='000', roommates='[Roommate Names Here]', gender='[Some Gender Here]', bedtime=0, lightsleep=0, halltime=0, top=1, bottom=0, left=0, right=1):
		self.roomNum = roomNum
		self.roommates = roommates
		self.gender = gender
		self.bedtime = bedtime
		self.lightsleep = lightsleep
		self.halltime = halltime
		self.top = top
		self.bottom = bottom
		self.left = left
		self.right = right

	def __str__(self):
		return 'Room Number: %s / Current Inhabitants: %s / Gender: %s / Average Bedtime: %s' %(self.roomNum, self.roommates, self.gender, self.bedtime)

	def drawRoom(self):
		if int(self.roomNum)<200:
			#draw on first floor
			rooms1 = p1.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								nonselection_fill_color=None,
								nonselection_line_color="firebrick",
								nonselection_line_alpha=1.0,
								selection_color="blue",
								selection_fill_alpha=.5)
				
		elif int(self.roomNum)<300:
			#draw on second floor
			rooms2 = p2.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								nonselection_fill_color=None,
								nonselection_line_color="firebrick",
								nonselection_line_alpha=1.0,
								selection_color="blue",
								selection_fill_alpha=.5)
		else:
			#draw on third floor
			rooms3 = p3.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								nonselection_fill_color=None,
								nonselection_line_color="firebrick",
								nonselection_line_alpha=1.0,
								selection_color="blue",
								selection_fill_alpha=.5)


TOOLS = "box_zoom,box_select,resize,reset,hover,tap"

#draws first floor of WH
p1 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall First Floor")
tab1 =  Panel(child=p1, title="WH1")
p1.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="#F4A582", line_width=3)
p1.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]

#draws second floor of WH
p2 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall Second Floor")
tab2 = Panel(child=p2, title="WH2")
p2.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="#F4A582", line_width=3)
p2.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]

#draws third floor of WH
p3 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall Third Floor")
tab3 = Panel(child=p3, title="WH3")
p3.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="#F4A582", line_width=3)
p3.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]


#Pull data from csv file and create Room objects from it!
with open('WH_Freshmen.csv') as csvfile:
	freshmen_data = csv.reader(csvfile, delimiter=',', quotechar='\"')
	#roomList = []
	for row in freshmen_data:
		roomA = Room() #initializes a new Room for each row in the csv data file
		roomA.roomNum = row[0]
		roomA.roomates = row[1] #not working for some reason?
		roomA.gender = row[2]
		roomA.bedtime = row[3]
		roomA.lightsleep = row[4]
		roomA.halltime = row[5]
		roomA.top = 13
		roomA.bottom = 12
		roomA.left = 0
		roomA.right = 1
		roomA.drawRoom()
		#roomList.append(roomA) #creates list of all Room objects

dropdown_choices = [("Gender", "gender"), ("Bedtime", "bedtime"), ("Light Sleeper", "lightsleep"), ("Time in Hallway", "halltime")]
dropdown = Dropdown(label="Hallway Metrics", type="warning", menu=dropdown_choices)

tabs = Tabs(tabs=[tab1, tab2, tab3])
layout = vform(dropdown, tabs)

# show the results
save(tabs)
show(layout)