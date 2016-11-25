from codecs import open
from json import dumps
from openpyxl import load_workbook
import sys
import collections


class Network:
  def __init__(self, path, sheet):
    self.counter=[]
    self.name_group = {}
    self.values = {}
    self.name_id = {}
    self.nodes = []
    self.edges = []
    self.bsm = load_workbook(path)[sheet]
    
  def count_from(self):
    for row in self.bsm.rows[1:]:
      from_type, from_name, edge_type, edge_name, to_type, to_name = [cell.value for cell in row]
      self.counter.append(from_name)
      self.name_group[from_name] = from_type

  def count_to(self):
    for row in self.bsm.rows[1:]:
      from_type, from_name, edge_type, edge_name, to_type, to_name = [cell.value for cell in row]
      self.counter.append(to_name)
      self.name_group[to_name] = to_type

  def count(self):
    self.values = collections.Counter(self.counter) 

  def give_id(self):
    i = 0
    for row in self.bsm.rows[1:]:
      from_type, from_name, edge_type, edge_name, to_type, to_name = [cell.value for cell in row]
      for name in [from_name, to_name]:
        if not name in self.name_id:
          i += 1
          self.name_id[name] = i

  def set_nodes(self):
    for name in self.name_id:
      node1 = {"id": self.name_id[name],
               "label": name,
               "title": name,
               "group": self.name_group[name],
               "value": self.values[name]
              }
      self.nodes.append(node1)
            
  def set_edges(self):
    for row in self.bsm.rows[1:]:
      from_type, from_name, edge_type, edge_name, to_type, to_name = [cell.value for cell in row]
      for name in [from_name, to_name]:
        edge = {"from": self.name_id[from_name],
                "to": self.name_id[to_name]
                }
        self.edges.append(edge)
                
  def write_to(self):
    with open("report/nodes.js", "w") as f:
      f.write("var nodesraw = " + dumps(self.nodes, indent=2) + ";")

    with open("report/edges.js", "w") as f:
      f.write("var edgesraw = " + dumps(self.edges, indent=2) + ";")

  def run(self):  
    self.count_from()
    self.count_to()
    self.count()
    self.give_id()
    self.set_nodes()
    self.set_edges()
    self.write_to()

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("The correct way to call this script from CL is to provide the path to Omar's Excel sheet as the argument.")
    print("python bsm.py /path/to/BelgischeStartupMaffia.xlsx")
  else:  
    network = Network(sys.argv[1], "Sheet1")
    network.run()

