
# ------------------------------------------------------------
# RangeX
#
# Interprete del lenguaje RangeX
# Entrega 1, Analisis Lexicografico, README
# CI-3725
# (Abril-Julio 2013)
#
#
# Hecho por:
#	@author: Stefano De Colli	09-10203
#	@author: Karen Troiano		09-10855
#	
# ------------------------------------------------------------

Selección de tokens y palabras reservadas
	La herramienta PLY provee un analizador lexicográfico en el cual sólo es necesario
	agregar las palabras reservadas y los tokens, dichos tokens y palabras reservadas
	tienen expresiones regulares para poder ser identificadas, por ejemplo la expresión
	para identificar las variables es [a-zA-Z_][a-zA-Z0-9_]*, y está asociada con el
	token TkId, mientras que la palabra reservada <IF> tiene asociada la expresión
	if, que produce el token TkIf. Esto lo hace el analizador de manera automática, lo
	único que se definió fueron las expresiones regulares con las cuales el analizador
	trabajaría para reconocer el token.

* Impresión
	Para imprimir los tokens es necesario saber el valor, la línea y la columna, la
	herramienta PLY ya provee el valor del token y en que línea se encuentra, por ello 
	se implementó la función find_column encargada de contar caracteres que existian 
	entre el token debido y el principio de la línea, esta función calculará que un 
	tabulador en el código será de un ancho de 4 columnas.
	Luego de haber realizado esto, por cada token que no fuese un error, y hasta encontrar un
	error se iban guardando en una lista y si el analizador no encontraba ningún error
	entonces se imprimen los tokens con su fila y columna correspondiente. Si en el 
	caso de encontrarse un error, entonces dicha lista pierde sentido y se procedían a
	continuar el análisis lexifográfico en nueva búsqueda de errores hasta el final del
	archivo.
