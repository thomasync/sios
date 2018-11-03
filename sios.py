#!/usr/bin/python

# Créer par Thomas Cauquil - @absmoca
# https://thomascauquil.fr

import sys, os, time
import requests
import re
import hashlib
import json

class colors:
	GRAY = '\033[90m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	END = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

cls()

# Fichier à récupérer
studentsBefore = open("sios.json", "r+")
infoFile = os.stat("sios.json")
studentsBefore.seek(0, 0)

derniereModifFile = time.strftime("%d/%m/%Y - %H:%M:%S", time.localtime(infoFile.st_mtime))

try:
	studtsBefore = json.loads(studentsBefore.read())
except:	
	studtsBefore = {}


urlDefault = "http://inet.btssio.net/"
classes = ["rouchon/sio1/", "rouchon/sio2/"]

# allSio = requests.get(urlDefault)
# allSio = re.findall("href=(.*?)>", allSio.text)

print("\n\t        ____ _______ _____    _____ _____ ____  ")
print("\t       |  _ \__   __/ ____|  / ____|_   _/ __ \ ")
print("\t       | |_) | | | | (___   | (___   | || |  | |")
print("\t       |  _ <  | |  \___ \   \___ \  | || |  | |")
print("\t       | |_) | | |  ____) |  ____) |_| || |__| |")
print("\t       |____/  |_| |_____/  |_____/|_____\____/ \n\n")
print("\t    Derniere actualisation :", derniereModifFile, "\n")
studentsActuels = {}

for url in classes:
	# Nom de la classe en majuscule
	nameClasse = re.match('rouchon/(.*?)/', url).group(1).upper()

	print("--------------------------------- "+nameClasse+" ---------------------------------\n")

	# Récupère tous les étudiants
	try:
		allStudents = requests.get(urlDefault+url)
	except:
		print("Pas de connexion internet.")
		sys.exit(0)

	allStudents = re.findall(r"<a(.*?)>(.*?)</a>", allStudents.text)

	i = 0

	#Créer la classe dans le dictionnaire
	studentsActuels[nameClasse] = {}

	for student in allStudents:
		# Créer l'id de l'étudiant
		idStudent = re.sub(r'\s', '', student[1].lower())
		
		# Récupère l'url du site de l'étudiant
		urlStudent = (urlDefault+re.match(r"(.*?)\s", student[1]).group(1)).lower()		
		
		# Permet d'aligner le texte sans défauts
		calc = 70 - len(student[1])

		# Récupère le contenu du site de l'étudiant et créer un hash unique
		try:
			contentStudent = requests.get(urlStudent)
		except:
			print("Connexion interrompue.")
			sys.exit(0)
		urlHash = hashlib.md5(bytes(contentStudent.text, encoding='utf-8')).hexdigest()

		try:
			# Récupère le hash précédent
			urlHashBefore = studtsBefore[nameClasse][idStudent]["urlHash"]

			# Si le hash du contenu du site est différent du dernier hash
			if urlHash != urlHashBefore:
				print(colors.GREEN+student[1]+" "+urlHash.rjust(calc, ' ')+colors.END)
			else:
				print(student[1]+" "+urlHash.rjust(calc, ' '))
		
		except:
			# Si l'étudiant n'avait jamais été enregistré
			print(colors.YELLOW+student[1]+" "+urlHash.rjust(calc, ' ')+colors.END)
		
		# Met l'étudiant dans le dictionnaire
		studentsActuels[nameClasse][idStudent] = { "name":student[1], "url": urlStudent, "urlHash": urlHash }

		i += 1
		# if i >= 3:
		# 	break

	print("")

print(colors.GRAY+"@absmoca - https://thomascauquil.fr"+colors.END+"\n")
studentsBefore.seek(0, 0)
studentsBefore.write(json.dumps(studentsActuels))
studentsBefore.close()