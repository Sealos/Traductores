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
	* Un bloque dentro de un if implica rehacer la TS de
	símbolos por cada iteración
	* TS es acrónimo de Tabla de símbolos.
