import numpy as np
import math


class VectorUtils:
    @staticmethod
    def project_coordinate(coordinate, camera_axis, zoom_factor):
        return (coordinate + camera_axis) * zoom_factor

    @staticmethod
    def correct_zoom(coord, zoom_factor):
        return coord * 1 / zoom_factor

    @staticmethod
    def calc_cursor_collision(x, y, object, zoom_factor):
        size = object.size * zoom_factor
        if object.posx + size >= x >= object.posx - size:
            if object.posy + size >= y >= object.posy - size:
                return True
        return False

    @staticmethod
    def calc_rect_collision(cursor, bottom_left, top_right):
        if bottom_left[0] < cursor[0] < top_right[0] and bottom_left[1] > cursor[1] > top_right[1]:
            return True
        return False

    @staticmethod
    def calc_vector(point_1, point_2):
        return np.array([point_2[0]-point_1[0], point_2[1]-point_1[1]])

    @staticmethod
    def unit_vector(vector):
        length = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))
        if length != 0:
            return np.array([vector[0]/length, vector[1]/length])
        else:
            return np.array([0, 0])

    @staticmethod
    def normal_vector(vector):
        return np.array([-vector[1], vector[0]])

    @staticmethod
    def uninormal_vector(vector):
        return VectorUtils.unit_vector(VectorUtils.normal_vector(vector))

    @staticmethod
    def get_rect_center(c1, c2, c3, c4):
        v1 = VectorUtils.calc_vector(c1, c2) * 0.5
        v2 = VectorUtils.calc_vector(c3, c1) * 0.5
        return c1 - v2 + v1

    @staticmethod
    def rotate_point(point, angle, origin):
        translated_point = point - origin
        temp = np.array([translated_point[0] * math.cos(angle) - translated_point[1] * math.sin(angle),
                         translated_point[0] * math.sin(angle) + translated_point[1] * math.cos(angle)])
        return temp + origin

    @staticmethod
    def get_vector_rotation(vector):
        coord_vector = np.array([1, 0])
        scalarproduct = (vector[0]*coord_vector[0]+vector[1]*coord_vector[1])
        absolute_vector = math.sqrt(vector[0]**2 + vector[1]**2)
        absolute_coord_vector = math.sqrt(coord_vector[0]**2 + coord_vector[1]**2)
        return math.acos(scalarproduct / (absolute_vector * absolute_coord_vector))

    @staticmethod
    def connection_cursor_collision(connection, cursor_x, cursor_y, camera_x, camera_y, zoom_factor):
        for vert in range(0, len(connection.vertices) - 1):
            connection_bounding_box_width = 15
            uninormal_vector = np.array(VectorUtils.calc_vector(connection.vertices[vert],
                                                                connection.vertices[vert + 1]))
            uninormal_vector = VectorUtils.uninormal_vector(uninormal_vector)
            uninormal_vector = uninormal_vector * connection_bounding_box_width

            c = [connection.vertices[vert] + uninormal_vector,
                 connection.vertices[vert] - uninormal_vector,
                 connection.vertices[vert + 1] + uninormal_vector,
                 connection.vertices[vert + 1] - uninormal_vector]
            for i in range(0, len(c)):
                c[i][0] = VectorUtils.project_coordinate(c[i][0], camera_x, zoom_factor)
                c[i][1] = VectorUtils.project_coordinate(c[i][1], camera_y, zoom_factor)

            temp_angle = VectorUtils.get_vector_rotation(np.array(VectorUtils.calc_vector(c[0], c[2])))
            temp_origin = VectorUtils.get_rect_center(c[0], c[1], c[2], c[3])
            temp_cursor = np.array([cursor_x + camera_x, cursor_y + camera_y])
            temp_cursor = temp_cursor * zoom_factor
            if connection.vertices[vert][1] < connection.vertices[vert + 1][1]:
                temp_angle = -temp_angle
            temp_cursor = VectorUtils.rotate_point(temp_cursor, temp_angle, temp_origin)

            bottom_left = c[0]
            top_right = c[3]

            if VectorUtils.calc_rect_collision(temp_cursor, VectorUtils.rotate_point(bottom_left, temp_angle, temp_origin),
                                               VectorUtils.rotate_point(top_right, temp_angle, temp_origin)):
                return True
        return False
