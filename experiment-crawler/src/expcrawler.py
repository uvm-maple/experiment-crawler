import argparse
import gzip
import os
import re

# Important things to learn:
# How to read in and manipulate files (reading from a file advances the location of where you are reading from)
# Using regular expressions to search through text data (here, in bytes)
# Be mindful about differences between bytes and strings

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
    
    # if __debug__:
    #   print("\tReceived {} bytes.".format(len(window)))

    if delim in window: 
        # if we find the delimiter in the string, grab the index of 
        # the first instance of the delimiter
        index = window.index(delim)
        # print(index, "\n", delim, "\n", window, "\nWINDOW STARTING AT\n", window[:index], 
        #   "\nWINDOW ENDING AT", window[index:])
        # exit(0)
        # append everything just read to the return value and advance the file reader
        to_concat = f.read(index)
        retval += to_concat
        # advance file reader to the location
        return retval

    else:
        # delimiter not yet found
        retval += window[:len(delim)] 
        # advance the file reader 
        f.read(len(delim))



# This has to be the last basic block in the file
if __name__ == "__main__":

  data_dir = "experiment-crawler/data"
  delim = b"Content-Length"

  # regular expression 
  pat = re.compile(rb"Content-Length: [0-9]+\r\n")

  # variables that are tracking information
  mathrandom = 0
  max_possible_pages = 32
  possible_pages = max_possible_pages

  for file in os.listdir(data_dir):
    fname = os.sep.join([data_dir, file])
    print("{} is {}MB".format(fname, int(os.path.getsize(fname) / (1024*1024))))

    with gzip.open(fname, 'rb') as f:
      while max_possible_pages > 0 : 
        
        first_header = sliding_seek(f, b"\r\n\r\n\r\n")
        with open("{}_header1.out".format(max_possible_pages), "wb") as outfile:
          outfile.write(first_header)

        assert len(first_header) > 1
        
        if delim in first_header:

          content_length = int(pat.findall(first_header)[0][len(delim)+1:-2])    
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