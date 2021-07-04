import csv
from math import sqrt
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo

import matplotlib
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure

from path_find import *

matplotlib.use("TkAgg")


class DisplayUI:

    def __init__(self):
        """
        Setting up the UI for the program
        """
        # setting up the window
        self.root = Tk()
        self.root.title("Shortest Route Calculation")
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (width / 1.8, height / 1.5))

        # defining the instance variables that we will use throughout the program
        self.vertices = []
        self.edges = []
        self.x_vertices = []
        self.y_vertices = []
        self.ed = []
        self.mainFigure = Figure(figsize=(9, 8), dpi=80)
        self.main_subplot = self.mainFigure.add_subplot(111)
        self.frm = Frame(master=self.root)
        self.fig_canvas = FigureCanvasTkAgg(self.mainFigure, self.root)
        self.toolbar = ""
        self.origin_x = 0.0
        self.origin_y = 0.0
        self.destination_x = 0.0
        self.destination_y = 0.0
        self.origin_id = 0
        self.destination_id = 0
        self.current_event = ""

        # setting up the initial elements
        self.setup_elements()

    def setup_elements(self):
        """
        This method sets up all the button elements on the screen
        """
        # setting up buttons and associating the method to handle the events for it
        btn1 = Button(self.root, text='Upload Vertices File',
                      command=self.handle_vertices_file)
        btn1.grid(row=0, column=1)

        btn2 = Button(self.root, text='Upload Edges File', command=self.handle_edges_file)
        btn2.grid(row=0, column=2)

        btn3 = Button(self.root, text='Draw', command=self.generate_chart)
        btn3.grid(row=0, column=3)

        btn4 = Button(self.root, text='Select Origin Point', command=self.handle_origin_event)
        btn4.grid(row=0, column=4)

        btn5 = Button(self.root, text='Select Destination Point', command=self.handle_desti_event)
        btn5.grid(row=0, column=5)

        btn6 = Button(self.root, text='Calculate Route', command=self.find_shortest_path)
        btn6.grid(row=0, column=6)

        btn7 = Button(self.root, text='Clear Route', command=self.clear_charts)
        btn7.grid(row=0, column=7)

        btn8 = Button(self.root, text='Quit', command=self.quit_program)
        btn8.grid(row=0, column=8)

        # running the program on the loop
        self.root.mainloop()

    def get_clean_vertices(self, location):
        """
        Method that reads the csv file and loads the data
        :param location: path for the csv file
        """
        self.vertices = []
        with open(location, 'r') as csvfile:
            all_vertices = csv.reader(csvfile, delimiter=',')
            for row in all_vertices:
                i = 0
                if row[0][0].isdigit() and row[1][0].isdigit():
                    self.vertices.append([float(row[0]), float(row[1])])
                    i += 1
        self.x_vertices = [x[0] for x in self.vertices]
        self.y_vertices = [x[1] for x in self.vertices]

    def handle_vertices_file(self):
        """
        Event handler for when open vertices file is clicked
        """
        try:
            filename = filedialog.askopenfilename(title="Open Vertices File",
                                                  filetypes=(('csv files', '*.csv'),))
            self.get_clean_vertices(filename)
            showinfo('Success', filename + " successfully selected.")
        except:
            showinfo('Error', "Error opening the file")

    def get_clean_edges(self, location):
        """
        Method that reads the csv file and loads the data
        :param location: path for the csv file
        """
        self.edges = []
        with open(location, 'r') as csvfile:
            all_edge = csv.reader(csvfile, delimiter=',')
            for row in all_edge:
                if row[0].isdigit() and row[1].isdigit():
                    self.edges.append([int(row[0]), int(row[1])])

    def handle_edges_file(self):
        """
        Event handler for when open vertices file is clicked
        """
        try:
            filename = filedialog.askopenfilename(title="Open Edges File",
                                                  filetypes=(('csv files', '*.csv'),))
            self.get_clean_edges(filename)
            showinfo('Success', filename + " successfully selected.")
        except:
            showinfo('Error', "Error opening the file")

    @staticmethod
    def edges_as_reg(vertices_list, edges_list):
        edges_reg = []
        for edg in edges_list:
            edges_reg.append([vertices_list[edg[0]], vertices_list[edg[1]]])
        return edges_reg

    def generate_chart(self):
        """
        This method generates the charts which displayed in the windows
        """
        self.ed = self.edges_as_reg(self.vertices, self.edges)
        self.mainFigure = Figure(figsize=(9, 8), dpi=80)
        self.main_subplot = self.mainFigure.add_subplot(111)

        for line in self.ed:
            self.main_subplot.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], linewidth=3, color="#FEEDDE")
        self.main_subplot.plot(self.x_vertices, self.y_vertices, "o", color="#44857D", markersize=6)
        self.main_subplot.tick_params(left=False, right=False, labelleft=False,
                                      labelbottom=False, bottom=False)
        self.fig_canvas = FigureCanvasTkAgg(self.mainFigure, self.root)
        self.fig_canvas.get_tk_widget().grid(row=3, column=1, rowspan=10, columnspan=10)
        self.frm = Frame(master=self.root)
        self.frm.grid(row=22, column=2, columnspan=7)
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, self.frm)

    def click_origin(self, event):
        """
        Event handler which handles when origin is to be selected
        :param event: event from clicking the diagram
        """
        if event.inaxes is not None:
            self.clear_charts()
            closest = []
            closest = self.close_points(event.xdata, event.ydata, self.vertices)
            self.origin_x = closest[0]
            self.origin_y = closest[1]
            self.origin_id = closest[2]
            self.main_subplot.plot(self.origin_x, self.origin_y, "X", color="#FE6625", markersize=12)
            self.fig_canvas = FigureCanvasTkAgg(self.mainFigure, self.root)
            self.fig_canvas.get_tk_widget().grid(row=3, column=1, rowspan=10, columnspan=10)
            # bar2.get_tk_widget().pack()
            self.mainFigure.canvas.mpl_disconnect(event)

    def handle_origin_event(self):
        """
        Binding click event to method
        :return:
        """
        self.current_event = self.mainFigure.canvas.mpl_connect('button_press_event', self.click_origin)

    @staticmethod
    def close_points(x, y, points):
        """
        method that returns the closes points from x and y to the points
        """
        closest = []
        min_distance = (sqrt((x - points[0][0]) ** 2 + (y - points[0][1]) ** 2))
        current_distance = 0.0
        closest = [points[0][0], points[0][1], 0]

        for pnt in points:
            current_distance = (sqrt((x - pnt[0]) ** 2 + (y - pnt[1]) ** 2))
            if current_distance < min_distance:
                min_distance = current_distance
                closest = [pnt[0], pnt[1], points.index(pnt)]
        return closest

    def click_dest(self, event):
        """
        Event handler for the click destination
        """
        if event.inaxes is not None:
            self.clear_charts()
            closest = self.close_points(event.xdata, event.ydata, self.vertices)
            self.destination_x = closest[0]
            self.destination_y = closest[1]
            self.destination_id = closest[2]

            self.main_subplot.plot(self.origin_x, self.origin_y, "X", color="#FE6625", markersize=12)
            self.main_subplot.plot(self.destination_x, self.destination_y, "X", color="#FB9334", markersize=12)
            self.fig_canvas = FigureCanvasTkAgg(self.mainFigure, self.root)
            self.fig_canvas.get_tk_widget().grid(row=3, column=1, rowspan=10, columnspan=10)
            self.mainFigure.canvas.mpl_disconnect(event)

    def handle_desti_event(self):
        """
        This binds the destination click to the method
        :return:
        """
        self.current_event = self.mainFigure.canvas.mpl_connect('button_press_event', self.click_dest)

    @staticmethod
    def path_to_xy(pathlist, vertices_list):
        pathxy = []
        for i in pathlist:
            pathxy.append([vertices_list[i][0], vertices_list[i][1]])
        return pathxy

    @staticmethod
    def path_to_edge_xy(allpath):
        edgexy = []
        for i in range(len(allpath) - 1):
            edgexy.append([allpath[i], allpath[i + 1]])
        return edgexy

    def find_shortest_path(self):
        """
        Brain of the program which finds the shortest path
        :return:
        """
        tree = Dijkstra(self.vertices, self.edges)
        matrix = tree.build_adj_matrix()
        short_path = [int(pnt) for pnt in tree.find_shortest_route(self.origin_id, self.destination_id, matrix)]
        all_path = self.path_to_xy(short_path, self.vertices)
        path_edges_xy = self.path_to_edge_xy(all_path)
        x_vertices_path = [x[0] for x in all_path]
        y_vertices_path = [x[1] for x in all_path]
        for path_line in path_edges_xy:
            self.main_subplot.plot([path_line[0][0], path_line[1][0]], [path_line[0][1], path_line[1][1]],
                                   color="#003D59",
                                   linewidth=3)
        self.main_subplot.plot(x_vertices_path, y_vertices_path, "o", markersize=7, color="#FE6625")
        self.fig_canvas = FigureCanvasTkAgg(self.mainFigure, self.root)
        self.fig_canvas.get_tk_widget().grid(row=3, column=1, rowspan=10, columnspan=10)

    def clear_charts(self):
        """
        Clearing the charts
        :return:
        """
        self.fig_canvas.get_tk_widget().grid_forget()
        self.frm.grid_forget()
        self.generate_chart()

    def quit_program(self):
        """
        Quiting the program
        :return:
        """
        self.root.quit()


if __name__ == '__main__':
    # starting the program
    DisplayUI()
