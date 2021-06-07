"""
the moon module is approximately intended for calculating the coordinate of the moon at a certain time,
the calculations are not very accurate since a circle instead of an ellipse is taken for the triangle of
the moon's rotation around the earth, which in turn causes some inaccuracies
"""
import datetime
import math
import ephem
import datetime as dt
import constants


class Moon:
    """
    the Moon class where object attributes are the coordinates of the
    moon at a specified time and date of these coordinates
    """

    def __init__(self, date_to_calculate: datetime.datetime):
        self.ra = None
        self.dec = None
        # start date with which we will compare to get the coordinates of the current date
        self.date_to_calculate = date_to_calculate
        start_date = dt.datetime(constants.start_date_year,
                                 constants.start_date_month,
                                 constants.start_date_day,
                                 constants.start_date_hour,
                                 constants.start_date_minute,
                                 constants.start_date_second)
        # time difference in seconds from the start date to the current date
        self.delta_time = int((self.date_to_calculate - start_date).total_seconds())
        # declination of the plane of the movement of the moon with a comparison of the celestial equator
        self.angle_slope = constants.angle_slope
        # the period of the full rotation of the moon around the earth in seconds
        period_for_on_cycle = constants.period_for_on_cycle
        # angle of full rotation of the moon around the earth in seconds
        perimeter = constants.perimeter
        # the angle of movement of the moon in 1 second
        self.one_sec_walk = perimeter / period_for_on_cycle
        # the size of the angle of the maximum and minimum declination of the moon
        dec_angle_slope_interval = 2 * self.angle_slope
        # rough calculation of the change in the ra coordinate in one second
        self.one_sec_walk_ra = math.cos(self.angle_slope) * self.one_sec_walk
        # rough calculation of the change in the dec coordinate in one second
        self.one_sec_walk_dec = dec_angle_slope_interval / period_for_on_cycle
        # the epham package is used to take the starting coordinates of the moon for calculation
        moon = ephem.Moon()
        moon.compute(constants.start_date)
        ra_ephem_start = moon.ra
        dec_ephem_start = moon.dec
        ra_start_list = str(ra_ephem_start).split(':')
        dec_start_list = str(dec_ephem_start).split(':')
        # RA coordinates when the moon deflection reaches its maximum and minimum values
        ra_dec_min = constants.ra_dec_min
        ra_dec_max = constants.ra_dec_max
        ra_dec_min_list = ra_dec_min.split(':')
        ra_dec_max_list = ra_dec_max.split(':')
        # converting the coordinates of the moon to seconds for calculations
        self.ra_start = float(ra_start_list[0]) * 3600 * 15 + float(ra_start_list[1]) * 60 + float(ra_start_list[2])
        self.dec_start = float(dec_start_list[0]) * 3600 + float(dec_start_list[1]) * 60 + float(dec_start_list[2])
        self.ra_dec_min = float(ra_dec_min_list[0]) * 3600 * 15 + float(ra_dec_min_list[1]) * 60 + float(
            ra_dec_min_list[2])
        self.ra_dec_max = float(ra_dec_max_list[0]) * 3600 * 15 + float(ra_dec_max_list[1]) * 60 + float(
            ra_dec_max_list[2])

    def ra_dec_calculate(self) -> dict:
        """
        the function calculates the coordinates of the moon at a certain time,
        for this you need the starting coordinates and the date of these coordinates,
        the point is to calculate the delta ra and delta dec in 1 second and cyclically
        add the previous coordinate until the required coordinates are calculated
        :return:
        """
        for sec in range(self.delta_time):
            if 0 < self.ra_start + self.one_sec_walk_ra < 360 * 3600:
                self.ra = self.ra_start + self.one_sec_walk_ra
                self.ra_start = self.ra
            else:
                self.ra = self.ra_start + self.one_sec_walk_ra - 360 * 3600
                self.ra_start = self.ra
            if self.ra_dec_min < self.ra < self.ra_dec_max:
                self.dec = self.dec_start - self.one_sec_walk_dec
                self.dec_start = self.dec
            else:
                self.dec = self.dec_start + self.one_sec_walk_dec
                self.dec_start = self.dec

        ra_res = f'{int(self.ra // (3600 * 15))}:{int((self.ra % 3600) // 60)}:' \
                 f'{round(float((self.ra % 3600) % 60), 1)}'
        dec_res = f'{int(self.dec // 3600)}:{int((self.dec % 3600) // 60)}:' \
                  f'{round(float((self.dec % 3600) % 60), 1)}'
        moon = {
            'ra': ra_res,
            'dec': dec_res
        }
        return moon
