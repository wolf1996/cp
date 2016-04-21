# -*- coding: utf-8 -*-
"""
    Module with classes to work with RDF base
"""
from rdflib import Graph
from rdflib.namespace import RDF, RDFS
from rdflib import Namespace
from neo4jrestclient.client import GraphDatabase as GDB


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

    def set_uri(self, uri):
        """
            Set's URI to object
        """
        self.__uri = uri

    def add_props(self, prop_update):
        """
            Add properties to props dictionary
        """
        self.__props.update(prop_update)

    def add_label(self, label_update):
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

    def __str__(self):
        """
            convert class to string
        """
        name_str = "node name is %s\n" % self.__name
        label_str = "labels are %s\n" % str(self.__labels)
        propety_str = "properties are %s\n" % str(self.__props)
        return name_str + label_str + propety_str


def rdf_loader(gdb, rdf):
    """
        Get Neo4j connection and rdf file
    """
    owl = Namespace("http://www.w3.org/2002/07/owl#")
    node_dict = {}
    for j in rdf.subjects(predicate=RDF.type, object=owl.Class):
        jdata = (j.split('#')[-1])
        for i in rdf.subjects(object=j, predicate=RDF.type):
            idata = i.split('#')[-1]
            if idata in node_dict.keys():
                node_dict[idata].add_label(jdata)
            else:
                buf_node = NodeContainer(idata)
                buf_node.add_label(jdata)
                buf_node.set_uri(i)
                node_dict.update({idata: buf_node})
    for i in node_dict.keys():
        print("%s %s" % (i, node_dict[i],))


def test():
    """
       some tests
    """
    rdf = Graph()
    rdf.parse("RDF2.owl", 'application/rdf+xml')
    gdb = GDB("http://localhost:7474/db/data",
              username='neo4j', password='123456')
    rdf_loader(gdb, rdf)


if __name__ == '__main__':
    test()
