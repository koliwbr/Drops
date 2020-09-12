# Spis treści
 <a href="README.md#instalacja">Instalacja</a><br>
 <a href="README.md#opis-plików">Opis Plików</a><br>
 <a href="README.md#historia">Historia</a><br>
# Instalacja  
Skopjować całe repozytorium<br>
Jeśli nie zainstalowano TinyBD:<br>
 $ pip install tinydb<br>
 Uruchomić code/init.sh<br>
# Opis Plików
 users*:      - katalog do przechowywania kont użytkowników (zawartość usuwana przez clear.sh)    <br>
code:         - folder z kodem aplikacji<br>
 * serwer.sh - główny plik serwera<br>
 * log.txt* - plik z logami (usuwany przez clear.sh)
 * db.json* - zawiera listę kont (usuwany przez clear.sh)<br>
 * clear.sh - usuwa pliki (W razie potrzeby można je znalesc w /var/kosz/LosowyNumer/ ) <br>
<div>Pliki oznaczone (*) są tworzone przez skrypty</div>

# Historia
To mój pierwszy wiekszy skrypt Pythona, napisany na podstawie przykładu użycia biblioteki ,,socket''
(niestety niewiem z jakiego dokładnie źródła) i kilku innych przykładów. 
Całość jest napisana dla zabawy i nauki. Skrypt prawdopodobne zawiera kilka błędów i nieoptymalnych (i nie bezpiecznych) rozwiąń.
Nazwa gry jest losowym ciągiem. Opisy sa w większości po polsku, ale niektóre komunikaty w logach sa po angielsku.<br>
Autor: Koliw aka Mikołaj Wojtkiewicz<br>
Mail: Koliw.br@gmail.com                                                          
 
 
