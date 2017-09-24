from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade
from openpyxl.drawing import spreadsheet_drawing
from xmllib import newline

class BotStrategy(object):
	
	def __init__(self):
		self.output = BotLog()
		self.prices = []
		self.closes = [] # Needed for Momentum Indicator
		self.trades = []
		self.currentPrice = ""
		self.currentClose = ""
		self.numSimulTrades = 1
		self.indicators = BotIndicators()
		self.spreadsheet = []

	def tick(self,candlestick):
		print candlestick.priceAverage
		self.currentPrice = float(candlestick.priceAverage)
		self.prices.append(self.currentPrice)
		
		#self.currentClose = float(candlestick['close'])
		#self.closes.append(self.currentClose)
		
		self.output.log("Price: "+str(candlestick.priceAverage)+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,15)))

		self.evaluatePositions()
		self.updateOpenTrades()
		self.showPositions()
		mess = str(candlestick['weightedAverage'])
		self.GenSpreadsheetInfo(self.prices)

	def evaluatePositions(self):
		openTrades = []
		for trade in self.trades:
			if (trade.status == "OPEN"):
				openTrades.append(trade)

		if (len(openTrades) < self.numSimulTrades):
			if (self.currentPrice < self.indicators.movingAverage(self.prices,20)):
				self.trades.append(BotTrade(self.currentPrice,stopLoss=.0001))

		for trade in openTrades:
			if (self.currentPrice > self.indicators.movingAverage(self.prices,20)):
				trade.close(self.currentPrice)

	def updateOpenTrades(self):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.currentPrice)

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()
			
	def plotData(self):
		print 'Plot Now'
	
	def GenSpreadsheetInfo(self, prices):
		newList = []
		
		if len(self.spreadsheet) == 0:
		    newList.append("Price")
		    newList.append("20_Per_MA")
		    newList.append("50_per_MA")
		    newList.append("TOP_STD")
		    newList.append("BOT_STD")
		    self.spreadsheet.append(newList)
		
		newList = []
		newList.append(self.currentPrice)
		newList.append(self.indicators.movingAverage(self.prices,20))
		newList.append(self.indicators.movingAverage(self.prices,50))
		newList.append(self.currentPrice + (2*self.indicators.standardDeviation(self.prices,20)))
		newList.append(self.currentPrice - (2*self.indicators.standardDeviation(self.prices,20)))
		self.spreadsheet.append(newList)
		
	def GetSpreadsheetInfo():
		return self.spreadsheet
		

		
