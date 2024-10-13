from abc import ABCMeta, abstractmethod
import random
import numpy as np


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
        return []


#####################################################################################################

class ValidacionSimple(EstrategiaParticionado):

    # Crea partitions segun el metodo tradicional de division de los datos segun el porcentaje deseado y el n�mero de ejecuciones deseado
    # Devuelve una lista de particiones (clase Particion)
    # TODO: implementar

    def __init__(self, n_executions, percentage):
        self.partitions = []
        self.executions = n_executions
        self.percentage = percentage

    def creaParticiones(self, datos, seed=None):
        random.seed(seed)

        data_len = datos.shape[0]
        test_len = round(data_len * self.percentage)
        data_rows = np.arange(data_len)

        for _ in range(self.executions):
            np.random.shuffle(data_rows)

            partition = Particion()
            partition.indicesTest = data_rows[:test_len].tolist()
            partition.indicesTrain = data_rows[test_len:].tolist()

            self.partitions.append(partition)

        return self.partitions


#####################################################################################################
class ValidacionCruzada(EstrategiaParticionado):

    # Crea partitions segun el metodo de validacion cruzada.
    # El conjunto de entrenamiento se crea con las nfolds-1 particiones y el de test con la partici�n restante
    # Esta funcion devuelve una lista de particiones (clase Particion)
    # TODO: implementar

    def __init__(self, n_folds):
        self.partitions = []
        self.folds = n_folds 

    def creaParticiones(self, datos, seed=None):
        random.seed(seed)

        data_len = datos.shape[0]
        folds_len_base = data_len // self.folds
        remainder = data_len % self.folds

        rows = np.arange(data_len)

        index = 0
        for i in range(self.folds):
            folds_len = folds_len_base + 1 if i < remainder else folds_len_base

            test_rows = rows[index:index + folds_len]
            train_rows = np.concatenate((rows[:index], rows[index + folds_len:]))

            partition = Particion()
            partition.indicesTest = test_rows 
            partition.indicesTrain = train_rows.tolist() 

            self.partitions.append(partition)

            index += folds_len

        return self.partitions