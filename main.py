import pygame
from pygame import QUIT, MOUSEBUTTONDOWN

w, h = 640, 480
window = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

points = []
polynomial = []

global_x_axis_offset = 40
global_y_scale = 40


def transform_coord(x_axis_offset, y_scale, x, y=None):
    if isinstance(x, tuple):
        x, y = x
    else:
        assert y is not None

    return x, h - ((y * y_scale) + x_axis_offset)


def draw_poly(window, color, poly, x_axis_offset, y_scale, width=1):
    prev = None
    for x, y in enumerate(poly):
        if prev is not None:
            pygame.draw.line(window, color, transform_coord(x_axis_offset, y_scale, prev), transform_coord(x_axis_offset, y_scale, x, y), width)
        # pygame.draw.circle(window, (255, 0, 0), transform_coord(x_axis_offset, y_scale, x, y), 1)
        prev = (x, y)


def calculate_polynomial(points):
    if len(points) < 2:
        return []
    else:
        polynomial = []
        totals = [0 for _ in range(w)]
        for lagrange_poly_index, (x_l, y_l) in enumerate(points):
            ys = []
            for x in range(0, w):
                numerator = 1
                for (index, (x_other, _)) in enumerate(points):
                    if index != lagrange_poly_index:
                        numerator *= (x - x_other)
                denomenator = 1
                for (index, (x_other, _)) in enumerate(points):
                    if index != lagrange_poly_index:
                        denomenator *= (x_l - x_other)

                y = numerator / denomenator
                ys.append(y)
                totals[x] += y * y_l

            polynomial.append(ys)

        polynomial.append(totals)
        return polynomial


colors = [
    (204, 68, 82),
    (36, 97, 128),
    (128, 29, 39),
    (47, 152, 204),
    (17, 128, 42),
    (67, 204, 98),
    (57, 204, 174),
    (102, 82, 74),
    (128, 124, 23),
    (204, 111, 78),
]


def color(index):
    if index >= len(colors):
        return 0, 0, 0
    return colors[index]


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == MOUSEBUTTONDOWN:
            points.append((event.pos[0], h - event.pos[1]))
            polynomial = calculate_polynomial(points)

    window.fill((255, 255, 255))

    for index, i in enumerate(points):
        pygame.draw.circle(window, color(index), (i[0], h - i[1]), 6)


    if global_x_axis_offset != 0:
        pygame.draw.line(window, (0, 0, 0), (0, h - global_x_axis_offset), (w, h - global_x_axis_offset))

    if len(polynomial) > 1:
        for index, poly in enumerate(polynomial[:-1]):
            draw_poly(window, color(index), poly, global_x_axis_offset, global_y_scale)
        draw_poly(window, (255, 0, 0), polynomial[-1], 0, 1, 2)

    clock.tick(60)
    pygame.display.update()