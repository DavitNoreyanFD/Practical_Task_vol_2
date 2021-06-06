import configparser


config = configparser.ConfigParser()
config.read('config.ini')
time_sleap = int(config['SERVER']['time_sleap'])
ip = config['SERVER']['ip']
port = int(config['SERVER']['port'])


angle_slope = 102888.0
period_for_on_cycle = 2358720.0
perimeter = 1296000
ra_dec_min = '6:45:48.54'
ra_dec_max = '18:45:48.54'
start_date = '2021/6/3 23:59:59'
start_date_year = 2021
start_date_month = 6
start_date_day = 3
start_date_hour = 23
start_date_minute = 59
start_date_second = 59