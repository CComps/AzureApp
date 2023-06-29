budete potrebovať:

*  Python
*   numpy
*   nltk
*   tensorflow
*   flask
*   werkzeug

Nasledujúce pokyny pomôžu s inštaláciou týchto knižníc:

 *  Inštalácia Pythonu:
    Najprv budete potrebovať Python. Ak už nemáte Python nainštalovaný, môžete ho stiahnuť z oficiálnej webovej stránky Pythonu na adrese https://www.python.org/downloads/. Odporúča sa inštalovať najnovšiu verziu Pythonu.

 *  Inštalácia potrebných knižníc pomocou pip:
    Po inštalácii Pythonu by ste mali mať k dispozícii program pip, ktorý je balíkovacím systémom Pythonu. Môžete ho použiť na inštaláciu ostatných potrebných knižníc.

 *  Otvorte príkazový riadok (cmd.exe na Windows alebo Terminal na MacOS alebo Linux) a zadajte nasledujúce príkazy:

      pip install numpy
      pip install nltk
      pip install tensorflow
      pip install flask
      pip install Werkzeug
      pip install gunicorn


Tieto príkazy by mali stiahnuť a nainštalovať všetky potrebné knižnice.

--------(optional)--------
v                        v
Pridanie na GitHub
Ak chcete pridať svoj projekt na GitHub, postupujte podľa nasledujúcich krokov:
    Vytvorte si účet na GitHub, ak ešte nemáte. Môžete to urobiť na adrese https://github.com/.
    Po vytvorení účtu kliknite v pravom hornom rohu na ikonu '+' a vyberte 'New repository'.
    Vyplňte potrebné informácie o vašom repozitári, ako je názov, popis, viditeľnosť atď.
    Kliknite na tlačidlo 'Create repository'.
    Teraz otvorte terminál na svojom počítači a prejdite do adresára, kde sa nachádza váš projekt.
    Spustite nasledujúce príkazy na pridanie vašich súborov do repozitára:

      git init
      git add .
      git commit -m "initial commit"
      git remote add origin https://github.com/yourusername/your-repo-name.git
      git push -u origin master

    Zamente yourusername a your-repo-name za svoje skutočné používateľské meno na GitHub a názov repozitára.

Pripojenie k Azure Web Services

    Najprv sa prihláste do svojho účtu Azure na adrese https://portal.azure.com/.
    V ľavom menu kliknite na 'Create a resource'.
    V poli 'Search the Marketplace' hľadajte 'Web App' a vyberte ju.
    Vyplňte potrebné informácie, ako je názov, predplatné, skupina zdrojov, plán hostingu atď.
    Kliknite na 'Next: Deployment' a vyberte možnosť 'GitHub' v sekcii 'Source'.
    Na nasledujúcej obrazovke budete musieť autorizovať Azure na prístup k vášmu účtu GitHub. Kliknite na tlačidlo "Authorize" a postupujte podľa pokynov.
    Po úspešnej autorizácii sa zobrazí formulár, ktorý musíte vyplniť s informáciami o vašom repozitári:
        - Organization: Vyberte organizáciu (v prípade osobného účtu je to vaše používateľské meno na GitHub).
        - Repository: Napíšte názov svojho repozitára.
        - Branch: Vyberte vetvu, ktorú chcete nasadiť (pre väčšinu projektov by to malo byť 'master' alebo 'main').
    Kliknite na 'Review + Create' a potom na 'Create' na vytvorenie webovej aplikácie.
    Azure teraz vytvorí vašu webovú aplikáciu a automaticky nasadí váš kód z GitHubu.

Týmto je váš projekt nastavený a pripravený na prácu s GitHub a Azure Web Services!
^                        ^
--------(optional)--------

Použijeme GuniCorn na spustenie subora app.py v Terminali/cmd.exe:
  gunicorn -w 4 -t 100 app:app