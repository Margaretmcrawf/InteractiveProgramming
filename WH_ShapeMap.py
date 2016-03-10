from bokeh.models import BoxSelectTool, BoxZoomTool, LassoSelectTool, HoverTool, Quad
from bokeh.plotting import figure, output_file, show, gridplot, ColumnDataSource, output_server
from bokeh.models.widgets import Dropdown, Panel, Tabs, CheckboxButtonGroup, RadioGroup
from bokeh.io import output_file, show, vform, save
import csv

#PROJECT OVERVIEW:
#Create an interactive map of West Hall showing hallway culture via gender distribution, sleeping habits, time spent in hallways, etc.
#(If we hear back from STAR, we'll also have data on how people move from year to year, which will be awesome to implement)

#PROGRESS:
#currently outputs to an html file which has 3 tabs - WH1, WH2, and WH3
#rooms are currently blue squares, have hover functionality with correct labels but no data
#rooms are 1 unit squares with an x position between 0 and 11 and a y position between 1 and 13.
#Also have buttons that are currently nonfunctional but are planned to be able to display different color coordinations for each room.
#Initializes and draws all rooms in correct places from a .csv file with data from survey sent to first years.

#NEXT STEPS:
#Get more room data from people (keep collecting survey responses)
#Make import for roommate names work correctly
#Make hover display given room number and inhabitant names instead of '???'
#Make buttons functional
	#figure out how to make buttons active
	#make metric for color changing and coordination
	#bokeh server things


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

	def findCoordinates(self): #defines positions for rooms
		coordinates = [1,0,0,1] #default
		mod = int(self.roomNum)%100 #can do all floors at once
		if mod<18:
			if mod%2==1:
				coordinates[0] = 13
				coordinates[1] = 12
			else:
				coordinates[0] = 11
				coordinates[1] = 10

			if mod==1 or mod==2:
				coordinates[2] = 7 
				coordinates[3] = 8
			elif mod==3 or mod==4:
				coordinates[2] = 8
				coordinates[3] = 9
			elif mod==5 or mod==6:
				coordinates[2] = 9
				coordinates[3] = 10
			elif mod==7:
				coordinates[2] = 10
				coordinates[3] = 11
			elif mod==9 or mod==10:
				if int(self.roomNum)==109 or int(self.roomNum)== 110: #special case: Nick Tatar
					coordinates[2] = 0
					coordinates[3] = 4
				else:
					coordinates[2] = 3
					coordinates[3] = 4
			elif mod==11 or mod==12:
				coordinates[2] = 3
				coordinates[3] = 2
			elif mod==13 or mod==14:
				coordinates[2] = 2
				coordinates[3] = 1
			elif mod==15:
				coordinates[2] = 0
				coordinates[3] = 1
		elif mod>=18:
			if mod%2==1:
				coordinates[2] = 6
				coordinates[3] = 7
			else:
				coordinates[2] = 4
				coordinates[3] = 5
			if mod==18:
				coordinates[0] = 9
				coordinates[1] = 8
			elif mod==20:
				coordinates[0] = 8
				coordinates[1] = 7
			elif mod==23 or mod==24:
				coordinates[0] = 6
				coordinates[1] = 5
			elif mod==25 or mod==26:
				coordinates[0] = 5
				coordinates[1] = 4
			elif mod==27 or mod==28:
				coordinates[0] = 4
				coordinates[1] = 3
			elif mod==29 or mod==30:
				coordinates[0] = 3
				coordinates[1] = 2
			elif mod==31:
				coordinates[0] = 2
				coordinates[1] = 1
		return coordinates

	def drawRoom(self): #Now with Olin colors! heyyyyyyyyyooooooo
		if self.gender == 'N/A':
			color='grey'
			alpha = .3
		else: 
			color='navy'
			alpha = 1.0
		if int(self.roomNum)<200:
			#draw on first floor
			rooms1 = p1.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								fill_color=color,
								alpha=alpha,
								line_color=color,
								hover_alpha = .7,
								hover_fill_color=color,
								nonselection_fill_color=color,
								nonselection_line_color=color,
								nonselection_line_alpha=1.0,
								selection_color=color,
								selection_fill_alpha=.5)
				
		elif int(self.roomNum)<300:
			#draw on second floor
			rooms2 = p2.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								fill_color=color,
								alpha=alpha,
								line_color=color,
								hover_fill_color=color,
								hover_alpha = .7,
								nonselection_fill_color=color,
								nonselection_line_color=color,
								nonselection_line_alpha=1.0,
								selection_color=color,
								selection_fill_alpha=.5)
		else:
			#draw on third floor
			rooms3 = p3.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								fill_color=color,
								alpha=alpha,
								line_color=color,
								hover_alpha = .7,
								hover_fill_color=color,
								nonselection_fill_color=color,
								nonselection_line_color=color,
								nonselection_line_alpha=1.0,
								selection_color=color,
								selection_fill_alpha=.5)

TOOLS = "box_zoom,box_select,resize,reset,hover,tap"

#draws first floor of WH
p1 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall First Floor")

p1.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="green", line_width=3)
p1.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]

#draws second floor of WH
p2 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall Second Floor")

p2.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="#F4A582", line_width=3)
p2.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]

#draws third floor of WH
p3 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall Third Floor")

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
		roomA.gendercolor = "green"
		roomA.bedtime = row[3]
		roomA.bedtimecolor = "yellow"
		roomA.lightsleep = row[4]
		roomA.halltime = row[5]
		coordinates = roomA.findCoordinates()
		roomA.top = coordinates[0]
		roomA.bottom = coordinates[1]
		roomA.left = coordinates[2]
		roomA.right = coordinates[3]
		roomA.drawRoom()
		#roomList.append(roomA) #creates list of all Room objects

dropdown_choices = [("Gender", "gender"), ("Bedtime", "bedtime"), ("Light Sleeper", "lightsleep"), ("Time in Hallway", "halltime")]
dropdown = Dropdown(label="Hallway Metrics", type="warning", menu=dropdown_choices)

tabs = Tabs(tabs=[Panel(child=p1, title="WH1"), Panel(child=p2, title="WH2"), Panel(child=p3, title="WH3")])
layout = vform(dropdown, tabs)

# show the results
save(tabs)
show(layout)