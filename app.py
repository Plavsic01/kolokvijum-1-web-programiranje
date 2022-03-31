from flask import Flask,url_for,redirect,render_template,request
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)

app.config["MYSQL_DATABASE_HOST"] = "localhost"
app.config["MYSQL_DATABASE_PORT"] = 3306
app.config["MYSQL_DATABASE_USER"] = "root" 
app.config["MYSQL_DATABASE_PASSWORD"] = "Najbolji3" 
app.config["MYSQL_DATABASE_DB"] = "prodavnica"

mysql = MySQL(app,cursorclass=pymysql.cursors.DictCursor)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dodaj/kupac",methods=["GET","POST"])
def dodaj_kupac():
    if request.method == "POST":
        novi_kupac = dict(request.form)
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO kupac(korisnickoIme,lozinka,ime,prezime) VALUES (%s,%s,%s,%s);"\
            ,(novi_kupac['korisnickoIme'],novi_kupac['lozinka'],novi_kupac['ime'],novi_kupac['prezime']))
        db.commit()
        return redirect(url_for('prikaz_kupaca'))
    return render_template("dodaj_kupac.html")

@app.route("/kupci")
def prikaz_kupaca():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id,korisnickoIme,lozinka,ime,prezime FROM kupac;")
    kupci = cursor.fetchall()
    return render_template("prikaz_kupci.html",kupci=kupci)


@app.route("/detalji/kupac/<int:id>")
def detalji_kupac(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id,korisnickoIme,lozinka,ime,prezime FROM kupac WHERE id=%s;",(id))
    jedan_kupac = cursor.fetchone()
    return render_template("detalji_kupac.html",jedan_kupac=jedan_kupac)


@app.route("/izmeni/kupac/<int:id>",methods=["GET","POST"])
def izmeni_kupac(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id,korisnickoIme,lozinka,ime,prezime FROM kupac WHERE id=%s;",(id))
    jedan_kupac = cursor.fetchone()

    if request.method == "POST":
        izmenjen_kupac = dict(request.form)
        cursor.execute("UPDATE kupac SET korisnickoIme = %s,lozinka = %s,ime = %s, prezime = %s WHERE id = %s;",\
            (izmenjen_kupac['korisnickoIme'],izmenjen_kupac['lozinka'],izmenjen_kupac['ime'],izmenjen_kupac['prezime'],izmenjen_kupac['id']))
        db.commit()
        return redirect(url_for('prikaz_kupaca'))

    return render_template("izmeni_kupac.html",jedan_kupac=jedan_kupac)


@app.route("/obrisi/kupac/<int:id>")
def obrisi_kupac(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM kupac WHERE id=%s",(id))
    db.commit()
    return redirect(url_for('prikaz_kupaca'))


# PROIZVODI #

@app.route("/proizvodi")
def prikaz_proizvoda():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM proizvod;")
    proizvodi = cursor.fetchall()
    return render_template("prikaz_proizvoda.html",proizvodi=proizvodi)



@app.route("/dodaj/proizvod",methods=["GET","POST"])
def dodaj_proizvod():
    db = mysql.get_db()
    cursor = db.cursor()
    if request.method == "POST":
        novi_proizvod = dict(request.form)
        cursor.execute("INSERT INTO proizvod(naziv,opis,cena,dostupno) VALUES (%s,%s,%s,%s);",\
            (novi_proizvod['naziv'],novi_proizvod['opis'],novi_proizvod['cena'],novi_proizvod['dostupno']))
        db.commit()
        return redirect(url_for('prikaz_proizvoda'))
    return render_template("dodaj_proizvod.html")


@app.route("/detalji/proizvod/<int:id>")
def detalji_proizvod(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id,naziv,opis,cena,dostupno FROM proizvod WHERE id=%s;",(id))
    jedan_proizvod = cursor.fetchone()
    return render_template("detalji_proizvod.html",jedan_proizvod=jedan_proizvod)


@app.route("/izmeni/proizvod/<int:id>",methods=["GET","POST"])
def izmeni_proizvod(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id,naziv,opis,cena,dostupno FROM proizvod WHERE id=%s;",(id))
    jedan_proizvod = cursor.fetchone()

    if request.method == "POST":
        izmenjen_proizvod = dict(request.form)
        cursor.execute("UPDATE proizvod SET naziv = %s,opis = %s, cena = %s, dostupno = %s WHERE id = %s;",\
            (izmenjen_proizvod['naziv'],izmenjen_proizvod['opis'],izmenjen_proizvod['cena'],izmenjen_proizvod['dostupno'],id))
        db.commit()
        return redirect(url_for('prikaz_proizvoda'))

    return render_template("izmeni_proizvod.html",jedan_proizvod=jedan_proizvod)


@app.route("/obrisi/proizvod/<int:id>")
def obrisi_proizvod(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM proizvod WHERE id=%s",(id))
    db.commit()
    return redirect(url_for('prikaz_proizvoda'))


# KUPOVINA

@app.route("/kupovine")
def prikaz_kupovine():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM kupovina;")
    kupovine = cursor.fetchall()
    return render_template("prikaz_kupovine.html",kupovine=kupovine)


@app.route("/dodaj/kupovinu",methods=["GET","POST"])
def dodaj_kupovinu():
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id,korisnickoIme FROM kupac;")
    id_kupci = cursor.fetchall()
    cursor.execute("SELECT id,naziv,dostupno FROM proizvod;")
    id_proizvodi = cursor.fetchall()

    if request.method == "POST":
        nova_kupovina = dict(request.form)
        for proizvod in id_proizvodi:
            if proizvod['id'] == int(nova_kupovina['proizvod_id']):
                if proizvod['dostupno'] != 0:            
                    cursor.execute("INSERT INTO kupovina(kupac_id,proizvod_id,kolicina,cena,datumKupovine) VALUES (%s,%s,%s,%s,%s);",\
                        (nova_kupovina['kupac_id'],nova_kupovina['proizvod_id'],nova_kupovina['kolicina'],nova_kupovina['cena'],nova_kupovina['datumKupovine']))
                    db.commit()
                    return redirect(url_for('prikaz_kupovine'))
                return redirect(url_for('dodaj_kupovinu'))
    return render_template("dodaj_kupovinu.html",id_kupci=id_kupci,id_proizvodi=id_proizvodi)


@app.route("/izmeni/kupovinu/<int:id>",methods=["GET","POST"])
def izmeni_kupovinu(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id,korisnickoIme FROM kupac;")
    id_kupci = cursor.fetchall()
    cursor.execute("SELECT id,naziv FROM proizvod;")
    id_proizvodi = cursor.fetchall()
    cursor.execute("SELECT id,kupac_id,proizvod_id,kolicina,cena,datumKupovine FROM kupovina WHERE id=%s;",(id))
    jedna_kupovina = cursor.fetchone()

    datum_vreme = jedna_kupovina['datumKupovine']
    datum_vreme = str(datum_vreme)
    novi = datum_vreme.replace(" " ,"T")
    print(novi)

    if request.method == "POST":
        izmenjena_kupovina = dict(request.form)
        cursor.execute("UPDATE kupovina SET kupac_id = %s,proizvod_id = %s,kolicina = %s, cena = %s, datumKupovine = %s WHERE id = %s;",\
            (izmenjena_kupovina['kupac_id'],izmenjena_kupovina['proizvod_id'],izmenjena_kupovina['kolicina'],izmenjena_kupovina['cena'],izmenjena_kupovina['datumKupovine'],id))
        db.commit()
        return redirect(url_for('prikaz_kupovine'))

    return render_template("izmeni_kupovinu.html",jedna_kupovina=jedna_kupovina,id_kupci=id_kupci,id_proizvodi=id_proizvodi,datum_vreme=novi)


@app.route("/detalji/kupovina/<int:id>")
def detalji_kupovine(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id,kupac_id,proizvod_id,kolicina,cena,datumKupovine FROM kupovina WHERE id=%s;",(id))
    jedna_kupovina = cursor.fetchone()
    cursor.execute("SELECT id,korisnickoIme FROM kupac WHERE id = %s;",(jedna_kupovina['kupac_id']))
    id_kupac = cursor.fetchone()
    cursor.execute("SELECT id,naziv FROM proizvod WHERE id = %s;",(jedna_kupovina['proizvod_id']))
    id_proizvod = cursor.fetchone()

    datum_vreme = jedna_kupovina['datumKupovine']
    datum_vreme = str(datum_vreme)
    vreme_formatirano = datum_vreme.replace(" " ,"T")
    
    return render_template("detalji_kupovina.html",jedna_kupovina=jedna_kupovina,id_kupac=id_kupac,id_proizvod=id_proizvod,datum_vreme=vreme_formatirano)


@app.route("/brisanje/kupovine/<int:id>")
def obrisi_kupovinu(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM kupovina WHERE id=%s",(id))
    db.commit()
    return redirect(url_for('prikaz_kupovine'))


# PRETRAGA PROIZVODA PO SVIM ATRIBUTIMA

@app.route("/pretraga/proizvoda",methods=["GET","POST"])
def pretraga_proizvoda():
    proizvod = ""
    if request.method == "POST":
        pretraga = dict(request.form)
        db = mysql.get_db()
        cursor = db.cursor()
        if pretraga['id'] != '':
            cursor.execute("SELECT * FROM proizvod WHERE id = %s;",(pretraga['id']))
            proizvod = cursor.fetchall()
        elif pretraga['naziv'] != '':
            cursor.execute("SELECT * FROM proizvod WHERE naziv = %s;",(pretraga['naziv']))
            proizvod = cursor.fetchall()
        elif pretraga['opis'] != '':
            cursor.execute("SELECT * FROM proizvod WHERE opis = %s;",(pretraga['opis']))
            proizvod = cursor.fetchall()
        elif pretraga['cena_veca'] != '' and pretraga['cena_manja'] != '':
            cursor.execute("SELECT * FROM proizvod WHERE cena BETWEEN %s AND %s;",(pretraga['cena_manja'],pretraga['cena_veca']))
            proizvod = cursor.fetchall()
        elif pretraga['dostupno'] != '':
            cursor.execute("SELECT * FROM proizvod WHERE dostupno = %s;",(pretraga['dostupno']))
            proizvod = cursor.fetchall()

    return render_template("pretraga_proizvoda.html",proizvod=proizvod)


if __name__ == "__main__":
    app.run()