from tkinter import *
import drawing_lib as dl
import numpy as np


class Viewport:
    # this class hold all object displayed on the canvas and deals with adding, moving and removing points
    # it also calls the draw method of layer objects

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
        self.layers[self.active_layer].add_point(screen_pos)
        self.draw()

    def add_layer(self):

        self.layers.append(Layer(self))

        self.active_layer = len(self.layers)-1
        new_layer = len(self.layers)-1
        colour = self.layers[self.active_layer].colour
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

            for i, point in enumerate(self.layers[self.active_layer].points):
                if point[0] == x and point[1] == y:
                    self.layers[self.active_layer].point_select(i)

    def remove(self, mouse_position):
        if self.layers:
            xr, yr = mouse_position.x, mouse_position.y
            x, y = dl.screen_to_real((xr, yr))
            to_delete = -1
            for i, point in enumerate(self.layers[self.active_layer].points):
                if point[0] == x and point[1] == y:
                    to_delete = i
            self.layers[self.active_layer].remove_point(to_delete)


    def deselect(self):
        if self.layers:
            self.layers[self.active_layer].point_deselect()

    def move_point(self, mouse_position):
        if self.layers and self.layers[self.active_layer].selected >= 0:

            xr, yr = mouse_position.x, mouse_position.y
            x, y = dl.screen_to_real((xr, yr))

            self.layers[self.active_layer].move_point((x,y))
            self.draw()

    def set_layer(self, layer):

        if layer == self.active_layer:
            self.buttons[layer].config(relief = RAISED)
            self.layers[self.active_layer].active = False
            self.active_layer = -1
            self.draw()
            return

        self.active_layer = layer
        self.layers[self.active_layer].active = True
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

    def __init__(self, parent_viewport):
        self.active = True
        self.index = len(parent_viewport.layers)
        self.parent = parent_viewport
        self.points = []
        self.animated_points = []
        self.colour = dl.rgb_to_hex(list(np.random.choice(range(256), size=3)))
        self.line_width = 1
        self.selected = -1

    def draw(self):
        # sort the points by x coordinate
        self.points.sort(key = lambda x: x[0])
        self.animated_points.sort(key = lambda x: x.my_x())

        # draw the lines
        for i, point in enumerate(self.points):
            if i < len(self.points)-1:
                other_point = self.points[i+1]
                dl.draw_lines(self.parent, point, other_point, self.active, self)

        # draw the points
        '''for point in self.points:
        # deprecated in favor of animated points
            dl.draw_point(self.parent, point, active, self)
            if active:
                dl.draw_label(self.parent, point)'''

        for point in self.animated_points:
            point.draw()

    def check_if_point_exists(self,point):
        x, y = dl.screen_to_real(point)
        return any([x == point[0] for point in self.points])

    def add_point(self, position):
        print('addpoint')
        # check if point at this x already exists
        if not self.check_if_point_exists(position):
            real_pos = dl.screen_to_real(position)
            self.points.append(real_pos)
            self.animated_points.append(Point(real_pos, self))

    def remove_point(self, index):
        if len(self.points) >= index and index != -1:
            del(self.points[index])
            del(self.animated_points[index])

    def move_point(self, new_position):
        if self.selected != -1:
            self.points[self.selected] = (new_position)
            self.animated_points[self.selected].change_position(new_position)

    def point_select(self, index):
        self.selected = index
        self.animated_points[index].select()

    def point_deselect(self):
        if self.selected >-1:
            self.animated_points[self.selected].deselect()
            self.selected = -1




class Point:
    def __init__(self, position, parent):
        self.parent = parent
        self.position = position
        self.animation_length = 25
        self.start_scale = 5
        self.end_scale = 1
        self.time_elapsed = 0
        self.animate = True
        self.selected = False


    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False
    def change_position(self, new_position):
        self.position = new_position
    def my_x(self):

        return self.position[0]

    def draw(self):
        if self.animate:

            scale = dl.remap(0, self.animation_length, self.start_scale, self.end_scale, self.time_elapsed)

            dl.draw_point_scale(self.parent.parent, self, self.parent.active, self.parent, scale)
            self.time_elapsed +=1
            if self.time_elapsed >= self.animation_length:
                self.animate = False
        else:
            scale = 1 + self.selected/2
            dl.draw_point_scale(self.parent.parent, self, self.parent.active, self.parent, scale)





        








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
canvas.bind("<ButtonRelease-3>", lambda event: my_viewport.remove(event))

my_viewport.draw()




while True:
    try:
        my_viewport.draw()
    except:
        pass
    root.update_idletasks()
    root.update()

