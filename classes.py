"""
    module translate natural language query
    to CYPHER query
"""

from nltk.parse.stanford import StanfordDependencyParser
from nltk.stem import SnowballStemmer


class Film:
    """
        class contain info about unknown film
    """
    synonims = ["films", "film", "picture", ]
    labels = ["horror", "romantic", "thriller", "comedy", ]
    properties = ["release", ]
    stemmer = SnowballStemmer("english")

    @staticmethod
    def valid_name(word):
        """
            check if word means film
        """
        word = Film.stemmer.stem(word)
        return (word in Film.synonims) or (word in Film.labels)

    def __init__(self, name):
        self.__name = name
        self.__stemname = Film.stemmer.stem(name)
        self.__labellist = []
        return

    def get_info(self, triples, objects):
        """
            getting info from triples
        """
        for i in triples:
            if i[0][0] == self.__name:
                dname = i[2][0]
                stemdname = Film.stemmer.stem(dname)
                if stemdname in Film.labels:
                    self.__labellist.append(stemdname)
                    objects.update({stemdname: None})
                if Connection.valid_name(stemdname):
                    if stemdname in objects.keys():
                        con = objects[stemdname]
                        con.set_source(self)
                        print("!!!!!!!!!!!!!lready in list!!!!!!!!!!!!!!!!!!!!")
                    else:
                        con = Connection(stemdname)
                        con.set_source(self)
                        objects.update({stemdname: con})
                        con.get_info(triples, objects)
                        objects[stemdname] = con
        return

    def __str__(self):
        return self.__name + '\t' + self.__stemname


class Person:
    """
        class contain info about unknown person
    """
    synonims = ["person", "persons", "men", ]
    labels = ["actor", "director", ]
    properties = ["born", ]
    stemmer = SnowballStemmer("english")

    @staticmethod
    def valid_name(word):
        """
            check if word means person
        """
        word = Person.stemmer.stem(word)
        return (word in Person.synonims) or (word in Person.labels)

    def __init__(self, name):
        self.__name = name
        self.__stemname = Person.stemmer.stem(name)
        self.__labellist = []
        return

    def get_info(self, triples, objects):
        """
            getting info from triples
        """
        for i in triples:
            if i[0][0] == self.__name:
                dname = i[2][0]
                stemdname = Person.stemmer.stem(dname)
                if stemdname in Person.labels:
                    self.__labellist.append(stemdname)
                    objects.update({dname: None})
        return

    def __str__(self):
        return self.__name + '\t' + self.__stemname


class Connection:
    """
        class contain info about connections
    """
    labels = ["play", "act", "direct", ]
    stemmer = SnowballStemmer("english")

    @staticmethod
    def valid_name(word):
        """
            check if word means Connection
        """
        word = Connection.stemmer.stem(word)
        return word in Connection.labels

    def __init__(self, name):
        self.__name = name
        self.__stemname = Connection.stemmer.stem(name)
        self.source = []
        self.dest = []
        return

    def get_info(self, triples, objects):
        """
            getting info from triples
        """
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        for i in triples:
            if i[0][0] == self.__name:
                dname = i[2][0]
                stemdname = Connection.stemmer.stem(dname)
                if Person.valid_name(dname):
                    obj = Person(stemdname)
                    objects.update({dname: obj})
                    obj.get_info(triples, objects)
                    objects[dname] = obj
                    self.set_dest(obj)
                    print('!!!!!!!!!!!!!!!!!!!!OBJECT ADDED!!!!!!!!!!!!!!!!!!!!!')
                if Film.valid_name(dname):
                    obj = Film(stemdname)
                    objects.update({dname: obj})
                    obj.get_info(triples, objects)
                    objects[dname] = obj
                    self.set_dest(obj)
                    print('!!!!!!!!!!!!!!!!!!!!OBJECT ADDED!!!!!!!!!!!!!!!!!!!!!')
                if Myobject.valid_name(dname):
                    obj = Myobject(stemdname)
                    objects.update({dname: obj})
                    obj.get_info(triples, objects)
                    objects[dname] = obj
                    self.set_dest(obj)
                    print('!!!!!!!!!!!!!!!!!!!!OBJECT ADDED!!!!!!!!!!!!!!!!!!!!!')
        return

    def set_source(self, obj):
        """
            adding first node of connection
        """
        self.source.append(obj)

    def set_dest(self, obj):
        """
            adding second node of connection
        """
        self.dest.append(obj)

    def __str__(self):
        rstr = ''
        rstr += '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
        rstr += self.__name + '\n'
        rstr += self.__stemname + '\n'
        rstr += 'sources:' + '\n'
        rstr += str([str(i) for i in self.source]) + '\n'
        rstr += 'dests:' + '\n'
        rstr += str([str(i) for i in self.dest]) + '\n'
        rstr += '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~' + '\n'
        return rstr


class Myobject:
    """
        objects class
    """
    objlist = []
    stemmer = SnowballStemmer("english")

    @staticmethod
    def valid_name(word):
        """
            check if word means named objects
        """
        return (word in Myobject.objlist) or word.isdigit()

    def __init__(self, name):
        self.__name = name
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

    def get_info(self, triples, objects):
        """
            getting info from triples
        """
        return

    def __str__(self):
        return self.__name


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
                print("name valid: " + name)
                obj = mclass(name)
                objlist.update({name: obj})
                obj.get_info(triples, objlist)
                objlist[name] = obj
    for i in triples:
        name = i[2][0]
        print("name: " + name)
        if name in objlist.keys():
            continue
        for mclass in classlist:
            if mclass.valid_name(name):
                print("name valid: " + name)
                obj = mclass(name)
                objlist.update({name: obj})
                obj.get_info(triples, objlist)
                objlist[name] = obj
    print(objlist.keys())
    for i in objlist.values():
        print(i)
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
