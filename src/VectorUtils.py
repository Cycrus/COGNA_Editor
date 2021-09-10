"""
VectorUtils.py

A class containing static methods for manipulating vectors.

Author: Cyril Marx
Date: 09.09.2021
"""

import numpy as np
import math


class VectorUtils:
    @staticmethod
    def project_coordinate(coordinate, camera_axis, zoom_factor):
        """
        Projects some coordinates on the canvas.
        :param coordinate:  The 2D coordinate to project.
        :param camera_axis: A 2D value representing where the camera is looking at.
        :param zoom_factor: The zoom factor as a float value.
        :return:            The projected 2D coordinate.
        """
        return (coordinate + camera_axis) * zoom_factor

    @staticmethod
    def correct_zoom(coord, zoom_factor):
        """
        Corrects a coordinate with a zoom factor.
        :param coord:       The coordinate to correct.
        :param zoom_factor: The zoom factor used for correction.
        :return:            The corrected coordinate.
        """
        return coord * 1 / zoom_factor

    @staticmethod
    def calc_cursor_collision(x, y, object, zoom_factor):
        """
        Calculates if the cursor collides with a certain object.
        :param x:           The x coordinate of the cursor.
        :param y:           The y coordinate of the cursor.
        :param zoom_factor: The zoom factor of the canvas.
        :return:            A boolean indicating if a collision happens.
        """
        size = object.size * zoom_factor
        if object.posx + size >= x >= object.posx - size:
            if object.posy + size >= y >= object.posy - size:
                return True
        return False

    @staticmethod
    def calc_rect_collision(cursor, bottom_left, top_right):
        """
        Calculates if the cursor collides with a rectangle based by two corners of the rectangle.
        :param cursor:      The cursor as a 2D vector.
        :param bottom_left: The bottom left corner coordinate of the rectangle.
        :param top_right:   The top right corner coordinate of the rectangle.
        :return:            A boolean indicating if a collision happens.
        """
        if bottom_left[0] < cursor[0] < top_right[0] and bottom_left[1] > cursor[1] > top_right[1]:
            return True
        return False

    @staticmethod
    def calc_rect_collision_by_size(cursor, obj_pos, size_x, size_y, zoom_factor):
        """
        Calculates if the cursor collides with a rectangle based on its size.
        :param cursor:      The cursor as a 2D vector.
        :param obj_pos:     The position of the rectangle as a 2D vector.
        :param size_x:      The x size of the rectangle.
        :param size_y:      The y size of the rectangle.
        :param zoom_factor: The zoom factor of the canvas.
        :return:            A boolean indicating if a collision happens.
        """
        corr_size_x = size_x * zoom_factor
        corr_size_y = size_y * zoom_factor
        bottom_left = [obj_pos[0] - corr_size_x, obj_pos[1] + corr_size_y]
        top_right = [obj_pos[0] + corr_size_x, obj_pos[1] - corr_size_y]

        if bottom_left[0] < cursor[0] < top_right[0] and bottom_left[1] > cursor[1] > top_right[1]:
            return True
        return False

    @staticmethod
    def calc_vector(point_1, point_2):
        """
        Calculates a vector from two points.
        :param point_1: Point 1
        :param point_2: Point 2
        :return:        The vector between both points.
        """
        return np.array([point_2[0]-point_1[0], point_2[1]-point_1[1]])

    @staticmethod
    def unit_vector(vector):
        """
        Calculates the unitvector from a certain vector.
        :param vector:  The vector to manipulate.
        :return:        The unitvector.
        """
        length = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))
        if length != 0:
            return np.array([vector[0]/length, vector[1]/length])
        else:
            return np.array([0, 0])

    @staticmethod
    def normal_vector(vector):
        """
        Calculates the normal vector to a vector.
        :param vector:  The vector to normalize.
        :return:        The uninormalized vector.
        """
        return np.array([-vector[1], vector[0]])

    @staticmethod
    def uninormal_vector(vector):
        """
        Uninormalizes a vector.
        :param vector:  The vector to manipulate.
        :return:        The uninormalized vector.
        """
        return VectorUtils.unit_vector(VectorUtils.normal_vector(vector))

    @staticmethod
    def get_rect_center(c1, c2, c3, c4):
        """
        Calculates the center of a rectangle.A
        :param c1:  Corner 1
        :param c2:  Corner 2
        :param c3:  Corner 3
        :param c4:  Corner 4
        :return:    The center of the rectangle as a 2D vector.
        """
        v1 = VectorUtils.calc_vector(c1, c2) * 0.5
        v2 = VectorUtils.calc_vector(c3, c1) * 0.5
        return c1 - v2 + v1

    @staticmethod
    def rotate_point(point, angle, origin):
        """
        Rotates a point around a certain origin.
        :param point:   The point to rotate.
        :param angle:   The rotation in degree.
        :param origin:  The origin point to rotate around.
        :return:        The rotated point position.
        """
        translated_point = point - origin
        temp = np.array([translated_point[0] * math.cos(angle) - translated_point[1] * math.sin(angle),
                         translated_point[0] * math.sin(angle) + translated_point[1] * math.cos(angle)])
        return temp + origin

    @staticmethod
    def get_vector_rotation(vector):
        """
        Calculates the rotation of a vector to the x axis.
        :param vector:  The vector to check.
        :return:        The rotation angle in degree.
        """
        coord_vector = np.array([1, 0])
        scalarproduct = (vector[0]*coord_vector[0]+vector[1]*coord_vector[1])
        absolute_vector = math.sqrt(vector[0]**2 + vector[1]**2)
        absolute_coord_vector = math.sqrt(coord_vector[0]**2 + coord_vector[1]**2)
        dividend = (absolute_vector * absolute_coord_vector)
        if dividend != 0:
            return math.acos(scalarproduct / dividend)
        else:
            return 0

    @staticmethod
    def connection_cursor_collision(connection, cursor_x, cursor_y, camera_x, camera_y, zoom_factor):
        """
        Checks if the cursor collides with a connection.
        :param connection:      The connection to check.
        :param cursor_x:        The x coordinate of the cursor.
        :param cursor_y:        The y coordinate of the cursor.
        :param camera_x:        The x coordinate of the camera.
        :param camera_y:        The y coordinate of the camera.
        :param zoom_factor:     The zoom factor of the canvas
        :return:                A boolean indicating if a collision happens.
        """
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
