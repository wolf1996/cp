"""
    module translate natural language query
    to CYPHER query
"""

from nltk.parse.stanford import StanfordDependencyParser
from nltk import Tree, ProbabilisticTree
from nltk.internals import find_jars_within_path
from nltk.stem.lancaster import LancasterStemmer

class Film:
    """
        class contain info about unknown film
    """
    synonims = ["films", "film", "picture", ]
    labels = ["horror", "romantic", "thriller", "comedy", ]
    stemmer = LancasterStemmer()
    @staticmethod
    def valid_name(word):
        """
            check if word means film
        """
        word = Film.stemmer.stem(word)
        return (word in Film.synonims) or (word in Film.labels)

    def __init__(self, name):
        return

    def get_info(self, triples, objects):
        """
            getting info from triples
        """
        return


class Person:
    """
        class contain info about unknown person
    """
    synonims = ["person", "persons", "men", ]
    labels = ["actor", "director", ]
    stemmer = LancasterStemmer()
    @staticmethod
    def valid_name(word):
        """
            check if word means person
        """
        return

    def __init__(self, name):
        return
    def get_info(self, triples, objects):
        """
            getting info from triples
        """
        word = Person.stemmer.stem(word)
        return (word in Person.synonims) or (word in Person.labels)


class Connection:
    """
        class contain info about connections
    """
    labels = ["played", "acted", "directed", ]
    stemmer = LancasterStemmer()
    @staticmethod
    def valid_name(word):
        """
            check if word means Connection
        """
        word = Connection.stemmer.stem(word)
        return (word in Connection.labels)

    def __init__(self, name):
        return
    def get_info(self, triples, objects):
        return


class Myobject:
    """
        objects class
    """
    objlist = []
    stemmer = LancasterStemmer()
    @staticmethod
    def valid_name(word):
        """
            check if word means named objects
        """
        word = Myobject.stemmer.stem(word)
        return (word in Myobject.objlist) or word.isdigit()

    def __init__(self, name):
        return

    @staticmethod
    def string_analys(gstr):
        """
            prepare string to next steps,
            and gets named objects from sentences
        """
        flag = 0
        rstr = ""
        obj_str = ""
        for i in gstr:
            if i == '[':
                flag = 1
                continue
            if i == ']':
                flag = 0
                rstr += obj_str
                Myobject.objlist.append(obj_str)
                obj_str = ""
                continue
            if flag and i == ' ':
                continue
            if flag:
                obj_str += i
                continue
            rstr += i
        return rstr


def tree_parser(triples):
    """
        pars graph
    """
    lst = []
    return lst

def get_obj(triples):
    """
        getting objects from triples
    """
    objlist = {}
    classlist = []
    classlist.append(Film)
    classlist.append(Person)
    classlist.append(Myobject)
    classlist.append(Connection)
    for i in triples:
        name = i[0][0]
        print("name: " + name)
        if name in objlist.keys():
            continue
        for mclass in classlist:
            if mclass.valid_name(name):
                print("name valid: "+name)
                obj = mclass(name)
                objlist.update({name:obj})
    print(objlist.keys())
    return objlist



def main():
    """
        main function
    """
    fl = open('examples2')
    #dumpfile = open('dumpfile','wb')
    path_to_jar = '../exp/stanford-corenlp-full-2015-12-09/stanford-corenlp-3.6.0.jar'
    path_to_models_jar = '../exp/stanford-corenlp-full-2015-12-09/stanford-\
english-corenlp-2016-01-10-models.jar'
    dep_parser = StanfordDependencyParser(
        path_to_jar=path_to_jar,
        path_to_models_jar=path_to_models_jar)
    pars_res = [[parse for parse in dep_parser.raw_parse(
        Myobject.string_analys(i))] for i in fl]  # doctest: +NORMALIZE_WHITESPACE
    # pickle.dump(pars_res,dumpfile)
    fl.seek(0)
    #val = Validator()
    #trip_pars([smp.tree() for smp in i])
    for i, j in zip(pars_res, fl):
        print([list(smp.triples()) for smp in i])
        print("-----------------------------------------------")
        print([smp.tree() for smp in i])
        #trip_pars([smp.tree() for smp in i], i)
        print("-----------------------------------------------")
        print(get_obj([list(smp.triples()) for smp in i][0]))
        print("-----------------------------------------------")
        print(j)
        print("###############################################")

if __name__ == '__main__':
    main()
