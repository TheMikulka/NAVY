# Hopfieldova síť
## Popis problému
Hopfieldova síť je rekurentní neuronová síť, která slouží k ukládání a následné rekonstrukci vzorů. Síť využívá asociativní paměť. 

## Struktura sítě
Síť se skládá z:
- **Neuronů** reprezentujících jednotlivé prvky vzoru.
- **Vahové matice**, která zachycuje vzájemné vazby mezi neurony.
- **Aktivační funkce**, která určuje, jak se aktualizují hodnoty neuronů.
## Implementace
- **Trénování sítě** 
    - Trénování Hopfieldovy sítě spočívá v uložení vzorů do váhové matice. Váhová matice slouží jako paměť, kde jsou vzory zakódovány a síť se pak na jejich základě pokouší obnovit neúplné nebo špatně rozpoznané vstupy.
    - Váhová matice se spočítá jako součet maticových součinů každého vzoru se svým transponovaným tvarem. Tento výpočet zajistí, že vzory budou stabilními stavy sítě:
        ```python
        for pattern in patterns:
            pattern = pattern.reshape(-1, 1)
            self.weights += pattern @ pattern.T
        ```
    - Aby se zabránilo tomu, že by se neurony samy ovlivňovaly, nastavení diagonálu váhové matice na nulu:
        ```python
        np.fill_diagonal(self.weights, 0)
        ```
- **Synchronní rekonstrukce** 
    - Síť postupně aktualizuje svůj stav pomocí váhové matice. Celý proces probíhá následujícím způsobem:
        1. Vstupní vzor se vynásobí váhovou maticí, což simuluje vliv všech neuronů na sebe navzájem.
        2. Použitím funkce sign() se výsledek převede zpět na binární hodnoty (-1 nebo 1)
        3. Tento proces se opakuje, dokud se stav vzoru přestane měnit (což znamená, že síť dosáhla stabilního bodu) nebo dokud není dosažen maximální počet iterací.
        ```python
        while(not np.array_equal(pattern, last_pattern) and max_iter != 0):
            last_pattern = np.copy(pattern)
            pattern = np.sign(self.weights @ pattern)
            max_iter -= 1
        ```

- **Asynchronní rekonstukce** 
    - Neurony se neaktualizují najednou, ale jeden po druhém. To znamená, že každý neuron si spočítá svou novou hodnotu na základě ostatních neuronů a hned se změní
        1. Spočítání aktivaci pro neuron jako vážený součet signálů od ostatních neuronů
        2. Opakování pro každý neuron zvlášť
        ```python
        for i in range(self.size):
        activation = np.sign(np.dot(self.weights[:,i], pattern))
        ```
## Výsledek
Síť je schopna správně rekonstruovat uložené vzory, pokud jejich počet nepřekročí kapacitu*:

$$ max\_patterns = \left\lfloor\frac{grid\_size^2}{2 \log_2(grid\_size^2)}\right\rfloor $$

*viz Wiki: [https://en.wikipedia.org/wiki/Hopfield_network capacity ](https://en.wikipedia.org/wiki/Hopfield_network#Capacity)


## Možné vylepšení
- Po výpočtu vah nastavím diagonálu na nulu pomocí `np.fill_diagonal(self.weights, 0)`, což ale může vést k nestabilitě v některých případech. Možná by bylo lepší použít nějakou metodu normalizace vah.
- V metodě `recover_sync` iteruju, dokud se vzorec nezmění, ale může dojít k tomu, že se vzory budou přepínat mezi dvěma stavy (oscilační chování). To by šlo omezit zavedením energetické funkce:

$$ E = -\frac{1}{2} \sum_{i,j=1}^{N} P_{ij} A_i A_j + \sum_{i=1}^{N} \theta_i A_i $$

- Maximální počet vzorů se dá odhadnout jako $$p \approx 0.15 \times N $$ nebo taky podle vzorce z prezentace:

$$ max\_patterns = \frac{grid\_size^2}{2 \log(grid\_size^2)} $$