import requests
import re
from pprint import pprint

def main():
	url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9053'
	response = requests.get(url)
	pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
	result = dict(re.findall(pattern, response.text))
	


if __name__ == '__main__':
	main()