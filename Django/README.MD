Instrukcja obs�ugi Django:

1. Instalacja:
	Opr�cz pythona3 i django 1.11:
	pip install djangorestframework
	pip install markdown
	pip install django-filter


2. Uruchamianie serwera Django:
	Przez wybrane ustawienia najpierw trzeba ustali� aktualny adres IP komputera, 
	nast�pnie przechodimy do folderu PKM i otwieramy plik settings.py w ALLOWED_HOSTS 
	dodajemy aktualny adres. Dzi�ki temu do serwera mog� si� dosta� inne komputery w sieci a nie tylko localhost.

	Nast�pnie w linii polece� uruchamiamy serwer:
	python manage.py runserver adres_ip:numer_portu
	
	lub te� python manage.py runserver wtedy domy�lnie b�dzie to adres 127.0.0.1 i port 8080

3.Opis aplikacji:
	W przegl�darce pod adresem adres_ip:numer_portu znajduje si� strona g��wna, wy�wietlane
	s� na niej ��dania poruszenia poci�giem.
	Aplikacja przyciski znajduje si� pod adres_ip:numer_portu/przyciski, z jej poziomu mo�na sterowa� poci�giem.
	Strona admnistratora pod adresem: adres_ip:numer_portu/admin
	Dodatkowe podstrony b�d� opisane w restowym api.

4.Dodatkowe funkcje manage.py:	
	migracje:
	python manage.py flush - usuwa aktualn� baz� danych
	
	Stworzenie nowej:
	python manage.py makemigrations przyciski
	python manage.py sqlmigrate przyciski 0001 - pierwsza migracja dla aplikacji przyciski, mog� by� inne numery i inne aplikacje
	python manage.py migrate
	
	Je�li chcemy mie� dost�p do konta administratora to tworzymy konto:
	python manage.py createsuperuser

5.Rest
	adres_ip:numer_portu/trains zwraca jsona z wszystkimi rozkazami
	
	API nie dozwala na usuwanie ani zmian� rekordu, pozwala tylko na dodanie nowego ��dania.
	Snippet pythona3 z u�ycie biblioteki request kt�ry wysy�a wymagane ��danie na localhosta i port 8000:
	
	import requests
	url = 'http://127.0.0.1:8000/train/0/'
	payload = {'id': '123123', 'device_type': '0', 'velocity': '100', 'train_identificator': '1', 'was_carried_out': '1'}
	r = requests.post(url, json=payload)
	print(r.text)
	
	train/0 si� nie zmienia i musi tak zosta�, nie oznacza to, �e jest to zapisane pod zerowym �adaniem, po prostu dodaje nowe.
	
