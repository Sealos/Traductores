
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

Selecci�n de tokens y palabras reservadas
	La herramienta PLY provee un analizador lexicogr�fico en el cual s�lo es necesario
	agregar las palabras reservadas y los tokens, dichos tokens y palabras reservadas
	tienen expresiones regulares para poder ser identificadas, por ejemplo la expresi�n
	para identificar las variables es [a-zA-Z_][a-zA-Z0-9_]*, y est� asociada con el
	token TkId, mientras que la palabra reservada <IF> tiene asociada la expresi�n
	if, que produce el token TkIf. Esto lo hace el analizador de manera autom�tica, lo
	�nico que se defini� fueron las expresiones regulares con las cuales el analizador
	trabajar�a para reconocer el token.

* Impresi�n
	Para imprimir los tokens es necesario saber el valor, la l�nea y la columna, la
	herramienta PLY ya provee el valor del token y en que l�nea se encuentra, por ello 
	se implement� la funci�n find_column encargada de contar caracteres que existian 
	entre el token debido y el principio de la l�nea, esta funci�n calcular� que un 
	tabulador en el c�digo ser� de un ancho de 4 columnas.
	Luego de haber realizado esto, por cada token que no fuese un error, y hasta encontrar un
	error se iban guardando en una lista y si el analizador no encontraba ning�n error
	entonces se imprimen los tokens con su fila y columna correspondiente. Si en el 
	caso de encontrarse un error, entonces dicha lista pierde sentido y se proced�an a
	continuar el an�lisis lexifogr�fico en nueva b�squeda de errores hasta el final del
	archivo.
