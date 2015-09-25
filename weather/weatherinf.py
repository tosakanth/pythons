import urllib2
from xml.dom.minidom import parse, parseString

class YahooWheater(object):
	def __init__(self,city='bangkok',country='th'):		
		query="select%20*%20from%20weather.forecast%20where%20woeid%20in%20%28"
		query=query+"select%20woeid%20from%20geo.places%281%29%20where%20text%3D%22"+city
		query=query+"%2C%20"+country+"%22%29&format=xml&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
		self.URL="https://query.yahooapis.com/v1/public/yql?q="+query
		self.forcast=[]
		self.today={}
		response = urllib2.urlopen(self.URL)
		xml_data = response.read()
		if xml_data :
			self.parse_Xml(xml_data)
				
	def parse_Xml(self,xml_data):
		dom = parseString(xml_data)
		res = dom.getElementsByTagName('result')
		if len(res) == 0:
			return
		#get today 
		for node in dom.getElementsByTagName('yweather:condition'):
			self.today={"temp":node.attributes['temp'].value,
						"text":node.attributes['text'].value}
			
		# get forcast data
		for node in dom.getElementsByTagName('yweather:forecast'): 
			d = {'day':node.attributes['date'].value,
				"high": node.attributes['high'].value ,
				"low":node.attributes['low'].value,
				 "text": node.attributes['text'].value}
			self.forcast.append(d)	 
		    
	def get_today(self):
		return self.today
		
	def get_forcast(self):
		return self.forcast				
		
#example
if __name__ == "__main__":
	ytw = YahooWheater(city='bangkok',country='th')
	print ytw.get_today()
	print ytw.get_forcast()
	
