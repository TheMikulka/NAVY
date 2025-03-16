# Perceptron
## Popis problému
- Perceptron je jednoduchý model umělé neuronové sítě, který byl vytvořen na základě biologických neuronů. Jeho hlavním úkolem je klasifikace dat do dvou tříd.
- Snažím se naučit perceptron, aby rozděloval body podle přímky y = 3x + 2.
- Každý bod má tři možné labely:
    - 1 - nad přímkou
    - 0 - na přímce
    - -1 - pod přímkou

## struktura sítě
- Dva vstupy (x, y), dvě váhy (w1, w2), jeden bias a aktivační funkce signum 

## Implementace
- Inicializace vah a biasu
- Trénování perceptronu
    - Výpočet predikce pomocí váženého součtu vstupů a biasu
    - Výpočet chyby jako rozdíl mezi predikcí a skutečným výstupem
    - Úprava vah a biasu na základě chyby
    - Opakování procesu, dokud se nenaučí správně klasifikovat body nebo dokud nevyprší počet epoch
- Predikce pomocí naučených vah a biasu k přiřazení labelů bodům
- Vykreslení bodů, původní přímky a rozhodovací hranice perceptronu

## Výsledek
- Perceptron se naučil rozdělovat body podle přímky y = 3x + 2
- Rozhodovací hranice perceptronu je viditelná na grafu
- Body jsou zbarveny podle labelu, který jim byl přiřazen