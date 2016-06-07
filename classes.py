"""
    module translate natural language query
    to CYPHER query
"""

from nltk.parse.stanford import StanfordDependencyParser
from nltk.stem import SnowballStemmer
import string
import random


def id_generator(size=6, chars=string.ascii_uppercase):
    """
        generate some id
    """
    return ''.join(random.choice(chars) for _ in range(size))


class Film:
    """
        class contain info about unknown film
    """
    synonims = ["film", "picture", ]
    labels = ["horror", "romantic", "thriller", "comedy", ]
    properties = ["releas", "publish", ]
    stemmer = SnowballStemmer("english")

    @staticmethod
    def valid_name(word):
        """
            check if word means film
        """
        word = Film.stemmer.stem(word)
        return (word in Film.synonims) or (word in Film.labels)

    def __init__(self, name):
        """
            init class
        """
        self.__name = name
        self.__stemname = Film.stemmer.stem(name)
        self.__labellist = ["Films",]
        if name in Film.labels:
            self.__labellist.append(name.title())
        self.__attr = {}
        return

    def get_prop(self, propertiname, stempropname, triples, objects):
        for i in triples:
            if i[0][0] == propertiname:
                dname = i[2][0]
                if dname.isdigit():
                    self.__attr.update({stempropname: dname})
                    break

    def get_info(self, triples, objects):
        """
            getting info from triples
        """
        for i in triples:
            if i[0][0] == self.__name:
                dname = i[2][0]
                stemdname = Film.stemmer.stem(dname)
                if stemdname in Film.labels:
                    self.__labellist.append(stemdname.title())
                    objects.update({dname: None})
                if dname in Film.labels:
                    self.__labellist.append(dname.title())
                    objects.update({dname: None})
                if stemdname in Film.properties:
                    print("PropertyFound!")
                    self.get_prop(dname, stemdname, triples, objects)
                if Connection.valid_name(dname):
                    if stemdname in objects.keys():
                        con = objects[dname]
                        con.set_source(self)
                    else:
                        con = Connection(dname)
                        con.set_source(self)
                        objects.update({dname: con})
                        con.get_info(triples, objects)
                        objects[dname] = con
        return

    @staticmethod
    def get_syn(word):
        """
            get synonim property name to word argumetn
        """
        return "Year_Of_Release"

    def get_cypher(self, dname):
        """
            create cypher query from class
        """
        rstr = 'MATCH ({} '.format(dname)
        for i in self.__labellist:
            rstr += ':{}'.format(i)
        rstr += '{'
        for i in self.__attr.items():
            rstr += '{0}:"{1}"'.format(Film.get_syn(i[0]),str(i[1]))
        rstr += '})'
        return rstr

    def get_name(self):
        """
            get name of connection
        """
        return self.__name

    def __str__(self):
        """
            return string interpretation of class
        """
        rstr = '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
        rstr += self.__name + '\t' + self.__stemname + '\n'
        for i in self.__attr.items():
            rstr += str(i[0]) + '\t' + str(i[1]) + '\n'
        rstr += '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
        return rstr


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
        """
            init class
        """
        self.__name = name
        self.__stemname = Person.stemmer.stem(name)
        self.__labellist = ["Person", ]
        if name in Person.labels:
            self.__labellist.append(name.title())
        self.__attr = {}
        return

    @staticmethod
    def get_syn(word):
        """
            return synonim property name
        """
        return "Birth_Year"

    def get_prop(self, propertiname, stempropname, triples, objects):
        """
            get property using its name and adding 
            element to objlist dictionary
        """
        for i in triples:
            if i[0][0] == propertiname:
                dname = i[2][0]
                if dname.isdigit():
                    self.__attr.update({stempropname: dname})
                    break

    def get_info(self, triples, objects):
        """
            getting info from triples
        """
        for i in triples:
            if i[0][0] == self.__name:
                dname = i[2][0]
                stemdname = Person.stemmer.stem(dname)
                if stemdname in Person.labels:
                    self.__labellist.append(stemdname.title())
                    objects.update({dname: None})
                if stemdname in Person.properties:
                    self.get_prop(dname, stemdname, triples, objects)
        return

    @staticmethod
    def get_syn(word):
        """
            get synonim property name to word argumetn
        """
        return "Birth_Year"

    def get_cypher(self, dname):
        """
            create cypher query using 
            data from class
        """
        rstr = 'MATCH ({} '.format(dname)
        for i in self.__labellist:
            rstr += ":{}".format(i)
        rstr += '{'
        for i in self.__attr.items():
            rstr += '{0}:"{1}"'.format(Person.get_syn(i[0]),str(i[1]))
        rstr += "})"
        return rstr

    def get_name(self):
        """
            get name of connection
        """
        return self.__name

    def __str__(self):
        """
            return string interpretation
            of class data
        """
        rstr = '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
        rstr += self.__name + '\t' + self.__stemname + '\n'
        for i in self.__attr.items():
            rstr += str(i[0]) + '\t' + str(i[1]) + '\n'
        rstr += '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
        return rstr

class Connection:
    """
        class contain info about connections
    """
    labels = ["play", "act", "direct", ]
    stemmer = SnowballStemmer("english")
    synonims = {"Acted_in": ["act", "play"], "Produced_by": ["direct", ]}

    @staticmethod
    def valid_name(word):
        """
            check if word means Connection
        """
        word = Connection.stemmer.stem(word)
        return word in Connection.labels

    def __init__(self, name):
        """
            class init
        """
        self.__name = name
        self.__stemname = Connection.stemmer.stem(name)
        self.source = []
        self.dest = []
        return

    def get_info(self, triples, objects):
        """
            getting info from triples
        """
        # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
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
                    #print('!!!!!!!!!!!!!!!!!!!!OBJECT ADDED!!!!!!!!!!!!!!!!!!!!!')
                if Film.valid_name(dname):
                    obj = Film(stemdname)
                    objects.update({dname: obj})
                    obj.get_info(triples, objects)
                    objects[dname] = obj
                    self.set_dest(obj)
                    #print('!!!!!!!!!!!!!!!!!!!!OBJECT ADDED!!!!!!!!!!!!!!!!!!!!!')
                if Myobject.valid_name(dname):
                    obj = Myobject(dname)
                    objects.update({dname: obj})
                    obj.get_info(triples, objects)
                    objects[dname] = obj
                    self.set_dest(obj)
                    #print('!!!!!!!!!!!!!!!!!!!!OBJECT ADDED!!!!!!!!!!!!!!!!!!!!!')
        return

    def get_cypher(self):
        """
            create cypher query
        """
        rstr = ''
        src = None
        dst = None
        if len(self.source):
            src = self.source[0]
        else:
            return None

        if len(self.dest):
            dst = self.dest[0]
        else:
            return None
        src_id = id_generator(4)
        dst_id = id_generator(4)
        conname = ''
        for i in Connection.synonims.items():
            if self.__stemname in i[1]:
                conname = i[0]
        rstr = 'MATCH (({0}) -[:{1}]-> ({2}))\n'.format(src_id, conname , dst_id)
        rstr += src.get_cypher(src_id)+'\n'
        rstr += dst.get_cypher(dst_id)+'\n'
        rstr+= "return {0},{1}".format(src_id, dst_id)
        return rstr

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

    def get_name(self):
        """
            get name of connection
        """
        return self.__name

    def get_dest_str(self):
        """
            get dest nodes in string format
        """
        return str([str(i) for i in self.dest])

    def get_source_str(self):
        """
            get source nodes in string format
        """
        return str([str(i) for i in self.source])

    def __str__(self):
        """
            return string interpretation
            of class data
        """
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
    objdict = {}
    stemmer = SnowballStemmer("english")
    @staticmethod
    def valid_name(word):
        """
            check if word means named objects
        """
        return (word in Myobject.objlist) or word.isdigit()

    def __init__(self, name):
        self.__name = name
        if name.isdigit():
            Myobject.objdict.update({name:name})
        return

    def get_name(self):
        """
            get name of connection
        """
        return self.__name

    @staticmethod
    def string_analys(gstr):
        """
            prepare string to next steps,
            and gets named objects from sentences
        """
        flag = 0
        rstr = ""
        obj_str_nonchanged = ""
        obj_str = ""
        for i in gstr:
            if i == '[':
                flag = 1
                continue
            if i == ']':
                flag = 0
                rstr += obj_str
                Myobject.objlist.append(obj_str)
                print("key:" + obj_str)
                Myobject.objdict.update({obj_str:obj_str_nonchanged})
                obj_str_nonchanged = ""
                obj_str = ""
                continue
            if flag and i == ' ':
                obj_str_nonchanged += i 
                continue
            if flag:
                obj_str += i
                obj_str_nonchanged += i
                continue
            rstr += i
        return rstr

    def get_cypher(self, dname):
        """
            create cypher query
        """
       # print("NAME " + self.__name)
        rstr = 'WHERE {0}.Person_Name="{1}" OR {0}.Film_Name="{1}"'.format(dname,Myobject.objdict[self.__name])
        return rstr

    def get_info(self, triples, objects):
        """
            getting info from triples
        """
        return

    def __str__(self):
        """
            return string interpretation
            of class data
        """
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
        #sprint("name: " + name)
        if name in objlist.keys():
            continue
        for mclass in classlist:
            if mclass.valid_name(name):
                #print("name valid: " + name)
                obj = mclass(name)
                objlist.update({name: obj})
                obj.get_info(triples, objlist)
                objlist[name] = obj
    for i in triples:
        name = i[2][0]
        #print("name: " + name)
        if name in objlist.keys():
            continue
        for mclass in classlist:
            if mclass.valid_name(name):
                #print("name valid: " + name)
                obj = mclass(name)
                objlist.update({name: obj})
                obj.get_info(triples, objlist)
                objlist[name] = obj
    print(objlist.keys())
    for i in objlist.values():
        print(i)
    return objlist


def objlist_analise(objlist):
    """
        analysis objlist and create Cypher query
    """
    for i in objlist.values():
        if isinstance(i, Connection):
            print("Connection Found")
            return i.get_cypher()
    for i in objlist.values():
        if isinstance(i, Film):
            print("Film Found")
            rstr =  i.get_cypher("SomeFilm")
            rstr += "\nreturn SomeFilm"
            return rstr
    for i in objlist.values():
        if isinstance(i, Person):
            print("Film Found")
            rstr =  i.get_cypher("SomePerson")
            rstr += "\nreturn SomePerson"
            return rstr
    return None

def entpoint(querystring):
    path_to_jar = '../exp/stanford-corenlp-full-2015-12-09/stanford-corenlp-3.6.0.jar'
    path_to_models_jar = '../exp/stanford-corenlp-full-2015-12-09/stanford-\
english-corenlp-2016-01-10-models.jar'
    dep_parser = StanfordDependencyParser(
        path_to_jar=path_to_jar,
        path_to_models_jar=path_to_models_jar)
    pars_res = [parse for parse in dep_parser.raw_parse(
        Myobject.string_analys(querystring))]
    objlist = get_obj([list(smp.triples()) for smp in pars_res][0])
    return objlist_analise(objlist)

def main():
    """
        main function
    """
    fl = open('input')
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
        objlist = get_obj([list(smp.triples()) for smp in i][0])
        print(objlist_analise(objlist))
        print("-----------------------------------------------")
        print(j)
        print("###############################################")

if __name__ == '__main__':
    main()
