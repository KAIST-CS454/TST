from parseXML import XMLParser

parser = XMLParser('Project.EFG.xml')

event_graph = parser.parse_event_graph()
initial = parser.parse_event_initial()

print (event_graph)
print (event_graph.shape)
print (initial)
print (initial.shape)
