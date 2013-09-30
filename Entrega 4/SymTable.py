#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# ------------------------------------------------------------
# RangeX
#
# Interprete del lenguaje RangeX
# Entrega 3, Tabla de simbolos.
# CI-3725
# (Abril-Julio 2013)
#
#
# Hecho por:
#	@author: Stefano De Colli	09-10203
#	@author: Karen Troiano		09-10855
#	
# ------------------------------------------------------------


#-------------------------------------------------#
#	Class variable									#
#-------------------------------------------------#

# Clase que representa el cuadro informativo de cada
# variable. Donde nombre, tipo y definida son los nombres
# tipo de variable y si la variable fue definida o no.

class variable:
	def __init__(self, nombre, tipo, reservado):
		self.nombre = nombre
		self.tipo = tipo
		self.reservado = reservado
		self.definida = False
		self.valor = 0
		self.valor2 = 0

	#	Acuatualiza el valor de una variable.
	def update(self, valor, valor2 = None):
		self.valor = valor
		self.valor2 = valor2
		self.definida = True
	
	def getValor(self): 
		return self.valor

	def getValor2(self):
		return self.valor2

	def getDefinida(self):
		return self.definida

	def getTipo(self):
		return self.tipo
	
	def getReservado(self):
		return self.reservado

#-------------------------------------------------#
#	Fin Class variable								#
#-------------------------------------------------#

#-------------------------------------------------#
#	Class SymTable									#
#-------------------------------------------------#
class SymTable:
	
	#----------------#
	# Constructor	 #
	#----------------#
	
	# 	Cada symtable tendra un padre y una tabla de 
	# variables que le pertenecen al bloque. 
	def __init__(self, padre, esBegin = True):
		self.padre = padre
		self.table = {}
		self.esBegin = esBegin

	#----------------#
	# insert		 #
	#----------------#
	
	# 	Se inserta un elemento a la tabla si y solo
	# si no pertenece ya previamente a ella y retorna 
	# True, en caso de pertenecer a la tabla de
	# Symbolos retorna Falso.
	
	def insert(self, nombre, tipo, reservado = False):
		if (not self.isMember(nombre, True)):
			self.table[nombre] = variable(nombre, tipo, reservado)
			return True
		else: 
			return False

	#----------------#
	# delete	 	#
	#----------------#
	
	#	Busca y elimina un elemento de la lista.
	def delete(self, nombre):
		self.table.pop(nombre) 

	#----------------#
	# Update	 	#
	#----------------#
	
	#	Actualiza el valor de una variable,
	# en caso de actualizarlo, retorna True,
	# en caso de no encontrarla retorna False.
	
	def update(self, nombre, valor):
		a = self.find(nombre)
		if (a == None):
			return False
		else: 
			a.update(valor)
			return True

	#----------------#
	# getPadre	 	#
	#----------------#
	
	#	 Retorna quien es el padre del bloque.
	# En este caso, si el bloque se encuentra anidado
	# dentro de otro bloque.
	def getPadre(self):
		return self.padre

	#----------------#
	# isMember	 	#
	#----------------#
	
	# 	Verifica si una variable pertenece o no a la
	# tabla de simbolos, en el caso de no ser local
	# la variable, revisa a sus padres hasta encontrarla.
	# Retorna False en caso de no existir.
	def isMember(self, nombre, local):
		if (local):
			return self.table.has_key(nombre)
		else:
			if (self.table.has_key(nombre)):
				return True
			else:
				if (self.padre == None):
					return False
				else:
					return self.padre.isMember(nombre, False)

	#----------------#
	# find		 #
	#----------------#

	# 	Busca la variable declarada y la retorna. Asumiendo
	# que ya ser verificó que esta variable pertenece
	# a la tabla de símbolos. Si no pertenece retorna None.
	
	def find(self, nombre, local):
		if (local):
			if (self.table.has_key(nombre)):
				return self.table[nombre]
			else:
				return None
		else:
			if (self.table.has_key(nombre)):
				return self.table[nombre]
			else:
				if (self.padre == None):
					return None
				else:
					return self.padre.find(nombre, False)