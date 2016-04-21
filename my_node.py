# -*- coding: utf-8 -*-
"""
    Module with classes to work with RDF base
"""
from rdflib import Graph
from rdflib.namespace import RDF, RDFS
from rdflib import Namespace

class NodeContainer:
    """
        Node data container
    """
    def __init__(self, name=None):
        """
            init function
        """
        self.__name = name
        self.__props = {}
        self.__labels = []
        self.__uri = None
        self.__node = None

    def set_name(self, name):
        """
            Set's name to object
        """
        self.__name = name

    def add_props(self, prop_update):
        """
            Add properties to props dictionary
        """
        self.__props.update(prop_update)

    def add_labels(self, label_update):
        """
            Add labels to labels array
        """
        if not label_update in self.__labels:
            self.__labels.append(label_update)

    def get_labels(self):
        """
            return labels
        """
        return self.__labels

    def get_props(self):
        """
           return properties dictionary
        """
        return self.__props


def rdf_loader(gdb,rdf):
    """
        Get Neo4j connection and rdf file
    """
    owl = Namespace("http://www.w3.org/2002/07/owl#")
    node_dict = {}
    for j in g.subjects(predicate=RDF.type,object=OWL.Class):
        jdata = (j.split('#')[-1])
        for i in g.subjects(object=j,predicate=RDF.type):
            idata = i.split('#')[-1]
            if idata in node_dict.keys():
                node_dict



def test():
    """
       some tests
    """
    print("thera are no tests... yet")


if __name__ == '__main__':
    test()
