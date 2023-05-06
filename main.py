from tkinter import *
import drawing_lib as dl


class Viewport:

    def __init__(self, canvas, layer_screen):
        self.colours = ['#a85632', '#a4a832', '#3e7014', '#0d8994', '#3214b8', '#3214b8', '#3214b8', '#3214b8']
        self.canvas = canvas
        self.layer_screen = layer_screen
        self.buttons = []
        self.scale = 1.0

        self.layers = []
        self.active_layer = -1
        self.point_radius = 2
        self.point_fill = "white"

    def draw_grid(self):
        dl.draw_grid(self)

    def add_point(self,mouse_position):
        #if no layer exists create one
        if (not self.layers) or self.active_layer == -1:
            self.add_layer()

        screen_pos = (mouse_position.x, mouse_position.y)

        # check if point at this x already exists
        if not self.layers[self.active_layer].check_if_point_exists(screen_pos):
            real_pos = dl.screen_to_real(screen_pos)
            self.layers[self.active_layer].points.append(real_pos)
            print(screen_pos, real_pos, self.active_layer)
            self.draw()

    def add_layer(self):
        colour = self.colours[len(self.layers)%len(self.colours)]
        self.layers.append(Layer(self, colour))
        self.active_layer = len(self.layers)-1
        new_layer = len(self.layers)-1
        b = Button(self.layer_screen, width = 30, height = 3, text= 'Layer ' + str(new_layer), command= lambda:my_viewport.set_layer(new_layer), relief=SUNKEN, bg = colour )
        b.pack()
        self.buttons.append(b)

    def clear_all(self):
        for button in self.buttons:
            button.destroy()

        self.buttons.clear()
        self.layers.clear()
        self.active_layer = -1

        self.draw()

    def select(self, mouse_position):

        if self.layers:
            xr, yr = mouse_position.x, mouse_position.y
            x, y = dl.screen_to_real((xr, yr))
            print(x,y)
            for i, point in enumerate(self.layers[self.active_layer].points):
                if point[0] == x and point[1] == y:
                    self.layers[self.active_layer].selected = i



    def deselect(self):

        if self.layers:
            self.layers[self.active_layer].selected = -1


    def move_point(self, mouse_position):
        if self.layers and self.layers[self.active_layer].selected >= 0:

            xr, yr = mouse_position.x, mouse_position.y
            x, y = dl.screen_to_real((xr, yr))
            active = self.layers[self.active_layer]
            active.points[active.selected] = (x,y)
            self.draw()













    def set_layer(self, layer):



        if layer == self.active_layer:
            self.buttons[layer].config(relief = RAISED)

            self.active_layer = -1
            self.draw()
            return

        self.active_layer = layer
        for button in self.buttons:
            button.config(relief = RAISED)
        self.buttons[layer].config(relief = SUNKEN)
        self.draw()

    def draw(self):
        self.canvas.delete('all')
        self.draw_grid()
        for single_layer in self.layers:
            single_layer.draw()


class Layer:

    def __init__(self, parent_viewport, colour):
        self.index = len(parent_viewport.layers)
        self.parent = parent_viewport
        self.points = []
        self.colour = colour
        self.line_width = 1
        self.selected = -1

    def draw(self):
        # sort the points by x coordinate
        self.points.sort(key = lambda x: x[0])
        active = self.parent.active_layer == self.index
        # draw the lines
        for i, point in enumerate(self.points):
            if i < len(self.points)-1:

                other_point = self.points[i+1]


                dl.draw_lines(self.parent, point, other_point, active, self)

        # draw the points
        for point in self.points:
            dl.draw_point(self.parent, point, active, self)
            if active:
                dl.draw_label(self.parent, point)

    def check_if_point_exists(self,point):
        x, y = dl.screen_to_real(point)
        return any([x == point[0] for point in self.points])




        








#LAYOUT SECTION--------------------------------------------------------------------------------------------------------------------
root = Tk()
root.geometry("+500+50")
drawing_screen = Frame(root,width = 800, height = 800)
drawing_screen.place(relx= 0.5, rely= 0.5, anchor= CENTER)
drawing_screen.pack(side= LEFT)
canvas = Canvas(drawing_screen,width = 800, height = 800, background="white")
canvas.pack()

layer_screen = Frame(root, width = 200, height = 800)
layer_screen.place(relx= 0.5, rely= 0.5, anchor= CENTER)
layer_screen.pack(side= LEFT)
my_viewport = Viewport(canvas, layer_screen)
my_viewport.draw_grid()

clear_button = Button(layer_screen, width = 30, height = 3, text = 'CLEAR', command = lambda: my_viewport.clear_all())
clear_button.pack()

canvas.bind("<Double-Button-1>", lambda event: my_viewport.add_point(event))
canvas.bind("<Button-1>", lambda event: my_viewport.select(event))
canvas.bind("<B1-Motion>", lambda event: my_viewport.move_point(event))
canvas.bind("<ButtonRelease-1>", lambda event: my_viewport.deselect())

my_viewport.draw()




root.mainloop()