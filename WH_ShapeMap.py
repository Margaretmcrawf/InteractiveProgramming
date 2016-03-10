from bokeh.models import BoxSelectTool, BoxZoomTool, LassoSelectTool, HoverTool, Quad
from bokeh.plotting import figure, output_file, show, gridplot, ColumnDataSource, output_server, hplot
from bokeh.models.widgets import Dropdown, Panel, Tabs, CheckboxButtonGroup, RadioGroup
from bokeh.io import output_file, show, vform, save
import csv

#PROJECT OVERVIEW:
#Create an interactive map of West Hall showing hallway culture via gender distribution, sleeping habits, time spent in hallways, etc.
#(If we hear back from STAR, we'll also have data on how people move from year to year, which will be awesome to implement)

#PROGRESS:
#currently outputs to an html file which has 4 tabs displaying 3 floors of WH with data from freshmen 
#rooms are currently blue squares, have hover functionality with correct labels but no data
#rooms are 1 unit squares with an x position between 0 and 11 and a y position between 1 and 13.
#Also have buttons that are currently nonfunctional but are planned to be able to display different color coordinations for each room.
#Initializes and draws all rooms in correct places from a .csv file with data from survey sent to first years.

#NEXT STEPS:
#Get more room data from people (keep collecting survey responses)
#Make import for roommate names work correctly
#Make hover display given room number and inhabitant names instead of '???'



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
		coordinates = [1,0,0,1] #top, bottom, left, right (respectively)
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

	def findColors(self):
		colors = [0,0,0,0]#gender, bedtime, light sleeper, hallway time (respectively)

		#gender
		if self.gender=='Male':
			colors[0] = '#663399'
		elif self.gender=='Female':
			colors[0] = '#FE5B35'
		else: colors[0] = '#87CEEB'

		#bedtime
		bedColors =	{'11':'#E9E7F1','11.5':'#D4D0E4','12':'#BEB8D7','12.5':'#A9A1C9','1':'#9489BC','1.5':'#7E72AF','2':'#695AA1','2.5':'#534294','3':'#3E2B87'}
		colors[1] = bedColors.get(self.bedtime, 'firebrick')

		#light sleeper
		lightsleepcolors = {'1':'#00B34D','1.5':'#00A145','2':'#008F3D','2.5':'#007D35','3':'#006B2E'}
		colors[2] = lightsleepcolors.get(self.lightsleep,'firebrick')

		#hallway time
		hallwaycolors = {'1':'#CEF1FO','1.5':'#B6EBE9','2':'#9EE4E2','2.5':'#86DEDB','3':'#6DD7D3','3.5':'#55D0CC','4':'#3DCAC5','4.5':'#25CBE','5':'#0DBDB7'}
		colors[3] = hallwaycolors.get(self.halltime,'firebrick')
		return colors

	def drawRoom(self): 
		if self.gender == 'N/A':
			gendercolor='grey'
			bedtimecolor='grey'
			lightsleepcolor='grey'
			halltimecolor='grey'
			alpha = .3
		else: 
			gendercolor=self.gendercolor
			bedtimecolor=self.bedtimecolor
			lightsleepcolor=self.lightsleepcolor
			halltimecolor=self.halltimecolor
			alpha = 1.0

		if int(self.roomNum)<200:
			#draw on first floor
			rooms1a = a1.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								fill_color=gendercolor,
								alpha=alpha,
								line_color=gendercolor,
								hover_alpha = .7,
								hover_fill_color=gendercolor,
								nonselection_fill_color=gendercolor,
								nonselection_line_color=gendercolor,
								nonselection_line_alpha=1.0,
								selection_color=gendercolor,
								selection_fill_alpha=.5)
			rooms1b = b1.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								fill_color=bedtimecolor,
								alpha=alpha,
								line_color=bedtimecolor,
								hover_alpha = .7,
								hover_fill_color=bedtimecolor,
								nonselection_fill_color=bedtimecolor,
								nonselection_line_color=bedtimecolor,
								nonselection_line_alpha=1.0,
								selection_color=bedtimecolor,
								selection_fill_alpha=.5)
			rooms1c = c1.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								fill_color=lightsleepcolor,
								alpha=alpha,
								line_color=lightsleepcolor,
								hover_alpha = .7,
								hover_fill_color=lightsleepcolor,
								nonselection_fill_color=lightsleepcolor,
								nonselection_line_color=lightsleepcolor,
								nonselection_line_alpha=1.0,
								selection_color=lightsleepcolor,
								selection_fill_alpha=.5)
			rooms1d = d1.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								fill_color=halltimecolor,
								alpha=alpha,
								line_color=halltimecolor,
								hover_alpha = .7,
								hover_fill_color=halltimecolor,
								nonselection_fill_color=halltimecolor,
								nonselection_line_color=halltimecolor,
								nonselection_line_alpha=1.0,
								selection_color=halltimecolor,
								selection_fill_alpha=.5)

		elif int(self.roomNum)<300:
			#draw on second floor
			rooms2a = a2.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								fill_color=gendercolor,
								alpha=alpha,
								line_color=gendercolor,
								hover_alpha = .7,
								hover_fill_color=gendercolor,
								nonselection_fill_color=gendercolor,
								nonselection_line_color=gendercolor,
								nonselection_line_alpha=1.0,
								selection_color=gendercolor,
								selection_fill_alpha=.5)
			rooms2b = b2.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								fill_color=bedtimecolor,
								alpha=alpha,
								line_color=bedtimecolor,
								hover_alpha = .7,
								hover_fill_color=bedtimecolor,
								nonselection_fill_color=bedtimecolor,
								nonselection_line_color=bedtimecolor,
								nonselection_line_alpha=1.0,
								selection_color=bedtimecolor,
								selection_fill_alpha=.5)
			rooms2c = c2.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								fill_color=lightsleepcolor,
								alpha=alpha,
								line_color=lightsleepcolor,
								hover_alpha = .7,
								hover_fill_color=lightsleepcolor,
								nonselection_fill_color=lightsleepcolor,
								nonselection_line_color=lightsleepcolor,
								nonselection_line_alpha=1.0,
								selection_color=lightsleepcolor,
								selection_fill_alpha=.5)
			rooms2d = d2.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								fill_color=halltimecolor,
								alpha=alpha,
								line_color=halltimecolor,
								hover_alpha = .7,
								hover_fill_color=halltimecolor,
								nonselection_fill_color=halltimecolor,
								nonselection_line_color=halltimecolor,
								nonselection_line_alpha=1.0,
								selection_color=halltimecolor,
								selection_fill_alpha=.5)
		else:
			#draw on third floor
			rooms3a = a3.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								fill_color=gendercolor,
								alpha=alpha,
								line_color=gendercolor,
								hover_alpha = .7,
								hover_fill_color=gendercolor,
								nonselection_fill_color=gendercolor,
								nonselection_line_color=gendercolor,
								nonselection_line_alpha=1.0,
								selection_color=gendercolor,
								selection_fill_alpha=.5)
			rooms3b = b3.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								fill_color=bedtimecolor,
								alpha=alpha,
								line_color=bedtimecolor,
								hover_alpha = .7,
								hover_fill_color=bedtimecolor,
								nonselection_fill_color=bedtimecolor,
								nonselection_line_color=bedtimecolor,
								nonselection_line_alpha=1.0,
								selection_color=bedtimecolor,
								selection_fill_alpha=.5)
			rooms3c = c3.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								fill_color=lightsleepcolor,
								alpha=alpha,
								line_color=lightsleepcolor,
								hover_alpha = .7,
								hover_fill_color=lightsleepcolor,
								nonselection_fill_color=lightsleepcolor,
								nonselection_line_color=lightsleepcolor,
								nonselection_line_alpha=1.0,
								selection_color=lightsleepcolor,
								selection_fill_alpha=.5)
			rooms3d = d3.quad(top=self.top,bottom=self.bottom, left=self.left, right=self.right,
								nonselection_fill_alpha=0.01,
								fill_color=halltimecolor,
								alpha=alpha,
								line_color=halltimecolor,
								hover_alpha = .7,
								hover_fill_color=halltimecolor,
								nonselection_fill_color=halltimecolor,
								nonselection_line_color=halltimecolor,
								nonselection_line_alpha=1.0,
								selection_color=halltimecolor,
								selection_fill_alpha=.5)

TOOLS = "box_zoom,box_select,resize,reset,hover,tap"

#GENDER 
#draws first floor of WH
a1 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall First Floor")
a1.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="#F4A582", line_width=3)
a1.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]
#draws second floor of WH
a2 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall Second Floor")
a2.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="#F4A582", line_width=3)
a2.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]
#draws third floor of WH
a3 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall Third Floor")
a3.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="#F4A582", line_width=3)
a3.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]

a = hplot(a1, a2, a3)

#BEDTIME
#draws first floor of WH
b1 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall First Floor")
b1.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="#F4A582", line_width=3)
b1.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]
#draws second floor of WH
b2 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall Second Floor")
b2.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="#F4A582", line_width=3)
b2.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]
#draws third floor of WH
b3 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall Third Floor")
b3.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="#F4A582", line_width=3)
b3.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]

b = hplot(b1, b2, b3)

#LIGHT SLEEPER
#draws first floor of WH
c1 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall First Floor")
c1.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="#F4A582", line_width=3)
c1.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]
#draws second floor of WH
c2 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall Second Floor")
c2.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="#F4A582", line_width=3)
c2.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]
#draws third floor of WH
c3 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall Third Floor")
c3.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="#F4A582", line_width=3)
c3.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]

c = hplot(c1, c2, c3)

#HALLWAY TIME
#draws first floor of WH
d1 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall First Floor")
d1.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="#F4A582", line_width=3)
d1.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]
#draws second floor of WH
d2 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall Second Floor")
d2.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="#F4A582", line_width=3)
d2.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]
#draws third floor of WH
d3 = figure(plot_width=400, plot_height=400, tools=TOOLS,title="West Hall Third Floor")
d3.segment(x0=[0, 4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0], y0=[13, 13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10], 
		  x1=[4, 4, 7, 7, 11, 11, 7, 7, 4, 4, 0, 0], y1=[13, 12, 12, 13, 13, 10, 10, 1, 1, 10, 10, 13], color="#F4A582", line_width=3)
d3.select_one(HoverTool).tooltips = [('Room Number','@roomNum'),('Inhabitants','@roommates')]

d = hplot(d1, d2, d3)

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

		colors = roomA.findColors()
		roomA.gendercolor = colors[0]
		roomA.bedtimecolor = colors[1]
		roomA.lightsleepcolor = colors[2]
		roomA.halltimecolor = colors[3]

		coordinates = roomA.findCoordinates()
		roomA.top = coordinates[0]
		roomA.bottom = coordinates[1]
		roomA.left = coordinates[2]
		roomA.right = coordinates[3]
		roomA.drawRoom()

		#roomList.append(roomA) #creates list of all Room objects

tabs = Tabs(tabs=[Panel(child=a, title="Gender"), Panel(child=b, title="Bedtime"), Panel(child=c, title="Heaviness of Sleep"), Panel(child=d, title="Time Spent In Hallway")])

# show the results
show(tabs)
