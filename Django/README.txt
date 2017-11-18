Instrukcja obs³ugi Django:

1. Instalacja:
	Oprócz pythona3 i django 1.11:
	pip install djangorestframework
	pip install markdown
	pip install django-filter


2. Uruchamianie serwera Django:
	Przez wybrane ustawienia najpierw trzeba ustaliæ aktualny adres IP komputera, 
	nastêpnie przechodimy do folderu PKM i otwieramy plik settings.py w ALLOWED_HOSTS 
	dodajemy aktualny adres. Dziêki temu do serwera mog¹ siê dostaæ inne komputery w sieci a nie tylko localhost.

	Nastêpnie w linii poleceñ uruchamiamy serwer:
	python manage.py runserver adres_ip:numer_portu
	
	lub te¿ python manage.py runserver wtedy domyœlnie bêdzie to adres 127.0.0.1 i port 8080

3.Opis aplikacji:
	W przegl¹darce pod adresem adres_ip:numer_portu znajduje siê strona g³ówna, wyœwietlane
	s¹ na niej ¿¹dania poruszenia poci¹giem.
	Aplikacja przyciski znajduje siê pod adres_ip:numer_portu/przyciski, z jej poziomu mo¿na sterowaæ poci¹giem.
	Strona admnistratora pod adresem: adres_ip:numer_portu/admin
	Dodatkowe podstrony bêd¹ opisane w restowym api.

4.Dodatkowe funkcje manage.py:	
	migracje:
	python manage.py flush - usuwa aktualn¹ bazê danych
	
	Stworzenie nowej:
	python manage.py makemigrations
	python manage.py sqlmigrate przyciski 0001 - pierwsza migracja dla aplikacji przyciski, mog¹ byæ inne numery i inne aplikacje
	python manage.py migrate
	
	Jeœli chcemy mieæ dostêp do konta administratora to tworzymy konto:
	python manage.py createsuperuser

5.Rest
	adres_ip:numer_portu/trains zwraca jsona z wszystkimi rozkazami
	
	
