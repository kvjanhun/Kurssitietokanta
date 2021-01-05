import sqlite3

db = sqlite3.connect("kurssit.db")
db.isolation_level = None
c = db.cursor()

def vuoden_op_summa():
    syote = input("Anna vuosi: ")
    vuosi = syote + "-%"
    try:
        c.execute("SELECT SUM(K.laajuus) "
                "FROM Kurssit K, Suoritukset S "
                "WHERE K.id=S.kurssi_id AND S.arvosana>=1 AND S.paivays LIKE ?", [vuosi])
    except:
        return "Tietokantaa ei löytynyt tai virhe kyselyssä."
    tulos = c.fetchone()
    if tulos[0] != None:
        return f"Opintopisteiden määrä: {tulos[0]}"
    else:
        return f"Vuotta '{syote}' ei löytynyt tietokannasta."

def tulosta_kurssit(kurssit:list):
    if type(kurssit) != list:
        print(kurssit)
    else:
        print(f'{"kurssi":12}{"op":4}{"päiväys":16}{"arvosana"}')
        for kurssi in kurssit:
            print(f"{kurssi[0]:5}\t{kurssi[1]:5}\t{kurssi[2]:5}\t{kurssi[3]}")

def opiskelijan_kurssit():
    nimi = input("Anna opiskelijan nimi: ")
    try:
        c.execute("SELECT K.nimi, K.laajuus, S.paivays, S.arvosana "
                "FROM Opiskelijat O, Kurssit K, Suoritukset S "
                "WHERE O.id=S.opiskelija_id AND K.id=S.kurssi_id AND O.nimi=? "
                "ORDER BY S.paivays", [nimi])
    except:
        return "Tietokantaa ei löytynyt tai virhe kyselyssä."
    tulos = c.fetchall()
    if tulos:
        return tulos
    else:
        return f"Opiskelijaa ei löytynyt."

def kurssin_ka():
    kurssi = input("Anna kurssin nimi: ")
    try:
        c.execute("SELECT COUNT(S.arvosana), SUM(S.arvosana) "
                "FROM Kurssit K, Suoritukset S "
                "WHERE K.id=S.kurssi_id AND K.nimi=?", [kurssi])
    except:
        return "Tietokantaa ei löytynyt tai virhe kyselyssä."
    haun_tulos = c.fetchone()
    if haun_tulos[0] > 0:
        kpl = haun_tulos[0]
        arvosanat = haun_tulos[1]
        return f"Keskiarvo: {arvosanat/kpl:.2f}"
    else:
        return f"Kurssia ei löytynyt"

def tulosta_opettajat(opet:list):
    if type(opet) != list:
        print(opet)
    else:
        print(f'{"opettaja":20}{"op"}')
        for ope in opet:
            print(f"{ope[0]:20}{ope[1]}")

def opettajat_topX_op():
    maara = input("Anna opettajien määrä: ")
    try:
        c.execute("SELECT O.nimi, SUM(K.laajuus) "
                "FROM Opettajat O, Kurssit K, Suoritukset S "
                "WHERE O.id=K.opettaja_id AND K.id=S.kurssi_id "
                "GROUP BY O.nimi "
                "ORDER BY SUM(K.laajuus) DESC LIMIT ?", [maara])
    except:
        return "Tietokantaa ei löytynyt tai virhe kyselyssä."
    haun_tulos = c.fetchall()
    return haun_tulos

def kayttoliittyma():
    print(60*"=")
    print("\t K U R S S I T I E T O K A N T A")
    print(60*"=")
    print("Toiminnot:")
    print("1 - Valittuna vuonna saatujen opintopisteiden yhteismäärä")
    print("2 - Valitun opiskelijan kaikki suoritetut kurssit")
    print("3 - Valitun kurssin suoritusten keskiarvo")
    print("4 - Eniten opintopisteitä antaneet opettajat")
    print("5 - Poistu ohjelmasta")
    print(60*"=")    
    while True:
        valinta = input("Valitse toiminto: ")
        if valinta == "1":
            print(vuoden_op_summa())
            print("---")
        elif valinta == "2":
            tulosta_kurssit(opiskelijan_kurssit())
            print("---")
        elif valinta == "3":
            print(kurssin_ka())
            print("---")
        elif valinta == "4":
            tulosta_opettajat(opettajat_topX_op())
            print("---")
        elif valinta == "5":
            return
        else:
            print("Valitse toiminto kirjoittamalla numero 1-5.")
            print("---")
        
kayttoliittyma()
