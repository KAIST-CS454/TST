import numpy as np
from bs4 import BeautifulSoup

class XMLParser:
    def __init__(self, file):
        self.file = file
        with open(self.file) as f:
            xml = f.read()
        soup = BeautifulSoup(xml, features='xml')
        self.soup = soup

    def parse_event_graph(self):
        li = []
        for row in self.soup.find('EventGraph').findAll('Row'):
            li.append([e.string for e in row.findAll('E')])
        self.array = np.array(li, dtype=int)
        return self.array

    def parse_event_initial(self):
        init = []
        for event in self.soup.findAll('Event'):
            init.append(1 if event.find('Initial').string == 'true' else 0)
        self.init = np.array(init, dtype=int)
        return self.init

