from io import StringIO
import os 
import gzip
import argparse
import math

from warc import WARCReader, WARCHeader, WARCRecord, WARCFile
# https://docs.python.org/3/library/argparse.html

# warc paths live in warc.paths.gz; may want to provide this as a 

if __name__ == "__main__":
  parser = argparse.ArgumentParser
  parser.add_argument("--warc_path", type=str)
  parser.add_argument("--num_paths", type=int)

  args = parser.parse_args()
  print(args.warc_path, args.num_paths)

  #with open(args.warc_path, 'rb') as paths, gzip.open(args.warc_path, 'wb') as paths:
  with open(args.warc_path,'rb') as paths:

  #with open(args.warc_paths, 'rb') as src, gzip.open(args.warc_paths, 'wb') as dst:
    #dst.writelines(src)
    warc_paths = paths.read()

  
#f = gzip.open('CC-MAIN-20220120035934-20220120065934-00447.warc.gz', 'rb')
#file_content = f.read()
#f.close()  
print((warc_paths))


if __name__ == '__main__':
    WARCReader().read_header()

    
def read_file(self):
        h = WARCHeader({
            "WARC-Type": "response",
            "X-New-Header": "42"
        })
        assert h['WARC-Type'] == "response"
        assert h['WARC-TYPE'] == "response"
        assert h['warc-type'] == "response"

        assert h['X-New-Header'] == "42"
        assert h['x-new-header'] == "42"

def prescence_of_str(self):
        h = WARCHeader({})
        assert str(h) == "WARC/1.0\r\n\r\n"

        h = WARCHeader({
            "WARC-Type": "response"
        })
        assert str(h) == "WARC/1.0\r\n" + "WARC-Type: response\r\n\r\n"


WARC_RECORD_TEXT = (
    "WARC/1.0\r\n" +
    "Content-Length: 10\r\n" +
    "WARC-Date: 2012-02-10T16:15:52Z\r\n" +
    "Content-Type: application/http; msgtype=response\r\n" +
    "WARC-Type: response\r\n" +
    "WARC-Record-ID: <urn:uuid:80fb9262-5402-11e1-8206-545200690126>\r\n" +
    "WARC-Target-URI: http://example.com/\r\n" +
    "\r\n" +
    "Helloworld" +
    "\r\n\r\n"
)

def init_defaults(self):
        # It should initialize all the mandatory headers
        h = WARCHeader({"WARC-Type": "resource"}, defaults=True)
        assert h.type == "resource"
        assert "WARC-Date" in h
        assert "Content-Type" in h
        assert "WARC-Record-ID" in h

def new_content_types(self):
        def f(type):
            return WARCHeader({"WARC-Type": type}, defaults=True)
        assert f("response")["Content-Type"] == "application/http; msgtype=response"
        assert f("request")["Content-Type"] == "application/http; msgtype=request"
        assert f("warcinfo")["Content-Type"] == "application/warc-fields"
        assert f("newtype")["Content-Type"] == "application/octet-stream"



class TestWARCReader:
    def read_header(self):
        f = StringIO(WARC_RECORD_TEXT)
        h = WARCReader(f).read_record().header
        assert h.date == "2012-02-10T16:15:52Z"
        assert h.record_id == "<urn:uuid:80fb9262-5402-11e1-8206-545200690126>"
        assert h.type == "response"
        assert h.content_length == 10
print()


m_random = math.random

def read_multiple_records(self):
  f = StringIO(WARC_RECORD_TEXT * 10)
  reader = WARCReader(f)
  for i in range(10):
    rec = reader.read_record()
    assert rec is not None
    records = 0
    responses = 0
    m_random = 0
    for r in f:
      records += 1
      if 'response' == r.header['warc-type']:
        responses += 1
      if 'm_random' == r['warc-type']:
        m_random += 1

      print()


    


  # grab num_paths paths
  # read n paths from the file









if __name__ == '__main__':
    WARCReader().read_header()







# import requests
# import lxml
# from bs4 import BeautifulSoup

# # Boostrap with search engines by domain
# # Start with a bound name; loop through text later

# # Basic instructions from here: https://www.topcoder.com/thrive/articles/web-crawler-in-python

# headers = {
#   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
# } 
# # parameterize this query in the future (make news a variable)
# # Note that you can copy the url below and drop it into the browser
# f = requests.get('https://www.google.com/search?q=news', headers=headers)

# soup = BeautifulSoup(f.content,'lxml')
# # I found the cite tag by:
# # 1. going to the section that I might want to expand in Chrome
# # 2. right clicking on that section and selecting 'Inspect Element"
# # 3. scrolling through the HTML
# #
# # You should play around with this more, following the example linked above. 
# # Track what you see and what you try in a notes file 
# results = soup.find('cite')
# print(results)