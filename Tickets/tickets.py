"""Train Tickets Query

Usage: 
	ticket [-dgktz] <from> <to> <date>

Options:
	-h --help Show the screen
	-d        Dongche
	-g        Gaotie
	-k        kuaiche
	-t        tekuai
	-z        zhida

"""
from docopt import docopt
import stations
import requests
from prettytable import PrettyTable

def cli():
	arguments= docopt(__doc__, version = 'Tickets 1.0')
	from_station = stations.get_telecode(arguments.get('<from>'))
	to_station = stations.get_telecode(arguments.get('<to>'))
	date = arguments.get('<date>')
	url = ('https://kyfw.12306.cn/otn/leftTicket/query?'
		   'leftTicketDTO.train_date={}&'
		   'leftTicketDTO.from_station={}&'
		   'leftTicketDTO.to_station={}&'
		   'purpose_codes=ADULT').format(date,from_station,to_station);
	response = requests.get(url, verify = False)
	raw_trains = response.json()['data']['result']
	ptable = PrettyTable()
	ptable._set_field_names('车次 车站 时间 历时 一等 二等 软卧 硬卧 软座 硬座 无座'.split())
	for raw_train in raw_trains:
		data_list = raw_train.split('|')
		train_no = data_list[3]
		from_station_code = data_list[6]
		to_station_code = data_list[7]
		from_station_name = stations.get_names(from_station_code)
		to_station_name = stations.get_names(to_station_code)
		start_time = data_list[8]
		arrive_time = data_list[9]
		time_duration = data_list[10]
		first_class_seat = data_list[31] or '--'
		second_class_seat = data_list[30] or '--'
		soft_sleep = data_list[23] or '--'
		hard_sleep = data_list[28] or '--'
		hard_seat = data_list[29] or '--'
		soft_seat = data_list[24] or '--'
		no_seat = data_list[26] or '--'
		ptable.add_row([
			train_no, 
			'\n'.join([from_station_name, 
			to_station_name]), 
			'\n'.join([start_time, 
			arrive_time]), 
			time_duration, 
			first_class_seat, 
 			second_class_seat, 
			soft_sleep, 
			hard_sleep, 
			soft_seat, 
			hard_seat, 
			no_seat
			])
	print(ptable)

if __name__ == '__main__':
	cli()


