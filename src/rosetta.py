#!/usr/bin/python3
#  The string at the top of the script is called the documentation string. 
# It documents the current script. Accessibile attraverso __doc__?
# Altra variabile speciale, __file__, la posizione di questo file
from componenti import lista_tipi_componenti
from operator import xor

'''
Created on 09 mar 2016

@author: francesco
'''
import sys
import collections
import os
import string
import importlib
import imp
import componenti
import pprint as pp



# Posizione assoluta del progetto
# In pratica, la cartella sopra di quella di questo script
# path_base = os.path.dirname( os.path.realpath( __file__ ) ) + '/../'

# Rimuovi src/
path_base = os.path.dirname( os.path.realpath( __file__ ) )[0:-4] + '/'

# ad es, 'Test1'
nome_circuito = sys.argv[1]
path_circuito = path_base + 'circuiti/' + nome_circuito + '/'
file_conf = path_circuito + nome_circuito + '.py'
print( path_base )
print( nome_circuito )
print( path_circuito )
print( file_conf )

# Importa il file di configurazioni del circuito
# componenti = imp.load_source('componenti' , path_base + 'src/componenti.py')
circuito_conf = imp.load_source( nome_circuito , file_conf )

# TODO: Classe 
class Circuito:
    __formatted_lines__ = []
    
    '''
    Sistema di rifermento
    *--------> X
    | 
    |
    |
    |
    v 
    Y
    Dunque adesso devo affettare la matrice per "lungo" e non per "largo", ie
    a b c
    d e f
    g h i
    da
    ((a,b,c),(d,e,f),(g,h,i))
    a
    ((a,d,g),(b,e,h),(c,f,i))
    cioè
    a d g
    b e h
    c f i
    (transposition)

    Lo facciamo cl metodo at()
    '''
    def at(self,x,y):
        return self.__formatted_lines__[y][x]
    
    def xmax(self):
        return len(self.__formatted_lines__[0])
    
    def ymax(self):
        return len(self.__formatted_lines__)
        
    def __init__(self, nome_circuito):
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
        # Nota, aggiungo uno spazio bianco ovunque attorno al circuito, per evitare di diver scrivere troppe
        # condizioni sulle dimensioni degli array quando sono vicino ai bordi
        self.__formatted_lines__ = [' ' * ( lunghezza_massima + 2 )]
        self.__formatted_lines__ = self.__formatted_lines__ + [' ' + riga.ljust( lunghezza_massima + 1 , ' ' ) for riga in raw_lines] + [' ' * ( lunghezza_massima + 2 )]
        
        '''
        Transposition        
        * is the splat operator
        list(...) because in python3 zip is an iterator and we want to reuse it
        '''
        # formatted_lines = list(zip(*formatted_lines))
        # self.formatted_lines = formatted_lines
        
    def print(self, filelog=None):
        if filelog == None:
            for linea in self.__formatted_lines__:
                print(linea)
        else:
            with open(filelog, 'w') as circlog:
                for linea in self.__formatted_lines__:
                    circlog.write(str(linea) + '\n')
                    
        return
    

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
    # Nota, aggiungo uno spazio bianco ovunque attorno al circuito, per evitare di diver scrivere troppe
    # condizioni sulle dimensioni degli array quando sono vicino ai bordi
    formatted_lines = [' ' * ( lunghezza_massima + 2 )]
    formatted_lines = formatted_lines + [' ' + riga.ljust( lunghezza_massima + 1 , ' ' ) for riga in raw_lines] + [' ' * ( lunghezza_massima + 2 )]
    
    ''' 
    TODO: Adesso devo affettare la matrice per "lungo" e non per "largo", ie
    a b c
    d e f
    g h i
    da
    ((a,b,c),(d,e,f),(g,h,i))
    a
    ((a,d,g),(b,e,h),(c,f,i))
    cioè
    a d g
    b e h
    c f i
    (tansposition)
    So we use the built-in zip on the matrix
    
    * is the splat operator
    list(...) because in python3 zip is an iterator and we want to reuse it
    '''
    
    formatted_lines = list(zip(*formatted_lines))
    pp.pprint(formatted_lines)
    
    return formatted_lines






# Il primo argomento è sys.argv[1]
# Prendi l'array bidimensionale rettangolare che rappresenta i componenti
# matcircuito = parseAsciiGraphFile( sys.argv[1] )
matcircuito = Circuito(sys.argv[1])





# Ritorna la stinga vuota se alla posizione i,j di matcircuito non c'è una maiuscola (e quindi un nome
# di variabile) altrimenti ritorna ((x,y),"NOME_VARIABILE") dove x,y è la coordinata della prima lettera
def scan_variable_name( x, y , matcircuito ):
    d = collections.deque()
    if matcircuito.at(x,y) == '+':
        return ( ( x, y ), '_CROSS' + 'X' + str( x ) + 'Y' + str( y ) )
    if matcircuito.at(x,y) not in string.ascii_uppercase:
        return ( ( -1, -1 ), '' )
    else:
        # O qua o col k dopo, si deve includere la lettera [x][y+0] in cui "atterriamo"
        k_prec = 0
        while ( y + k_prec >= 0 and ( matcircuito.at(x,y + k_prec) in string.ascii_uppercase + string.digits ) ):
            d.appendleft( matcircuito.at(x,y + k_prec) )
            # print( ( x, y + k_prec ), '=', matcircuito[x][y + k_prec] )
            k_prec = k_prec - 1
        

        # Qui quindi dobbiamo partire da 1
        k = 1
        while ( y + k < matcircuito.xmax() and ( matcircuito.at(x,y + k) in string.ascii_uppercase + string.digits ) ):
            d.append( matcircuito.at(x,y + k) )
            # print( ( x, y + k ), '=', matcircuito[x][y + k] )
            k = k + 1
        
        # k_prec+1 perché l'ultimo tentativo di ricerca all'indietro di maisucole è fallito
        # print( 'variabile in ', ( x, y + k_prec + 1 ), '=', ''.join( d ) )
        return ( ( x, y + k_prec + 1 ) , ''.join( d ) )



def crea_lista_variabili_grafo( matcircuito ):
    '''
    Riempi l'array con le variabili nel grafo
    '''
    variabili_nel_grafo = set( {} )
    i = 0
    while ( i < matcircuito.xmax() ):
        # In teoria sono tutti uguali, ma se cambio dopo...
        j = 0
        while ( j < matcircuito.ymax() ):
            # c = matcircuito[i][j]
            # print(c,(i,j))
            # print(len(matcircuito[i]))
            # print(scan_variable_name(i,j,matcircuito))
            # print(scan_variable_name(i,j,matcircuito)[0])
            # print(scan_variable_name(i,j,matcircuito)[1])
            
            nome_pos_variabile = scan_variable_name( i, j , matcircuito )
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
        
    return variabili_nel_grafo






'''
Ritorna una lista delle coordinate intorno al punto, inclusi i punti in diagonale
123
4#5
678
'''
def intorno_cella_pieno( p_x, p_y ):
    
    intorno_cella = ( ( p_x - 1, p_y - 1 ), ( p_x + 0, p_y - 1 ), ( p_x + 1, p_y - 1 ),
                      ( p_x - 1, p_y + 0 ), ( p_x + 1, p_y + 0 ),
                      ( p_x - 1, p_y + 1 ), ( p_x + 0, p_y + 1 ), ( p_x + 1, p_y + 1 ) )
    
    return intorno_cella

'''
Ritorna una lista delle coordinate intorno al punto, a forma di +
 1 
2#3
 4 
'''
def intorno_cella_piu( p_x, p_y ):
    
    intorno_cella = ( ( p_x + 0, p_y - 1 ),
                      ( p_x - 1, p_y + 0 ), ( p_x + 1, p_y + 0 ),
                                            ( p_x + 0, p_y + 1 ) )
    
    return intorno_cella

'''
Ritorna una lista delle coordinate orizzontali intorno al punto
  
1#2
   
'''
def intorno_cella_orizz( p_x, p_y ):
    
    intorno_cella = ( 
                      ( p_x - 1, p_y + 0 ), ( p_x + 1, p_y + 0 ),
                                                                                       )
    
    return intorno_cella

'''
Ritorna una lista delle coordinate intorno al punto, a forma di +
 1 
 # 
 2 
'''
def intorno_cella_vert( p_x, p_y ):
    
    intorno_cella = ( ( p_x + 0, p_y - 1 ),
                      
                                            ( p_x + 0, p_y + 1 ) )
    
    return intorno_cella



class Componente:
    '''
    Classe che rappresenta un componente nel circuito, ad esempio una resistenza o un op-amp.
    
    Contiene il nome, il tipo e un dict con i parametri.
    Unifica la descrizione geoetrica di variabile in un grafo con quella fisica (i vari parametri)
    '''
    # Ad es "R1"
    nome = ''
    tipo = ''
    # Ad es {'V'=10, 'R'=2.3e10}. Letti da Test1.circuitoconf
    parametri = {}
    # Coordinate della prima lettera del nome di variabile
    coordinate = ( -1, -1 )
    # dict dei contatti uscenti del componente, identificati da minuscole, dove sono e dove sono connessi
    # Un adjacency list tecnicamente, credo
    # Es {'m': (xm,ym, [ variabili_nel_grafo['R1'].contatti_poli['b'], variabili_nel_grafo['C1'].contatti_poli['a'] ]), 
    #     'p': (xp,yp, [ G.contatti_poli['a'] ]), 
    #     'o': (xo,yo, [ C1.contatti_poli['b'], V0.contatti_poli['a'] ])}
    contatti_poli = {}
    def __init__( self, nome, coordinate ):
        # TODO: Leggere da circuito_conf.parametri_componenti i parametri dei componenti
        # TODO: controllare validità della lista (dict) dei parametri con quella dichiarata 
        # in componenti.lista_tipi_componenti per quel tipo
        self.nome = nome
        self.coordinate = coordinate
        
        # TODO: Caso speciale se la variabile si chiama _CROSSX?Y?
        if self.nome[0:6] == '_CROSS':
            print( '[DEBUG]: Trovato cross' + str(coordinate) )
            self.tipo = '_cross'
            self.contatti_poli = {'p': ( coordinate[0], coordinate[1], [] )}
        else:
            # Leggi e setta i parametri, togliendo quello con chiave 'type' già usato per il tipo
            # Dovrebbe dare KeyError se nome non è nella lista
            dict_param = circuito_conf.parametri_componenti[nome]
            self.tipo = dict_param['type']
            
            # http://stackoverflow.com/questions/15411107/delete-a-dictionary-item-if-the-key-exists
            # Togli la chiave (e l'elemento associato a) 'type'
            dict_param.pop( 'type', None )
            self.parametri = dict_param
        
            self.__trova_poli_componente__()
            
    # Funzione che rende questa classe  hashabile (usabile come indice in un dict ad esempio)
    def __hash__( self ):
        # Qui repr ritorna una stringa rappresentante questo oggetto in modo "unico" (approfondire...)
        # e quindi generiamo un hash da questa stringa
        return hash( repr( self ) )
    
    def __trova_poli_componente__( self ):
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
            # trovare modo pythonico di sommare un numero a ciascun elemento di una lista
            # TODO: Riscrivere con intorno_orizz ecc
            # a): Prima del nome
            for yp in ( pos_comp_y - 1, pos_comp_y + 0, pos_comp_y + 1 ):
                
                #           a)              b)
                for xp in ( pos_comp_x - 1, pos_comp_x + len( self.nome ) + 1 ):
                    # Se la cella in (xp,yp) contiene una lettera minuscola...
                    print( "xp: " + str( xp ) + " yp: " + str( yp ) )
                    print( "#ighe:" + str( len( matcircuito ) ) + " #colonne" + str( len( matcircuito[xp] ) ))
                    if matcircuito[xp][yp] in string.ascii_lowercase:
                        # Usa la lettera come etichetta del polo e associaci le coordinate
                        label_polo = matcircuito[xp][yp]
                        
                        # Controlla che sia una label di polo ammessa, come indicato in componenti.py
                        '''if ( label_polo not in lista_tipi_componenti[self.tipo]['lista_poli'] ):
                            raise ValueError( "[ERROR]: Pole label" + label_polo + " of variable " + self.nome + 
                                            "of type " + self.tipo + "' not valid. Valid names are: \n" + 
                                            str( lista_tipi_componenti[self.tipo]['lista_poli'] ) + 
                                              "\nCheck file componenti.py" )
                        '''    
                        
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

                        # Utile, se tanto controllo sotto?
                        '''# Controlla che sia una label di polo ammessa, come indicato in componenti.py
                        if ( label_polo not in lista_tipi_componenti[self.tipo]['lista_poli'] ):
                            raise ValueError( "[ERROR]: Pole label" + label_polo + " of variable " + self.nome + 
                                            "of type " + self.tipo + "' not valid. Valid names are: \n" + 
                                            str( lista_tipi_componenti[self.tipo]['lista_poli'] ) + 
                                              "\nCheck file componenti.py" )
                        '''    

                        
                        # Dopo riempiremo la lista dei contatti...
                        self.contatti_poli[label_polo] = ( xp, yp, [] )
            
        
        # Controlla che ci siano i poli corretti
        if ( 'lista_nomi_poli' in lista_tipi_componenti[self.tipo].keys() and 
            len( lista_tipi_componenti[self.tipo]['lista_nomi_poli'] ) != 0 ):
            
            if ( set( self.contatti_poli.keys() ) != set( lista_tipi_componenti[self.tipo]['lista_poli'] ) ):
                raise ValueError( "[ERROR]: Poles of variable " + self.nome + 
                                  " not equal to those declared for type " + self.tipo + 
                                  " in componenti.py" )
            
        elif ( lista_tipi_componenti[self.tipo]['numero_poli'] != len( self.contatti_poli ) ):
            raise ValueError("[ERROR]: Number of poles of variable " + self.nome +
                             "not equal to the number declared for type " + self.tipo +
                             "in componenti.py")





    # Da chiamare dopo che trova_poli_componente è stata chiamata su ogni componente
    def trova_connessioni( self ):
        '''
        Trova a cosa è connesso ciascun polo di questo Component, seguendo i fili
        '''
        for nome_polo in self.contatti_poli.keys():
            px = self.contatti_poli[nome_polo][0]
            py = self.contatti_poli[nome_polo][1]
            
            
            '''
            Unifichiamo il codice per i fili orizzontali e verticali
            
            Dei  vari modi per farlo, questo mi è sembrato il più chiaro, anche se
            un po' prolisso.
            '''
            direzione_cella = dict( su=( px, py - 1 ),
                                    giu=( px, py + 1 ),
                                    dx=( px + 1, py ),
                                    sx=( py - 1, py ) )
            char_filo = dict( su='|', giu='|', dx='-', sx='-' )
            
            # d come direzione
            
            for d in ( 'su', 'giu', 'dx', 'sx' ):
                
                # for ( x_polo_intorno, y_polo_intorno ) in intorno_cella_corretto[d]:
                ( x_polo_intorno, y_polo_intorno ) = direzione_cella[d]
                
                if matcircuito[x_polo_intorno][y_polo_intorno] in char_filo[d]:
                    
                    if ( d == 'dx' ):
                        
                        # -->
                        # "Seguiamo" il filo, cioè controlliamo fin dove ci sono caratteri validi
                        i = 1
                        while matcircuito[x_polo_intorno + i][y_polo_intorno] in char_filo[d] + '^<>':
                            i = i + 1
                        
                        x_finefilo = x_polo_intorno + i
                        y_finefilo = y_polo_intorno
                        
                    elif ( d == 'sx' ):
                        # <--
                        i = -1
                        while matcircuito[x_polo_intorno + i][y_polo_intorno] in char_filo[d] + '^<>':
                            i = i - 1
                        x_finefilo = x_polo_intorno + i
                        y_finefilo = y_polo_intorno

                    elif ( d == 'su' ):
                        # ^
                        # |
                        i = -1
                        while matcircuito[x_polo_intorno][y_polo_intorno + i] in char_filo[d] + '^<>':
                            i = i - 1
                        x_finefilo = x_polo_intorno
                        y_finefilo = y_polo_intorno + i

                    elif ( d == 'giu' ):
                        # |
                        # v
                        i = 1
                        while matcircuito[x_polo_intorno][y_polo_intorno + i] in char_filo[d] + '^<>':
                            i = i + 1
                        x_finefilo = x_polo_intorno
                        y_finefilo = y_polo_intorno + i
                    
                    
                    
                    '''
                    Una volta usciti dal while, matcircuito[x_polo_intorno + i][y_polo_intorno] non è
                    un pezzo di filo valido
                    TODO: Cerchiamo poli di altre componenti, oppure un nome di variabile, oppure un più
                    Occhio a qualche caso limite...
                
                    Ad esempio, se stiamo seguendo il filo che dal polo p di V1 va al polo p di X1,
                    abbiamo che:    
                    
                            ?_ff_intorno
                                 v v
                             |  |
                    G-mV1p---^-->-pX1m-G2
                             |  |
                        ^ ^
                    ?_polo_intorno
                    
                    in questo caso
                    V1 = self
                    X1 = variabile_polo_arrivo
                    
                    '''
                    
                    # Controlliamo dove siamo arrivati. Se è un polo...
                    if matcircuito[x_finefilo][y_finefilo] in string.ascii_lowercase :
                        variabile_polo_arrivo = ( ( -1, -1 ), '' )
                        
                        # ... cerca la variabile (componente) a cui appartiene
                        for ( x_ff_intorno, y_ff_intorno ) in intorno_cella_pieno( x_finefilo , y_finefilo ):
                            # TODO: Condizione insensata!!!
                            variabile_trovata = False
                            variabile_polo_arrivo = scan_variable_name( x_ff_intorno, y_ff_intorno )
                            
                            # Controlla che il polo non sia attaccato a due variabili
                            if (not variabile_trovata) and variabile_polo_arrivo != ( ( -1, -1 ), '' ):
                                
                                # TODO: aggiungere il nome del polo di arrivo in self.contatti_poli[2][nome_polo]
                                # Ricordiamo che nome_polo è il polo di partenza, attacato a self
                                # TODO: Non vanno aggiunti da componenti_grafo?
                                self.contatti_poli[2][nome_polo].append( componenti_grafo[variabile_polo_arrivo] )
                                
                                variabile_trovata = True
                            elif variabile_trovata and variabile_polo_arrivo != ( ( -1, -1 ), '' ):
                                raise ValueError( "Polo associato a più variabili! X" + 
                                                 str( x_ff_intorno ) + " Y" + str( y_ff_intorno ) )
                                
                                
                                
                    # TODO: Se è un incrocio ('+')...
                    #elif matcircuito[x_finefilo][y_finefilo] == '+':
                    #    nome_cross = '_CROSSX'+str(x_finefilo)+'Y'+str(y_finefilo)
                        
                        self.contatti_poli
                        
                                
                
                # Cerca e segui i fili
            
            
 
            
            
            
            
            
            
            
            
            
            
            
            
'''
"MAIN"
'''
# TODO:Potremmo separarare l'inizializzazione (parseAsciiGraphFile, la creazione delle variabili globali) 
# in un altro file..) in un altro

variabili_nel_grafo = crea_lista_variabili_grafo( matcircuito )

pp.pprint( variabili_nel_grafo )

for y in range(0,matcircuito.ymax()):
    for x in range(0, matcircuito.xmax()):
        print(matcircuito.at(x,y),end='')
    print()


# TODO: Stampa il circuito usato, per il debug
matcircuito.print("circlog")
matcircuito.print()

# TODO: fare una lista/dict componenti_grafo di Component con chiave il loro nome
componenti_grafo = dict()
for var in variabili_nel_grafo:
    posx = var[0][0]
    posy = var[0][1]
    nome = var[1]

    # Il costruttore chiama anche i poli componente
    componenti_grafo[nome] = Componente( nome, ( posx, posy ) )

# Cerca tutte le connesioni
for comp in componenti_grafo:
    comp.trova_connessioni()

for comp in componenti_grafo:
    print(repr( comp ) +"\n\n")

#print( variabili_nel_grafo )
#print( componenti.lista_tipi_componenti )
#print( circuito_conf.parametri_componenti )

# TODO: Per il debug
for i in range( 0, len( matcircuito ) ):
    print( matcircuito[i] )

    


""" 
    Adesso vogliamo una lista delle variabili e dei rispettivi nodi, e di cosa sono connessi questi nodi
    Cosa vogliamo ottenere? Una cosa del tipo
    {
        'OPAMP':( (3, 4),{'p': [. .. ]} )
    }
"""
# Adesso cerchiamo i nodi associati alle variabili (variabile = componente)

'''
print( str( variabili_nel_grafo ) )
print( os.path.dirname( os.path.realpath( __file__ ) ) )
print( 2.3e3 )
print( test )
print( componenti.lista_tipi_componenti )

print( ( 0, 1, 2, 3, 4 )[0:4] )

for i in range( -1, 1 ):
    print( i )
'''
