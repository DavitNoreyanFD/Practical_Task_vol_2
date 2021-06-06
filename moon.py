import datetime
import math
import ephem
import datetime as dt
import constants


class Moon:
    def __init__(self, date_to_calculate):
        self.ra = None
        self.dec = None
        self.date_to_calculate = date_to_calculate
        start_date = dt.datetime(constants.start_date_year,
                                 constants.start_date_month,
                                 constants.start_date_day,
                                 constants.start_date_hour,
                                 constants.start_date_minute,
                                 constants.start_date_second)
        self.delta_time = int((self.date_to_calculate - start_date).total_seconds())
        self.angle_slope = constants.angle_slope
        period_for_on_cycle = constants.period_for_on_cycle
        perimeter = constants.perimeter
        self.one_sec_walk = perimeter / period_for_on_cycle
        self.one_sec_walk_ra = math.cos(self.angle_slope) * self.one_sec_walk
        self.one_sec_walk_dec = math.sin(self.angle_slope) * self.one_sec_walk
        moon = ephem.Moon()
        moon.compute(constants.start_date)
        ra_ephem_start = moon.ra
        dec_ephem_start = moon.dec
        ra_start_list = str(ra_ephem_start).split(':')
        dec_start_list = str(dec_ephem_start).split(':')
        ra_dec_min = constants.ra_dec_min
        ra_dec_max = constants.ra_dec_max
        ra_dec_min_list = ra_dec_min.split(':')
        ra_dec_max_list = ra_dec_max.split(':')
        self.ra_start = float(ra_start_list[0]) * 3600 * 15 + float(ra_start_list[1]) * 60 + float(ra_start_list[2])
        self.dec_start = float(dec_start_list[0]) * 3600 + float(dec_start_list[1]) * 60 + float(dec_start_list[2])
        self.ra_dec_min = float(ra_dec_min_list[0]) * 3600 * 15 + float(ra_dec_min_list[1]) * 60 + float(
            ra_dec_min_list[2])
        self.ra_dec_max = float(ra_dec_max_list[0]) * 3600 * 15 + float(ra_dec_max_list[1]) * 60 + float(
            ra_dec_max_list[2])

    def ra_dec_calculate(self):

        for sec in range(self.delta_time):
            if 0 <= self.ra_start + self.one_sec_walk_ra < 360 * 3600:
                self.ra = self.ra_start + self.one_sec_walk_ra
                self.ra_start = self.ra
            else:
                self.ra = self.ra_start + self.one_sec_walk_ra - 360 * 3600
                self.ra_start = self.ra
            if 0 <= self.dec_start:
                if self.ra_dec_min <= self.ra < self.ra_dec_max:
                    self.dec = self.dec_start - self.one_sec_walk_dec
                    self.dec_start = self.dec
                else:
                    self.dec = self.dec_start + self.one_sec_walk_dec
                    self.dec_start = self.dec
            elif self.dec_start < 0:
                if self.ra_dec_min < self.ra <= self.ra_dec_max:
                    self.dec = self.dec_start + self.one_sec_walk_dec
                    self.dec_start = self.dec
                else:
                    self.dec = self.dec_start - self.one_sec_walk_dec
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


if __name__ == '__main__':
    moon_obj = Moon(datetime.datetime.now())
    print(moon_obj.ra_dec_calculate()['ra'], moon_obj.ra_dec_calculate()['dec'])

    moon_test = ephem.Moon()
    moon_test.compute()

    print(moon_test.ra, moon_test.dec)
