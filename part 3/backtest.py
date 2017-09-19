import sys, getopt
import datetime
from openpyxl import Workbook

from botchart import BotChart
from botstrategy import BotStrategy

def main(argv):
	chart = BotChart("poloniex","BTC_XMR",300)

	strategy = BotStrategy()
	print strategy.spreadsheet

	for candlestick in chart.getPoints():
		strategy.tick(candlestick)

	#Create Worbook with an active sheet
	m_wb = Workbook()
	wslist = m_wb.active
	wslist.title = 'Charts'
	
	list = strategy.spreadsheet
	
	for row_list in list:
	    wslist.append(row_list)
	
	# Save
	dt = str(datetime.datetime.now())
	wb_name = 'CryptoChartInfo' + dt[0:10] + '.xlsx'
	m_wb.save(wb_name)
	
if __name__ == "__main__":
	main(sys.argv[1:])