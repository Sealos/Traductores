#!/usr/bin/env python

# ------------------------------------------------------------
# RangeX
#
# Interprete del lenguaje RangeX
# Entrega 1, Analisis Lexicografico
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
import sys

hayError = False
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
	'TkId',
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
	'TkEquivalente',
	'TkDesIgual',
	'TkAsignacion',
	'TkFlechaCase',
	'TkString',
	'TkComa',
	'TkConstruccion',
	'TkModulo',
	'TkDiv',

	# Funcionales
	'TkNum',
	'TkComent'
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
t_TkEquivalente		= r'=='
t_TkDesIgual		= r'/='
t_TkAsignacion 		= r'='
t_TkFlechaCase		= r'->'
t_TkComa			= r'\,'
t_TkConstruccion	= r'\.\.'
t_TkModulo			= r'%'
t_TkDiv				= r'/'

# Expresiones regulares para tokens complejos.
# (que requieren instrucciones adicionales)

def t_TkId(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	if t.value in reserved:
		t.type = reserved[ t.value ]
	return t

def t_ignore_TkComent(t):
	r'\/\/[^\n]*'


def t_TkString(t):
    r'"([^"\\]|\\"|\\\\|\\n|\\t|\\r|\\f|\\v)*"'
    t.value = (t.value)[1:-1]
    return t

def t_TkNum(t):
	r'(-|\+)?\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print("Entero muy largo %d", t.value)
	return t

# Se calcula la columna en la que comienza la palabra que
# contiene el error.
# lineno - Numero de linea actual
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
# (espacios, tabulaciones)
t_ignore = ' \t'

# Se utiliza para que la linea en la que se encuentra
# el lexer leyendo vaya aumentando cada vez que encuentra
# un '\n'

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# Se define accion a tomar cuando ocurre un error.
def t_error(t):
	print "Error: caracter inesperado \"%s\" en linea %s, columna %s." %(t.value[0], t.lineno, find_column(text, t))
	global hayError
	hayError = True
	t.lexer.skip(1)
	return t


# Se construye el lexer.
lexer = lex.lex()

def chek(entrada):
	lexer.input(entrada)
	
	while True:
		t = lexer.token()
		if not t: break
	lex.lex()

	
# Main:

# Se toma el archivo por entrada estandar.

archivo = sys.argv[1]
f = open(archivo, "r")
text = f.read()
lexer.input(text)

# Se crea una lista para almacenar los Tokens que no
# generaron errores.

ListaTokens = []

#Empezando la impresion.
while True:
	tok = lexer.token()

	if not tok:
			break      # Se culmino la lectura.

	if not (tok.type == 'error'):
		# print tok.type + '--' + tok.value + '\n'
		if (tok.type == 'TkNum' or tok.type == 'TkId' or tok.type == 'TkString'):
			ListaTokens.append("%s \"%s\" %s %s %s %s%s\n"%(tok.type, tok.value, "(Linea", tok.lineno, "Columna", find_column(text, tok), ")"))
			tok_ant = tok
		else:
			ListaTokens.append("%s %s %s %s %s%s\n"%(tok.type, "(Linea", tok.lineno, "Columna", find_column(text, tok), ")"))
			tok_ant = tok
	else:
		break	# Se encontro un error

# Se debe verificar si el ciclo anterior culmino a causa de
# un error o porque no quedan mas Tokens por leer.

if tok:

	# Dado que la culminacion del ciclo anterior fue a
	# causa de un error entonces se continua la busqueda
	# de errores en el archivo de entrada. Al haber
	# errores en el archivo no es necesario seguir
	# almacenando en la lista los Tokens funcionales.
	while True:
		tok = lexer.token()
		if not tok: break      # Se culmino la lectura.

else:
	# Dado que la culminacion del ciclo anterior fue a
	# causa de que se termino la lectura del archivo
	# entonces se procede a imprimir la lista de Tokens.
	for i in range(0,len(ListaTokens)):
		print ListaTokens[i],