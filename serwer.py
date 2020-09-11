#!/bin/python
PORT = 2080	# Port gry
PANEL_ADMINA=1 	# 1-tak 0-nie
LOG_FILE="log.txt" 

#####################################################################################
#                                       Koliw                                       #  
#   Autor:                               aka                                        #
#                                  Mikolaj Wojtkiewicz                              #
#                                                                                   # 
#    Pierwsz moj wiekszy skrypt Pythona, napisany na podstawie przykladu uzycia     #
# biblioteki ,,socket''(niestety niewiem z jakiego dokladnie zrodla) i kilku innych #
# przykladow. Calosc jest napisana dla zabawy i nauki. Skrypt prawdopodobne zawiera #
# kilka bledow i nieoptymalnych (i niebespiecznych) rozwiazan.  Nazwa gry jest      #
# losowym ciagiem. Opisy sa w wiekszosci po polsku, ale niektore komunikaty w logah #
# sa po angielsku.                                                                  #
#                                                                                   #
# Mail: koliw.br@gmail.com                                                          #
#####################################################################################

import socket, datetime, time, threading, string, sys
from glob     import glob
from tinydb   import TinyDB, Query
from hashlib  import sha256
log=0   #???


def log(napis):								#FUNKCJA LOGUJACA DO PLIKU
	teraz = datetime.datetime.now()
	sekunda = teraz.second
	dzien   = str(teraz.day)
	miesiac = str(teraz.month)
	rok     = str(teraz.year)
	godzina = teraz.hour
	minuta  = teraz.minute
	if sekunda<10:		#V	04 nie 4 (Dopisuje wiodace zero)
		sekunda = "0"+str(sekunda)
	else:
		sekunda = str(sekunda)
	if minuta<10:
		minuta = "0"+str(minuta)
	else:
		minuta = str(minuta)
	if godzina<10:
		godzina = "0"+str(godzina)
	else:
		godzina = str(godzina)	#      V  To zeby watki sie nie pogryzly   V
	wpis="["+godzina+":"+minuta+":"+sekunda+" "+dzien+"/"+miesiac+"/"+rok+"] "+str(napis)+"\r\n"
	print wpis
	f = open(LOG_FILE,"a")
	f.write(wpis)
	f.close()
 
#db.search(Cars.color == 'green') #Przypomnienie jak dziala bazadanych
#db.insert({'id': 1, 'name': 'car1', 'color': 'green'})

def Login(conn):							#LOGOWANIE DO GRY
	conn.sendall("Logowanie:\r\n")	
	conn.sendall("Login: ")
	login = conn.recv(1024)
	login=login[:len(login)-2]
	conn.sendall("Haslo: ")
	haslo = conn.recv(1024)
	haslo=haslo[:len(haslo)-2]
	if db.search(users.name == login) and db.search(users.sha == sha256(b""+login+haslo).hexdigest()) :
		conn.sendall("Zalogowano poprawnie!\r\n")
		conn.recv(1024)
		return login
	else:
		conn.sendall("Nie zalogowano\r\n")
		conn.recv(1024)
		login="ERROR"
		return "ERROR"
	

def stat(conn):								#STATYSTYKI
	conn.sendall(chr(27)+"[2J"+chr(27)+"[H")

	conn.sendall("Statystyki:\r\n")
	conn.sendall(" Konta posiadaja:\r\n")
	for x in glob("../users/*.json"):	# Ten galimatjas ponirzej jest tak zlorzony ze go nawet nie dotykam 
		conn.sendall("  "+x[9:(len(x)-5)]+" "*(12-len(x[6:(len(x)-5)]))+str(infog(x))+" G\r\n")
	conn.recv(1024)

def infog(url):								#INFO Gold
	DB = TinyDB(url)
	value = DB.get(Query()["gold"])
	try:
		return value.get("gold")
	except:
		return -1

def infoh(name):							#INFO haslo
	value=db.search(users.name==name)
	try:
		return value[0].get("haslo")
	except:
		return "BRAK"	

#Koliw jest super
def Nkonto(coon,adr):							#NOWE KONTO
	conn.sendall("Nowe konto\r\n")	#Pobieranie danych
	conn.sendall("Nowy Login: ")
	login=conn.recv(1024)
	login=login[:len(login)-2]	#(Obcina \r\n z wejscia)
	conn.sendall("Nowe Haslo: ")	
	haslo1=conn.recv(1024)
	haslo1=haslo1[:len(haslo1)-2]
	conn.sendall("Powtorz Haslo: ")
	haslo2=conn.recv(1024)
	haslo2=haslo2[:len(haslo2)-2]
	
	ok2=1
	if haslo1!=haslo2:
		conn.sendall("Hasla nie sa identyczne!\r\n")
		ok2=0
	if db.search(users.name == login):
		conn.sendall("Podany urzytkownik istnieje!\r\n")
		ok2=0
	if ok2:			#Wkladanie danych do baz 
		haslo=haslo1 #Zapsywanie hasla tylko dla panelu admina 
		db.insert({'name':login,'haslo':haslo,'sha':sha256(b""+login+haslo).hexdigest()})
		Re = TinyDB('../users/'+login+'.json')
		Re.insert({"kopalnie1":0,"kopalnie2":0,"kopalnie3":0,"kopalnie4":0,"gold":10})
		log(str(adr)+" stworzyl konto "+login)
		conn.sendall("Konto utworzone poprawnie!\r\n\r\n")
		conn.sendall("       [ZALOGUJ]")
	conn.recv(1024)



def admin(conn): #UWAGA czyta hasla uzytkownikow 
	conn.sendall(chr(27)+"[H"+chr(27)+"[2J"+"Users:\r\nname  gold  pass\r\n")

	for x in glob("../users/*.json"):
			name=x[9:(len(x)-5)]
			conn.sendall(name+"   "+str(infog(x))+"   "+infoh(name)+"\r\n")
	conn.recv(1024)


def adminp(conn):		        #STARA FUNKCJA DO LOGOWANIA 
	conn.sendall(chr(27)+"[2J")     #do panelu "admina" (Mniej bezpieczna)
	conn.sendall(chr(27)+"[H") 
			 	  #Nowa jest w tytulowym panelu 
	conn.sendall("Admin:")     #Zostalo dla pamieci 
	login_a=conn.recv(1024)
	haslo_a=conn.recv(1024)
	login_a=login_a[:len(login_a)-2]
	login_a=login_a[:len(login_a)-2]
	
	#print sha256(b""+login_a+haslo_a).hexdigest() # ZMIANA HASLA (RENCZNA)
	#if sha256(b""+login_a+haslo_a).hexdigest()=="b4aeeb0d2fc565490af1eabf4ba04e4cf84358db49f3a2c5550c201732325ca7": # L:koliw H:haslo #STARE		
		#admin(conn) #od komentowaci jesli adminp() ma dzialac (if'a tez)
	

	
		
def client(conn,adr):					#START KOD
	try:
		while 1:
			ok1 = 1
			adm=0
			while ok1:
				conn.sendall(chr(27)+"[2J")
				conn.sendall(chr(27)+"[H")

				conn.sendall("""Autor: Koliw
	 ______    ________  ________  ________  ________ 
	|  __  \  |  ____  | |  ___  | |  ____ | /  ____ \ 
	| |  \  \ | |    | | | (   ) | | (    )| | (    \/
	| |   | | | |____| | | |   | | | (____)| | (_____ 
	| |   | | |  _  ___/ | |   | | |  _____) (_____  )
	| |   | | | | \ \    | |   | | | |             ) |
	| |__/  / | |  \ \__ | (___) | | |       /\____) |
	|______/  |/    \__/ |_______| |/        \_______)

	Witaj w Dropsie
		Darmowej grze internetowej

	    [1] Zaloguj
	    [2] Utworz konto
	    [3] Statystyki
	    [4] Wyjscie
	       >""")

				data = conn.recv(1024)

				if data=="1\r\n":
								#zaloguj
					login=Login(conn)
					if login!="ERROR":
						ok1=0
				if data=="2\r\n":
								#nowe konto
					Nkonto(conn,adr)
				if data=="4\r\n":
								#wyjscie
					conn.sendall("Pa pa.\r\n")
					log("Conection close by"+str(adr))
					conn.close()
					return 0

				if data=="3\r\n":
								#statystyki
					stat(conn)
				if adm==2:		#Panel admina (patrz: @ADMIN)
					has=data		#trzeci
					log=log[:len(log)-2]
					has=has[:len(has)-2]
					#print sha256(b""+log+has).hexdigest() #renczna zmiana hasla
	 				if sha256(b""+log+has).hexdigest()=="24ab2ed7b877e2b860cc936b11310e9dcf500219a897dc144fa1aa0b3e36e0e9": # login:log_kol haslo:osiem	
						log(str(adr)+"Udalo sie zalogowac do panelu admina")
						admin(conn)
					else:
						log(str(adr)+"Nie udalo sie zalogowac do panelu admina. login:"+log+" haslo:"+has)
					adm=0			 #              /\
				if adm==1:				#drugi  |
					log=data
					adm=2			  #			       /\
				if data=="admin\r\n"&&PANEL_ADMINA #      @ADMIN  Pierwsz krok   |  
					#adminp(conn)
					log(str(adr)+"loguje sie do panelu admina")
					adm=1


			#zalogowano

			log(str(adr)+" zalogowal sie jako "+login)
			Re = TinyDB('../users/'+login+'.json') 
			Re_tab = Query()
			err='Nie wiesz co robic? wpisz "lis"'
			lis=1
			spi=1
			koniec=1
			while koniec:						#myslenie
									#Wczytywanie danych
				conn.sendall(chr(27)+"[2J"+chr(27)+"[H")

				gold = Re.get(Query()['gold'])
				gold = gold.get('gold')	

				kopalnie1 = Re.get(Query()['kopalnie1'])
				kopalnie2 = Re.get(Query()['kopalnie2'])
				kopalnie3 = Re.get(Query()['kopalnie3'])
				kopalnie4 = Re.get(Query()['kopalnie4'])

				kopalnie1 = kopalnie1.get('kopalnie1')
				kopalnie2 = kopalnie2.get('kopalnie2')
				kopalnie3 = kopalnie3.get('kopalnie3')
				kopalnie4 = kopalnie4.get('kopalnie4')

									#liczenie
				conoc=kopalnie1+kopalnie2*10+kopalnie3*50+kopalnie4*100
				if spi:		
					gold+=conoc
				spi=0
								#pisanie
				conn.sendall("Witaj "+login+"\r\n")
											#godzine nad tym siedzialem
				conn.sendall(" "+"_"*80+"\r\n") #80 znaki _
				conn.sendall("/      Przychody"+" "*65+"\\\r\n")
				conn.sendall("|"+"-"*80+"|\r\n")
				conn.sendall("| Kopalnie Mk1: "+str(kopalnie1) + " "*(63-len(str(kopalnie1*1)+str(kopalnie1)))   + str(kopalnie1)    + "G |\r\n")
				conn.sendall("| Kopalnie Mk2: "+str(kopalnie2) + " "*(63-len(str(kopalnie2*10)+str(kopalnie2)))  + str(kopalnie2*10) + "G |\r\n")
				conn.sendall("| Kopalnie Mk3: "+str(kopalnie3) + " "*(63-len(str(kopalnie3*50)+str(kopalnie3)))  + str(kopalnie3*50) + "G |\r\n")	
				conn.sendall("| Kopalnie Mk4: "+str(kopalnie4) + " "*(63-len(str(kopalnie4*100)+str(kopalnie4))) + str(kopalnie4*100)+ "G |\r\n")
				conn.sendall("|"+ " "*80+"|"+"\r\n"+"|"+ " "*80+"|\r\n")
				conn.sendall("|"+" "*(78-len(str( gold ))) + str(gold) +" G|\r\n") #80-2( G)=78
				conn.sendall("\\"+"_"*80+"/\r\n\r\n")

				conn.sendall(err+"\r\n")  #Panel na bledy (uzywany tez do innych celi)
				if lis:
			 		err="Nie wiesz co robic? wpisz 'lis'"
				else:
					err=""	
						
			#	co? Ile? Za co?		
			#	mk1 10   1
			#	mk2 50   10
			#	mk3 200  50
			#	mk4 1000 100

				dane=conn.recv(1024)				#ODBIERANIE DANYCH i ich interpretacja
				comend=dane[:3]
				param=dane[4:7]
				if comend=="kup":	#Kupno
					if param=="mk1":
						if gold>=10:
							kopalnie1 += 1
							gold-=10
						else:
							err="Nie masz tyle pieniendzy (10)"
					if param=="mk2":	
						if gold>=50:
							kopalnie2 += 1
							gold-=50
						else:
							err="Nie masz tyle pieniendzy (50)"
					if param=="mk3":		
						if gold>=200:
							kopalnie3 += 1
							gold-=200
						else:
							err="Nie masz tyle pieniendzy (200)"
					if param=="mk4":		
						if gold>=1000:
							kopalnie4 += 1
							gold-=1000
						else:
							err="Nie masz tyle pieniendzy (1000)"
				
				if comend=="spi":
					spi=1		
				if comend=="lis":
					lis=0
					err="""
		kup - kupuje kopalnie mk(1-4)
			Produkt  Cena   Produkcja/dzien
			mk1      10     1 
			mk2      50     10
			mk3      200    50
			mk4      1000   100
		*ceny wyrazone w G (gold)

		spi - spanie (podczas spania kopalnie kopia)
		lis - ta lista
		qui - wylogowuje
		
		Autor - Mikolaj Wojtkiewicz"""
				if comend=="qui":
					koniec=0
								#zapisywanie zmian				
				Re.update({'gold':gold,'kopalnie1':kopalnie1,'kopalnie2':kopalnie2,'kopalnie3':kopalnie3,'kopalnie4':kopalnie4})
					# ^ Dobrze by bylo zamienic to na czyczenie i wkladanie nowych danych ^  
	except socket.error:
		log("Conection close with error by"+str(adr))
	#except:
	#	print "Nieobslugiwany blad:",sys.exc_info()
#Koniec funkcji glownej


db = TinyDB('db.json')		#Inicjacja bazy danych 
users = Query()			#i wyszukiwarki
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Watek(threading.Thread):					#watki klasa
    def __init__(self, value, value2):		#Nie ogarniam za bardzo 
        threading.Thread.__init__(self)		#zywcem z przykladu
        self.value = value
	4ut0r="K0liw"
        self.value2 = value2
    def run(self):
        ret = client(self.value,self.value2)

#print chr(27)+"[2J"+chr(27)+"[H"
print "Waiting for socket"
conect=1
timesocket=0
while conect:
	try:
		s.bind(("",PORT))
	except:
		conect+=1				#Oczekiwanie na zwolnienie gniazda przez system (Linux) 
		time.sleep(1)				#Jesli dlorzej niz 120s. to jakis inn blad (np. brak dostepu)
		print chr(27)+"[2J"+chr(27)+"[H"
		timesocket+=1
		if conect==2:
			print "Waiting for socket.   "+str(timesocket)+"s."
		if conect==3:
			print "Waiting for socket..  "+str(timesocket)+"s."
		if conect==4:
			print "Waiting for socket... "+str(timesocket)+"s."
			conect=1
			  
	else:
		conect=0
#print chr(27)+"[2J"+chr(27)+"[H"
print "Waiting for socket [OK]  "+str(timesocket)+"s."
s.listen(1)
while 1:
	conn, addr = s.accept()			#Petla odbierajaca polaczenia 
	log('Connected by'+str(addr))
	Watek(conn,addr).start()		
