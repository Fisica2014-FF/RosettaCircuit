# Elenco dei possibili componenti e loro poli e parametri
# 'nome': (( lista_parametri ), numero_poli, OPZIONALE (lista_nomi_poli) )
# Se è bipolare e simmetrico non serve mettere la lista nomi poli
# Neanche i monopoli hanno bisogno di sapere il nome dell'(unica) uscita



lista_tipi_componenti = {
'monopole': ((),1,()),
'voltage_source': ( ( 'V' ), 2, ('m','p')  ),
'resistor': ( ( 'R' ), 2 ),
'capacitor': ( ( 'C' ), 2 ),
'inductance': ( ( 'L' ), 2 ),
'op_amp': ( (), 3, () ),

# m=minus, p=plus, o=output
'op_amp_reale': ( ( 'gain', 'Rinput', 'Routput' ), 3, ('m','p','o') )
}
