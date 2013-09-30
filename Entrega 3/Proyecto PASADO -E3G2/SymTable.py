# -*- coding: UTF8 -*-

# ------------------------------------------------------------
# SymTable
#
# Interprete del lenguaje Gisela
# Entrega 3, Tabla de símbolos.
# CI-3725
# (Sep-Dic 2012)
#
#
# Hecho por:
#	@author: Karen Troiano	09-10855
#	@author: Yeiker Vazquez	09-10882
# ------------------------------------------------------------


# ------------------------------------------------------------
# Observaciones SymTable:
#
# Se utiliza una lista enlazada en la que cada elemento 
# representa el nombre de una variable (siendo estas distintas).
# Cuando se declara una variable con el mismo nombre, su
# elemento en la lista se despliega con cuadros informativos
# correspondientes a cada proceso en el que fue declarado. En
# general los elementos de la lista enlazada son listas de 
# cuadros informativos (llamados Items -ver class Item-).
#
# El let's go será visto como un procedimiento más de Gisela.
# ------------------------------------------------------------


#---------------------------------------------------#
#	Class Item 				    #
#---------------------------------------------------#

# Clase que representa el cuadro informativo de cada
# variable. Donde name, type y value, son los nombres
# tipo de variable y su valor correspondiente. Function
# es el nombre del proceso en el que fue declarado (Let's go
# es visto como un proc) y proc apunta al cuadro informativo
# de una variable con el mismo nombre pero declarada en otro
# procedimiento

class Item:
	def __init__(self, nombre, tipo, valor, funcion, isArg, isRef):
		self.name = nombre 
		self.type = tipo
		self.value = valor
		self.function = funcion
		self.isArg = isArg
		self.isRef = isRef
		self.padre = None
		self.proc = None
		self.sig = None
	

#---------------------------------------------------#
#	Fin Class Item 				    #
#---------------------------------------------------#


#---------------------------------------------------#
#	Class SymTable 				    #
#---------------------------------------------------#
class SymTable:
  
	#----------------#
	# Constructor	 #
	#----------------#
	
	# Constructor de la clase de SymTable.
	def __init__(self, inicio=None, fin=None):
		self.inicio = inicio
		self.fin = fin
		
		

	#----------------#
	# isMember	 #
	#----------------#
 
	# Funcion isMember:  busca que el nombre de la
	# variable declarada. Si existe en la tabla
	# retorna true, en caso contrario es false.
		
	def isMember(self, nombre):
		Encontrado = False
		aux = self.inicio
				
		while not (Encontrado or aux.sig == None):
			if (aux.name == nombre): 
				Encontrado = True
			else: 
				aux = aux.sig
		
		# Ultima caja
		if (aux.name == nombre): 
			Encontrado = True
		
		return Encontrado


	#----------------#
	# find		 #
	#----------------#

	# Funcion find:  busca el item de la
	# variable declarada y lo retorna. Asumiendo
	# que ya ser verificó que esta variable pertenece
	# a la tabla de símbolos.
		
	def find(self, nombre):
		aux = self.inicio
				
		while not (aux.name == nombre or aux.sig == None):
			aux = aux.sig
		
		return aux
      
	
	#----------------#
	# insertar	 #
	#----------------#
	
	# Funcion insertar:  inserta las variables declaradas
	# (incluso cuando son declaradas varias veces)
	
	# ADVERTENCIA: Al momento de una declaración,se llama  
	# a insertar con los valores predeterminados segun el
	# tipo, es decir, si es int se pasa como parámetro 0,
	# si es char se pasa ! y si es bool false.
	
	def insertar(self, nombre, tipo, valor, funcion, isArg, isRef):
	  	if (self.inicio == None and self.fin == None):
		
		# Primer caso: Está vacía la lista de tablas de símbolos.
			self.inicio = Item(nombre,tipo,valor,funcion,isArg,isRef) 
			self.fin = self.inicio
			
		
		else: 
	
		
		# Segundo caso: La lista no esta vacía.
		
		# Subcasos:
			
			if (self.isMember(nombre)):
			# Pertenece a la lista, se agrega los nuevos datos
			# a la variable que ya ha sido declarada.
				aux = self.find(nombre)
				aux2 = aux
				while not (aux.proc == None): 
					aux = aux.proc
				aux.proc = Item(nombre,tipo,valor,funcion,isArg,isRef)
				while not (aux2.padre == None):
					aux2 = aux2.padre
				aux.proc.padre = aux2
			else: 
			# No pertenece a la lista, se agrega en la tabla
			# de símbolos la nueva variable
				aux = Item(nombre,tipo,valor,funcion,isArg,isRef)
				self.fin.sig = aux
				self.fin = aux
				

				
	
	
	#----------------#
	# Update	 #
	#----------------#
	
	# Funcion Update: actualiza el valor de una variable
	# en el procedimiento especificado.
	
	def Update(self, nombre, funcion, valor):
		
		if (isMember(nombre)):
		 # Si existe lo buscamos
			aux = find(nombre)
			
			# Se busca entre los posibles procedimientos
			# en los cuales también se ha declarado
			# esa variable.
			while not (aux.function == funcion):
				aux = aux.proc
			
			aux.value = valor 	


	#----------------#
	# delete	 #
	#----------------#
	
	# Funcion delete: resetea el tipo, valor y función que pertenece
	# una variable en el procedimiento especificado.
	
	def delete(self,nombre, funcion):
		
		if (isMember(nombre)):
		 # Si existe lo buscamos
			aux = find(nombre)
			
			# Se busca entre los posibles procedimientos
			# en los cuales también se ha declarado
			# esa variable.
			while not (aux.function == funcion):
				aux = aux.proc
			
			# Una vez ya encontrada se conserva la estructura
			# pero es reseteada la información de la estructura
			aux.type = None
			aux.function = None
			aux.valor = None
	
	
	#---------------------------------------------------#
	#	Funciones Impresión			    #
	#---------------------------------------------------#
  
	# Funcion errores: Se imprimen los errores de dobles declaraciones
	# de variables o declaraciones de variables ya dadas en un parámetro
	# de argumentos. La caja de cada variable contiene la información 
	# necesaria para determinar el tipo de error.
	
	def errores(self,diccionario):
		aux = self.inicio      
		i = 1
		Conjunto = set([])
		while not (aux.sig == None):
			while not (aux.proc == None):
				Conjunto.add(aux.function)
				aux = aux.proc
				i = i+1
			Conjunto.add(aux.function)
			if not (len(Conjunto) == i):
				self.VerificarTipoError(aux.name, diccionario)
			Conjunto.clear()
			i = 1
			if (aux.padre == None):
				aux = aux.sig
			else:
				aux = aux.padre.sig
			
		# Ciclo para la última caja
		while not (aux.proc == None):
			Conjunto.add(aux.function)
			aux = aux.proc
			i = i+1
		Conjunto.add(aux.function)
		if not (len(Conjunto) == i):
			self.VerificarTipoError(aux.name, diccionario)
			
	
	# Funcion VerificarTipoError: Se busca de que tipo fue el error, si de argumentos 
	# en una función o de doble declaración en un mismo bloque.
	
	def VerificarTipoError(self, nombre, diccionario):
		pivote = self.find(nombre)
		centinela = False
		# centinela determina si hay algun error con los argumentos y declaraciones en un
		# procedimiento.
		while not (pivote.proc == None or centinela):
			comp = self.find(nombre)
			while not (comp.proc == None or centinela):
				if (not(comp == pivote)) and (comp.function == pivote.function) and (comp.isArg or pivote.isArg):
					if (pivote.isArg):
						print "Error: Se está intentando declarar la variable \"%s\" pero la misma forma parte de los argumentos del procedimiento \"%s\"." %(pivote.name, diccionario[pivote.function])
					else:
						print "Error: Se está intentando declarar la variable \"%s\" pero la misma forma parte de los argumentos del procedimiento \"%s\"." %(pivote.name, diccionario[comp.function])
					centinela = True
				comp = comp.proc
			
			if (not(comp == pivote)) and (comp.function == pivote.function) and (not(centinela)) and (comp.isArg or pivote.isArg):
					if (pivote.isArg):
						print "Error: Se está intentando declarar la variable \"%s\" pero la misma forma parte de los argumentos del procedimiento \"%s\"." %(pivote.name, diccionario[pivote.function])
					else:
						print "Error: Se está intentando declarar la variable \"%s\" pero la misma forma parte de los argumentos del procedimiento \"%s\"." %(pivote.name, diccionario[comp.function])
					centinela = True
			pivote = pivote.proc
	
		# Ciclo para la última caja
		while not (comp.proc == None or centinela):
			if (not(comp == pivote)) and (not(centinela)) and (comp.function == pivote.function) and (comp.isArg or pivote.isArg):
				if (pivote.isArg):
					print "Error: Se está intentando declarar la variable \"%s\" pero la misma forma parte de los argumentos del procedimiento \"%s\"." %(pivote.name, diccionario[pivote.function])
				else:
					print "Error: Se está intentando declarar la variable \"%s\" pero la misma forma parte de los argumentos del procedimiento \"%s\"." %(pivote.name, diccionario[comp.function])
			comp = comp.proc
		
		if (not(comp == pivote)) and (comp.function == pivote.function) and (not(centinela)) and (comp.isArg or pivote.isArg):
				if (pivote.isArg):
					print "Error: Se está intentando declarar la variable \"%s\" pero la misma forma parte de los argumentos del procedimiento \"%s\"." %(pivote.name, diccionario[pivote.function])
				else:
					print "Error: Se está intentando declarar la variable \"%s\" pero la misma forma parte de los argumentos del procedimiento \"%s\"." %(pivote.name, diccionario[comp.function])
		
		# Caso donde la variable no tiene poblemas en una función.
		if not (centinela):
			print "Error: La variable \"%s\" ha sido declarada en un mismo bloque más de una vez." %(nombre)
				
				
	# Funcion VariablesNoProc: Impresión de las variables globales
	# y bloque principal.
	
	def VariablesNoProc(self,modo):
		# Donde el modo 0 son las variables globales.
		aux = self.inicio      
		while not (aux.sig == None):
			while not (aux.proc == None):
				if (aux.function == modo):
					print "Variable: %s | Tipo: %s | Valor: %s" %(aux.name,aux.type,aux.value)
				aux = aux.proc
			if (aux.function == modo):
				print "Variable: %s | Tipo: %s | Valor: %s" %(aux.name,aux.type,aux.value)
			if (aux.padre == None):
				aux = aux.sig
			else:
				aux = aux.padre.sig
		
		# Caso de la ultima caja.
		while not (aux.proc == None):
			if (aux.function == modo):
				print "Variable: %s | Tipo: %s | Valor: %s" %(aux.name,aux.type,aux.value)
			aux = aux.proc
		if (aux.function == modo):
			print "Variable: %s | Tipo: %s | Valor: %s" %(aux.name,aux.type,aux.value)
		
	
	
	# Funcion VariablesProc: Impresión de las variables y parámetros de
	# un procedimiento
	
	def VariablesProc(self,modo):
		print "Argumentos:"
		aux = self.inicio      
		while not (aux.sig == None):
			while not (aux.proc == None):
				if (aux.function == modo):
					if (aux.isArg):
						if (aux.isRef):
							print "   Variable: %s | Tipo: %s | Pasaje: Referencia" %(aux.name,aux.type)
						else:
							print "   Variable: %s | Tipo: %s | Pasaje: Valor" %(aux.name,aux.type)
				aux = aux.proc
			if (aux.function == modo):
				if (aux.isArg):
						if (aux.isRef):
							print "   Variable: %s | Tipo: %s | Pasaje: Referencia" %(aux.name,aux.type)
						else:
							print "   Variable: %s | Tipo: %s | Pasaje: Valor" %(aux.name,aux.type)
			if (aux.padre == None):
				aux = aux.sig
			else:
				aux = aux.padre.sig
		
		# Caso de la última caja.
		while not (aux.proc == None):
			if (aux.function == modo):
				if (aux.isArg):
					if (aux.isRef):
						print "   Variable: %s | Tipo: %s | Pasaje: Referencia" %(aux.name,aux.type)
					else:
						print "   Variable: %s | Tipo: %s | Pasaje: Valor" %(aux.name,aux.type)
			aux = aux.proc
		if (aux.function == modo):
			if (aux.isArg):
				if (aux.isRef):
					print "   Variable: %s | Tipo: %s | Pasaje: Referencia" %(aux.name,aux.type)
				else:
					print "   Variable: %s | Tipo: %s | Pasaje: Valor" %(aux.name,aux.type)
		
		
		# Variables
		print "Variables:"
		
		aux = self.inicio
			
		while not (aux.sig == None):
			while not (aux.proc == None):
				if (aux.function == modo):
					if (not (aux.isArg) and not (aux.isRef)):
						print "   Variable: %s | Tipo: %s | Valor: %s" %(aux.name,aux.type,aux.value)
				aux = aux.proc
			if (aux.function == modo):
				if (not (aux.isArg) and not (aux.isRef)):
					print "   Variable: %s | Tipo: %s | Valor: %s" %(aux.name,aux.type,aux.value)
			if (aux.padre == None):
				aux = aux.sig
			else:
				aux = aux.padre.sig
		
		# Caso de la última caja.
		while not (aux.proc == None):
			if (aux.function == modo):
				if (not (aux.isArg) and not (aux.isRef)):
					print "   Variable: %s | Tipo: %s | Valor: %s" %(aux.name,aux.type,aux.value)
			aux = aux.proc
		if (aux.function == modo):
			if (not (aux.isArg) and not (aux.isRef)):
				print "   Variable: %s | Tipo: %s | Valor: %s" %(aux.name,aux.type,aux.value)
		

	#---------------------------------------------------#
	#	Fin Funciones Impresión			    #
	#---------------------------------------------------#

#---------------------------------------------------#
#	Fin Class SymTable			    #
#---------------------------------------------------#

