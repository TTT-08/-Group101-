from requests_html import HTMLSession
session = HTMLSession()
url = 'https://api.blockcypher.com/v1/btc/test3/addrs/tb1qq7chjccfcmpal29rv3ans74wa6ewa9kenqzmef/full?limit=50'
response = session.get(url)
with open("parse result.txt","w") as f:

    f.write(response.html.full_text)
