# Řešení XOR problému pomocí vícevrstvého perceptronu
## Popis problému
- Jednoduchý perceptron XOR problém nezvládne, protože není lineárné separovatelný
- To znamená, že není možné najít jednu rovinu, která by rozdělila vstupní data do dvou tříd
- Proto je potřeba použít vícevrstvou neuronovou síť s nelineární aktivační funkcí

## struktura sítě
- 2 vstupní neurony, skrytá vrstva s 2 neurony a výstupní neuron

## Implementace
- sigmoid aktivační funkce
- forward pass - výpočet výstupu sítě
- backward pass - výpočet gradientu pro zpětnou propagaci chyby
- update weights - aktualizace vah a biasů podle vypočtených gradientů
- plot_decision_boundary - vizualizace rozhodovací hranice
- XOR_problem - trénování sítě na XOR problém

## Výsledek
- Výstup modelu odpovídá očekávaným hodnotám, chyba se postupně snižuje a rozhodovací hranice rozděluje vstupní data do dvou tříd
- U výsledku záleží na inicializaci vah a biasů, které jsou náhodné takže výsledek může být různý, proto jsem zvolila pevný seed pro generování náhodných čísel
- Rozhodovací hranice vykreslená pomocí plot_decision_boundary
- Graf průběhu chyby během trénování

# Možné úpravy
## Pokud by se řešil jiný problém
- Změnit počet skrytých neuronů
- Použít jinou aktivační funkci
- Experimentovat s learning rate