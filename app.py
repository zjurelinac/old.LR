"""App configuration file and initialization file

The Flask `app` object is created here, as well as the peewee `db` database.
This module also contains app configuration options, such as database name, a not-so-secret key and debug status
"""

# Ukljucuje Flask za stvaranje objekta, i peewee za kreiranje baze.
from flask  import Flask
from peewee import *

import os

# Ovo su konfiguracijski podaci:

# Naredba koja pronađe folder u koji je smještena aplikacija
APP_ROOT = os.path.dirname( os.path.realpath( __file__ ) )

# Ime datoteke u kojoj je baza podataka
DATABASE = "linker.db"
# Tajni ključ za enkripciju cookiea u kojima se čuvaju podaci o trenutnoj sjednici
SECRET_KEY = "t!3pbh+o3zh9l3xtm!=5$+uy^7#7s7+aarxc=yb5v4!$b!o^77"
# Vrti li se aplikacija u debug modu, ako da, onda za svaku grešku i iznimku ispiše detalje i gdje je nastala - kao Java Stack Trace
DEBUG = True


# app je objekt koji je zapravo klasa aplikacije, sve bitno se nalazi u njoj
app = Flask( __name__ )
# Aplikacija ucitava postavke iz ove datoteke (__name__ predstavlja ime ovog fajla)
app.config.from_object( __name__ )
# Za testiranje se najčešće odabire SQLite baza podataka, naredbe su iste kao i
# u svim drugim SQL bazama, samo je ova baza cijela u jednoj datoteci,
# a sustav za upravljanje je biblioteka koja je u skljopu Pythona
db = SqliteDatabase( app.config[ 'DATABASE' ], threadlocals = True )
