import random
import timeit


# ============================================================
# TRABALHO 2 - ALGORITMOS DE ORDENACAO
# Inclui:
# 1) Tabela do primeiro trabalho:
#    Bubble, Bubble Otimizado, Selection, Selection Otimizado,
#    Insertion, Insertion Otimizado, Shell, Shell Otimizado
#
# 2) Novas implementacoes:
#    MergeSort basico e otimizado
#    HeapSort basico e otimizado
#    QuickSort basico e otimizado
#
# 3) Metodos extras:
#    CountingSort, BucketSort e RadixSort
# ============================================================


# ============================================================
# FUNCOES AUXILIARES
# ============================================================

def gerador_aleatorio(inicio, fim, n):
    return [random.randint(inicio, fim) for _ in range(n)]


def gerar_bases(tamanhos, inicio=1, fim=20000, seed=10):
    random.seed(seed)
    bases = {}

    for n in tamanhos:
        bases[n] = gerador_aleatorio(inicio, fim, n)

    return bases


def medir_tempo(func, array, repeticoes=5):
    tempo = timeit.timeit(lambda: func(array[:]), number=repeticoes) / repeticoes
    return tempo


def formatar_tempo(tempo, pior_tempo):
    diferenca = ((tempo / pior_tempo) - 1) * 100
    return f"{tempo:.6f}s ({diferenca:.2f}%)"


def gerar_tabela(algoritmos, bases, repeticoes=5):
    resultados = []

    for n, base in bases.items():
        tempos_linha = {}

        for nome, func in algoritmos.items():
            tempos_linha[nome] = medir_tempo(func, base, repeticoes)

        pior_tempo = max(tempos_linha.values())

        linha = {"n": n}
        for nome in algoritmos.keys():
            linha[nome] = formatar_tempo(tempos_linha[nome], pior_tempo)

        resultados.append(linha)

    return resultados


def imprimir_tabela(titulo, tabela):
    print("\n" + titulo)
    print("=" * len(titulo))

    colunas = list(tabela[0].keys())
    larguras = {}

    for coluna in colunas:
        maior = len(coluna)
        for linha in tabela:
            maior = max(maior, len(str(linha[coluna])))
        larguras[coluna] = maior

    cabecalho = " | ".join(f"{coluna:<{larguras[coluna]}}" for coluna in colunas)
    separador = "-+-".join("-" * larguras[coluna] for coluna in colunas)

    print(cabecalho)
    print(separador)

    for linha in tabela:
        print(" | ".join(f"{str(linha[coluna]):<{larguras[coluna]}}" for coluna in colunas))


def imprimir_big_o(titulo, big_o):
    print("\n" + titulo)
    print("=" * len(titulo))

    for nome, complexidade in big_o.items():
        print(f"{nome}: {complexidade}")


def validar_algoritmos(algoritmos, bases):
    for n, base in bases.items():
        esperado = sorted(base)

        for nome, func in algoritmos.items():
            resultado = func(base[:])
            if resultado != esperado:
                raise ValueError(f"Erro no algoritmo {nome} para n={n}")

    print("\nTodos os algoritmos foram validados com sucesso.")



# PRIMEIRO TRABALHO


def bubble(arr):
    numeros = arr[:]
    n = len(numeros) - 1

    for i in range(n):
        k = 0
        while k < n:
            if numeros[k] > numeros[k + 1]:
                numeros[k], numeros[k + 1] = numeros[k + 1], numeros[k]
            k += 1

    return numeros


def bubble_otimizado(arr):
    numeros = arr[:]
    n = len(numeros) - 1

    for i in range(n):
        trocou = False
        k = 0

        while k < n - i:
            if numeros[k] > numeros[k + 1]:
                numeros[k], numeros[k + 1] = numeros[k + 1], numeros[k]
                trocou = True
            k += 1

        if not trocou:
            break

    return numeros


def selection(arr):
    numeros = arr[:]
    n = len(numeros)

    for i in range(n - 1):
        menor = i

        for j in range(i + 1, n):
            if numeros[j] < numeros[menor]:
                menor = j

        numeros[i], numeros[menor] = numeros[menor], numeros[i]

    return numeros


def selection_otimizado(arr):
    numeros = arr[:]
    inicio = 0
    fim = len(numeros) - 1

    while inicio < fim:
        menor = inicio
        maior = inicio
        k = inicio + 1

        while k <= fim:
            if numeros[k] < numeros[menor]:
                menor = k
            if numeros[k] > numeros[maior]:
                maior = k
            k += 1

        numeros[inicio], numeros[menor] = numeros[menor], numeros[inicio]

        if maior == inicio:
            maior = menor

        numeros[fim], numeros[maior] = numeros[maior], numeros[fim]

        inicio += 1
        fim -= 1

    return numeros


def insercao(arr):
    numeros = arr[:]

    for i in range(1, len(numeros)):
        k = i - 1
        valor = numeros[i]

        while k >= 0 and valor < numeros[k]:
            numeros[k + 1] = numeros[k]
            k -= 1

        numeros[k + 1] = valor

    return numeros


def busca_binaria(numeros, valor, inicio, fim):
    while inicio < fim:
        meio = (inicio + fim) // 2

        if numeros[meio] <= valor:
            inicio = meio + 1
        else:
            fim = meio

    return inicio


def insercao_otimizada(arr):
    numeros = arr[:]

    for i in range(1, len(numeros)):
        valor = numeros[i]
        posicao = busca_binaria(numeros, valor, 0, i)
        k = i

        while k > posicao:
            numeros[k] = numeros[k - 1]
            k -= 1

        numeros[posicao] = valor

    return numeros


def shellsort(arr):
    numeros = arr[:]
    n = len(numeros)
    h = n // 2

    while h > 0:
        for i in range(h, n):
            valor = numeros[i]
            j = i

            while j >= h and valor < numeros[j - h]:
                numeros[j] = numeros[j - h]
                j -= h

            numeros[j] = valor

        h //= 2

    return numeros


def shellsort_otimizado(arr):
    numeros = arr[:]
    n = len(numeros)
    h = 1

    while h < n // 3:
        h = 3 * h + 1

    while h >= 1:
        for i in range(h, n):
            valor = numeros[i]
            j = i

            while j >= h and valor < numeros[j - h]:
                numeros[j] = numeros[j - h]
                j -= h

            numeros[j] = valor

        h //= 3

    return numeros



# NOVAS IMPLEMENTACOES - MERGESORT


def merge_basico(esquerda, direita):
    resultado = []
    i = 0
    j = 0

    while i < len(esquerda) and j < len(direita):
        if esquerda[i] <= direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])

    return resultado


def mergesort_basico(arr):
    numeros = arr[:]

    if len(numeros) <= 1:
        return numeros

    meio = len(numeros) // 2
    esquerda = numeros[:meio]
    direita = numeros[meio:]

    esquerda = mergesort_basico(esquerda)
    direita = mergesort_basico(direita)

    return merge_basico(esquerda, direita)


def insertion_intervalo(vetor, inicio, fim):
    for i in range(inicio + 1, fim + 1):
        valor = vetor[i]
        j = i - 1

        while j >= inicio and vetor[j] > valor:
            vetor[j + 1] = vetor[j]
            j -= 1

        vetor[j + 1] = valor


def merge_otimizado(vetor, inicio, meio, fim, auxiliar):
    if vetor[meio] <= vetor[meio + 1]:
        return

    for i in range(inicio, fim + 1):
        auxiliar[i] = vetor[i]

    i = inicio
    j = meio + 1
    k = inicio

    while i <= meio and j <= fim:
        if auxiliar[i] <= auxiliar[j]:
            vetor[k] = auxiliar[i]
            i += 1
        else:
            vetor[k] = auxiliar[j]
            j += 1

        k += 1

    while i <= meio:
        vetor[k] = auxiliar[i]
        i += 1
        k += 1


def mergesort_otimizado(arr, LIMIAR=32):
    numeros = arr[:]
    n = len(numeros)

    if n <= 1:
        return numeros

    auxiliar = [0] * n

    for inicio in range(0, n, LIMIAR):
        fim = min(inicio + LIMIAR - 1, n - 1)
        insertion_intervalo(numeros, inicio, fim)

    tamanho = LIMIAR

    while tamanho < n:
        for inicio in range(0, n, tamanho * 2):
            meio = min(inicio + tamanho - 1, n - 1)
            fim = min(inicio + 2 * tamanho - 1, n - 1)

            if meio < fim:
                merge_otimizado(numeros, inicio, meio, fim, auxiliar)

        tamanho *= 2

    return numeros



# NOVAS IMPLEMENTACOES - HEAPSORT


def max_heapify_basico(arr, n, i):
    maior = i
    esquerda = 2 * i + 1
    direita = 2 * i + 2

    if esquerda < n and arr[esquerda] > arr[maior]:
        maior = esquerda

    if direita < n and arr[direita] > arr[maior]:
        maior = direita

    if maior != i:
        arr[i], arr[maior] = arr[maior], arr[i]
        max_heapify_basico(arr, n, maior)


def heapsort_basico(arr):
    numeros = arr[:]
    n = len(numeros)

    for i in range(n // 2 - 1, -1, -1):
        max_heapify_basico(numeros, n, i)

    for fim in range(n - 1, 0, -1):
        numeros[0], numeros[fim] = numeros[fim], numeros[0]
        max_heapify_basico(numeros, fim, 0)

    return numeros


def max_heapify_iterativo(arr, n, i):
    while True:
        maior = i
        esquerda = 2 * i + 1
        direita = 2 * i + 2

        if esquerda < n and arr[esquerda] > arr[maior]:
            maior = esquerda

        if direita < n and arr[direita] > arr[maior]:
            maior = direita

        if maior == i:
            break

        arr[i], arr[maior] = arr[maior], arr[i]
        i = maior


def heapsort_otimizado(arr):
    numeros = arr[:]
    n = len(numeros)

    for i in range(n // 2 - 1, -1, -1):
        max_heapify_iterativo(numeros, n, i)

    for fim in range(n - 1, 0, -1):
        numeros[0], numeros[fim] = numeros[fim], numeros[0]
        max_heapify_iterativo(numeros, fim, 0)

    return numeros



# NOVAS IMPLEMENTACOES - QUICKSORT


def quicksort_basico(arr):
    numeros = arr[:]

    if len(numeros) <= 1:
        return numeros

    pivo = numeros[0]
    menores = []
    maiores = []

    for valor in numeros[1:]:
        if valor <= pivo:
            menores.append(valor)
        else:
            maiores.append(valor)

    return quicksort_basico(menores) + [pivo] + quicksort_basico(maiores)


def mediana_de_tres(a, b, c):
    if a <= b <= c or c <= b <= a:
        return b
    if b <= a <= c or c <= a <= b:
        return a
    return c


def quicksort_otimizado(arr, LIMIAR=16):
    numeros = arr[:]

    def quick_rec(inicio, fim):
        if inicio >= fim:
            return

        if fim - inicio + 1 <= LIMIAR:
            insertion_intervalo(numeros, inicio, fim)
            return

        meio = (inicio + fim) // 2
        pivo = mediana_de_tres(numeros[inicio], numeros[meio], numeros[fim])

        menor = inicio
        atual = inicio
        maior = fim

        while atual <= maior:
            if numeros[atual] < pivo:
                numeros[menor], numeros[atual] = numeros[atual], numeros[menor]
                menor += 1
                atual += 1
            elif numeros[atual] > pivo:
                numeros[atual], numeros[maior] = numeros[maior], numeros[atual]
                maior -= 1
            else:
                atual += 1

        quick_rec(inicio, menor - 1)
        quick_rec(maior + 1, fim)

    quick_rec(0, len(numeros) - 1)
    return numeros



# METODOS EXTRAS - COUNTINGSORT, BUCKETSORT E RADIXSORT


def countingsort(arr):
    numeros = arr[:]

    if not numeros:
        return numeros

    min_val = min(numeros)
    max_val = max(numeros)
    deslocamento = -min_val

    count = [0] * (max_val - min_val + 1)
    saida = [0] * len(numeros)

    for valor in numeros:
        count[valor + deslocamento] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for i in range(len(numeros) - 1, -1, -1):
        valor = numeros[i]
        indice = valor + deslocamento

        saida[count[indice] - 1] = valor
        count[indice] -= 1

    return saida


def insertion_bucket(bucket):
    for i in range(1, len(bucket)):
        valor = bucket[i]
        j = i - 1

        while j >= 0 and bucket[j] > valor:
            bucket[j + 1] = bucket[j]
            j -= 1

        bucket[j + 1] = valor


def bucketsort(arr):
    numeros = arr[:]

    if not numeros:
        return numeros

    min_val = min(numeros)
    max_val = max(numeros)

    if min_val == max_val:
        return numeros

    n = len(numeros)
    bucket_range = (max_val - min_val) / n
    buckets = [[] for _ in range(n)]

    for valor in numeros:
        if valor == max_val:
            indice = n - 1
        else:
            indice = int((valor - min_val) / bucket_range)

        buckets[indice].append(valor)

    for bucket in buckets:
        insertion_bucket(bucket)

    k = 0
    for bucket in buckets:
        for valor in bucket:
            numeros[k] = valor
            k += 1

    return numeros


def counting_por_digito(arr, pos):
    n = len(arr)
    saida = [0] * n
    count = [0] * 10

    for i in range(n):
        digito = (arr[i] // pos) % 10
        count[digito] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        digito = (arr[i] // pos) % 10
        saida[count[digito] - 1] = arr[i]
        count[digito] -= 1

    for i in range(n):
        arr[i] = saida[i]


def radixsort_positivos(arr):
    numeros = arr[:]

    if not numeros:
        return numeros

    max_num = max(numeros)
    pos = 1

    while max_num // pos > 0:
        counting_por_digito(numeros, pos)
        pos *= 10

    return numeros


def radixsort(arr):
    numeros = arr[:]

    negativos = [-valor for valor in numeros if valor < 0]
    positivos = [valor for valor in numeros if valor >= 0]

    negativos_ordenados = radixsort_positivos(negativos)
    positivos_ordenados = radixsort_positivos(positivos)

    negativos_ordenados = [-valor for valor in negativos_ordenados[::-1]]

    return negativos_ordenados + positivos_ordenados



# DICIONARIOS DOS ALGORITMOS


algoritmos_trabalho_1 = {
    "Bubble": bubble,
    "Bubble Opt": bubble_otimizado,
    "Selection": selection,
    "Selection Opt": selection_otimizado,
    "Insertion": insercao,
    "Insertion Opt": insercao_otimizada,
    "Shell": shellsort,
    "Shell Opt": shellsort_otimizado
}


big_o_trabalho_1 = {
    "Bubble": "Melhor O(n) se otimizado / Medio O(n²) / Pior O(n²)",
    "Bubble Opt": "Melhor O(n) / Medio O(n²) / Pior O(n²)",
    "Selection": "Melhor O(n²) / Medio O(n²) / Pior O(n²)",
    "Selection Opt": "Melhor O(n²) / Medio O(n²) / Pior O(n²)",
    "Insertion": "Melhor O(n) / Medio O(n²) / Pior O(n²)",
    "Insertion Opt": "Melhor O(n) / Medio O(n²) / Pior O(n²)",
    "Shell": "Depende da sequencia de gaps / Pior O(n²)",
    "Shell Opt": "Depende da sequencia de gaps / Pior O(n²)"
}


algoritmos_trabalho_2 = {
    "Merge": mergesort_basico,
    "Merge Opt": mergesort_otimizado,
    "Heap": heapsort_basico,
    "Heap Opt": heapsort_otimizado,
    "Quick": quicksort_basico,
    "Quick Opt": quicksort_otimizado,
    "Counting": countingsort,
    "Bucket": bucketsort,
    "Radix": radixsort
}


big_o_trabalho_2 = {
    "Merge": "Melhor O(n log n) / Medio O(n log n) / Pior O(n log n)",
    "Merge Opt": "Melhor O(n) em partes ja ordenadas / Medio O(n log n) / Pior O(n log n)",
    "Heap": "Melhor O(n log n) / Medio O(n log n) / Pior O(n log n)",
    "Heap Opt": "Melhor O(n log n) / Medio O(n log n) / Pior O(n log n)",
    "Quick": "Melhor O(n log n) / Medio O(n log n) / Pior O(n²)",
    "Quick Opt": "Melhor O(n log n) / Medio O(n log n) / Pior O(n²), mas reduz chance do pior caso",
    "Counting": "O(n + k), onde k e a amplitude dos valores",
    "Bucket": "Melhor O(n + k) / Medio O(n + k) / Pior O(n²)",
    "Radix": "O(d * (n + k)), onde d e a quantidade de digitos"
}



# EXECUCAO


if __name__ == "__main__":
    tamanhos = [100, 300, 500, 1000]
    bases = gerar_bases(tamanhos, inicio=1, fim=20000, seed=10)

    todos_algoritmos = {}
    todos_algoritmos.update(algoritmos_trabalho_1)
    todos_algoritmos.update(algoritmos_trabalho_2)

    validar_algoritmos(todos_algoritmos, bases)

    tabela_1 = gerar_tabela(algoritmos_trabalho_1, bases, repeticoes=5)
    imprimir_tabela("TABELA DO PRIMEIRO TRABALHO", tabela_1)
    imprimir_big_o("BIG O - PRIMEIRO TRABALHO", big_o_trabalho_1)

    tabela_2 = gerar_tabela(algoritmos_trabalho_2, bases, repeticoes=5)
    imprimir_tabela("TABELA DO TRABALHO 2", tabela_2)
    imprimir_big_o("BIG O - TRABALHO 2", big_o_trabalho_2)

    print("\nOBSERVACOES")
    print("===========")
    print("1. A tabela mostra o tempo medio de execucao de cada algoritmo.")
    print("2. O percentual entre parenteses mostra a diferenca em relacao ao pior tempo da mesma linha.")
    print("3. Merge Opt usa insertion sort para blocos pequenos, vetor auxiliar unico e evita merge se os blocos ja estiverem ordenados.")
    print("4. Heap Opt usa heapify iterativo para evitar chamadas recursivas.")
    print("5. Quick Opt usa mediana de tres, particao em tres grupos e insertion sort para sublistas pequenas.")
    print("6. Counting, Bucket e Radix sao metodos extras nao baseados apenas em comparacao direta.")
