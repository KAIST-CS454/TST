from collections import defaultdict
from xml.etree import cElementTree as ET
from pprint import pprint

# usage : locate at the folder with (TC/*, EFG.xml, GUI.xml)
# and run : "python3 tst_parser.py"

def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


def etree_to_dict_GUIxml(t, l = list(), p = "root"):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc, l in map(lambda t: etree_to_dict_GUIxml(t, l, p), children):
            for k, v in dc.items():
                if k == "Attributes":
                    l.append(t)
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d, l

def parse_EFG():
    s = ""
    with open("Project.EFG.xml", "r") as f:
        s = f.read()
    e = ET.XML(s)
    return etree_to_dict(e)["EFG"]

def parse_GUI():
    s = ""
    with open("Project.GUI.xml", "r") as f:
        s = f.read()
    e = ET.XML(s)
    return etree_to_dict_GUIxml(e)

def parse_TST(n):
    with open("TC/t%s.tst" % str(n), "r") as f:
        #_ = f.readline()
        s = f.read()
    e = ET.XML(s)
    return etree_to_dict(e)["TestCase"]["Step"]


def main():
    # from EFG xml, obtain a map from event id to widget id.
    efg = parse_EFG()
    eid_wid_dict = dict()
    for event in efg["Events"]["Event"]:
        eid_wid_dict[event["EventId"]] = event["WidgetId"]

    # obtain the widget id from the parsing table
    gui = parse_GUI()
    def attr_to_dict(t):
        return {d["Name"] : d["Value"] for d in t}

    widget_list = list()
    for i in range(len(gui[1])):
        tree = etree_to_dict(gui[1][i])
        root_type = tree.keys()[0]
        widget_list.append(attr_to_dict(tree[root_type]["Attributes"]["Property"]))

    widget_dict = {widget["ID"] : widget for widget in widget_list if widget["ID"][0] == "w"}
    
    # generate coverage table (trial number of consecutive events)
    # e1 -> e2 -> e3 : S[0][1] = S[1][2] = 1, 0 for the other cells
    table = [[0] * 64 for i in range(64)]
    for i in range(851):
        data = parse_TST(i)
        S = [j["EventId"] for j in data]
        for j in range(len(S) - 1):
            start_index = int(S[j][1:])
            end_index = int(S[j+1][1:])
            table[start_index][end_index] += 1

    # write each data into files
    with open('output_etow.txt', 'w') as out:
        pprint(eid_wid_dict, stream=out)

    with open('output_widget.txt', 'w') as out:
        pprint(widget_dict, stream=out)

    with open('output_testcov.txt', 'w') as out:
        pprint(list(map(str, table)), stream=out)

if __name__ == "__main__":
    main()
