# L-systems

## Popis problému
- L-systém je formální gramatika určená pro rekurzivní generování fraktálních struktur, často využívaná pro modelování přírodních tvarů jako jsou větve stromů, listy nebo krystaly.
- Vstupem je axiom (počáteční řetězec) a množina pravidel, podle kterých se znaky iterativně nahrazují.
- Po několika iteracích vznikne dlouhý řetězec, který je následně interpretován jako grafické instrukce a vykreslen pomocí Turtle grafiky.

## Struktura sítě
- Aplikace je rozdělena do dvou částí:
    - **`LSystem` třída** – zodpovídá za přepisování řetězce podle pravidel a vykreslování výsledného obrazce pomocí Turtle.
    - **`LSystemGUI` třída** – poskytuje uživatelské rozhraní v Tkinteru, kde lze nastavit počáteční pozici, úhel, délku úseček, počet iterací a zadat vlastní pravidla.
- Grafická interpretace řetězce používá tyto instrukce:
    - `F` – posun vpřed s kreslením
    - `b` – posun vpřed bez kreslení
    - `+` – otočení doprava o zvolený úhel
    - `-` – otočení doleva o zvolený úhel
    - `[` – uložení aktuální pozice a směru
    - `]` – návrat na poslední uloženou pozici a směr

## Implementace
- Inicializace plátna a Turtle grafiky v Tkinter GUI
- Získání vstupních parametrů od uživatele (axiom, pravidla, úhel, délka čáry, počet iterací, počáteční pozice)
- Opakovaná aplikace pravidel na axiom podle zvoleného počtu iterací (tzv. *nesting*)
- Interpretace výsledného řetězce a vykreslení fraktálu:
    - Kreslení čar (`F`), pohyb bez kreslení (`b`)
    - Otočení vlevo/vpravo (`+`, `-`)
    - Uložení/obnovení stavu (`[`, `]`)
- Možnost volby předdefinovaných fraktálů nebo zadání vlastních pravidel
- Možnost vymazání plátna a vykreslení nové struktury

## Předdefinované fraktály

### 1. Čtvercový fraktál
- **Axiom:** F+F+F+F
- **Pravidla:** 
  - F-> F+F-F-FF+F+F-F
- **Úhel:** 90°
- **Popis:** Fraktál založený na rekurzivním dělení čtvercových útvarů. Vzniká tzv. Kochův čtverec.

### 2. Trojúhelníkový fraktál (Kochova křivka)
- **Axiom:** F++F++F
- **Pravidla:** 
  - F-> F+F--F+F
- **Úhel:** 60°
- **Popis:** Klasická Kochova křivka, tvořící trojúhelníkový vzor s ostrými hranami.

### 3. Jednoduchá větev
- **Axiom:** F
- **Pravidla:**
  - F -> F[+F]F[-F]F
- **Úhel:** π/7
- **Popis:** 
  - Sruktura připomínající rostoucí větev, kde se v každé iteraci hlavní větev rozdělí na tři části: jednu přímou a dvě postranní. Díky úhlu π/7 vznikají jemné a rovnoměrné odbočky.

### 4. Hustě větvená struktura
- **Axiom:** F
- **Pravidla:** 
  - F -> FF+[+F-F-F]-[-F+F+F] 
- **Úhel:** π/8
- **Popis:** 
  - Tento L-systém vytváří komplexnější, hustě větvenou strukturu podobnou koruně stromu. Díky větší složitosti pravidel a menšímu úhlu π/8 dochází k častému větvení a překrývání větviček.




## Výsledek
- Aplikace umožňuje uživateli vizuálně prozkoumávat chování L-systémů a vytvářet fraktální obrazce na základě jednoduchých pravidel.
- K dispozici jsou čtyři předdefinované fraktály, ale uživatel si může zadat i vlastní definici.
- Výsledné fraktály jsou přehledně vykresleny včetně možnosti posouvání.

