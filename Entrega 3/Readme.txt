Readme - RangeX

Interprete del lenguaje RangeX
Entrega 3, Tabla de símbolos y errores de tipos estáticos.
CI-3725
(Abril-Julio 2013)


Hecho por:
	@author: Stefano De Colli	09-10203
	@author: Karen Troiano		09-10855

Implementacion
	* Se implementó una TS usando el diccionario de Python
	y las funciones de la TS se centran en operaciones sobre
	dicho diccionario, adicionalmente cada TS tiene un apuntador
	a otra TS.
	* En el programa principal al momento de inciar el programa
	se tiene un apuntador global a la TS, y cada vez que se entra
	en un bloque, se crea una nueva TS con su padre a la TS global
	y luego se actualiza la TS global.
	* Al llegar al end de los bloques se actualiza la TS global al
	padre de la TS actual.


Problemas
	* Problemas con la impresión por el formato establecido,
	dado a la falta de ingenio.
	* Verificación de las variables usadas dentro de las
	iteraciones determinadas
	

Aclaratorias
	* TS es acrónimo de Tabla de símbolos.
	* Un bloque dentro de una iteracion implica rehacer la TS de
		símbolos por cada iteración
	* Las expresiones tienen precedencia, por ejemplo:
		** x = true + 4 or false
		** Se traduce "a (true + 4) or false" por la precedencia de
			"+" sobre el "or"
		** Da un error:
			*** Intento de utilizar el operador "Mas" con la expresion 
				"true" del tipo "bool" y una expresion "4" del tipo "int".
		** Pero no verifica el "or false", dado que no se sabe el tipo de 
			la expresion "true + 4"
	* Se tomó en consideración la aclaratoria de las 6:45pm del 24/06/2013 en las noticias 
		del curso.
	* La entrega será enviada antes de las 8:15pm, si hay más aclaratorias sin tiempo
		de prórroga, no consideraremos esos casos. 

Verficaciones extras:
	* Verifica todas las expresiones, sin importar la localidad
		de ellas o que tan anidados se encuentren.
		** Por ejemplo, en p4.rgx (caso de prueba dado por ustedes)
			se imprime adicionalmente:
			
			Error en línea 40, columna 40: el parametro de la funcion "rtoi" es
				del tipo "int" y debe ser del tipo "range".
			Error en línea 40, columna 51: el parametro de la funcion "length" es 
				del tipo "int" y debe ser del tipo "range".

		
