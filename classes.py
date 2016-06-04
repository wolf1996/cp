from nltk.parse.stanford import StanfordDependencyParser
from nltk import Tree, ProbabilisticTree
from nltk.internals import find_jars_within_path
from enum import Enum

class film:
    synonims = ["films", "film", "picture",]
    labels = ["horror", "romantic", "thriller", "comedy", ]
    @staticmethod
    def valid_name(word):
        a = a 
    def __init__(self, name):
        a = a

class person:
    synonims = ["person", "persons", "men",]
    labels = ["actor", "director", ]
    @staticmethod
    def valid_name(word):
        a = a 
    def __init__(self, name):
        a = a 

class connection:
    labels = ["played", "acted", "directed", ]
    @staticmethod
    def valid_name(word):
        a = a 
    def __init__(self, name):
        a = a 

def tree_parser(triples):
    lst = []
    return lst




def main():
    fl = open('examples2')
    #dumpfile = open('dumpfile','wb')
    path_to_jar = './stanford-corenlp-full-2015-12-09/stanford-corenlp-3.6.0.jar'
    path_to_models_jar = './stanford-corenlp-full-2015-12-09/stanford-english-corenlp-2016-01-10-models.jar'
    dep_parser=StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

    val= Validator()
    pars_res=[[parse for parse in dep_parser.raw_parse(val.prep_str(i))] for i in fl] # doctest: +NORMALIZE_WHITESPACE
    #pickle.dump(pars_res,dumpfile)
    fl.seek(0)

    #trip_pars([smp.tree() for smp in i])
    for i,j in zip(pars_res,fl):
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