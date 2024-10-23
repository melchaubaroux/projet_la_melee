""" Le fichier ci dessous contiens une liste  de wrapper pour encadrer l'execution de fonction dans le cadre d'une journalisation """

import time 


############################ wrappeur unitaire ###########################################

# wrapper vide 

def empty_wrappeur(func):
    def wrapper(*args, **kwargs):

        func(*args, **kwargs) 

    return wrapper

# wrappeur pour afficher le nom d'une fonction appelé 

def get_fonction_name(func):
    def wrapper(*args, **kwargs):

        print(func.__name__)

        func(*args, **kwargs) 

    return wrapper

# wrapper pour calculer le temps d'une fonction

def execution_time(func):
    def wrapper(*args, **kwargs):

        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        duration = end -start

        print(f"Temps d'exécution : {duration:.6f} secondes")

    return wrapper

# wrapper pour faire remonter les problemes d'execution sans crash 

def check_execution(func):
    def wrapper(*args, **kwargs):

        try:
            # print("EXECUTED")
            # return func(*args, **kwargs)
            func(*args, **kwargs)
            print("EXECUTED")

        except Exception as e:
            print( "ERROR : ", str(e))
    
    return wrapper


############################ combinateur de  wrappeur  ##################################


def wrappers_combinator(decorators):
    
    def wrapper(func):
        for decorator in reversed(decorators):
            func = decorator(func)
        return func
    return wrapper


if __name__ == '__main__':
    
    
###########################      test des wrappeur simple #############################


    @get_fonction_name
    def test_get_fonction_name(): 
        time.sleep(2)

    test_get_fonction_name()

    @check_execution
    def test_check_execution(): 
        time.sleep(2)

    test_check_execution()

    @execution_time
    def test_execution_time(): 
        time.sleep(2)

    test_execution_time()


################# test des wrappeur combiné  ####################

    name_execution_time = wrappers_combinator([execution_time,check_execution,get_fonction_name])

    @name_execution_time
    def test_wrappers_combinator(): 
        pass

    test_wrappers_combinator()










