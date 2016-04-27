"""
    Movie rdf loading module
"""
import tmdbsimple as tmdb
import re
import apikey
from rdflib import Graph
from rdflib.namespace import RDF, RDFS
from rdflib import Namespace
from rdflib import URIRef, Literal


FIL = re.compile('\w+')
MY_ONT = Namespace(
    'http://www.semanticweb.org/ksg/ontologies/2016/3/untitled-ontology-20#') 
OWL = Namespace("http://www.w3.org/2002/07/owl#")


def add_genre(rdf, name):
    """
        adding genre to rdf
    """
    gnode = URIRef(MY_ONT[name.replace(' ', '_')])
    rdf.add((gnode, RDFS.subClassOf, URIRef(MY_ONT['Films'])))
    rdf.add((gnode, RDF.type, URIRef(OWL['Class'])))
    return gnode


def add_country(rdf, name):
    cnode = URIRef(MY_ONT[name.replace(' ', '_')])
    rdf.add((cnode, RDF.type, MY_ONT['Country']))
    rdf.add((cnode, URIRef(MY_ONT['Country_Name']), Literal(name)))
    return cnode


class MovieNode:
    """
        Movie content node
    """

    def __init__(self, _id=None, name=None, genre=None, country=None, release_year=None):
        """
            s
        """
        self.__name = name
        self.__country = country
        self.__id = _id
        self.__genre = genre
        self.__release_year = release_year
        self.__node = None

    def set_release_year(self, year):
        """
            s
        """
        self.__release_year = year

    def set_name(self, name):
        """
            s
        """
        self.__name = name

    def set_genre(self, genre):
        """
            s
        """
        self.__genre = genre

    def set_country(self, country):
        """
            s
        """
        self.__country = country

    def set_id(self, _id):
        """
            s
        """
        self.__id = _id

    def get_release_year(self):
        """
            s
        """
        return self.__release_year

    def get_name(self):
        """
            s
        """
        return self.__name

    def get_country(self):
        """
            s
        """
        return self.__country

    def get_id(self):
        """
            s
        """
        return self.__id

    def get_genre(self):
        """
            s
        """
        return self.__genre

    def __str__(self):
        """
            s
        """
        year_str = str(self.__release_year)
        name_str = str(self.__name)
        genre_str = str(self.__genre)
        id_str = str(self.__id)
        country_str = str(self.__country)
        return id_str + name_str + genre_str + country_str + year_str

    def add_to_rdf(self, rdf):
        """
            adding to rdf some node
        """
        self.__node = URIRef(MY_ONT[self.__name.replace(' ', '_')])
        rdf.add((self.__node, URIRef(
            MY_ONT['Film_Name']), Literal(self.__name)))
        for i in self.__genre:
            gnode = add_genre(rdf, i)
            rdf.add((self.__node, RDF.type, gnode))
        for i in self.__country:
            cnode = add_country(rdf, i)
            rdf.add((self.__node, URIRef(MY_ONT['Release_country']), cnode))
        rdf.add((self.__node, URIRef(MY_ONT['Link']), Literal(self.__id)))
        rdf.add((self.__node, URIRef(
            MY_ONT['Year_Of_Release']), Literal(self.__release_year)))
        print(self.__node)

    def get_node(self):
        """
            get node
        """
        return self.__node


class PersonNode:
    """
        person container
    """

    def __init__(self, _id=None, name=None, acted="", directed="", country=None, birth_year=None):
        """
        """
        self.__name = name
        self.__acted = acted
        self.__directed = directed
        self.__country = country
        self.__id = _id
        self.__birth_year = birth_year
        self.__node = None

    def set_birth_year(self, year):
        """
            s
        """
        self.__birth_year = year

    def set_name(self, name):
        """
            s
        """
        self.__name = name

    def set_country(self, country):
        """
            s
        """
        self.__country = country

    def set_directed(self, directed):
        """
            s
        """
        self.__directed = directed

    def set_acted(self, acted):
        """
            s
        """
        self.__acted = acted

    def set_id(self, _id):
        """
            s
        """
        self.__id = _id

    def get_birth_year(self):
        """
            s
        """
        return self.__birth_year

    def get_name(self):
        """
            s
        """
        return self.__name

    def get_country(self):
        """
            s
        """
        return self.__country

    def get_directed(self):
        """
            s
        """
        return self.__directed

    def get_acted(self):
        """
            s
        """
        return self.__acted

    def get_id(self):
        """
            s
        """
        return self.__id

    def __str__(self):
        """
            s
        """
        name_str = str(self.__name)
        str_acted = ""
        str_directed = ""
        if self.__acted:
            str_acted = "acted"
        if self.__directed:
            str_directed = "directed"
        id_str = str(self.__id)
        year_str = str(self.__birth_year)
        country_str = str(self.__country)
        return id_str + " " + name_str + " " + str_acted + " " + str_directed + " " + country_str + " " + year_str

    def add_to_rdf(self, rdf, mov):
        """
            adding to rdf some node
        """
        self.__node = URIRef(MY_ONT[self.__name.replace(' ', '_')])
        if self.__acted:
            rdf.add((self.__node, RDF.type, URIRef(MY_ONT['Actor'])))
            rdf.add((self.__node, MY_ONT['Acted_in'], mov.get_node()))
        if self.__directed:
            rdf.add((self.__node, RDF.type, URIRef(MY_ONT['Director'])))
            rdf.add((self.__node, MY_ONT['Produced'], mov.get_node()))
        rdf.add((self.__node, URIRef(
            MY_ONT['Person_Name']), Literal(self.__name)))
        if self.__country:
            cnode = add_country(rdf, self.__country)
            rdf.add((self.__node, URIRef(MY_ONT['Country_of_birth']), cnode))
        rdf.add((self.__node, URIRef(MY_ONT['Link']), Literal(self.__id)))
        rdf.add((self.__node, URIRef(
            MY_ONT['Birth_Year']), Literal(self.__birth_year)))
        print(self.__node)


def filmload(movie_id, rdf):
    """
        Load film
    """
    snode = None
    #movie_id = search.movie(query='Doctor Who')['results'][0]['id']
    movie_buf = tmdb.Movies(movie_id)
    movie = movie_buf.info()
    mnode = MovieNode()
    mnode.set_name(movie['original_title'])
    mnode.set_country([i['name'] for i in movie['production_countries']])
    mnode.set_genre([i['name'] for i in movie['genres']])
    mnode.set_release_year(movie['release_date'].split('-')[0])
    mnode.set_id(movie['id'])
    # print(movie.credits()['cast'][:4])
    # print(movie)
    print(mnode)
    actors = movie_buf.credits()['cast'][:4]
    actors_node = {}
    for i in actors:
        node = PersonNode()
        act = tmdb.People(i['id']).info()
        # print(act)
        node.set_name(act['name'])
        node.set_id(act['id'])
        node.set_acted(1)
        if act['place_of_birth']:
            node.set_country(FIL.findall(act['place_of_birth'])[-1])
        if act['birthday']:
            node.set_birth_year(act['birthday'].split('-')[0])
        # print(node)
        actors_node.update({node.get_id(): node})
        snode = node

    for i in movie_buf.credits()['crew']:
        if i['job'] == 'Director':
            if i['id'] in actors_node.keys():
                actors_node[i['id']].set_directed(1)
            else:
                node = PersonNode()
                act = tmdb.People(i['id']).info()
                node.set_name(act['name'])
                node.set_id(act['id'])
                node.set_directed(1)
                if act['place_of_birth']:
                    node.set_country(FIL.findall(act['place_of_birth'])[-1])
                if act['birthday']:
                    node.set_birth_year(act['birthday'].split('-')[0])
                # print(act)
                # print(node)
                actors_node.update({node.get_id(): node})
    # print(actors_node)
    mnode.add_to_rdf(rdf)
    for i in actors_node.keys():
        actors_node[i].add_to_rdf(rdf, mnode)


def test():
    """
        some tests
    """
    rdf = Graph()
    rdf.parse("RDF2.owl", 'application/rdf+xml')
    filmload('lock stock and two smoking barrels', rdf)
    #lsresfile = open("rdfr.owl","w")
    rdf.serialize(destination="rdfr.owl")


def main():
    """
        filling owl films
    """
    rdf = Graph()
    rdf.parse("RDF2.owl", 'application/rdf+xml')
    tmdb.API_KEY = apikey.key
    search = tmdb.Search()
    #movie_id = search.movie(query='')['results']
    #movie_id = search.movie(query='lock stock and two smoking barrels')['results'][0]['id']
    #filmload(movie_id, rdf)
    mv = tmdb.Movies()
    print(mv.popular(page=100))
    for i in mv.popular(page=10)['results']:
        filmload(i['id'],rdf)
    #lsresfile = open("rdfr.owl","w")
    rdf.serialize(destination="rdfr.owl")


if __name__ == '__main__':
    main()
