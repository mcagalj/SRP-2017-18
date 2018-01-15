# **Sigurnost računala i podataka**

- [Python i Scapy skripte](#python-i-scapy-skripte)
- [Upravljanje korisnicima i kontrola pristupa na Linux OS](#upravljanje-korisnicima-i-kontrola-pristupa-na-linux-os)
  - [A. Dodavanje novog korisnika](#a-dodavanje-novog-korisnika)
  - [B. Prava pristupa datotekama](#b-prava-pristupa-datotekama)
  - [C. Linux procesi i kontrola pristupa](#c-linux-procesi-i-kontrola-pristupa)
  - [Reference](#reference)

## FESB, Računarstvo, 2017/18

Na ovom GitHub repozitoriju profesor će objavljivati upute, dijelove koda, konfiguracijske skripte, i druge sugestije vezane uz predmet a sa svrhom povećanja produktivnosti studenta tijekom rada na laboratorijskim vježbama.

## Python i Scapy skripte

U direktoriju [scapy](/scapy) možete naći nekoliko Python skripti za testiranje i demonstraciju određenih ranjivosti računalnih mreža. Skripte koriste izvrnu biblioteku za manipulaciju mrežnih paketa [Scapy](http://www.secdev.org/projects/scapy).

Za pokretanje skripti koristite Linux OS (npr. [Kali Linux](https://www.kali.org/)) kao i Python 2.7. Kali Linux možete instalirati kao virtualni stroj na Windows računalo koristeći npr. [Oracle VirtualBox](https://www.virtualbox.org).

**VAŽNO:** _Skripte služe isključivo u edukacijske svrhe i kao takve trebaju se koristiti u kontroliranom okruženju. Ne odgovaramo za eventualnu štetu nastalu zloporabom ovih skripti._

## Upravljanje korisnicima i kontrola pristupa na Linux OS

U okviru ove vježe student će se upoznati s osnovnim postupkom upravljanja korisničkim računima na Linux OS-u. Pri tome će se poseban naglasak staviti na **kontrolu pristupa (eng. _access control_)** datotekama, programima i drugim resursima Linux sustava.

Za listu i opis Linux naredbi potrebnih za realizaciju zadataka u nastavku konzultirajte dokument naveden pod [Reference](#reference).

### A. Dodavanje novog korisnika

Na Linux OS-u svaka datoteka ili program (_binary executable file_) ima vlasnika (_user_). Svakom korisniku pridjeljen je jedinstveni identifikator _User ID (UID)_. Svaki korisnik mora pripadati barem jednoj grupi (_group_), pri čemu više korisnika može dijeliti istu grupu. Linux grupe također imaju jedinstvene identifikatore _Group ID (GID)_.

Svoj `uid`, `gid` i pripadnost grupama možete provjeriti kako je prikazano u nastavku:

```bash
root@kali:~$ id
uid=0(root) gid=0(root) groups=0(root)
```

1. Kreirajte novi korisnički račun za sebe, odnosno dodajte sebe kao novog korisnika (npr. `mcagalj`). Pri tome možete koristiti naredbe `adduser, deluser, userdel, usermod`. Logirajte se kao novi korisnik i saznajte vaš UID, GID, grupe kojim pripadate.

    _Napomena:_ Prilikom kreiranja novog korisnika koristite naredbu `adduser` (ne `useradd`).

    ```bash
    root@kali:~$ adduser mcagalj
    Adding user `mcagalj` ...
    Adding new group `mcagalj` (1001) ...
    Adding new user `mcagalj` (1001) with group `mcagalj` ...
    Creating home directory `/home/mcagalj` ...
    Copying files from `/etc/skel` ...
    Enter new UNIX password:
    Retype new UNIX password:
    ```

### B. Prava pristupa datotekama

1. Logirajte se u sustav kao novi korisnik (npr. `mcagalj`). U `home` direktoriju kreirajte direktorij `Sigurnost`. U tom direktoriju kreirajte datoteku `sigurnost.txt` te u nju upište proizvoljni tekst. Korisne naredbe `mkdir`, `cd`, `echo "Ovo je moj tekst" > sigurnost.txt`.

    Primjenom naredbe `ls -lh` izlistajte informacije o novom direktoriju i datoteci. Odredite vlasnike ovih resursa (korisnike i grupe) kao i dopuštenja (_access permissions_) definirana na njima.

2. Pokušajte pročitati sadržaj datoteka `/etc/passwd` i `/etc/shadow`; provjerite je li navedene datoteke sadržavaju vaše informacije; informacije o korisniku kojeg ste dodali u sustav.

    Sadržaj datoteke možete provjeriti na više načina (npr. za datoteku `/etc/passwd`):

    ```bash
    mcagalj@kali:~$ cat /etc/passwd
    mcagalj@kali:~$ more /etc/passwd
    mcagalj@kali:~$ tail -n 5 /etc/passwd
    ```

    Što ste uočili prilikom pokušaja pristupa navedenim datotekama? Objasnite razlog tog ishoda; odredite vlasnike navedenih datoteka (korisnike i grupe) kao i dopuštenja definirana na njima. Pri tome možete koristiti informacije o datotekama koje vam daje naredba `ls`. Naredbu `ls` koristite kako je prikazano u nastavku:

    ```bash
    mcagalj@kali:~$ ls -lh /etc/passwd
    mcagalj@kali:~$ ls -lh /etc/shadow
    ```

    Alternativno, možete koristiti naredbu `getfacl`:

    ```bash
    mcagalj@kali:~$ getfacl /etc/passwd
    mcagalj@kali:~$ getfacl /etc/shadow
    ```

3. Oduzmite pravo pristupa datoteci `sigurnost.txt` vašem korisniku modifikacijom dopuštenja (_access permissions_) ali na način da u tom postupku ne oduzimate (**r**) dopuštenje korisniku. Za promjenu dopuštenja koristite naredbu `chmod`, npr.:

    ```bash
    # Oduzimanje dopuštenja pisanja u datoteku vlasniku datoteke
    mcagalj@kali:~/Sigurnost$ chmod -v u-w sigurnost.txt

    # Oduzimanje dopuštenja čitanja sadržaja vlasniku i grupi
    mcagalj@kali:~/Sigurnost$ chmod -v u-r,g-r sigurnost.txt

    # Prethodni primjer sa skraćenom notacijom
    mcagalj@kali:~/Sigurnost$ chmod -v ug-r sigurnost.txt

    # Davanje dopuštenja za izvršavanje datoteke grupi
    mcagalj@kali:~/Sigurnost$ chmod -v g+x sigurnost.txt

    # Davanje dopuštenja svim ostalim korisnicima za
    # ispisivanje/listanje (`ls`) sadržaja direktorija (read)
    # i ulaska (`cd`) u direktorij (execute)
    mcagalj@kali:~/Sigurnost$ chmod -v o=rx sigurnost.txt
    ```

     U dokumentu navedenom pod [Reference](#reference) možete naći dodatne primjere primjene `chmod` naredbe.

4. Nastavno na prethodni zadatak, kreirajte još jednog korisnika (npr. `iivic`) te mu omogućite pristup sadržaju datoteke `sigurnost.txt`. Napravite ovo na način da novi korisnik ima pristu datoteci isključivo ako je član grupe kojoj pripada datoteka `sigurnost.txt` (u ovom primjeru grupi `mcagalj`). _Hint:_ Osim dodjele novog korisnika spomenutoj grupi trebate modificirati i jedno pravo na direktoriju `Sigurnost`.

    Novom korisniku (`iivic`) možete omogućiti članstvo u dopunskoj grupi `mcagalj` na sljedeći način:

    ```bash
    root@kali:~$ usermod -G mcagalj iivic
    ```

    Popis grupa i informacija o grupama na Linux OS-u nalazi se u datoteci `/etc/group`.

    ```bash
    # Izlistaj sve grupe
    root@kali:~$ cat /etc/group

    # Izlistaj sve grupe i filtriraj grupu `mcagalj`
    root@kali:~$ cat /etc/group | grep mcagalj

    # Ukloni korisnika `iivic`-a iz dopunske grupe
    root@kali:~$ usermod -G "" iivic
    ```

    Uvjerite se da ste realizirali scenarij u kojem ste vlasniku datoteke `sigurnost.txt` uskratili pristup istoj dok istovremeno novi korisnik (npr. `iivic`) može pristupiti datoteci.

5. Koristeći saznanja iz prethodnog zadatka pokušajte vašem prvom korisniku (u našem primjeru `mcagalj`) omogućiti pristup sadržaju datoteke `/etc/shadow`. _Hint:_ Provjerite primarnu grupu navedene datoteke (možete koristit naredbu `ls -lh /etc/shadow`).

### C. Linux procesi i kontrola pristupa

Linux procesi su programi koji se trenutno izvršavaju u odgovarajućem adresnom prostoru. Trenutno aktivne procese možete izlistati korištnjem naredbe `ps -ef` (`ps -aux` za detaljniji prikaz). Svakom procesu dodjeljen je jedinstveni identifikator _process identifier (PID)_.

1. Kreirajte Python skriptu sljdećeg sadržaja:

    ```Python
    #!/usr/bin/evn python
    import os

    print('Real, effective and saved UIDs:')
    print(os.getresuid())
    ```

    Pokrenite skriptu kao dva različita korisnika (u našem primjeru npr. `mcagalj` i `iivic`). Komentirajte ispis skripte. Po potrebi prilagodite dozvole (_access permissions_) nad skriptom tako da oba korisnika mogu izvršiti istu.

2. Promjenite dopuštenja za datoteku `sigurnost.txt` tako da samo vlasnik datoteke (npr. `mcagalj`) može čitati istu. Modificirajte Python skriptu iz prethodnog zadatka tako da ista učitava i ispisuje sadržaj datoteke `sigurnost.txt`.

    ```Python
    #!/usr/bin/evn python
    import os

    print('Real, effective and saved UIDs:')
    print(os.getresuid())

    with open('/home/mcagalj/Sigurnost/sigurnost.txt', 'r') as f:
        print(f.read())
    ```

    Pokrenite skriptu kao dva različita korisnika (u našem primjeru npr. `mcagalj` i `iivic`). Komentirajte ispis skripte.

3. U nastavku ćemo pokušati omogućiti korisniku koji nije vlasnik Python skripte (`iivic` u našem primjeru) uspješno izvršenje prethodne zadaće. Na sličan način Linux OS omogućava _običnim_ korisnicima (bez _root_ privilegija) pristup programima i resursima koje zahtjevaju administratorske (_root_) ovlasti.

    Budući da ova tehnika radi samo za _executables_ a ne i za skripte, u prvom koraku ćemo konvertirati našu Python skriptu u _executable_ datoteku. Pri tome ćemo korisititi program [PyInstaller](http://www.pyinstaller.org). Instalirajte ovaj program:

    ```bash
    mcagalj@kali:~/Sigurnost$ pip install pyinstaller
    ```

    Konverzija Python skripte (`proc.py` u našem primjeru) u samostalan program (`proc`):
    ```bash
    mcagalj@kali:~/Sigurnost$ pyinstaller --distpath . --onefile proc.py

    # Brišite nepotrebene direktorije i datoteke
    mcagalj@kali:~/Sigurnost$ rm -r build
    mcagalj@kali:~/Sigurnost$ rm proc.spec

    # Testirajte novi `executable`
    mcagalj@kali:~/Sigurnost$ ./proc
    ```

4. Pokrenite _executable_ `proc` kao korisnik `iivic`). Uvjerite se da je rezultat ovog identičan onom prilikom izvršavanja Python skripte.

    Da bi omogućili drugom korisniku (`iivic`) uspješno izvršavanje programa `proc` koristit ćemo Linux **`setuid`** dopuštenje. Postavljanjem `setuid` bita na program `proc`, Linux nam dozvoljava izvršavanje ovog programa s dopuštenjima koja odgovaraju dopuštenjima vlasnika ovog programa (u našem primjeru s dopuštenjima koje ima `mcagalj`).

    Prije postavljanja `setuid` bita za program `proc` provjerite i zabilježite trenutačna dopuštenja definirana za program `proc`:

    ```bash
    mcagalj@kali:~/Sigurnost$ ls -lh proc

    # Alternativno
    mcagalj@kali:~/Sigurnost$ getfacl proc
    ```

    Postavite `setuid` bit programa `proc` (ne Python skripte) kako slijedi:

    ```bash
    mcagalj@kali:~/Sigurnost$ chmod u+s proc
    ```

    Provjerite trenutačna dopuštenja definirana za program `proc` i usporedite ih s prethodnim dopuštenjima (prije postavljanja `setuid` bita).

    Konačno pokrenite program `proc` kao ne-vlasnik `iivic` i komentirajte vaša opažanja.

    **KOMENTAR:** Na Linux OS-u postoji niz programa koje možete izvršavati s _root_ privilegijama iako ste logirani kao obični _non-root_ korisnici. Primjer takvih programa su `passwd`, `ping`, `sudo` i drugi. Uvjerite sebe da dani programi imaju postavljen `setuid` bit te da pripadaju _root_ korisniku. Koristite naredbbu `which ime_programa` da doznate lokaciju tih programa. Npr.:

    ```bash
    mcagalj@kali:~$ ls -lh $(which ping)
    ```

5. Koristeći znanja stečena u prethodnim zadacima pokušajte realizirati program koji će omogućiti _non-root_ korisniku čitanje sadržaja datoteke `/etc/shadow`.

### Reference

- [_Linux Security_ by Paul Cobbaut](http://linux-training.be/linuxsec.pdf)

## Role-based access control (RBAC) in web application

Dok je prethodnoj vježbi fokus bio na diskrecijskoj kontroli pristupa, u okviru ove vježe zadatak je implementirati RBAC kontrolu pristupa za web aplikaciju. Web aplikacija je pisana primjenom u izvrsnom [Flask](http://flask.pocoo.org/) _microframework_-u za Python.

Kod potreban za izvršenje ovog zadatka nalazi se na ovom repozitoriju unutar direktorija [flask-web](/flask-web). Nakon što ste skinuli kod, a prije pokretanja web aplikacije, instalirajte potrebne Python module. U lokalnom direktoriju gdje se nalazi datoteka `requirements.txt` izvršite sljedeću naredbu:

```bash
pip install -r requirements.txt
```