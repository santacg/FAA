from abc import ABCMeta, abstractmethod
import random


class Particion():

    # Esta clase mantiene la lista de �ndices de Train y Test para cada partici�n del conjunto de particiones
    def __init__(self):
        self.indicesTrain = []
        self.indicesTest = []

    def __str__(self):
        return f'train: {self.indicesTrain} test: {self.indicesTest}'

#####################################################################################################


class EstrategiaParticionado:

    # Clase abstracta
    __metaclass__ = ABCMeta

    # Atributos: deben rellenarse adecuadamente para cada estrategia concreta. Se pasan en el constructor

    @abstractmethod
    # TODO: esta funcion deben ser implementadas en cada estrategia concreta
    def creaParticiones(self, datos, seed=None):
        pass


#####################################################################################################

class ValidacionSimple(EstrategiaParticionado):

    # Crea particiones segun el metodo tradicional de division de los datos segun el porcentaje deseado y el n�mero de ejecuciones deseado
    # Devuelve una lista de particiones (clase Particion)
    # TODO: implementar
    def creaParticiones(self, datos, porcentaje, nEjecuciones, seed=None):
        random.seed(seed)
        lista_seeds = []

        for _ in range(nEjecuciones):
            lista_seeds.append(random.random())

        datos_len = datos.shape[0]
        test_len = int(datos_len * porcentaje)

        lista_filas = set(range(datos_len))

        lista_particiones = []
        for i in range(nEjecuciones):
            random.seed(lista_seeds[i])

            lista_test = random.sample(range(datos_len), test_len)

            lista_entranamiento = list(lista_filas - set(lista_test))

            particion = Particion()
            particion.indicesTest = sorted(lista_test)
            particion.indicesTrain = sorted(lista_entranamiento)

            lista_particiones.append(particion)

        return lista_particiones


#####################################################################################################
class ValidacionCruzada(EstrategiaParticionado):

    # Crea particiones segun el metodo de validacion cruzada.
    # El conjunto de entrenamiento se crea con las nfolds-1 particiones y el de test con la particion restante
    # Esta funcion devuelve una lista de particiones (clase Particion)
    # TODO: implementar
    def creaParticiones(self, datos, nFolds, seed=None):
        random.seed(seed)

        datos_len = datos.shape[0]
        folds_len = int(datos_len / nFolds)

        lista_filas = set(range(datos_len))

        lista_particiones = []
        for i in range(nFolds):
            lista_test = range(folds_len * i, folds_len * (i + 1))
            lista_entranamiento = list(lista_filas - set(lista_test))

            particion = Particion()
            particion.indicesTest = lista_test
            particion.indicesTrain = lista_entranamiento

            lista_particiones.append(particion)

        return lista_particiones
