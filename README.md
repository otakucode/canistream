# canistream

CLI tool to determine a movies digital availability through online services using http://canistream.it

# Usage:
     canistream.py [-h] [--verbose] [--no-streaming] [--no-rental]
                     [--no-purchase] [--no-xfinity]
                     Title

Search www.canistream.it for movie availability.

positional arguments:
  Title           title to search for

optional arguments:
  -h, --help      show this help message and exit
  --verbose, -v
  --no-streaming  do not search for streaming availability
  --no-rental     do not search for rental availability
  --no-purchase   do not search for purchase availability
  --no-xfinity    do not search for xfinity availability

# Requirements:
- Python 3+
- requests
- bs4

