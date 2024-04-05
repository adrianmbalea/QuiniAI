import data
import threading

n_threads = 8
threads = []

def main_func(id_hilo):
    if id_hilo==0:
        data.getResultsLeague('laliga', 2013)
        data.getResultsLeague('laliga2', 2013)
        data.getResultsLeague('laliga', 2021)
        print(f'\n********************************************************************\nTHREAD {id_hilo} TERMINADO\n********************************************************************\n')
    elif id_hilo==1:
        data.getResultsLeague('laliga', 2014)
        data.getResultsLeague('laliga2', 2014)
        data.getResultsLeague('laliga2', 2021)
        print(f'\n********************************************************************\nTHREAD {id_hilo} TERMINADO\n********************************************************************\n')
    elif id_hilo==2:
        data.getResultsLeague('laliga', 2015)
        data.getResultsLeague('laliga2', 2015)
        data.getResultsLeague('laliga', 2022)
        print(f'\n********************************************************************\nTHREAD {id_hilo} TERMINADO\n********************************************************************\n')
    elif id_hilo==3:
        data.getResultsLeague('laliga', 2016)
        data.getResultsLeague('laliga2', 2016)
        data.getResultsLeague('laliga2', 2022)
        print(f'\n********************************************************************\nTHREAD {id_hilo} TERMINADO\n********************************************************************\n')
    elif id_hilo==4:
        data.getResultsLeague('laliga', 2017)
        data.getResultsLeague('laliga2', 2017)
        data.getResultsLeague('laliga', 2023)
        print(f'\n********************************************************************\nTHREAD {id_hilo} TERMINADO\n********************************************************************\n')
    elif id_hilo==5:
        data.getResultsLeague('laliga', 2018)
        data.getResultsLeague('laliga2', 2018)
        data.getResultsLeague('laliga2', 2023)
        print(f'\n********************************************************************\nTHREAD {id_hilo} TERMINADO\n********************************************************************\n')
    elif id_hilo==6:
        data.getResultsLeague('laliga', 2019)
        data.getResultsLeague('laliga2', 2019)
        print(f'\n********************************************************************\nTHREAD {id_hilo} TERMINADO\n********************************************************************\n')
    elif id_hilo==7:
        data.getResultsLeague('laliga', 2020)
        data.getResultsLeague('laliga2', 2020)
        print(f'\n********************************************************************\nTHREAD {id_hilo} TERMINADO\n********************************************************************\n')
    else:
        print("¡¡¡ERROR!!!")
    

for i in range(0, n_threads):
    thread = threading.Thread(target=main_func, args=(i,))
    threads.append(thread)

# Iniciar todos los threads
for thread in threads:
    thread.start()

# Esperar a que todos los threads terminen
for thread in threads:
    thread.join()