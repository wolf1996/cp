"""
    Movie rdf loading module
"""
import tmdbsimple as tmdb
import re
import apikey
from rdflib import Graph
from rdflib.namespace import RDF, RDFS
from rdflib import Namespace
from rdflib import URIRef, BNode, Literal

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



class PersonNode:
    """
        person container
    """
    def __init__(self, _id=None, name=None, acted="", directed="", country=None, birth_year = None):
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
        return id_str + " "+ name_str +" "+ str_acted +" " + str_directed + " " +country_str + " " + year_str

    def add_to_rdf(self, rdf):
        """
            adding to rdf some node
        """
        pnsp = Namespace('http://www.semanticweb.org/ksg/ontologies/2016/3/untitled-ontology-20#')
        my_ont = Namespace('http://www.semanticweb.org/ksg/ontologies/2016/3/untitled-ontology-20#')
        self.__node = URIRef(pnsp[self.__name.replace(' ','_')])
        if self.__acted:
            rdf.add((self.__node, RDF.type, URIRef(my_ont['Actor'])))
        if self.__directed:
            rdf.add((self.__node, RDF.type, URIRef(my_ont['Director'])))
        rdf.add((self.__node, URIRef(my_ont['Person_Name']), Literal(self.__name)))
        rdf.add((self.__node, URIRef(my_ont['Link']), Literal(self.__id)))
        rdf.add((self.__node, URIRef(my_ont['Birth_Year']), Literal(self.__birth_year)))
        print(self.__node)

def filmload(filmname,rdf):
    """
        Load film
    """
    snode = None
    tmdb.API_KEY = apikey.key
    search = tmdb.Search()
    movie_id = search.movie(query=filmname)['results'][0]['id']
    fil = re.compile('\w+')
    #movie_id = search.movie(query='Doctor Who')['results'][0]['id']
    movie_buf = tmdb.Movies(movie_id)
    movie = movie_buf.info()
    mnode = MovieNode()
    mnode.set_name(movie['original_title'])
    mnode.set_country([i['name'] for i in movie['production_countries']])
    mnode.set_genre([i['name'] for i in movie['genres']])
    mnode.set_release_year(movie['release_date'].split('-')[0])
    # print(movie.credits()['cast'][:4])
    #print(movie)
    print(mnode)
    actors = movie_buf.credits()['cast'][:4]
    actors_node = {}
    for i in actors:
        node = PersonNode()
        act = tmdb.People(i['id']).info()
        #print(act)
        node.set_name(act['name'])
        node.set_id(act['id'])
        node.set_acted(1)
        if act['place_of_birth']:
            node.set_country(fil.findall(act['place_of_birth'])[-1])
        if act['birthday']:
            node.set_birth_year(act['birthday'].split('-')[0])
        #print(node)
        actors_node.update({node.get_id():str(node)})
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
                    node.set_country(fil.findall(act['place_of_birth'])[-1])
                if act['birthday']:
                    node.set_birth_year(act['birthday'].split('-')[0])
                #print(act)
                #print(node)
                actors_node.update({node.get_id():str(node)})
    print(actors_node)
    snode.add_to_rdf(rdf)


def test():
    """
        some tests
    """
    rdf = Graph()
    rdf.parse("RDF2.owl", 'application/rdf+xml')
    filmload('lock stock and two smoking barrels', rdf)
    #lsresfile = open("rdfr.owl","w")
    rdf.serialize(destination="rdfr.owl")

if __name__ == '__main__':
    test()