from collections import Counter, defaultdict


def sustituye_palabras(texto: str, diccionario: dict[str, str]) -> str:
    """Sustituye en el texto las palabras que aparecen en el diccionario como claves por sus valores asociados.

    Parámetros:
        texto: Texto en el que se van a sustituir las palabras.
        diccionario: Diccionario con las palabras a sustituir como claves y las palabras sustitutas como valores.

    Devuelve:
        Texto resultante de las sustituciones.
    """
    palabras = texto.split()
    palabras_sustituidas = []
    for palabra in palabras:
        if palabra in diccionario: #estoy preguntando si palabra es una clave de diccionario
            palabras_sustituidas.append(diccionario[palabra])
        else:
            palabras_sustituidas.append(palabra)
    #otra opción, usando get y el segundo parámetro que indica
    # palabras_sustituidas.append(diccionario.get(palabra,palabra))
    return " ".join(palabras_sustituidas) #para que concatene con el espacio en los medios

def indexa_por_iniciales(texto: str) -> dict[str, set[str]]:
    """
    Construye un diccionario que indexa las distintas palabras del texto
    (pasado a minúsculas) por sus iniciales.
    
    Parámetros:
        texto: Texto del que se van a extraer las palabras.
    
    Devuelve:
        Diccionario que asocia a cada inicial el conjunto de palabras
         que comienzan por dicha inicial.
    
    """ #MUY IMPORTANTE SABER COMO SE USA
    res = {} # esto es un  DICCIONARIO no un conjunto
    for palabra in texto.lower().split():
        clave = palabra[0]
        if clave in res:
            res[clave].add(palabra)
        else:
            res[clave] = {palabra}
    return res


def construye_frecuencias_bigramas(texto: str) -> dict[str, float]:
    """
    Construye un diccionario con las frecuencias normalizadas de cada bigrama 
    en el texto dado, ignorando mayúsculas y minúsculas.

    Un bigrama es una secuencia de dos letras consecutivas en el texto.

    Cada frecuencia estará contenida entre 0 y 1.
    
    Parámetros:
        texto: Texto del que se van a contar los bigramas.
    Devuelve:
        Diccionario que asocia a cada bigrama su frecuencia normalizada en el texto.
    """
    '''
    conteo = {}
    texto = texto.lower()
    for i in range(len(texto) - 1): #para que el índice no se salga del rango del texto
        bigrama = texto[i] + texto[i + 1] #para concatenar el texto en bigramas
        if bigrama.isalpha():
            if bigrama in conteo:
                conteo[bigrama] += 1
            else:
                conteo[bigrama] = 1
        if not conteo:
            return {} # esto para cuando no haya ningun bigrama válido
        
    total_bigramas = sum(conteo.values())

    frecuencia = {}
    for clave, valor in conteo.items():
        frecuencia[clave] = valor/ total_bigramas

    return frecuencia
'''
#opción profesor, más eficiente
    bigramas = []
    texto = texto.lower()
    for c1, c2 in zip(texto, texto[1:]):
        if c1.isalpha() and c2.isalpha():
            bigramas.append(c1 + c2)
    contador = Counter(bigramas) #hacer este counter sin crear la lista bigramas. TO DO!
    total_bigramas = len(bigramas)
    res = {}
    for bigrama, conteo in contador.items():
        res[bigrama] = conteo / total_bigramas
    return res

    ''' USANDO DEFAULTDICT
    contador = defaultdict(int)
    for c1, c2 in zip (texto, texto[1:]):
        if c1.isalpha() and c2.isalpha():
            bigramas.append(c1 + c2)
    el resto igual
    '''

def calcula_distancia_media_frecuencias(freq1: dict[str, float], freq2: dict[str, float]) -> float:
    """
    Calcula la distancia media entre las frecuencias normalizadas
    representadas por dos diccionarios de frecuencias.

    Parámetros:
        freq1: Primer diccionario de frecuencias.
        freq2: Segundo diccionario de frecuencias.

    Devuelve:
        Distancia media entre los dos vectores de frecuencias, o 0.0 si ambos diccionarios están vacíos.
    """
    freq = set(freq1) | set(freq2) #uno ambos en un solo diccionario, sin perder las claves únicas

    if not len(freq): #para comprobar que el conjunto no esté vacío y evitar errores como ZeroDivision
        return 0.0
    
    res = 0.0

    for clave in freq: #get se usa para que me busque un elemento en un diccionario. Si no lo encuentra NO dará error
        valor1 = freq1.get(clave, 0.0) #para obtener el valor de cada clave
        valor2 = freq2.get(clave, 0.0) #para obtener el valor de cada clave
        res += abs(valor1 - valor2) 
    return res / len(freq)

''' VERSIÓN FERMÍN EN CLASE
    if len(freq1) == 0 and len(freq2) == 0:
        return 0.0
    todos_bigramas = set(freq1).unionset(freq2)
    suma_diferencias = 0
    for bigrama in todos_bigramas:
        suma_diferencias += abs(freq1.get(bigrama, 0)-freq2.get(bigrama, 0))
    return suma_diferencias / len(todos_bigramas)
'''

def identifica_idioma(textos_ejemplo: dict[str, str], texto_a_identificar: str) -> str:
    """
    Identifica el idioma de un texto comparando sus frecuencias de bigramas
    con las frecuencias de bigramas de textos de ejemplo en distintos idiomas.

    Parámetros:
        textos_ejemplo: Diccionario que asocia a cada idioma (por ejemplo 'es') un texto de ejemplo en ese idioma.
        texto_a_identificar: Texto cuyo idioma se quiere identificar.

    Devuelve:
        El idioma identificado del texto.
    """
    #PASOS SEGUIDOS
    #1. obtener el diccionario de frecuencias para _texto
    freq_nuevo_texto = construye_frecuencias_bigramas(texto_a_identificar)

    lista_contador = []

    for idioma, texto in textos_ejemplo.items():
        freq_ejemplo = construye_frecuencias_bigramas(texto)
        contador= calcula_distancia_media_frecuencias(freq_nuevo_texto, freq_ejemplo)
        lista_contador.append((contador, idioma))
    
    return min(lista_contador)[1]



