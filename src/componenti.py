# Elenco dei possibili componenti e loro poli e parametri
# 'nome': dict( lista_parametri=(...), numero_poli=..., lista_nomi_poli=(...) )
# Se è bipolare e simmetrico non serve mettere la lista nomi poli
# Neanche i monopoli hanno bisogno di sapere il nome dell'(unica) uscita


# Ricordarsi gli apici!
# a = dict( k=i )
# Si accede a i con a['k'] ovviamente, non con a[k]
lista_tipi_componenti = {
'monopole': dict( lista_parametri=(), numero_poli=1, lista_nomi_poli=() ),
'voltage_source': dict( lista_parametri=( 'V' ), numero_poli=2, lista_nomi_poli=( 'm', 'p' ) ),
'resistor': dict( lista_parametri=( 'R' ), numero_poli=2 ),
'capacitor': dict( lista_parametri=( 'C' ), numero_poli=2 ),
'inductance': dict( lista_parametri=( 'L' ), numero_poli=2 ),
'ground': dict(lista_parametri=(), numero_poli=1, lista_nomi_poli=()),
'op_amp': dict( lista_parametri=(), numero_poli=3, lista_nomi_poli=( 'm', 'p', 'o' ) ),

# m=minus, p=plus, o=output
'op_amp_reale': dict( lista_parametri=( 'gain', 'Rinput', 'Routput' ), numero_poli=3, lista_nomi_poli=( 'm', 'p', 'o' ) )
}
