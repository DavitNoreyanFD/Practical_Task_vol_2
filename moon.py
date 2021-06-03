import datetime
import math
import ephem
import datetime as dt


class Moon:
    def __init__(self, date_to_calculate):
        self.ra = None
        self.dec = None
        self.date_to_calculate = date_to_calculate
        start_date = dt.datetime(2021, 5, 29, 23, 59, 59)
        self.delta_time = int((self.date_to_calculate - start_date).total_seconds())
        self.angle_slope = (23.44 + 5.14) * 3600
        period_for_on_cycle = 27.3 * 24 * 60 * 60
        perimeter = 360 * 3600
        self.one_sec_walk = perimeter / period_for_on_cycle
        self.one_sec_walk_ra = math.cos(self.angle_slope) * self.one_sec_walk
        self.one_sec_walk_dec = math.sin(self.angle_slope) * self.one_sec_walk
        moon = ephem.Moon()
        moon.compute('2021/5/29 23:59:59')
        ra_ephem_start = moon.ra
        dec_ephem_start = moon.dec
        ra_start_list = str(ra_ephem_start).split(':')
        dec_start_list = str(dec_ephem_start).split(':')
        ra_dec_min = '6:45:48.54'
        ra_dec_max = '18:45:48.54'
        ra_dec_min_list = ra_dec_min.split(':')
        ra_dec_max_list = ra_dec_max.split(':')
        self.ra_start = float(ra_start_list[0]) * 3600 * 15 + float(ra_start_list[1]) * 60 + float(ra_start_list[2])
        self.dec_start = float(dec_start_list[0]) * 3600 + float(dec_start_list[1]) * 60 + float(dec_start_list[2])
        self.ra_dec_min = float(ra_dec_min_list[0]) * 3600*15  + float(ra_dec_min_list[1]) * 60 + float(ra_dec_min_list[2])
        self.ra_dec_max = float(ra_dec_max_list[0]) * 3600*15  + float(ra_dec_max_list[1]) * 60 + float(ra_dec_max_list[2])
    def moon_ra_dec_calculate(self):

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


        ra_res = f'{int(self.ra // (3600 * 15))}:{int((self.ra % (3600)) // 60)}:{round(float((self.ra % (3600)) % 60), 1)}'
        dec_res = f'{int(self.dec // 3600)}:{int((self.dec % 3600) // 60)}:{round(float((self.dec % 3600) % 60), 1)}'

        return 'moon ra is a  ' + ra_res + '--' + 'moon dec is a ' + dec_res

moon_obj = Moon(datetime.datetime.now())
print(moon_obj.moon_ra_dec_calculate())

moon_test = ephem.Moon()
moon_test.compute()

print(moon_test.ra, moon_test.dec)

