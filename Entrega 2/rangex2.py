#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# ------------------------------------------------------------
# RangeX
#
# Interprete del lenguaje RangeX
# Entrega 2, Analisis Sintactico con arbol sintactico abstracto.
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

global impresion 
impresion = '\n'
global Error
Error = False

#---------------------------------------------------#
#		PRIMERA ENTREGA			   					 #
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
		if input[i] == '\n':
			break
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
		print "Entero fuera de rango 32b \"%d\"en linea %s, columna %s."%(t.value, t.lineno, find_column(text, t))
	else:
		print "Error: caracter inesperado \"%s\"en linea %s, columna %s."%(t.value[0], t.lineno, find_column(text, t))
	t.lexer.skip(1)
	return t


#------------------------------------------------------#
#			FIN DE PRIMERA ENTREGA						# 
#-----------------------------------------------------#

#---------------------#
# Clases			  #
#--------------------#	

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
			palabra += "\n"+ tab + "else: " +  self.elsse.toString(tab, False)
		return palabra

class Case:
	def __init__(self, exp, casos):
		self.exp = exp
		self.casos = casos

	def toString(self, tab, booleano):
		
		palabra = "CASE\n"
		if ( type(self.exp) is str):
			palabra += tab + "exp: "  + self.exp
		else:
			palabra += tab + "exp: " + self.exp.toString(tab, False) + "\n"
		palabra += tab + "caso: \n" + tab + self.casos.toString(tab, False) 
		return palabra

class CaseCond:
	def __init__(self, ran, ins, casos):
		self.ran = ran
		self.ins = ins
		self.casos = casos

	def toString(self, tab, booleano):
		palabra = "\t" + "ran: " + self.ran.toString(tab + "\t", False) + "\n"
		palabra += tab + "\t" +  "ins: " + self.ins.toString(tab + "\t", False) + "\n"
		if (self.casos != 'vacio'):
			palabra += tab + "caso: \n" + tab + self.casos.toString(tab, False) 
		return palabra

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

class Bloque:
	def __init__(self, declaraciones, instrucciones):
		self.declaraciones = declaraciones
		self.instrucciones = instrucciones

	def toString(self, tab, booleano):
		tab = tab + "\t"
		palabra = "BLOQUE\n"
		palabra += tab + self.instrucciones.toString(tab, False) + "\n"
		return palabra

class Simple:
	def __init__(self, tipo, valor):
		self.tipo = tipo
		self.valor = valor

	def toString(self, tab, booleano, bool2 = True):
		tab = tab + "\t"
		if (self.tipo == 'VARIABLE' or self.tipo == 'CADENA'):
			if (booleano == True and bool2 == True):
				palabra = "elemento: " + str(self.tipo) + "\n"
				if (self.tipo == 'VARIABLE'):
					palabra += tab + "nombre: " + str(self.valor)
				else:
					cadena = str(self.valor)
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
				cadena = cadena.replace("\\", "")
				palabra += tab + "valor: " + cadena 
		else:
			if (booleano == True):
				palabra = "elemento: " + str(self.tipo) + "\n"
			else:
				palabra = str(self.tipo) + "\n"
			palabra += tab + "valor: " + str(self.valor)
		return palabra

class Secuenciacion:
	def __init__(self, instruccion1, instruccion2):
		self.instruccion1 = instruccion1
		self.instruccion2 = instruccion2

	def toString(self, tab, booleano):
		palabra = self.instruccion1.toString(tab, False) + "\n"
		palabra += tab + "SEPARADOR\n"
		palabra += tab + self.instruccion2.toString(tab, False)
		return palabra

class LineaDeclaracion:
	def __init__(self, variable, tipo, declaraciones):
		self.variable = variable
		self.tipo = tipo
		self.declaraciones = declaraciones

class Variables:
	def __init__(self, variable1, variable2):
		self.variable1 = variable1
		self.variable2 = variable2

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

class Impresion:
	def __init__(self, expresion1, expresion2):
		self.expresion1 = expresion1
		self.expresion2 = expresion2
		
	def toString(self, tab, booleano):
		palabra = self.expresion1.toString(tab, True) + "\n"
		palabra += tab + "elemento: " + self.expresion2.toString(tab, False)
		return palabra

		
class Funcion:
	def __init__(self, valor, expresion):
		self.valor = valor
		self.expresion = expresion
		
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

class ExpresionUnaria:
	def __init__(self, tipo, operador, operando):
		self.tipo = tipo
		self.operador = operador
		self.operando = operando

	def toString(self, tab, booleano):
		if (booleano == True):
			palabra = "elemento: "
		else:
			palabra = "EXPRESION_UN\n"
		tab = tab + "\t"
		if (type(self.operador) is str):
			palabra += tab + "operador: "+ self.tipo + "\n"
		else:
			palabra += tab + "operador: "  + self.operador.toString(tab, False) + "\n"
		palabra += tab + "operando:  "  + self.operando.toString(tab, False)
		return palabra

		
class ExprBinaria:
	def __init__(self, operacion, tipo, operando1, operando2, relacional):
		self.operacion = operacion
		self.tipo = tipo
		self.operando1 = operando1
		self.operando2 = operando2
		self.relacional = relacional

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
		
#--------------------------#
#	Fin de clases		   	#
#--------------------------#


#----------------#
# Precedencia	 #
#----------------#

#Se define la precedencia de los operadores.

precedence = (
	('left','Impresion'),
	('right', 'Else'),
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
#	Producciones de la gramática		    #
#---------------------------------------------------#

def p_PROGRAMA(p):
	"""
	PROGRAMA : TkProgram INSTRUCCION
	"""
	p[0] = p[2]
	if (not (Error)): 
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
		| 
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
	CASECOND : EXPRESION TkFlechaCase INSTRUCCION CASECONDDOS
	"""
	p[0] = CaseCond(p[1], p[3], p[4])

def p_CASECONDDOS(p):
	"""
	CASECONDDOS : EXPRESION TkFlechaCase INSTRUCCION CASECONDDOS
		| 
	"""
	if (len(p) > 1): p[0] = CaseCond(p[1], p[3], p[4])
	else: p[0] = "vacio"

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
	BLOQUE : TkBegin DECLARE SECUENCIACION TkEnd
	"""
	p[0] = Bloque(p[2], p[3])

def p_DECLARE(p):
	"""
	DECLARE : TkDeclare LINEADECLARACION
		| 
	"""
	if (len(p) > 1): p[0] = p[2]
	else: p[0] = "vacio"

def p_SECUENCIACION(p):
	"""
	SECUENCIACION : SECUENCIACION TkPuntoYComa INSTRUCCION
		| INSTRUCCION 
	"""
	if (len(p) <= 2): p[0] = p[1]
	else: p[0] = Secuenciacion(p[1], p[3])
	

def p_LINEADECLARACION(p):
	"""
	LINEADECLARACION : VARIABLES TkAs TYPE
		| LINEADECLARACION TkPuntoYComa VARIABLES TkAs TYPE
	"""
	if (len(p) <= 4): p[0] = LineaDeclaracion(p[1], p[3], 'vacio') 
	else: LineaDeclaracion(p[3], p[5], p[1])

def p_TYPE(p):
	"""
	TYPE : TkInt
		| TkBool
		| TkRange
	"""
	p[0] = p[1]

def p_VARIABLES(p):
	"""
	VARIABLES : VARIABLES TkComma VARIABLES
		| VARIABLE
	"""
	if (len(p) <= 2): p[0] = p[1]
	else: p[0] = Variables(p[1], p[3])
	

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
	IMPRESION : IMPRESION TkComma STRINEXP %prec Impresion
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
	p[0] = Funcion(p[1], p[3])

def p_FUNCIONES(p):
	"""
	FUNCIONES : TkBottom
		| TkRtoi
		| TkLength
		| TkPertenece
		| TkTop
	"""
	p[0] = p[1]

def p_EXPRANGO(p):
	"""
	EXPRANGO : EXPRESION TkConstruccion EXPRESION
		| EXPRESION TkInterseccion EXPRESION
	"""
	if (p[2] == '..'): p[0] = ExprBinaria('Construccion', 'rango', p[1], p[3], False)
	else:  p[0] = ExprBinaria('Interseccion','rango', p[1], p[3], False)

def p_VARIABLE(p):
	"""
	VARIABLE : TkId
	"""
	p[0] = Simple('VARIABLE', p[1])
	

def p_NUMERO(p):
	"""
	NUMERO : TkNum
	"""
	p[0] = Simple('CONSTANTE_ENT', p[1])

def p_EXPRELACIONAL(p):
	"""
	EXPRELACIONAL : EXPRESION TkIgual EXPRESION
		| EXPRESION TkDesIgual EXPRESION
		| EXPRESION TkMenor EXPRESION
		| EXPRESION TkMenorIgual EXPRESION
		| EXPRESION TkMayor EXPRESION
		| EXPRESION TkMayorIgual EXPRESION
	"""
	if (p[2] == '=='): p[0] = ExprBinaria('Igual que', 'boolean', p[1], p[3], True)
	elif (p[2] == '/='): p[0] = ExprBinaria('No igual a', 'boolean', p[1], p[3], True)
	elif (p[2] == '<'): p[0] = ExprBinaria('Menor que', 'boolean', p[1], p[3], True)
	elif (p[2] == '<='): p[0] = ExprBinaria('Menor Igual que', 'boolean', p[1], p[3], True)
	elif (p[2] == '>'): p[0] = ExprBinaria('Mayor que', 'boolean', p[1], p[3], True)
	elif (p[2] == '>='): p[0] = ExprBinaria('Mayor Igual que', 'boolean', p[1], p[3], True)

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
	if (p[2] == '+'): p[0] = ExprBinaria('Mas', 'integer', p[1], p[3], False)
	elif (p[2] == '-'): p[0] = ExprBinaria('Resta', 'integer', p[1], p[3], False)
	elif (p[2] == '*'): p[0] = ExprBinaria('Por', 'integer', p[1], p[3], False)
	elif (p[2] == '/'): p[0] = ExprBinaria('Div', 'integer', p[1], p[3], False)
	elif (p[2] == '%'): p[0] = ExprBinaria('Modulo', 'integer', p[1], p[3], False)

def p_UNEXPRARITME(p):
	"""
	UNEXPRARITME : TkResta EXPRESION %prec RestaU
		| TkSuma EXPRESION %prec SumaU
	"""
	if (p[1] == '-'):	p[0] = ExpresionUnaria('MENOS_UNARIO', p[1] , p[2])
	else: 	p[0] = ExpresionUnaria('MAS_UNARIO', p[1], p[2])
	
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
	if (p[2] == "or"): p[0] = ExprBinaria('Or', 'boolean', p[1], p[3], False)
	else: p[0] = ExprBinaria('And', 'boolean', p[1], p[3], False)

def p_UNEXPRBOOL(p):
	"""
	UNEXPRBOOL : TkNot EXPRESION
	"""
	p[0] = ExpresionUnaria('NEGACION',p[1] , p[2])

def p_BOOL(p):
	"""
	BOOL : TkTrue
		| TkFalse
	"""
	p[0] = Simple('BOOLEANO', p[1])

def p_error(p):
	global Error
	if (Error != True and p != None):
		Error = True
		sys.exit("Error de sintaxis en la linea %s, columna %s: token '%s' inesperado." %(p.lineno , find_column(text, p), p.value));

#---------------------------------------------------#
#	Fin de producciones de la gramática	  		  #
#---------------------------------------------------#

####################################################
####################################################

#---------------------------------------------------#
#			MAIN			   						 #
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
#		FIN MAIN			    #
#---------------------------------------------------#