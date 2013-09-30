Readme - RangeX

Interprete del lenguaje RangeX
Entrega 2, Analisis Sintactico con arbol sintactico abstracto.
CI-3725
(Abril-Julio 2013)


Hecho por:
	@author: Stefano De Colli	09-10203
	@author: Karen Troiano		09-10855


Implementacion
		Lo primero a realizarse fue la gramática (ver gramatica.txt),
	una vez definida, se procedió a construir el arbol sintáctico
	abstracto a travez de clases. Seguidamente, se les incluyó una
	función llamada toString a cada clase para así poder imprimir el
	árbol sintáctico que estabamos construyendo. El árbol como tal
	no existe dado que no se almacena información sobre los nodos
	ni de los caminos, sólo se van recorriendo la gramática y
	se imprimen las clases de manera ordenada (Lo que produce
	la estructura de arbol)


Problemas
	* Problemas con la impresión por el formato establecido.

Aclaratorias
	* Los else asocian a la derecha.
	* Las asociaciones se hacen a criterio de los programadores.
	* Si hay errores lexicográficos no continúa ni busca errores sintácticos.
	* Si hay un error sintáctico, sólo detecta uno y aborta la ejecución del
		programa.
	* Si no hay errores, imprime el árbol sintáctico abstracto.
