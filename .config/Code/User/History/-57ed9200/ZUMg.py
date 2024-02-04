# Define
def adiciona_c ( elem , lista ) :
    """ Adiciona o elem ao fim da lista . """
    lista . append ( elem )
    return lista

# --- Usa
print ( ' Tua ')
tua_lista = [1 ,2 ,3]

print ( adiciona_c (1 , tua_lista ) )
print ( adiciona_c (1 , adiciona_c (1 , tua_lista ) ) )
print ( adiciona_c ( adiciona_c (1 , tua_lista ) , adiciona_c(1 , tua_lista )) )
print ( adiciona_c (1 ,1))