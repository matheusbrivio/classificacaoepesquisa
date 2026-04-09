import random
import timeit

def gerador_aleatorio(inicio, fim, n):
    return [random.randint(inicio, fim) for _ in range(n)]


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


def medir_tempo(func, array, repeticoes=5):
    tempo = timeit.timeit(lambda: func(array[:]), number=repeticoes) / repeticoes
    return tempo


def formatar_tempo(tempo, pior_tempo):
    diferenca = ((tempo / pior_tempo) - 1) * 100
    return f"{tempo:.6f}s ({diferenca:.2f}%)"


algoritmos = {
    "Bubble": bubble,
    "Bubble Opt": bubble_otimizado,
    "Selection": selection,
    "Selection Opt": selection_otimizado,
    "Insertion": insercao,
    "Insertion Opt": insercao_otimizada,
    "Shell": shellsort,
    "Shell Opt": shellsort_otimizado
}


big_o = {
    "Bubble": "O(n²)",
    "Bubble Opt": "O(n²)",
    "Selection": "O(n²)",
    "Selection Opt": "O(n²)",
    "Insertion": "O(n²)",
    "Insertion Opt": "O(n²)",
    "Shell": "depende da sequencia",
    "Shell Opt": "depende da sequencia"
}


def gerar_tabela(tamanhos, inicio=1, fim=20000, repeticoes=5):
    resultados = []

    for n in tamanhos:
        base = gerador_aleatorio(inicio, fim, n)
        tempos_linha = {}

        for nome, func in algoritmos.items():
            tempos_linha[nome] = medir_tempo(func, base, repeticoes)

        pior_tempo = max(tempos_linha.values())

        linha = {"n": n}
        for nome in algoritmos.keys():
            linha[nome] = formatar_tempo(tempos_linha[nome], pior_tempo)

        resultados.append(linha)

    return resultados


def imprimir_tabela(tabela):
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


def imprimir_big_o():
    print("\nBIG O DOS METODOS")
    print("-----------------")
    for nome in algoritmos.keys():
        print(f"{nome}: {big_o[nome]}")


tamanhos = [100, 300, 500, 1000]
tabela = gerar_tabela(tamanhos, inicio=1, fim=20000, repeticoes=5)
imprimir_tabela(tabela)
imprimir_big_o()


#tabela apos executar:
# TABELA DE TEMPO DE EXECUÇÃO
#
# n    | Bubble            | Bubble Opt          | Selection           | Selection Opt       | Insertion           | Insertion Opt       | Shell               | Shell Opt
# -----+-------------------+---------------------+---------------------+---------------------+---------------------+---------------------+---------------------+--------------------
# 100  | 0.000459s (0.00%) | 0.000347s (-24.50%) | 0.000110s (-75.96%) | 0.000217s (-52.67%) | 0.000120s (-73.94%) | 0.000116s (-74.79%) | 0.000050s (-89.16%) | 0.000040s (-91.26%)
# 300  | 0.004091s (0.00%) | 0.002887s (-29.42%) | 0.000959s (-76.56%) | 0.001289s (-68.49%) | 0.001122s (-72.58%) | 0.000808s (-80.25%) | 0.000188s (-95.40%) | 0.000154s (-96.23%)
# 500  | 0.012816s (0.00%) | 0.009284s (-27.56%) | 0.002734s (-78.67%) | 0.002544s (-80.15%) | 0.002840s (-77.84%) | 0.002344s (-81.71%) | 0.000326s (-97.46%) | 0.000308s (-97.60%)
# 1000 | 0.049541s (0.00%) | 0.034543s (-30.27%) | 0.011795s (-76.19%) | 0.011418s (-76.95%) | 0.011489s (-76.81%) | 0.009631s (-80.56%) | 0.000826s (-98.33%) | 0.000808s (-98.37%)
# O insertion otimizado ficou mais lento para N pequenos porque,
# apesar de reduzir o número de comparações usando busca binária,
# ele adiciona um custo extra de processamento.
# Como o insertion normal já é simples e rápido, esse overhead não compensa
# em vetores pequenos, e a otimização só começa a fazer diferença
# quando o tamanho da entrada aumenta.

