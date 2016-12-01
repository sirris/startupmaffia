# Building a hierarchical edge bundling graph for the Belgian Startup landscape.

from codecs import open
from json import dumps
from openpyxl import load_workbook
import sys
import collections


class Network:
    def __init__(self, path, sheet):
        self.people = {}
        # people =  dict {name, [other names]}
        self.bsm = load_workbook(path)[sheet]

    def write_to_file(self):
        maffia = []
        for name, connections in self.people.iteritems():
            maffia.append({'name': name, 'imports': connections})
        # print dumps(maffia)
        with open("report/heb_network.json", "w") as f:
            f.write(dumps(maffia))


    def add_connection(self, from_name, to_name):
        # print "adding %s and %s" %(from_name, to_name)
        connections_from = self.people.get(from_name, [])
        connections_from.append(to_name)
        self.people[from_name] = connections_from
        connections_to = self.people.get(to_name, [])
        self.people[to_name] = connections_to


    def run(self):
        for row in self.bsm.rows[1:]:
            from_type, from_name, edge_type, edge_name, to_type, to_name = [cell.value for cell in row]
            from_name = from_name.replace('.','')
            to_name = to_name.replace('.','')
            self.add_connection('%s.%s' % (from_type,from_name), '%s.%s' % (to_type,to_name))
            #self.add_connection(from_name, to_name)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("The correct way to call this script from CL is to provide the path to Omar's Excel sheet as the argument.")
        print("python heb.py /path/to/BelgischeStartupMaffia.xlsx")
    else:
        network = Network(sys.argv[1], "Sheet1")
        network.run()
        network.write_to_file()
