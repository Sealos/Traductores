#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# ------------------------------------------------------------
# RangeX
#
# Interprete del lenguaje RangeX
# Entrega 3, Tabla de simbolos con arbol sintactico abstracto.
# CI-3725
# (Abril-Julio 2013)
#
#
# Hecho por:
#	@author: Stefano De Colli	09-10203
#	@author: Karen Troiano		09-10855
#	
# ------------------------------------------------------------



import ply.lex as lex
import ply.yacc as yacc
import sys
from SymTable import *

global impresion 
impresion = '\n'
global Error
Error = False
global ErrorEst
ErrorEst = False
global TS
TS = None

#---------------------------------------------------#
#		PRIMERA ENTREGA								#
#---------------------------------------------------#

# Lista de palabras reservadas.

reserved = {
	# Bloques
	'program'	:	'TkProgram',
	'begin'		:	'TkBegin',
	'end'		:	'TkEnd',
	'declare'	:	'TkDeclare',
	'as'		:	'TkAs',

	# Secuenciadores
	'if'		:	'TkIf',
	'do' 		: 	'TkDo',
	'then'		:	'TkThen',
	'else'		:	'TkElse',
	'for'		:	'TkFor',
	'while'		:	'TkWhile',
	'in'		:	'TkIn',
	'case'		:	'TkCase',
	'of'		:	'TkOf',

	# I/O
	'read'		: 	'TkRead',
	'write'		:	'TkWrite',
	'writeln'	:	'TkWriteLn',

	# Funciones
	'rtoi'		:	'TkRtoi',
	'length'	:	'TkLength',
	'top'		:	'TkTop',
	'bottom'	:	'TkBottom',

	# Tipos
	'bool'	 	: 	'TkBool',
	'int'		:	'TkInt',
	'range'		:	'TkRange',
	
	 # Booleans
	'true'		:	'TkTrue',
	'false'		:	'TkFalse',
	'and'		:	'TkAnd',
	'or'		:	'TkOr',
	'not'		:	'TkNot'
}

# Lista de Tokens.
tokens = [
	# Simples
	'TkPuntoYComa',
	'TkParAbre',
	'TkParCierra',
	'TkSuma',
	'TkResta',
	'TkAsterisco',
	'TkInterseccion',
	'TkPertenece',
	'TkMenor',
	'TkMenorIgual',
	'TkMayor',
	'TkMayorIgual',
	'TkIgual',
	'TkDesIgual',
	'TkAsignacion',
	'TkFlechaCase',
	'TkComma',
	'TkConstruccion',
	'TkModulo',
	'TkDiv',

	# Funcionales
	'TkId',
	'TkComent',
	'TkString',
	'TkNum'
	] + list(reserved.values())

# Expresiones regulares para tokens simples.
t_TkPuntoYComa 		= r';'
t_TkParAbre			= r'\('
t_TkParCierra		= r'\)'
t_TkSuma			= r'\+'
t_TkResta 			= r'-'
t_TkAsterisco		= r'\*'
t_TkInterseccion	= r'<>'
t_TkPertenece		= r'>>'
t_TkMenor			= r'<'
t_TkMenorIgual 		= r'<='
t_TkMayor 			= r'>'
t_TkMayorIgual 		= r'>='
t_TkIgual			= r'=='
t_TkDesIgual		= r'/='
t_TkAsignacion 		= r'='
t_TkFlechaCase		= r'->'
t_TkComma			= r'\,'
t_TkConstruccion	= r'\.\.'
t_TkModulo			= r'%'
t_TkDiv				= r'/'

# Expresiones regulares para tokens complejos.
# (que requieren instrucciones adicionales)

def t_TkId(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	if t.value in reserved:
		t.type = reserved[t.value]
	return t

def t_ignore_TkComent(t):
	r'\/\/[^\n]*'

def t_TkString(t):
	r'"([^"\\]|\\"|\\\\|\\n|\\t|\\r|\\f|\\v)*"'
	t.value = (t.value)[1:-1]
	return t

def t_TkNum(t):
	r'\d+'
	t.value = int(t.value)
	if (t.value > 2147483647 or t.value < -2147483648):
		t_error(t)
	return t

# Se calcula la columna en la que comienza la palabra que
# contiene el error.
# lineno - Numero de linea actual.
# lexpos - Posicion actual en el archivo de entrada.

def find_column(input, token):
	i = token.lexpos
	j = 0
	k = 0  
	while i > 0:
		if input[i] == '\n':			break
		if input[i] == '\t': 
			k += 1
		i -=1
	if (token.lineno == 1):
		k += 0
		j = 0
	else:
		j = 1
	column = ((((token.lexpos - i) + (k*4)) - k) - j) + 1
	return column

	
def find_column_parser(input, num, linea):
	i = num
	j = 0
	k = 0  
	while i > 0:
		if input[i] == '\n':			break
		if input[i] == '\t': 
			k += 1
		i -=1
	if (linea == 1):
		k += 0
		j = 0
	else:
		j = 1
	column = ((((num - i) + (k*4)) - k) - j) + 1
	return column
	
	
# Aqui se toman en cuenta los caracteres en blanco.
# (espacios, tab)
t_ignore = ' \t'

# Se utiliza para que la linea en la que se encuentra
# el lexer leyendo vaya aumentando cada vez que encuentra
# un '\n'.
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# Se define accion a tomar cuando ocurre un error.
def t_error(t):
	global Error
	Error = True
	if (t.type == 'TkNum'):
		#print "hola"
		print "Entero fuera de rango 32b \"%d\"en linea %s, columna %s."%(t.value, t.lineno, find_column(text, t))
	else:
		#print "hola1"
		print "Error: caracter inesperado \"%s\"en linea %s, columna %s."%(t.value[0], t.lineno, find_column(text, t))
	t.lexer.skip(1)
	return t


#-------------------------------------------------------#
#			FIN DE PRIMERA ENTREGA						#
#-------------------------------------------------------#

#-----------------------#
#	Clases				#
#-----------------------#

class Declaracion:
	def __init__(self, variables ,tipo ,linea, columna):
		self.variables = variables
		self.tipo = tipo
		self.linea = linea
		self.columna = columna

	def getVariables(self):
		return self.variables

	def getLinea(self):
		return self.linea
	
	def getTipo(self,flag = False):
		return self.tipo
	
	def getColumna(self):
		return self.columna

class Asignacion:
	def __init__(self, var, val):
		self.var = var
		self.val = val

	def toString(self, tab, booleano):
		tab = tab + "\t"
		palabra = "ASIGNACION\n"
		palabra += tab + "var: " + str(self.var.toString(tab, True, False)) + "\n"
		palabra += tab + "val: " + str(self.val.toString(tab, False))
		return palabra

	def verificar(self):
		global TS
		global ErrorEst
		a = TS.find(self.var.getVariable(), False)
		if (a != None):
			if (a.getReservado()):
				ErrorEst = True
				print("Error en la linea %s, columna %s: se intenta modificar la variable \"%s\" la cual pertenece a una iteracion." %(self.var.getLinea() , self.var.getColumna(), self.var.getVariable()))
			else: 
				if (self.val.getTipo() != "TypeError" and self.var.getTipo() != self.val.getTipo()): 
					ErrorEst = True
					print("Error en la linea %s, columna %s: intento de asignar a la variable \"%s\" de tipo \"%s\" una expresion del tipo \"%s\"." %(self.var.getLinea() , self.var.getColumna(), self.var.getVariable(), TS.find(self.var.getVariable(), False).getTipo(), self.val.getTipo()))
		else:
			ErrorEst = True
			print("Error en linea %s, columna %s: no puede usar la variable \"%s\" pues no ha sido declarada." %(self.var.getLinea() , self.var.getColumna(), self.var.getVariable()))
			
		self.val.verificar()

class Condicional:
	def __init__(self, guardia, then, elsse):
		self.guardia = guardia
		self.then = then
		self.elsse = elsse
		
	def toString(self, tab, booleano):
		tab = tab + "\t"
		palabra = "CONDICIONAL\n"
		palabra += tab + "condicion: " + self.guardia.toString(tab, False) + "\n"
		palabra += tab + "verdadero: " + self.then.toString(tab, False)
		if (self.elsse != 'vacio'):
			palabra += "\n"+ tab + "falso: " +  self.elsse.toString(tab, False)
		return palabra

	def verificar(self):
		self.then.verificar()
		if (self.elsse != "vacio"):
			self.elsse.verificar()

		if (self.guardia.getTipo() != "TypeError" and self.guardia.getTipo() != "bool"):
			global ErrorEst
			ErrorEst = True
			print("Error en la linea %s, columna %s: la condicion no es del tipo \"bool\"." %(self.guardia.getLinea() , self.guardia.getColumna()))

class Case:
	def __init__(self, exp, casos):
		self.exp = exp
		self.casos = casos

	def toString(self, tab, booleano):
		palabra = "CASE\n"
		if (type(self.exp) is str):
			palabra += tab + "exp: "  + self.exp
		else:
			palabra += tab + "exp: " + self.exp.toString(tab, False) + "\n"
		palabra += tab + "caso: \n" + tab + self.casos.toString(tab, False) 
		return palabra

	def verificar(self):
		self.exp.verificar()

		if (self.exp.getTipo() != "TypeError" and self.exp.getTipo() != "int"):
			global ErrorEst
			ErrorEst = True
			print("Error en la linea %s, columna %s: la condicion no es del tipo \"int\"." %(self.exp.getLinea() , self.exp.getColumna()))

		self.casos.verificar()

class CaseCond:
	def __init__(self, rango, instruccion, casos):
		self.rango = rango
		self.instruccion = instruccion
		self.casos = casos

	def toString(self, tab, booleano):
		palabra = "\t" + "ran: " + self.rango.toString(tab + "\t", False) + "\n"
		palabra += tab + "\t" +  "ins: " + self.instruccion.toString(tab + "\t", False) + "\n"
		if (self.casos != 'vacio'):
			palabra += tab + "caso: \n" + tab + self.casos.toString(tab, False)
		return palabra

	def verificar(self):
		self.rango.verificar()

		if (self.rango.getTipo() == "TypeError" and self.rango.getTipo() != "range"):
			global ErrorEst
			ErrorEst = True
			print("Error en la linea %s, columna %s: la condicion no es del tipo \"range\"." %(self.rango.getLinea() , self.rango.getColumna()))

		self.instruccion.verificar()
		if (self.casos != "vacio"):
			self.casos.verificar()

class RepeticionDet:
	def __init__(self, variable, rango, instruccion):
		self.variable = variable
		self.rango = rango
		self.instruccion = instruccion

	def toString(self, tab, booleano):
		tab = tab + "\t"
		palabra = "ITERACION_DET\n"
		palabra += tab + "variable: " + self.variable.toString(tab, True, False) + "\n"
		palabra += tab + "rango: "  + self.rango.toString(tab, False) + "\n"
		palabra += tab + "instruccion: " + self.instruccion.toString(tab, False)
		return palabra

	def verificar(self):
		global ErrorEst
		global TS
		TS = SymTable(TS, False)
		if (self.variable.getTipo(True) == "variable" or self.variable.getTipo() == "TypeError"):
			if not(TS.insert(self.variable.getVariable(), "int", True)):
				ErrorEst = True
				x = self.variable
				print("Error en linea %s, columna %s: la variable '%s' ya ha sido declarada." %(x.getLinea() , x.getColumna(), x.getVariable()))
		if (self.rango.getTipo() != "TypeError" and self.rango.getTipo() != "range"):
			ErrorEst = True
			print("Error en la linea %s, columna %s: el rango no es del tipo \"range\"." %(self.rango.getLinea() , self.rango.getColumna()))
		self.instruccion.verificar()
		TS = TS.getPadre()

class RepeticionIndet:
	def __init__(self, guardia, instruccion):
		self.guardia = guardia
		self.instruccion = instruccion

	def toString(self, tab, booleano):
		tab = tab + "\t"
		palabra = "ITERACION_INDET\n"
		palabra += tab + "condicion: "  + self.guardia.toString(tab, False) + "\n"
		palabra += tab + "instruccion: "  + self.instruccion.toString(tab, False)
		return palabra

	def verificar(self):
		if (self.guardia.getTipo() != "TypeError"):
			if (self.guardia.getTipo() != "bool"):
				global ErrorEst
				ErrorEst = True
				print("Error en la linea %s, columna %s: la condicion no es del tipo \"bool\"." %(self.guardia.getLinea() , self.guardia.getColumna()))

		self.instruccion.verificar()

class Bloque:
	def __init__(self, declaraciones, instrucciones, end):
		self.declaraciones = declaraciones
		self.instrucciones = instrucciones
		self.end = end

	def toString(self, tab, booleano):
		palabra = "BLOQUE\n"
		tab = tab + "\t"
		if (not (self.declaraciones == 'vacio')):
			palabra += tab + "TABLA DE SIMBOLOS\n"
			for x in self.declaraciones.getLista():
				for y in x.getVariables():
					palabra += tab + "variable: " + y + " | tipo: " + x.getTipo() + "\n"
			palabra += "\n"
				
		palabra += tab + self.instrucciones.toString(tab, False) + "\n"
		return palabra

	def verificar(self):
		global TS
		TS = SymTable(TS)
		if (not (self.declaraciones == 'vacio')):
			for x in self.declaraciones.getLista():
				for y in x.getVariables():
					if (not (TS.insert(y, x.getTipo()))):
						global ErrorEst
						ErrorEst = True
						print("Error en linea %s, columna %s: la variable '%s' ya ha sido declarada." %(x.getLinea() , x.getColumna(), y))

		self.instrucciones.verificar()
		self.end.verificar()

class End:
	def __init__(self):
		self.basura = 0

	def verificar(self):
		global TS
		if (not (TS == None)):
			TS = TS.getPadre()
		else:
			TS = None

class Simple:
	def __init__(self, tipo, valor, linea = 0, columna = 0):
		self.tipo = tipo
		self.valor = valor
		self.linea = linea
		self.columna = columna
		
	def getColumna(self):
		return self.columna
		
	def getLinea(self):
		return self.linea
		
	def getVariable(self):
		return self.valor

	def Conjunto(self):
		ls = []
		ls.append(self.valor)
		return ls

	def toString(self, tab, booleano, bool2 = True):
		tab = tab + "\t"
		if (self.tipo == 'VARIABLE' or self.tipo == 'CADENA'):
			if (booleano == True and bool2 == True):
				palabra = "elemento: " + str(self.tipo) + "\n"
				if (self.tipo == 'VARIABLE'):
					palabra += tab + "nombre: " + str(self.valor)
				else:
					cadena = str(self.valor)
					cadena = cadena.replace("\\n", " ")
					cadena = cadena.replace("\\t", "	")
					cadena = cadena.replace("\\", "")
					palabra += tab + "valor: " + cadena
			elif (booleano == True and bool2 == False):
				palabra = str(self.valor)
			elif (self.tipo == 'VARIABLE'):
				palabra = str(self.tipo) + "\n"
				palabra += tab + "nombre: " + str(self.valor)
			elif (self.tipo == 'CADENA'):
				palabra = str(self.tipo) + "\n"
				cadena = str(self.valor)
				cadena = cadena.replace("\\n", " ")
				cadena = cadena.replace("\\t", "	")
				cadena = cadena.replace("\\", "")
				palabra += tab + "valor: " + cadena 
		else:
			if (booleano == True):
				palabra = "elemento: " + str(self.tipo) + "\n"
			else:
				palabra = str(self.tipo) + "\n"
			palabra += tab + "valor: " + str(self.valor)
		return palabra

	def getTipo(self, flag = False):
		if (self.tipo == "CONSTANTE_ENT"):
			return "int"
		elif (self.tipo == "VARIABLE"):
			global TS
			if (TS.find(self.valor, False) == None):
				return "TypeError" # No encontrado
			else:
				if (not flag):
					return TS.find(self.valor, False).getTipo()
				else:
					return "variable"
		elif(self.tipo == "BOOLEANO"):
			return "bool"
		else:
			return "string"

	def verificar(self):
		global TS
		if (self.tipo == "VARIABLE"):
			if (TS.find(self.valor, False) == None):
				global ErrorEst
				ErrorEst = True
				print("Error en línea %s, columna %s: no puede usar la variable \"%s\" pues no ha sido declara." %(self.linea, self.columna, self.valor))

	def getExpresion(self):
		#print("hola3")
		return str(self.valor)

class Secuenciacion:
	def __init__(self, instruccion1, instruccion2):
		self.instruccion1 = instruccion1
		self.instruccion2 = instruccion2

	def toString(self, tab, booleano):
		palabra = self.instruccion1.toString(tab, False) + "\n"
		palabra += tab + "SEPARADOR\n"
		palabra += tab + self.instruccion2.toString(tab, False)
		return palabra

	def verificar(self):
		self.instruccion1.verificar()
		self.instruccion2.verificar()

class LineaDeclaracion:
	def __init__(self, variable, tipo, declaraciones, linea, columna):
		self.declaraciones = []
		self.linea = linea
		self.columna = columna
		self.declaraciones.append(Declaracion(variable.Conjunto(), tipo, self.linea, self.columna))
		if (not declaraciones == "vacio"):
			self.declaraciones = declaraciones.getLista() + self.declaraciones

	def getLinea(self):
		return self.linea

	def getColumna(self):
		return self.columna

	def getLista(self):
		return self.declaraciones

class Variables:
	def __init__(self, variable1, variable2, linea, columna):
		self.variable1 = variable1.Conjunto()
		self.variable2 = variable2.Conjunto()
		self.linea = linea
		self.columna = columna
		
	def getLinea(self):
		return self.linea
		
	def getColumna(self):
		return self.linea
		
	def Conjunto(self):
		return self.variable1 + self.variable2

def gets(list_or_iterator):
	return "[" + ", ".join( str(x) for x in list_or_iterator) + "]"

class IO:
	def __init__(self, nombre, expresion):
		self.nombre = nombre
		self.expresion = expresion
	
	def toString(self, tab, booleano):
		palabra = self.nombre + "\n"
		if (self.nombre == 'READ'):
			palabra += tab + "\t" + "variable: " + self.expresion.toString(tab, True, False)
		else:
			tab = tab + "\t"
			palabra += tab + self.expresion.toString(tab, True)
		return palabra

	def verificar(self):
		if (self.nombre == 'READ'):
			global TS
			a = TS.find(self.expresion.getVariable(), False)
			if (a != None):
				print str(a.getReservado())
				if (a.getReservado()):
					global ErrorEst
					ErrorEst = True
					print("Error en la linea %s, columna %s: se intenta modificar la variable \"%s\" la cual pertenece a una iteracion." %(self.expresion.getLinea() , self.expresion.getColumna(), self.expresion.getVariable()))
		self.expresion.verificar()

class Impresion:
	def __init__(self, expresion1, expresion2):
		self.expresion1 = expresion1
		self.expresion2 = expresion2
		
	def toString(self, tab, booleano):
		palabra = self.expresion1.toString(tab, True) + "\n"
		palabra += tab + "elemento: " + self.expresion2.toString(tab, False)
		return palabra

	def verificar(self, reserved = None):
		self.expresion1.verificar()
		self.expresion2.verificar()

class Funcion:
	def __init__(self, valor, expresion, linea, columna):
		self.valor = valor
		self.expresion = expresion
		self.linea = linea
		self.columna = columna
		self.tipo = None

	def getLinea(self):
		return self.linea

	def getColumna(self):
		return self.columna

	def toString(self, tab, booleano):
		if (booleano == True):
			palabra = "elemento: "
		else:
			palabra = ""
		palabra += "FUNCION_EMB\n"
		tab = tab + "\t"
		palabra += tab + "nombre: " + str(self.valor) + "\n"
		palabra += tab + "argumento: " + self.expresion.toString(tab, False)
		return palabra

	def getTipo(self, flag = False):
		if (self.expresion.getTipo != "TypeError"):
			return "int"
		else:
			return "TypeError"

	def verificar(self):
		self.expresion.verificar()
		global ErrorEst
		if (self.expresion.getTipo() != "TypeError"):
			if (self.expresion.getTipo() != "range"):
				ErrorEst = True
				print("Error en línea %s, columna %s: el parametro de la funcion \"%s\" es del tipo \"%s\" y debe ser del tipo \"range\"." %(self.expresion.getLinea(), self.expresion.getColumna(), self.valor, self.expresion.getTipo()))

class ExpresionUnaria:
	def __init__(self, tipo, operador, operando, linea, columna, simbolo):
		self.tipo = tipo
		self.operador = operador
		self.operando = operando
		self.linea = linea
		self.columna = columna
		self.simbolo = simbolo

	def getLinea(self):
		return self.linea
	
	def getColumna(self):
		return self.columna
		
	def toString(self, tab, booleano):
		if (booleano == True):
			palabra = "elemento: "
		else:
			palabra = "EXPRESION_UN\n"
		tab = tab + "\t"
		if (type(self.operador) is str):
			palabra += tab + "operador: "+ str(self.tipo) + "\n"
		else:
			palabra += tab + "operador: "  + self.operador.toString(tab, False) + "\n"
		palabra += tab + "operando:  "  + self.operando.toString(tab, False)
		return palabra

	def getTipo(self, flag = False):
		# Tenemos un error interno, entonces el tipo de la expresion sigue tienendo errores
		if (self.operando.getTipo() == "TypeError"):
			return "TypeError"

		# El operador es el TkNot, la expresion tiene que ser bool
		if (self.tipo == "NEGACION" and self.operando.getTipo() == "bool"):
			return "bool"

		# El operador es un + o -, la expresion tiene que ser int
		if ((self.tipo == "MAS_UNARIO" or self.tipo == "MENOS_UNARIO")
			and self.operando.getTipo() == "int"):
			return "int"

		# No encontramos nada... Devolvemos TypeError
		return "TypeError"

	def verificar(self):
		self.operando.verificar()
		a = self.operando

		if (self.getTipo() == "TypeError" and a.getTipo() != "TypeError"):
			global ErrorEst
			ErrorEst = True
			impr = "Error en línea " + str(self.linea) + ", columna " + str(self.columna) + ": Intento de uso del operador unario \"" + str(self.operador) + "\" con la "
			if (a.getTipo(True) == "variable"):
				impr = impr + "variable \"" + str(a.getVariable()) + "\""
			else:
				impr = impr + "expresion \"" + str(a.getExpresion()) + "\""

			impr = impr + " del tipo \"" + str(a.getTipo()) + "\"."
			print(impr)

	def getExpresion(self):
		#print("hola1")
		return self.simbolo + " " + self.operando.getExpresion()

class ExprBinaria:
	def __init__(self, operacion, tipo, operando1, operando2, relacional, linea, columna, simbolo):
		self.operacion = operacion
		self.tipo = tipo
		self.operando1 = operando1
		self.operando2 = operando2
		self.relacional = relacional
		self.linea = linea
		self.columna = columna
		self.simbolo = simbolo

		self.opBool = set(['And', 'Or'])
		self.opInt = set(['Construccion','Modulo', 'Div', 'Resta', 'Igual que', 'No igual a', 'Menor que', 'Menor Igual que', 'Mayor que', 'Mayor Igual que'])
		self.opRango = set(['Interseccion'])

		self.devuelveBool = set(['Igual que', 'No igual a', 'Menor que', 'Menor Igual que', 'Mayor que', 'Mayor Igual que'])
		self.devuelveInt = set(['Modulo', 'Div', 'Resta', 'Mas', 'Por'])

	def getLinea(self):
		return self.linea
	
	def getColumna(self):
		return self.columna

	def toString(self, tab, booleano):
		if (booleano == True):
			palabra = "elemento: "
		else:
			palabra = ""
		tab = tab + "\t"
		palabra += "EXPRESION_BIN\n"
		palabra += tab + "operador: " + str(self.operacion) + "\n"
		if ( type(self.operando1) is str):
			palabra += tab + "operando izq: " + self.expresion
		else:
			palabra += tab + "operando izq: " + self.operando1.toString(tab, False) + "\n"
		if (type(self.operando2) is str):
			palabra += tab + "operando der: " + self.expresion
		else:
			palabra += tab + "operando der: " + self.operando2.toString(tab, False)
		return palabra

	def getTipo(self, flag = False):
		#print "Intentando comparar un operador de tipo " + str(self.operando1.getTipo()) + " operando 2 con" + str(self.operando2.getTipo()) + "OPERADOR " + str(self.operacion)
		# Tenemos un error interno, entonces el tipo de la expresion sigue tienendo errores
		if (self.operando1.getTipo() == "TypeError" or self.operando1.getTipo() == "TypeError"):
			return "TypeError"

		# No tenemos errores, verificamos los tipos
		# El operador es un operador que devuelve booleanos
		if (self.operacion == "Or" or self.operacion == "And"
			and (self.operando1.getTipo() == "bool" and self.operando2.getTipo() == "bool")):
			return "bool"

		if (self.operacion in self.devuelveBool
			and (self.operando1.getTipo() == "int"  and self.operando2.getTipo() == "int")):
			return "bool"

		if (self.operacion == 'Pertenece'
			and (self.operando1.getTipo() == "int" and self.operando2.getTipo() == "range")):
			return "bool"

		# El operador devuelve int
		if (self.operacion in self.devuelveInt
			and (self.operando1.getTipo() == "int" and self.operando2.getTipo() == "int")):
			return "int"

		# El operador devuelve range
		if (self.operacion == 'Construccion'
			and (self.operando1.getTipo() == "int" and self.operando2.getTipo() == "int")):
				return "range"

		if (self.operacion == 'Interseccion' or self.operacion == 'Mas'
			and (self.operando1.getTipo() == "range" and self.operando2.getTipo() == "range")):
			return "range"

		if (self.operacion == 'Por'
			and (self.operando1.getTipo() == "range" and self.operando2.getTipo() == "int")):
			return "range"

		# No encontramos nada... Devolvemos TypeError
		return "TypeError"

	def verificar(self):
		self.operando1.verificar()
		self.operando2.verificar()
		a = self.operando1
		b = self.operando2
		if (self.getTipo() == "TypeError" and a.getTipo() != "TypeError" and b.getTipo() != "TypeError"):
			global ErrorEst
			ErrorEst = True
			impr = "Error en línea " + str(self.linea) + ", columna " + str(self.columna) + ": Intento de utilizar el operador \"" + str(self.operacion) + "\" con la "
			if (a.getTipo(True) == "variable"):
				impr = impr + "variable \"" + str(a.getVariable()) + "\""
			else:
				impr = impr + "expresion \"" + str(a.getExpresion()) + "\""

			impr = impr + " del tipo \"" + a.getTipo() + "\" y una "

			if (b.getTipo(True) == "variable"):
				impr = impr + "variable \"" + str(b.getVariable()) + "\""
			else:
				impr = impr + "expresion \"" + str(b.getExpresion()) + "\""

			impr = impr + " del tipo \"" + str(b.getTipo()) + "\"."
			print(impr)

	def getExpresion(self):
		#print("hola2")
		return str(self.operando1.getExpresion()) + " " + str(self.simbolo) + " " + str(self.operando2.getExpresion())


#---------------------------#
#	Fin de clases			#
#---------------------------#

#-------------------#
# Precedencia		#
#-------------------#

#Se define la precedencia de los operadores.

precedence = (
	#('left','Impresion'),
	('nonassoc','Then'),
	('nonassoc', 'Else'),
	# Expresiones logicos.
	('left','TkOr'),
	('left','TkAnd'),
	('right', 'TkNot'),
	# De menor a mayor
	('nonassoc', 'TkPertenece'),
	# Operadores relacionales.
	('nonassoc' ,'TkIgual','TkDesIgual'),
	('nonassoc', 'TkMayor', 'TkMayorIgual', 'TkMenor', 'TkMenorIgual'),
	# Expresiones aritmeticas.
	('left','TkInterseccion'),
	('left', 'TkSuma', 'TkResta'),
	('left', 'TkAsterisco','TkDiv','TkModulo'),
	('left', 'TkConstruccion'),
	('right','RestaU', 'SumaU')
)

#------------------#
# Fin Precedencia  #
#------------------#

#---------------------------------------------------#
#	Producciones de la gramática					#
#---------------------------------------------------#

def p_PROGRAMA(p):
	"""
	PROGRAMA : TkProgram INSTRUCCION
	"""
	p[0] = p[2]
	if (not (Error)):
		global TS
		TS = SymTable(None)
		p[0].verificar()
		if (not (ErrorEst)):
			global impresion
			impresion += p[0].toString('', False)
			print impresion

def p_INSTRUCCION(p):
	"""
	INSTRUCCION : ASIGNACION
		| CONDICIONAL
		| CASE
		| REPETICION_DET
		| REPETICION_INDET
		| BLOQUE
		| INPUT
		| OUTPUT
	"""
	p[0] = p[1]

def p_ASIGNACION(p):
	"""
	ASIGNACION : VARIABLE TkAsignacion EXPRESION
	"""
	p[0] = Asignacion(p[1], p[3])

def p_CONDICIONAL(p):
	"""
	CONDICIONAL : TkIf EXPRESION TkThen INSTRUCCION ELSE 
	"""
	p[0] = Condicional(p[2], p[4], p[5])

def p_ELSE(p):
	"""
	ELSE : TkElse INSTRUCCION %prec Else
		| %prec Then
	"""
	if (len(p) > 1): p[0] = p[2]
	else: p[0] = "vacio"

def p_CASE(p):
	"""
	CASE : TkCase EXPRESION TkOf CASECOND TkEnd
	"""
	p[0] = Case(p[2], p[4])

def p_CASECOND(p):
	"""
	CASECOND : EXPRESION TkFlechaCase INSTRUCCION TkPuntoYComa CASECONDDOS
	"""
	p[0] = CaseCond(p[1], p[3], p[5])

def p_CASECONDDOS(p):
	"""
	CASECONDDOS : EXPRESION TkFlechaCase INSTRUCCION TkPuntoYComa CASECONDDOS
		| 
	"""
	if (len(p) > 1):
		p[0] = CaseCond(p[1], p[3], p[5])
	else:
		p[0] = "vacio"

def p_REPETICION_DET(p):
	"""
	REPETICION_DET : TkFor VARIABLE TkIn EXPRESION TkDo INSTRUCCION
	"""
	p[0] = RepeticionDet(p[2], p[4], p[6])

def p_REPETICION_INDET(p):
	"""
	REPETICION_INDET : TkWhile EXPRESION TkDo INSTRUCCION
	"""
	p[0] = RepeticionIndet(p[2], p[4])

def p_BLOQUE(p):
	"""
	BLOQUE : TkBegin DECLARE SECUENCIACION END
	"""
	p[0] = Bloque(p[2], p[3], p[4])

def p_END(p):
	"""
	END : TkEnd
	"""
	p[0] = End()
	
def p_DECLARE(p):
	"""
	DECLARE : TkDeclare LINEADECLARACION
		| 
	"""
	if (len(p) > 1):
		p[0] = p[2]
	else: 
		p[0] = "vacio"

def p_SECUENCIACION(p):
	"""
	SECUENCIACION : SECUENCIACION TkPuntoYComa INSTRUCCION
		| INSTRUCCION 
	"""
	if (len(p) <= 2): p[0] = p[1]
	else: p[0] = Secuenciacion(p[1], p[3])
	

def p_LINEADECLARACION(p):
	"""
	LINEADECLARACION : LINEADECLARACION TkPuntoYComa VARIABLES TkAs TYPE
		| VARIABLES TkAs TYPE
	"""
	if (len(p) <= 4):
		k = p.lineno(2)
		s = p.lexpos(2)
		p[0] = LineaDeclaracion(p[1], p[3], 'vacio', k, find_column_parser(text, s, k) - 2)
	else:
		k = p.lineno(4)
		s = p.lexpos(4)
		p[0] = LineaDeclaracion(p[3], p[5], p[1], k, find_column_parser(text, s, k) - 2)

def p_TYPE(p):
	"""
	TYPE : TkInt
		| TkBool
		| TkRange
	"""
	p[0] = p[1]

def p_VARIABLES(p):
	"""
	VARIABLES : VARIABLES TkComma VARIABLE
		| VARIABLE
	"""
	if (len(p) <= 2):
		p[0] = p[1]
	else:
		k = p.lineno(2)
		s = p.lexpos(2)
		p[0] = Variables(p[1], p[3], k, find_column_parser(text, s, k))

def p_INPUT(p):
	"""
	INPUT : TkRead VARIABLE
	"""
	p[0] = IO('READ', p[2])

def p_OUTPUT(p):
	"""
	OUTPUT : TkWrite IMPRESION
		| TkWriteLn IMPRESION
	"""
	if (p[1] == 'write'): p[0] = IO('WRITE', p[2])
	else: p[0] = IO('WRITELN', p[2]) 

def p_IMPRESION(p):
	"""
	IMPRESION : IMPRESION TkComma STRINEXP
		| STRINEXP
	"""
	if (len(p) > 2): p[0] = Impresion(p[1], p[3])
	else: p[0] = p[1]
	
def p_STRINEXP(p):
	"""
	STRINEXP : TkString
		| EXPRESION
	"""
	if (type(p[1]) is str): 
		p[0] = Simple('CADENA', p[1])
	else: 
		p[0] = p[1]

def p_EXPRESION(p):
	"""
	EXPRESION : EXPRBOOL
		| EXPREARITME
		| VARIABLE
		| EXPRANGO
		| TkParAbre EXPRESION TkParCierra
		| FUNCION
	"""
	if (len(p) > 2): p[0] = p[2]
	else: p[0] = p[1]

def p_FUNCION(p):
	"""
	FUNCION : FUNCIONES TkParAbre EXPRESION TkParCierra
	"""
	p[0] = Funcion(p[1], p[3],p.lineno(2),find_column_parser(text,p.lexpos(2) ,p.lineno(2)))

def p_FUNCIONES(p):
	"""
	FUNCIONES : TkBottom
		| TkRtoi
		| TkLength
		| TkTop
	"""
	p[0] = p[1]

def p_EXPRANGO(p):
	"""
	EXPRANGO : EXPRESION TkConstruccion EXPRESION
		| EXPRESION TkInterseccion EXPRESION
		| EXPRESION TkPertenece EXPRESION
	"""
	k = p.lineno(2)
	s = find_column_parser(text, p.lexpos(2), k) - 2
	if (p[2] == '..'): p[0] = ExprBinaria('Construccion', 'range', p[1], p[3], False, k, s, p[2])
	elif (p[2] == '<>'):  p[0] = ExprBinaria('Interseccion','range', p[1], p[3], False, k, s, p[2])
	elif (p[2] == '>>'):  p[0] = ExprBinaria('Pertenece','range', p[1], p[3], False, k, s, p[2])

def p_VARIABLE(p):
	"""
	VARIABLE : TkId
	"""
	k= p.lineno(1)
	s= p.lexpos(1)
	p[0] = Simple('VARIABLE', p[1], k, find_column_parser(text, s, k))


def p_NUMERO(p):
	"""
	NUMERO : TkNum
	"""
	k= p.lineno(1)
	s= p.lexpos(1)
	p[0] = Simple('CONSTANTE_ENT', p[1], k, find_column_parser(text, s, k))

def p_EXPRELACIONAL(p):
	"""
	EXPRELACIONAL : EXPRESION TkIgual EXPRESION
		| EXPRESION TkDesIgual EXPRESION
		| EXPRESION TkMenor EXPRESION
		| EXPRESION TkMenorIgual EXPRESION
		| EXPRESION TkMayor EXPRESION
		| EXPRESION TkMayorIgual EXPRESION
	"""
	k = p.lineno(2)
	s = find_column_parser(text, p.lexpos(2), k) - 2
	if (p[2] == '=='): p[0] = ExprBinaria('Igual que', 'boolean', p[1], p[3], True, k, s, p[2])
	elif (p[2] == '/='): p[0] = ExprBinaria('No igual a', 'boolean', p[1], p[3], True, k, s, p[2])
	elif (p[2] == '<'): p[0] = ExprBinaria('Menor que', 'boolean', p[1], p[3], True, k, s, p[2])
	elif (p[2] == '<='): p[0] = ExprBinaria('Menor Igual que', 'boolean', p[1], p[3], True, k, s, p[2])
	elif (p[2] == '>'): p[0] = ExprBinaria('Mayor que', 'boolean', p[1], p[3], True, k, s, p[2])
	elif (p[2] == '>='): p[0] = ExprBinaria('Mayor Igual que', 'boolean', p[1], p[3], True, k, s, p[2])

def p_EXPREARITME(p):
	"""
	EXPREARITME : BINEXPRARITM
		| UNEXPRARITME
		| NUMERO
	"""
	p[0] = p[1]

def p_BINEXPRARITM(p):
	"""
	BINEXPRARITM : EXPRESION TkSuma EXPRESION
		| EXPRESION TkResta EXPRESION
		| EXPRESION TkAsterisco EXPRESION
		| EXPRESION TkDiv EXPRESION
		| EXPRESION TkModulo EXPRESION
	"""
	k = p.lineno(2)
	s = find_column_parser(text, p.lexpos(2), k)
	if (p[2] == '+'): p[0] = ExprBinaria('Mas', 'integer', p[1], p[3], False, k, s, p[2])
	elif (p[2] == '-'): p[0] = ExprBinaria('Resta', 'integer', p[1], p[3], False, k, s, p[2])
	elif (p[2] == '*'): p[0] = ExprBinaria('Por', 'integer', p[1], p[3], False, k, s, p[2])
	elif (p[2] == '/'): p[0] = ExprBinaria('Div', 'integer', p[1], p[3], False, k, s, p[2])
	elif (p[2] == '%'): p[0] = ExprBinaria('Modulo', 'integer', p[1], p[3], False, k, s, p[2])

def p_UNEXPRARITME(p):
	"""
	UNEXPRARITME : TkResta EXPRESION %prec RestaU
		| TkSuma EXPRESION %prec SumaU
	"""
	k = p.lineno(1)
	s = find_column_parser(text, p.lexpos(1), k) + 1
	if (p[1] == '-'):
		p[0] = ExpresionUnaria('MENOS_UNARIO', p[1], p[2], k, s, p[1])
	else: 
		p[0] = ExpresionUnaria('MAS_UNARIO', p[1], p[2], k, s, p[1])
	
def p_EXPRBOOL(p):
	"""
	EXPRBOOL : EXPRBINBOOL
		| BOOL
		| EXPRELACIONAL
		| UNEXPRBOOL
	"""
	p[0] = p[1]

def p_EXPRBINBOOL(p):
	"""
	EXPRBINBOOL : EXPRESION TkOr EXPRESION
		| EXPRESION TkAnd EXPRESION
	"""
	k = p.lineno(2)
	s = find_column_parser(text, p.lexpos(2), k)
	if (p[2] == "or"): p[0] = ExprBinaria('Or', 'boolean', p[1], p[3], False, k, s, p[2])
	else: p[0] = ExprBinaria('And', 'boolean', p[1], p[3], False, k, s, p[2])

def p_UNEXPRBOOL(p):
	"""
	UNEXPRBOOL : TkNot EXPRESION
	"""
	k = p.lineno(1)
	s = find_column_parser(text, p.lexpos(1), k)
	p[0] = ExpresionUnaria('NEGACION', p[1], p[2], k, s, p[1])

def p_BOOL(p):
	"""
	BOOL : TkTrue
		| TkFalse
	"""
	k = p.lineno(1)
	s = find_column_parser(text, p.lexpos(1), k)
	p[0] = Simple('BOOLEANO', p[1], k, s)

def p_error(p):
	global Error
	if (Error != True and p != None):
		Error = True
		sys.exit("Error de sintaxis en la linea %s, columna %s: token '%s' inesperado." %(p.lineno , find_column(text, p), p.value));

#---------------------------------------------------#
#	Fin de producciones de la gramática				#
#---------------------------------------------------#

####################################################
####################################################

#---------------------------------------------------#
#			MAIN									#
#---------------------------------------------------#

# Se construye el lexer.
lexer = lex.lex()

# Se toma el archivo por entrada estandar.
archivo = sys.argv[1]
f = open(archivo, "r")
text = f.read()

# Se pasa al lexer.
lexer.input(text)
# Se construye el parser
parser = yacc.yacc()
# Se pasa al parser.
result = parser.parse(text)


#---------------------------------------------------#
#		FIN MAIN									#
#---------------------------------------------------#