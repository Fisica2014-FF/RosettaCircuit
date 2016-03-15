#!/usr/bin/python3
#  The string at the top of the script is called the documentation string. 
# It documents the current script. Accessibile attraverso __doc__?
# Altra variabile speciale, __file__, la posizione di questo file

'''
Created on 09 mar 2016

@author: francesco
'''
import sys
import collections
import os
import string
import componenti

# Posizione assoluta del progetto
# In pratica, la cartella sopra di quella di questo script
path_base = os.path.dirname( os.path.realpath( __file__ ) ) + '/../'

def parseAsciiGraphFile( nome_circuito ):
    # Leggi tutto il file in una stringa
    with open( path_base + 'circuiti/' + nome_circuito + '/' + 
               nome_circuito + '.circuitograph', 'r' ) as f:
        read_data = f.read()
        
    # TODO Ma davvero servira' farle di lunghezza invariata? Vediamo a codice finito
    # Dobbiamo farle di lunghezza uguale, paddiamole a destra con spazi secondo quella piu' lunga
    # Splitlines le divide in righe e toglie l'a capo
    raw_lines = read_data.splitlines()
    # Max ritorna la stringa piu' lunga, secondo la funzione len appunto. Quindi richiamiamo
    # len(...) sulla stringa piu' lunga per salvare la sua lunghezza in lunghezza_massima
    # Credo che  max(raw_lines,key=len) e  max(raw_lines, len) siano ecquivalenti?
    lunghezza_massima = len( max( raw_lines, key=len ) )
    
    # for riga in raw_lines:
    #  # ljust aggiunge spazi bianchi alla stringa finche' non e' della lunghezza indicata, altrimenti
    #   # se e' uguale (o maggiore, ma non dovrebbe essere il caso qua...) la lascia invariata
    #    riga=riga.ljust(lunghezza_massima,'#')
    # Esempio di list comprehension
    formatted_lines = [riga.ljust( lunghezza_massima ) for riga in raw_lines]
    
    return formatted_lines




# Il primo argomento è sys.argv[1]
# Prendi l'array bidimensionale rettangolare che rappresenta i componenti
matcircuito = parseAsciiGraphFile( sys.argv[1] )




# Ritorna la stinga vuota se alla posizione i,j di matcircuito non c'è una maiuscola (e quindi un nome
# di variabile) altrimenti ritorna ((x,y),"NOME_VARIABILE") dove x,y è la coordinata della prima lettera
def scan_variable_name( i, j ):
    d = collections.deque()
    if matcircuito[i][j] not in string.ascii_uppercase:
        return ( ( -1, -1 ), "" )
    else:
        # O qua o col k dopo, si deve includere la lettera [i][j+0] in cui "atterriamo"
        k_prec = 0
        while ( j + k_prec >= 0 and ( matcircuito[i][j + k_prec] in string.ascii_uppercase + string.digits ) ):
            d.appendleft( matcircuito[i][j + k_prec] )
            print( ( i, j + k_prec ), '=', matcircuito[i][j + k_prec] )
            k_prec = k_prec - 1
        

        # Qui quindi dobbiamo partire da 1
        k = 1
        while ( j + k < len( matcircuito[i] ) and ( matcircuito[i][j + k] in string.ascii_uppercase + string.digits ) ):
            d.append( matcircuito[i][j + k] )
            print( ( i, j + k ), '=', matcircuito[i][j + k] )
            k = k + 1
        
        # k_prec+1 perché l'ultimo tentativo di ricerca all'indietro di maisucole è fallito
        print( 'variabile in ', ( i, j + k_prec + 1 ), '=', ''.join( d ) )
        return ( ( i, j + k_prec + 1 ) , ''.join( d ) )
 
# lista_totale_poli = 

class Componente:
    '''
    Classe che rappresenta un componente nel circuito, ad esempio una resistenza o un op-amp.
    Contiene il nome, un dict con i parametri
    '''
    matcircuito = [[]]
    # Ad es "R1"
    nome = ''
    tipo = ''
    # Ad es {'V'=10, 'R'=2.3e10}. Letti da Test1.circuitoconf
    parametri = {}
    # Coordinate della prima lettera del nome di variabile
    coordinate = ( -1, -1 )
    # dict dei contatti uscenti del componente, identificati da minuscole, dove sono e dove sono connessi
    # Un adjacency list tecnicamente, credo
    # Es {'m': (xm,ym, [ R1.contatti_poli['b'], C1.contatti_poli['a'] ]), 
    #     'p': (xp,yp, [ G.contatti_poli['a'] ]), 
    #     'o': (xo,yo, [ C1.contatti_poli['b'], V0.contatti_poli['a'] ])}
    contatti_poli = {}
    def __init__( self, matcircuito, nome, tipo, coordinate, contatti_poli={} ):
        self.matcircuito = matcircuito
        self.nome = nome
        self.coordinate = coordinate
        self.contatti_poli = contatti_poli
    
    # Funzione che rende questa classe  hashabile (usabile come indice in un dict ad esempio)
    def __hash__( self ):
        # Qui repr ritorna una stringa rappresentante questo oggetto in modo "unico" (approfondire...)
        # e quindi generiamo un hash da questa stringa
        return hash( repr( self ) )
    
    def trova_poli_componente( self, variabili_nel_grafo ):
        '''
        Metodo che riempe la lista 'contatti_poli' del componente e controlla che corrispondano al suo tipo
        come definito in componenti.py
        '''
        for comp in variabili_nel_grafo:
            pos_comp_x = comp[0][0]
            pos_comp_y = comp[0][1]
            '''
            Cerca prima e dopo il nome di variabile. Ricordiamo che 
            (pos_comp_x, pos_comp_y) è la posizione della prima lettera del nome della variabile,
            ad esempio qua è la 'O' di OPAMP
            
            a)    b)
            #     #
            #OPAMP#
            #     #
            '''
            # TODO: trovare modo pythonico di sommare un numero a ciascun elemento di una lista
            # a): Prima del nome
            for yp in ( pos_comp_y - 1, pos_comp_y + 0, pos_comp_y + 1 ):
                
                #           a)              b)
                for xp in ( pos_comp_x - 1, pos_comp_x + len( self.nome ) + 1 ):
                    # Se la cella in (xp,yp) contiene una lettera minuscola...
                    if matcircuito[xp][yp] in string.ascii_lowercase:
                        # Usa la lettera come etichetta del polo e associaci le coordinate
                        label_polo = matcircuito[xp][yp]
                        # Dopo riempiremo la lista dei contatti...
                        self.contatti_poli[label_polo] = ( xp, yp, [] )
                
            '''
            Cerca "sopra" e "sotto" la variabile
             #####
             OPAMP
             #####
            '''
            for yp in ( pos_comp_y - 1, pos_comp_y + 1 ):

                # C'è un "+1" in più perché range(a,b) "matematicamente", 
                # con la notazione di intervallo dell'analisi, è [a,b)
                for xp in range( pos_comp_x, pos_comp_x + len( self.nome ) + 2 ):
                    if matcircuito[xp][yp] in string.ascii_lowercase:
                        # 
                        label_polo = matcircuito[xp][yp]
                        # Dopo riempiremo la lista dei contatti...
                        self.contatti_poli[label_polo] = ( xp, yp, [] )
                        
# "Main"

# TODO: Per il debug
for i in range( 1, len( matcircuito ) ):
    print( matcircuito[i] )

i = 0
variabili_nel_grafo = set( [] )
while ( i < len( matcircuito ) ):
    # In teoria sono tutti uguali, ma se cambio dopo...
    j = 0
    while ( j < len( matcircuito[i] ) ):
        # c = matcircuito[i][j]
        # print((i,j))
        # print(len(matcircuito))
        # print(scan_variable_name(matcircuito,i,j))
        # print(scan_variable_name(matcircuito,i,j)[0])
        # print(scan_variable_name(matcircuito,i,j)[1])
        
        nome_pos_variabile = scan_variable_name( matcircuito, i, j )
        if ( nome_pos_variabile[1] != '' ):
            variabili_nel_grafo.add( nome_pos_variabile )
            # Se abbiamo trovato la variabile, salta alla fine della variabile corrente, data dalla 
            # posizione della prima lettera più la lunghezza della variabile (ricordiamo che 
            # nome_pos_variabile ha la forma ((x,y),"NOME_VARIABILE") ) con x e coordinate della prima lettera 
            j = nome_pos_variabile[0][1] + len( nome_pos_variabile[1] ) + 1
            continue
        # Altrimenti passa al prossimo carattere
        j = j + 1
    i = i + 1

""" 
    Adesso vogliamo una lista delle variabili e dei rispettivi nodi, e di cosa sono connessi questi nodi
    Cosa vogliamo ottenere? Una cosa del tipo
    {
        'OPAMP':( (3, 4),{'p': [. .. ]} )
    }
"""
# Adesso cerchiamo i nodi associati alle variabili (variabile = componente)

test = {
    'a': 
      1,
        'b': 2
}

print( str( variabili_nel_grafo ) )
print( os.path.dirname( os.path.realpath( __file__ ) ) )
print( 2.3e3 )
print( test )
print( componenti.lista_tipi_componenti )

for i in range( -1, 1 ):
    print( i )
