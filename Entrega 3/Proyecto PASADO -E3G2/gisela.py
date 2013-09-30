#!/usr/bin/python
# -*- coding: UTF8 -*-

# ------------------------------------------------------------
# Gisela
#
# Interprete del lenguaje Gisela
# Entrega 3, Llenado de la tabla de símbolos.
# CI-3725
# (Sep-Dic 2012)
#
#
# Hecho por:
#	@author: Karen Troiano	09-10855
#	@author: Yeiker Vazquez	09-10882
# ------------------------------------------------------------

import lex
import yacc
import sys
from SymTable import *

Error = False
Indicador = 1
global Tabla
Tabla = SymTable()
global Diccionario
Diccionario = {}
Diccionario[0] = 'global'  

#---------------------------------------------------#
#		PRIMERA ENTREGA			    #
#---------------------------------------------------#
# Lista de palabras reservadas.

reserved = {

	'if'		:	'TkIf',
	'read'		: 	'TkRead',
	'print'		: 	'TkPrint',
	'return'	: 	'TkReturn',
	'bool' 		: 	'TkBoolean',
	'char' 		: 	'TkChar',
	'skip' 		: 	'TkSkip',
	'abort' 	: 	'TkAbort',
	'fi' 		:	'TkFi',
	'go' 		: 	'TkGo',
	'og' 		: 	'TkOg',
	'do' 		: 	'TkDo',
	'od' 		: 	'TkOd',
	'proc' 		: 	'TkProc',
	'int' 		: 	'TkInt',
	'chr'		:	'TkChr',
	'ord'		:	'TkOrd',
	'isupper'	:	'TkUpper',
	'isalpha'	:	'TkAlpha',
	'isdigit'	:	'Tkdigit',
	'isspace'	:	'TkSpace',
	'xor'		:	'TkXor',
	'and'		:	'TkAnd',
	'or'		:	'TkOr',
	'not'		:	'TkNot',
	'div'		:	'TkDiv',
	'mod'		:	'TkMod',
	'var'		:	'TkVar'

}

#---------------------------------------------------#
#	Lista de tokens				    #
#---------------------------------------------------#

tokens = [
	'TkIdent','TkNum','TkPuntoYComa','TkParAbre','TkParCierra','TkSuma',
	'TkResta','TkAsterisco','TkDobleAsterico','TkMenor','TkMenorIgual',
	'TkMayor','TkMayorIgual','TkEquivalente','TkDesIgual','TkElse',	'TkAsignacion',
	'TkTrue','TkFalse','ID','TkComent','TkSec','TkSecSimple','TkLG',
	'TkThen','TkComa', 'TkCharContent'
	] + list(reserved.values())


#---------------------------------------------------#
#	Expresiones regulares			    #
#---------------------------------------------------#


def t_TkCharContent(t):
	r'(\'[a-zA-Z0-9_]\' | \"[a-zA-Z0-9_]\" | \_[a-zA-Z0-9_])'
	return t



t_TkIdent		= r'[a-zA-Z_][a-zA-Z0-9_]*'
t_TkPuntoYComa 		= r';'
t_TkParAbre		= r'\('
t_TkParCierra		= r'\)'
t_TkSuma		= r'\+'
t_TkResta 		= r'-'
t_TkAsterisco		= r'\*'
t_TkDobleAsterico	= r'\*\*'
t_TkMenor		= r'<'
t_TkMenorIgual 		= r'<='
t_TkMayor 		= r'>'
t_TkMayorIgual 		= r'>='
t_TkEquivalente		= r'=='
t_TkDesIgual		= r'\!='
t_TkElse 		= r'\|'
t_TkAsignacion 		= r':='
t_TkThen 		= r'->'
t_TkComa		=r'\,'
t_TkSec			= r'"[^"]*"'
t_TkSecSimple		= r'\'[^\']*\''

# Expresiones regulares para tokens complejos.
# (que requieren instrucciones adicionales)

def t_ignore_TkComent(t):
	r'\/\/[^\n]*'


def t_TkLG(t):
	r'\let\'s(?=[\040][\012\040]*go)'
	return (t)

def t_TkNum(t):
	r'(-?)(\+?)\d+'
	try:
		t.value=int(t.value)
	except ValueError:
		print("Entero muy largo %d",t.value)
	return t

def t_TkTrue(s):
	r'([tT] | [tT][rR] | [tT][rR][uU] | [tT][rR][uU][eE])(?![A-Za-z0-9_])'
	return s


def t_TkFalse(f):
	r'([fF] |[fF][aA] |[fF][aA][lL] |[fF][aA][lL][sS]|[fF][aA][lL][sS][eE])(?![A-Za-z0-9_])'
	return f



# Se calcula la columna en la que comienza la palabra que
# contiene el error.
# lineno - Numero de linea actual
# lexpos - Posicion actual en el archivo de entrada.

def find_column(input,token):
	  ultimoS = input.rfind('\n',0,token.lexpos)
	  if ultimoS < 0:
	      ultimoS = 0
	  elif ultimoS > 0:
	      ultimoS = ultimoS + 1
	  colum = (token.lexpos - ultimoS) + 1
	  return colum


# Aqui se toman en cuenta los caracteres en blanco.
# (espacios, tabulaciones)

t_ignore  = ' \t'


# Se utiliza para que la linea en la que se encuentra
# el lexer leyendo vaya aumentando cada vez que encuentra
# un '\n'

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# Se define accion a tomar cuando ocurre un error.
def t_error(t):
	print "Error: Caracter inesperado \"%s\" en la fila %s, columna %s"  %(t.value[0],t.lineno, find_column(text, t))
	global Error
	Error = True
	t.lexer.skip(1)
	return t


# Todas aquellas palabras que no contengan errores o no
# pertenezcan a los tokens de las palabras reservadas se
# convertiran en TkIdent mediante t_ID.

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'TkIdent')
	return t

#---------------------------------------------------#
#	 Fin de Primera Entrega			    #
#---------------------------------------------------#


#----------------#
# Precedencia	 #
#----------------#

#Se define la precedencia de los operadores.

precedence = (
	('left','TkOr'),
	('left','TkAnd'),
	('nonassoc', 'TkXor'),
	('right', 'TkNot'),
	('left', 'TkSuma', 'TkResta'),
	('left', 'TkAsterisco'),
	('right','TkDiv','TkMod'),
	('right', 'TkDobleAsterico'),
	('nonassoc', 'TkMayor', 'TkMayorIgual', 'TkMenor', 'TkMenorIgual', 'TkEquivalente', 'TkDesIgual')

)

#------------------#
# Fin Precedencia  #
#------------------#


#---------------------------------------------------#
#	Producciones de la gramática		    #
#---------------------------------------------------#

#Inicio de la gramática de Gisela
def p_INICIO(p):
	'''INICIO : DR TkLG TkGo CUERPO TkOg
	'''
	Tabla.errores(Diccionario)
	print " "
	print "TABLAS DE SÍMBOLOS\n"
	print "Variables Globales:\n"
	Tabla.VariablesNoProc(0)
	print "\nBloque principal:\n"
	Tabla.VariablesNoProc(Indicador)
	print "\nProcedimientos:\n"
	for i in range (1, Indicador):
		print "Nombre del procedimiento: %s" %(Diccionario[i])
		Tabla.VariablesProc(i)
		print " "
	
	
	
def p_CUERPO(p):
	''' CUERPO : DECLARACION CUERPO 
		    | SEC
	'''

#Declaraciones y procedimientos previos a Let's go (LG)
def p_DR(p):
	'''DR : PROC DR
	   | DECLARACIONGLOBAL DR
	   |
	'''

#Gramática para los procedimientos de Gisela.
def p_procedimientos(p):
	'''PROC : TkProc TkIdent TkParAbre ARG TkParCierra CUERPOSIMPLE
	| TkProc TkIdent TkParAbre TkParCierra CUERPOSIMPLE
	'''
	global Diccionario, Indicador
	Diccionario[Indicador] = p[2]
	Indicador = Indicador + 1
	#print "procedimiento %s" %(p[2])

def p_cuerposimple(p):
	'''
	CUERPOSIMPLE : INSTRUCCIONSIMPLE
	| DECLARACION INSTRUCCIONSIMPLE
	'''
  
def p_instruccionsimple(p):
	''' INSTRUCCIONSIMPLE : ASIGNACION
	| TkIdent TkParAbre ARGINV TkParCierra
	| TkIdent TkParAbre TkParCierra
	| INOUT
	| TkSkip
	| TkAbort
	| TkReturn
	| IF
	| GO
	| DO
	'''
#Gramática para los argumentos de parámetros para los procedimientos.
def p_Argumentos(p):
	'''ARG : ARGBOOL
	  | ARGCHAR
	  | ARGINT 
	'''
	
def p_ArgumentosInt(p):
	'''ARGINT : TkInt TkIdent
	  | TkInt TkIdent TkComa ARG
	  | TkVar TkInt TkIdent
	  | TkVar TkInt TkIdent TkComa ARG
	'''
	if (p[1] == 'int'): 
		Tabla.insertar(p[2],p[1],'0',Indicador,True, False)
	else: 
		Tabla.insertar(p[3],p[2],'0',Indicador,True, True)
	

def p_ArgumentosBool(p):
	'''ARGBOOL : TkBoolean TkIdent
	  | TkBoolean TkIdent TkComa ARG
	  | TkVar TkBoolean TkIdent
	  | TkVar TkBoolean TkIdent TkComa ARG
	'''
	if (p[1] == 'bool'): 
		Tabla.insertar(p[2],p[1],'False',Indicador,True, False)		
	else: 
		Tabla.insertar(p[3],p[2],'False',Indicador,True, True)

def p_ArgumentosChar(p):
	'''ARGCHAR : TkChar TkIdent
	  | TkChar TkIdent TkComa ARG
	  | TkVar TkChar TkIdent
	  | TkVar TkChar TkIdent TkComa ARG
	'''
	if (p[1] == 'char'): 
		Tabla.insertar(p[2],p[1],'!',Indicador,True, False)		
	else: 
		Tabla.insertar(p[3],p[2],'!',Indicador,True, True)

#Gramática de los tipos de Gisela.
def p_TIPO(p):
	'''TIPO : TkInt
	  | TkChar
	  | TkBoolean'''

#Tipo de expresiones complejas que se encuentran Gisela
def p_expression(p):
	'''expression : ARIT
		| BOOL
		| OPCHAR
		| EXPRESION 
	'''

#Gramática de las expresiones aritméticas que ofrece Gisela,
#Suma, resta, multiplicación, división, mod, 
def p_aritmeticas(p):
	'''ARIT : ARIT TkSuma ARIT
		| ARIT TkResta ARIT
		| ARIT TkAsterisco ARIT
		| ARIT TkMod ARIT
		| ARIT TkDiv ARIT
		| ARIT TkDobleAsterico ARIT
		| TkParAbre ARIT TkParCierra
		| TkResta ARIT 
		| ARIT ARIT
		| VALORES
	'''
	
	## NO ESTAMOS SEGUROS DE ESTA PARTE CON EL TKRESTA ARIT.

#Valores válidos.
def p_valores(p):
	'''VALORES : TkTrue 
	   | TkFalse 
	   | TkNum
	   | TkCharContent
	   | TkIdent
	'''

#Gramática de las expresiones booleanas que ofrece Gisela,
#and, or, xor, not
def p_booleano(p):
	'''BOOL : BOOL TkAnd BOOL
	  | BOOL TkXor BOOL
	  | BOOL TkOr BOOL
	  | TkNot BOOL
	  | TkParAbre BOOL TkParCierra 
	  | EXPRESION
	  | VALORES
	'''

def p_DeclaracionGlobal(p):
	'''
	DECLARACIONGLOBAL : DECINTG
	| DECCHARG
	| DECBOOLG
	'''
	
	
def p_DeclaracionIntG(p):
	'''
	DECINTG : TkInt TkIdent TkPuntoYComa
	| TkInt TkIdent TkComa RESTOINTG
	RESTOINTG : TkIdent TkComa RESTOINTG
	| TkIdent TkPuntoYComa
	'''
	
	if (p[1] == 'int'):
		Tabla.insertar(p[2],p[1],'0',0,False,False)

	else: 
		Tabla.insertar(p[1],'int','0',0,False,False)

def p_DeclaracionBoolG(p):
	'''
	DECBOOLG : TkBoolean TkIdent TkPuntoYComa
	| TkBoolean TkIdent TkComa RESTOBOOLG
	RESTOBOOLG : TkIdent TkComa RESTOBOOLG
	| TkIdent TkPuntoYComa
	'''
	
	if (p[1] == 'bool'): 
		Tabla.insertar(p[2],p[1],'False',0,False,False)
	else: 
		Tabla.insertar(p[1],'bool','False',0,False,False)

def p_DeclaracionCharG(p):
	'''
	DECCHARG : TkChar TkIdent TkPuntoYComa
	| TkChar TkIdent TkComa RESTOCHARG
	RESTOCHARG : TkIdent TkComa RESTOCHARG
	| TkIdent TkPuntoYComa
	'''
	
	if (p[1] == 'char'): 
		Tabla.insertar(p[2],p[1],'!',0,False,False)
	else: 
		Tabla.insertar(p[1],'char', '!',0,False,False)



def p_Declaracion(p):
	'''
	DECLARACION : DECINT
	| DECCHAR
	| DECBOOL
	'''
	
	
def p_DeclaracionInt(p):
	'''
	DECINT : TkInt TkIdent TkPuntoYComa
	| TkInt TkIdent TkComa RESTOINT
	RESTOINT : TkIdent TkComa RESTOINT
	| TkIdent TkPuntoYComa
	'''
	
	if (p[1] == 'int'): 
		Tabla.insertar(p[2],p[1],'0',Indicador,False,False)

	else: 
		Tabla.insertar(p[1],'int','0',Indicador,False,False)

def p_DeclaracionBool(p):
	'''
	DECBOOL : TkBoolean TkIdent TkPuntoYComa
	| TkBoolean TkIdent TkComa RESTOBOOL
	RESTOBOOL : TkIdent TkComa RESTOBOOL
	| TkIdent TkPuntoYComa
	'''
	
	if (p[1] == 'bool'): 
		Tabla.insertar(p[2],p[1],'False',Indicador,False,False)
	else: 
		Tabla.insertar(p[1],'bool','False',Indicador,False,False)

def p_DeclaracionChar(p):
	'''
	DECCHAR : TkChar TkIdent TkPuntoYComa
	| TkChar TkIdent TkComa RESTOCHAR
	RESTOCHAR : TkIdent TkComa RESTOCHAR
	| TkIdent TkPuntoYComa
	'''
	
	if (p[1] == 'char'): 
		Tabla.insertar(p[2],p[1],'!',Indicador,False,False)
	else: 
		Tabla.insertar(p[1],'char', '!',Indicador,False,False)


def p_Asignacion(p):
	'''
	ASIGNACION  : TkIdent TkAsignacion expression
	| TkIdent TkComa ASIGNACION TkComa expression
	'''


def p_Go(p):
	'''GO : TkGo CUERPO TkOg
	'''

def p_If(p):
	'''IF : TkIf COMANDOGUARDIA ACTION 
	ACTION : TkFi
	| TkElse COMANDOGUARDIA ACTION
	'''

def p_Do(p):
	'''DO : TkDo COMANDOGUARDIA ACTION2 
	ACTION2 : TkOd
	| TkElse COMANDOGUARDIA ACTION2
	'''


def p_ComandoGuardia(p):
	'''
	 COMANDOGUARDIA : expression TkThen INSTRUCCIONSIMPLE 
	 | INSTRUCCIONSIMPLE
	'''
	


#Gramática de las definicones de funciones ofrecidas por Gisela
# isupper, isdigit, isalpha, isspace, chr, ord.
def p_OperaChar(p):
	 ''' 
	OPCHAR : TkUpper TkParAbre OPCHAR TkParCierra
	  | TkChr TkParAbre ARIT TkParCierra
	  | TkOrd TkParAbre OPCHAR TkParCierra
	  | TkAlpha TkParAbre OPCHAR TkParCierra
	  | Tkdigit TkParAbre OPCHAR TkParCierra
	  | TkSpace TkParAbre OPCHAR TkParCierra
	  | VALORES
	 '''
 
#Gramática de print and read
def p_InOut(p):
	'''
	INOUT : TkPrint TkSec expression 
	| TkPrint TkSecSimple expression
	| TkPrint expression 
	| TkRead TkSec TkIdent
	| TkRead TkSecSimple TkIdent
	| TkRead TkIdent
	'''


#Secuencias de todo lo que puede contener un programa o procedimiento

def p_secuenciacion(p):
	'''SEC : INSTRUCCIONSIMPLE TkPuntoYComa SEC
	| INSTRUCCIONSIMPLE
	'''


def p_argumentosinvocativos(p):
	''' 
	 ARGINV : VALORES TkComa ARGINV
	    | VALORES
	'''
  
#Gramática de las expresiones relacionales de Gisela.
def p_EXPRBIN_RELACIONAL(p):
    """
    EXPRESION : EXPRESION TkEquivalente EXPRESION
	| EXPRESION TkDesIgual EXPRESION
	| EXPRESION TkMenor EXPRESION
	| EXPRESION TkMenorIgual EXPRESION
	| EXPRESION TkMayor EXPRESION
	| EXPRESION TkMayorIgual EXPRESION
	| TkParAbre EXPRESION TkParCierra 
	| VALORES
	| OPCHAR
	| ARIT TkEquivalente ARIT
	| ARIT TkDesIgual ARIT
	| ARIT TkMenor ARIT
	| ARIT TkMenorIgual ARIT
	| ARIT TkMayor ARIT
	| ARIT TkMayorIgual ARIT
    """


def p_error(p):
	if (p != None):
		print "Error de sintaxis en la linea %s, columna %s."  %(p.lineno, find_column(text, p));
	else:
		pass;

#---------------------------------------------------#
#	Fin de producciones de la gramática	    #
#---------------------------------------------------#


#---------------------------------------------------#
#			MAIN			    #
#---------------------------------------------------#

# Se construye el lexer.
lexer = lex.lex()

# Se toma el archivo por entrada estandar.
archivo = sys.argv[1]
f = open(archivo, "r")
text = f.read()
lexer.input(text)

# Se pasa al análisis sintáctico.
parser = yacc.yacc()
result = parser.parse(text)


#---------------------------------------------------#
#		FIN MAIN			    #
#---------------------------------------------------#
