# -*- coding: utf-8 -*-
"""
    Module with classes to work with RDF base
"""
from rdflib import Graph
from rdflib.namespace import RDF, RDFS
from rdflib import Namespace
from neo4jrestclient.client import GraphDatabase as GDB
import keyring


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

    def get_name(self):
        """
            Get's name to object
        """
        return self.__name

    def set_uri(self, uri):
        """
            Set's URI to object
        """
        self.__uri = uri

    def set_node(self, node):
        """
            Set's graph db node to object
        """
        self.__node = node

    def get_node(self):
        """
            Get's graph db node to object
        """
        return self.__node

    def get_uri(self):
        """
            Set's URI to object
        """
        return self.__uri

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


def rdf_get_branch(rdf, label):
    """
        get all classes which considered as
        parent class to label
    """
    buffer_list = [label, ]
    for i in rdf.objects(subject=label, predicate=RDFS.subClassOf):
        print(i)
        buffer_list += rdf_get_branch(rdf, i)
    return buffer_list


def rdf_update_labels(rdf, node):
    """
        complit label list of node
        with parent class labels
    """
    final_list = []
    for i in node.get_labels():
        # print(i)
        final_list += rdf_get_branch(rdf, i)
    for i in final_list:
        node.add_label(i)

def rdf_update_connections(rdf, prop, obj, subj, owl):
    """
        Finding all subPropertys
        and adding them to Datatbase
    """
    conname = prop.split('#')[-1]
    print("createcon "+str(obj)+ " "  + str(subj))
    obj.relationships.create(conname, subj)
    for i in rdf.objects(subject=prop, predicate=RDFS.subPropertyOf):
        print(i)
        rdf_update_connections(rdf, i, obj, subj, owl)
    for i in rdf.objects(subject=prop, predicate=owl.inverseOf):
        conname = i.split('#')[-1]
        subj.relationships.create(conname, obj)

def gdb_add_node(node, gdb, rdf, owl):
    """
        adding node with labels
    """
    gdb_node = gdb.nodes.create()
    node.set_node(gdb_node)
    gdb_node.labels.add([label.split('#')[-1] for label in node.get_labels()])
    for _, pro, obj in rdf.triples((node.get_uri(), None, None)):
        if (pro, RDF.type, owl.DatatypeProperty) in rdf:
            prop_name = pro.split('#')[-1]
            value = obj.split('#')[-1]
            gdb_node.set(prop_name, value)


def gdb_add_connection(node, node_dict, rdf, owl):
    """
        adding connection
    """
    for sub, pro, obj in rdf.triples((node.get_uri(), None, None)):
        oname = obj.split('#')[-1]
        sname = sub.split('#')[-1]
        if (pro, RDF.type, owl.ObjectProperty) in rdf:
            rdf_update_connections(
                rdf, pro, node_dict[sname].get_node(), node_dict[oname].get_node(), owl)


def rdf_loader(gdb, rdf):
    """
        Get Neo4j connection and rdf file
    """
    owl = Namespace("http://www.w3.org/2002/07/owl#")
    node_dict = {}
    for j in rdf.subjects(predicate=RDF.type, object=owl.Class):
        for i in rdf.subjects(object=j, predicate=RDF.type):
            idata = i.split('#')[-1]
            if idata in node_dict.keys():
                node_dict[idata].add_label(j)
                print(idata)
            else:
                buf_node = NodeContainer(idata)
                buf_node.add_label(j)
                buf_node.set_uri(i)
                node_dict.update({idata: buf_node})
                print(idata)
    for i in node_dict.keys():
        print("%s %s" % (i, node_dict[i],))
    for i in node_dict.keys():
        rdf_update_labels(rdf, node_dict[i])
    for i in node_dict.keys():
        print("%s %s" % (i, node_dict[i],))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for i in node_dict.keys():
        node = node_dict[i]
        gdb_add_node(node, gdb, rdf, owl)
    for i in node_dict.keys():
        node = node_dict[i]
        gdb_add_connection(node, node_dict, rdf, owl)

def test():
    """
       some tests
    """
    rdf = Graph()
    rdf.parse("rdfr.owl", 'application/rdf+xml')
    gdb = GDB("http://localhost:7474/db/data",
              username='neo4j', password=keyring.get_password('neo4j', 'neo4j'))
    rdf_loader(gdb, rdf)


if __name__ == '__main__':
    test()
