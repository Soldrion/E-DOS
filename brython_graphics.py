from browser import bind, document, html, timer, window
import math
import random
import sys

FRAME_RATE = 40


class ErrorHandler(object):
    def write(self, value):
        window.postToParent({'type': 'program_stderr', 'stderr': value})


class OutputHandler(object):
    def write(self, value):
        window.postToParent({'type': 'program_stdout', 'stdout': value})


sys.stderr = ErrorHandler()
sys.stdout = OutputHandler()

elements = []
canvas = document["brython-canvas"]
ctx = canvas.getContext("2d")


def clear():
    ctx.clearRect(0, 0, canvas.width, canvas.height)


def set_size(width, height):
    canvas.attrs['width'] = width
    canvas.attrs['height'] = height


def draw():
    clear()
    for el in elements:
        if el.visible:
            el.draw()


def add(el):
    el.add()
    elements.append(el)


def remove(el):
    global elements
    el.remove()
    elements = list(filter(lambda e: e != el, elements))


def remove_all():
    for el in elements:
        remove(el)


def get_width():
    return canvas.width


def get_height():
    return canvas.height


def get_element_at(x, y):
    for el in elements:
        if el.contains_point(x, y):
            return el


handlers = {
    'mousemove': [],
    'click': [],
    'mousedown': [],
    'mouseup': [],
    'dblclick': [],
    'keydown': [],
    'keypress': [],
    'keyup': [],
}


@bind(document, "mousemove")
def mouse_move_handler(e):
    relativeX = e.clientX - canvas.offsetLeft
    relativeY = e.clientY - canvas.offsetTop
    try:
        for handler in handlers['mousemove']:
            handler(relativeX, relativeY)
    except Exception:
        pass


def add_mouse_move_handler(func):
    handlers['mousemove'].append(func)


@bind(document, "mousedown")
def mouse_down_handler(e):
    relativeX = e.clientX - canvas.offsetLeft
    relativeY = e.clientY - canvas.offsetTop
    try:
        for handler in handlers['mousedown']:
            handler(relativeX, relativeY)
    except Exception:
        pass


def add_mouse_down_handler(func):
    handlers['mousedown'].append(func)


@bind(document, "mouseup")
def mouse_up_handler(e):
    relativeX = e.clientX - canvas.offsetLeft
    relativeY = e.clientY - canvas.offsetTop
    try:
        for handler in handlers['mouseup']:
            handler(relativeX, relativeY)
    except Exception:
        pass


def add_mouse_up_handler(func):
    handlers['mouseup'].append(func)


@bind(document, "click")
def mouse_click_handler(e):
    relativeX = e.clientX - canvas.offsetLeft
    relativeY = e.clientY - canvas.offsetTop
    try:
        for handler in handlers['click']:
            handler(relativeX, relativeY)
    except Exception:
        pass


def add_mouse_click_handler(func):
    handlers['click'].append(func)


@bind(document, "dblclick")
def mouse_double_click_handler(e):
    relativeX = e.clientX - canvas.offsetLeft
    relativeY = e.clientY - canvas.offsetTop
    try:
        for handler in handlers['dblclick']:
            handler(relativeX, relativeY)
    except Exception:
        pass


def add_mouse_double_click_handler(func):
    handlers['dblclick'].append(func)


@bind(document, "keydown")
def key_down_handler(e):
    try:
        for handler in handlers['keydown']:
            handler(e)
    except Exception:
        pass


def add_key_down_handler(func):
    handlers['keydown'].append(func)


@bind(document, "keypress")
def key_press_handler(e):
    try:
        for handler in handlers['keypress']:
            handler(e)
    except Exception:
        pass


def add_key_press_handler(func):
    handlers['keypress'].append(func)


@bind(document, "keyup")
def key_up_handler(e):
    try:
        for handler in handlers['keyup']:
            handler(e)
    except Exception:
        pass


def add_key_up_handler(func):
    handlers['keyup'].append(func)


def interaction(name):
    def wrap(handler):
        handlers[name].append(handler)
    return wrap


DRAW_LOOP = timer.set_interval(draw, FRAME_RATE)


class Thing:
    x = 0
    y = 0
    dx = 0
    dy = 0
    width = 0
    height = 0
    color = '#000000'
    stroke = '#000000'
    lineWidth = 1
    filled = True
    visible = False

    def __init__(self, x=0, y=0, color='#000000'):
        self.x = x
        self.y = y
        self.color = color

    def add(self):
        self.visible = True

    def remove(self):
        self.visible = False

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_size(self, w, h):
        self.width = w
        self.height = h

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_stroke(self, stroke):
        self.stroke = stroke

    def get_stroke(self):
        return self.stroke

    def set_line_width(self, line_width):
        self.lineWidth = line_width

    def get_line_width(self):
        return self.lineWidth

    def set_filled(self, filled):
        self.filled = filled

    def is_filled(self):
        return bool(self.filled)

    def move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy


class Circle(Thing):
    radius = 0
    lineWidth = 0

    def __init__(self, radius, x=0, y=0):
        self.radius = radius
        self.x = x
        self.y = y
        self.set_filled(True)

    def draw(self):
        ctx.beginPath()
        ctx.arc(self.x, self.y, self.radius, 0, math.pi * 2)
        ctx.strokeStyle = self.stroke
        ctx.lineWidth = self.lineWidth
        if self.lineWidth:
            ctx.stroke()
        if self.is_filled():
            ctx.fillStyle = self.color
            ctx.fill()
        ctx.closePath()

    def contains_point(self, x, y):
        dx = x - self.x
        dy = y - self.y
        return self.radius * self.radius > dx * dx + dy * dy

    def get_radius(self):
        return self.radius

    def set_radius(self, radius):
        self.radius = radius


class Rectangle(Thing):
    x = 0
    y = 0
    width = 0
    height = 0
    roation = 0

    def __init__(self, width=0, height=0, x=0, y=0, rotation=0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rotation = rotation

    def draw(self):
        ctx.save()
        ctx.beginPath()
        ctx.translate(self.x + self.width / 2, self.y + self.height / 2)
        ctx.rotate(self.rotation)
        ctx.rect(-self.width / 2, -self.height / 2, self.width, self.height)
        ctx.fillStyle = self.color
        ctx.closePath()
        ctx.fill()
        ctx.restore()

    def contains_point(self, x, y):
        in_x = x >= self.x and x <= self.x + self.width
        in_y = y >= self.y and y <= self.y + self.height
        return in_x and in_y

    def get_rotation(self):
        return self.rotation

    def set_rotation(self, rotation):
        self.rotation = rotation


class Line(Thing):
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    width = 0
    height = 0
    rotation = 0

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self):
        ctx.fillStyle = self.color
        ctx.beginPath()
        ctx.strokeStyle = self.color
        ctx.lineWidth = self.lineWidth
        rotatedPoints = self.get_rotated_points(
            self.rotation, self.x1, self.y1, self.x2, self.y2)
        ctx.moveTo(rotatedPoints[0], rotatedPoints[1])
        ctx.lineTo(rotatedPoints[2], rotatedPoints[3])
        ctx.closePath()
        ctx.stroke()

    def get_rotated_points(self, rotation, x1=0, y1=0, x2=0, y2=0):
        midX = (x1 + x2) / 2
        midY = (y1 + y2) / 2
        sinAngle = math.sin(rotation)
        cosAngle = math.cos(rotation)

        # Rotate point 1
        x1 -= midX
        y1 -= midY
        newX = x1 * cosAngle - y1 * sinAngle
        newY = x1 * sinAngle + y1 * cosAngle
        x1 = newX + midX
        y1 = newY + midY

        # Rotate point 2
        x2 -= midX
        y2 -= midY
        newX = x2 * cosAngle - y2 * sinAngle
        newY = x2 * sinAngle + y2 * cosAngle
        x2 = newX + midX
        y2 = newY + midY

        return [x1, y1, x2, y2]

    def set_line_width(self, width):
        self.lineWidth = width

    def set_position(self, x, y):
        self.x1 = x
        self.y1 = y

    def set_start_point(self, x1, y1):
        self.x1 = x1
        self.y1 = y1

    def set_startpoint(self, x1, y1):
        self.x1 = x1
        self.y1 = y1

    def set_end_point(self, x2, y2):
        self.x2 = x2
        self.y2 = y2

    def set_endpoint(self, x2, y2):
        self.x2 = x2
        self.y2 = y2

    def move(self, dx, dy):
        self.x1 += dx
        self.x2 += dx
        self.y1 += dy
        self.y2 += dy

    def contains_point(self, x, y):
        in_x = x >= self.x and x <= self.x + self.width
        in_y = y >= self.y and y <= self.y + self.height
        return in_x and in_y

    def get_rotation(self):
        return self.rotation

    def set_rotation(self, rotation):
        self.rotation = rotation


class Text(Thing):
    x = 0
    y = 0
    width = 0
    height = 0
    font = '20pt Arial'
    label = ''

    def __init__(self, label, x=0, y=0, color=None, font=None):
        self.label = label
        self.x = x
        self.y = y
        if font:
            self.font = font
        if color:
            self.color = color
        self.reset_dimensions()

    def reset_dimensions(self):
        ctx.font = self.font
        self.width = ctx.measureText(self.label).width
        self.height = ctx.measureText('m').width * 1.2

    def draw(self):
        ctx.fillStyle = self.color
        ctx.beginPath()
        ctx.font = self.font
        self.reset_dimensions()
        ctx.translate(self.x, self.y)
        ctx.fillText(self.label, 0, 0)
        ctx.closePath()
        ctx.fill()
        ctx.translate(-self.x, -self.y)

    def contains_point(self, x, y):
        in_x = x >= self.x and x <= self.x + self.width
        in_y = y >= self.y and y <= self.y + self.height
        return in_x and in_y

    def get_text(self):
        return self.label

    def get_label(self):
        return self.label

    def set_text(self, label):
        self.label = label

    def set_label(self, label):
        self.label = label

    def set_font(self, font):
        self.font = font
        self.reset_dimensions()


class Image(Thing):
    x = 0
    y = 0
    width = 50
    height = 50
    filename = ''
    image = None
    rotation = 0
    display_from_data = False
    data = None

    NUM_CHANNELS = 4
    RED = 0
    GREEN = 1
    BLUE = 2
    ALPHA = 3

    def __init__(self, filename, x=0, y=0, width=50, height=50, rotation=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.filename = filename
        self.image = html.IMG('', src=filename)
        self.image.attrs['crossOrigin'] = 'Anonymous'
        self.image.attrs['src'] = filename

        def onload(e):
            self.display_from_data = True

        self.image.bind('load', onload)

    def draw(self):
        if self.display_from_data and self.data:
            ctx.beginPath()
            ctx.putImageData(self.data, self.x, self.y)
            ctx.closePath()
        else:
            ctx.save()
            ctx.beginPath()
            ctx.translate(self.x + self.width / 2, self.y + self.height / 2)
            ctx.rotate(self.rotation)
            ctx.drawImage(self.image, -self.width / 2, -
                          self.height / 2, self.width, self.height)
            ctx.closePath()
            ctx.restore()
        if self.display_from_data:
            self.get_image_data()

    def contains_point(self, x, y):
        in_x = x >= self.x and x <= self.x + self.width
        in_y = y >= self.y and y <= self.y + self.height
        return in_x and in_y

    def get_image_data(self):
        ctx.save()
        self.data = ctx.getImageData(self.x, self.y, self.width, self.height)
        ctx.restore()
        if self.data:
            self.display_from_data = True
        return self.data

    def get_image(self):
        return self.filename

    def set_image(self, filename):
        self.filename = filename

    def get_rotation(self):
        return self.rotation

    def set_rotation(self, rotation):
        self.rotation = rotation
        self.display_from_data = False

    def get_pixel(self, x, y):
        index = self.NUM_CHANNELS * (y * self.width + x)
        pixel = [
            self.data.data[index + self.RED],
            self.data.data[index + self.GREEN],
            self.data.data[index + self.BLUE],
            self.data.data[index + self.ALPHA]
        ]
        return pixel

    def get_red(self, x, y):
        return self.get_pixel(x, y)[self.RED]

    def get_green(self, x, y):
        return self.get_pixel(x, y)[self.GREEN]

    def get_blue(self, x, y):
        return self.get_pixel(x, y)[self.BLUE]

    def get_alpha(self, x, y):
        return self.get_pixel(x, y)[self.ALPHA]

    def set_pixel(self, x, y, component, val):
        index = self.NUM_CHANNELS * (y * self.width + x)
        self.data.data[index + component] = val

    def set_red(self, x, y, val):
        return self.set_pixel(x, y, self.RED, val)

    def set_green(self, x, y, val):
        return self.set_pixel(x, y, self.GREEN, val)

    def set_blue(self, x, y, val):
        return self.set_pixel(x, y, self.BLUE, val)

    def set_alpha(self, x, y, val):
        return self.set_pixel(x, y, self.ALPHA, val)


class Arc(Thing):

    # Constants for Arcs.
    DEGREES = 0
    RADIANS = 1

    counterclockwise = False
    radius = 0
    # set in radians, converted if angle_unit is DEGREES
    start_angle = 0
    end_angle = math.pi
    angle_unit = RADIANS
    x = 0
    y = 0

    # Choices are 'none', 'filled', 'pacman'
    fill_type = 'none'

    def __init__(self, radius, start_angle, end_angle, angle_unit=RADIANS, x=0, y=0):
        self.radius = radius
        self.angle_unit = angle_unit
        self.x = x
        self.y = y
        self.set_start_angle(start_angle)
        self.set_end_angle(end_angle)

    def draw(self):
        ctx.save()
        ctx.beginPath()
        ctx.arc(self.x, self.y, self.radius, self.start_angle, self.end_angle)
        ctx.strokeStyle = self.stroke
        ctx.lineWidth = self.lineWidth
        ctx.stroke()
        if self.fill_type == 'filled':
            ctx.fillStyle = self.color
            ctx.fill()
        elif self.fill_type == 'pacman':
            ctx.lineTo(self.x, self.y)
            ctx.fillStyle = self.color
            ctx.fill()
        ctx.closePath()
        ctx.restore()

    def contains_point(self, x, y):
        dx = x - self.x
        dy = y - self.y
        in_circle = self.radius * self.radius + self.lineWidth > dx * dx + dy * dy
        if not in_circle:
            return False

        # Get vector/ angle for the point
        vx = x - self.x
        vy = self.y - y
        theta = math.atan(vy / vx)

        # Adjust the arctan based on the quadran the point is in using the
        # position of the arc as the origin
        # Quadrant II and III
        if vx < 0:
            theta += math.pi
        # Quadrant IV
        elif vy < 0:
            theta += 2 * math.pi

        # Check whether angle is between start and end, take into account fill
        # direction
        between_CCW = theta >= self.start_angle and theta <= self.end_angle
        if self.counterclockwise:
            return between_CCW
        else:
            return not between_CCW

    def get_radius(self):
        return self.radius

    def set_radius(self, radius):
        self.radius = radius

    def set_fill_type(self, fill_type):
        # Choices are 'none', 'filled', 'pacman'
        self.fill_type = fill_type

    def get_start_angle(self):
        if self.angle_unit == self.RADIANS:
            return self.start_angle
        else:
            return self.radians_to_degrees(self.start_angle)

    def set_start_angle(self, start_angle):
        if self.angle_unit == self.RADIANS:
            self.start_angle = start_angle
        else:
            self.start_angle = self.degrees_to_radians(start_angle)

    def get_end_angle(self):
        if self.angle_unit == self.RADIANS:
            return self.end_angle
        else:
            return self.radians_to_degrees(self.end_angle)

    def set_end_angle(self, end_angle):
        if self.angle_unit == self.RADIANS:
            self.end_angle = end_angle
        else:
            self.end_angle = self.degrees_to_radians(end_angle)

    def get_direction(self):
        return self.counterclockwise

    # Parameter is Boolean taking
    def set_direction(self, is_counterclockwise):
        self.counterclockwise = is_counterclockwise

    def degrees_to_radians(self, angle_degrees):
        return angle_degrees / 180 * math.pi

    def radians_to_degrees(self, angle_radians):
        return angle_radians / math.pi * 180


class Color():
    red = '#de5844'
    RED = red
    orange = '#fbaf34'
    ORANGE = orange
    green = '#8cc63e'
    GREEN = green
    blue = '#27a9e1'
    BLUE = blue
    white = '#FFFFFF'
    WHITE = white
    black = '#000000'
    BLACK = black
    gray = '#cccccc'
    GRAY = gray
    grey = gray
    GREY = gray
    purple = '#9B30FF'
    PURPLE = purple
    yellow = '#FFFF00'
    YELLOW = yellow
    cyan = '#00FFFF'
    CYAN = cyan
    brown = '#964B00'
    BROWN = brown

    def random():
        return '#' + ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
