import sys

print(sys.version)
from digiLib import webapp
from digiLib import db, manager
if __name__ == '__main__':
	manager.run()