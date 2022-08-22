import argparse
import gzip
import os
import re

class WARCHeader():

  def __init__(self, blob):
    self.version = None
    self.http = None

    self.populate(blob)

  def populate(self, blob: bytes):
    headers, http = blob.decode('utf-8').split('\r\n\r\n')
    self.http = http
    # can probably do something more clever with regexes
    # or a python parser combinator package
    assert headers.startswith('WARC/1.0')
    self.version = 1.0
    for line in headers.split('\n')[1:]:
      try:
        key, val = line.split(': ')
        self.__setattr__(key.strip(), val)
      except ValueError as e:
        print(e, line)

  def __str__(self):
    warc_info = "\n".join(
      ["{}: {}".format(k, v) for k, v in self.__dict__.items() if k != 'version' and k!='http']
    )
    return """WARC/1.0\n{}\n\n{}""".format(warc_info, self.http)

  def __len__(self):
    # don't count version or http
    return len(self.__dict__) - 2 

  def __iter__(self):
    return self.__dict__.__iter__()



def sliding_seek(f, delim):
  # reads until the delimiter, returning everything until just before the 
  # delimiter. Advances file reader to start just after the delimiter
  window_size = len(delim) * 2
  retval = b""

  while True:
    # if __debug__:
    #   print("Requesting {} bytes".format(window_size))

    # this will store bytes from location 0 in the file stream 
    # until some n, which we are requesting to be window_size, but may not be
    window = f.peek(window_size)
    
    if __debug__:
      print("\tReceived {} bytes.".format(len(window)))

    if delim in window: 
        # if we find the delimiter in the string, grab the index of 
        # the first instance of the delimiter
        index = window.index(delim)
        # print(type(window), type(delim), 'ASDF'+window[:index].decode('utf-8')+'FDSA', 'ASDF'+window[index:].decode('utf-8')+'FDSA')
        
        # exit(0)
        # append everything just read to the return value and advance the file reader
        to_concat = f.read(index)
        assert(len(to_concat) == index)
        # now need to advance past the delimiter
        f.read(len(delim))
        retval += to_concat
        # advance file reader to the location
        return retval

    else:
        # delimiter not yet found
        retval += window[:len(delim)] 
        # advance the file reader; our window is 2x the length of the delimiter
        # only advance the length of the delimiter
        f.read(len(delim))



# This has to be the last basic block in the file
if __name__ == "__main__":

  data_dir = "experiment-crawler/data"
  delim = b"Content-Length"

  # regular expression 
  pat = re.compile(rb"Content-Length: [0-9]+\r\n")

  # variables that are tracking information
  mathrandom = 0
  max_possible_pages = 1
  possible_pages = max_possible_pages

  for file in os.listdir(data_dir):
    fname = os.sep.join([data_dir, file])
    print("{} is {}MB".format(fname, int(os.path.getsize(fname) / (1024*1024))))

    with gzip.open(fname, 'rb') as f:
      while max_possible_pages > 0 : 
        
        first_header = WARCHeader(sliding_seek(f, b"\r\n\r\n\r\n"))

        with open("{}_header1.out".format(max_possible_pages), "w") as outfile:
          outfile.write(str(first_header))

        assert len(first_header) > 1
        
        delim_str = delim.decode('utf-8')
        if delim_str in first_header:
          content_length = int(first_header.__getattribute__(delim_str))
          # print("reading next {} bytes:".format(content_length))

          second_header = f.read(content_length)
          with open("{}_header2.out".format(max_possible_pages), "wb") as outfile:
            outfile.write(second_header)

          try:
            html_length = int(pat.findall(second_header)[0][len(delim)+1:-2])
            page = f.read(html_length)
            with open("{}_body.out".format(max_possible_pages), "wb") as outfile:
              outfile.write(page)
            if b"Math.random" in page:
              mathrandom += 1

          except: 
            with open ("{}.err".format(max_possible_pages), "wb") as err:
              err.write(second_header)
        else:
          print("Delimiter not in first header!!")

        max_possible_pages -= 1

  assert max_possible_pages == 0      
  print("{}/{} pages use Math.random".format(mathrandom, possible_pages))
