import math

def draw_grid(viewport):
    main_line_width = 2
    secondary_line_width = 1
    canvas = viewport.canvas



    for i in range(40):
        d = 20 * i
        canvas.create_line(d, 0, d, 800, fill="gray90", width=secondary_line_width/3)
        canvas.create_line(0, d, 800, d, fill="gray90", width=secondary_line_width/3)
    for i in range(20):
        d = 40 * i

        canvas.create_line(d, 0, d, 800, fill="gray80", width=secondary_line_width)
        canvas.create_line(0, d, 800, d, fill="gray80", width=secondary_line_width)
        vpos = (405,d)
        hpos = (d, 405)
        viewport.canvas.create_text(*vpos, text=int(screen_to_real(vpos)[1]), font=("Roboto", int(7)), fill= 'gray20')
        viewport.canvas.create_text(*hpos, text=int(screen_to_real(hpos)[0]), font=("Roboto", int(7)), fill= 'gray20')



    canvas.create_line(400, 0, 400, 800, fill="gray80", width = main_line_width)
    canvas.create_line(0, 400, 800, 400, fill="gray80", width = main_line_width)

#rounds up to the nearest 10
def roundup(x, base):
    #print("base = ", base)
    r = x%base
    if(r<base/2):
        x = x-r

    if(r>=base/2):
        x= x-r+base
    #print("x = ", x)
    return x

def screen_to_real(point, screen_width=800, grid_width=40):
    pointx, pointy = point
    x = (pointx - (screen_width / 2)) / (grid_width)
    x = roundup(x, 0.5)
    y = (pointy - (screen_width / 2)) / (grid_width)
    y = roundup(y, 0.5)
    return x, -y

def real_to_screen(point, screen_width=800, grid_width=40):
    pointx, pointy = point
    x = (pointx * grid_width) + (screen_width / 2)
    y = -(pointy * grid_width) + (screen_width / 2)

    return x, y

def draw_point(viewport,point, active, layer):

    point_radius = viewport.point_radius * (1+active)
    fill = viewport.point_fill
    x, y = real_to_screen(point)
    viewport.canvas.create_rectangle(x - point_radius, y - point_radius, x + point_radius,
                                     y + point_radius, fill=layer.colour, outline = layer.colour)

def draw_point_scale(viewport,point, active, layer, scale):

    point_radius = viewport.point_radius * (1+active) * scale
    fill = viewport.point_fill
    x, y = real_to_screen(point.position)
    viewport.canvas.create_rectangle(x - point_radius, y - point_radius, x + point_radius,
                                     y + point_radius, fill=layer.colour, outline = layer.colour)

def draw_lines(viewport, point_a, point_b, active, layer):
    x1, y1 = real_to_screen(point_a)
    x2, y2 = real_to_screen(point_b)
    line_mult = 1 + active

    viewport.canvas.create_line(x1, y1, x2, y2, width = layer.line_width * line_mult, fill = layer.colour, smooth=True)

def draw_label(viewport, point):
    xr, yr = real_to_screen(point)
    x, y = point
    label =  str(x) + ", " + str(y)

    viewport.canvas.create_text(xr, yr - (15), text=label, font=("Roboto", int(8)))

def rgb_to_hex(rgb):

    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale.
    Examples
    --------
        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - t) * a + t * b


def inv_lerp(a: float, b: float, v: float) -> float:
    """Inverse Linar Interpolation, get the fraction between a and b on which v resides.
    Examples
    --------
        0.5 == inv_lerp(0, 100, 50)
        0.8 == inv_lerp(1, 5, 4.2)
    """
    return (v - a) / (b - a)


def remap(i_min: float, i_max: float, o_min: float, o_max: float, v: float) -> float:
    """Remap values from one linear scale to another, a combination of lerp and inv_lerp.
    i_min and i_max are the scale on which the original value resides,
    o_min and o_max are the scale to which it should be mapped.
    Examples
    --------
        45 == remap(0, 100, 40, 50, 50)
        6.2 == remap(1, 5, 3, 7, 4.2)
    """
    return lerp(o_min, o_max, inv_lerp(i_min, i_max, v))
# this is a change



