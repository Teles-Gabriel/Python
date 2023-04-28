teste = input().split(" ")
valor= teste[0]
parcela = teste[1]

valor = float(valor)
parcela = float(parcela)

print(valor,parcela)

if(parcela == 1):
    juros = (valor/100)*5
    valorFinal = valor-juros
    print('%.2f'%valorFinal, '%.2f'%valorFinal)
if(parcela == 2):
    valorParcela = valor/parcela
    print('%.2f'%valor, '%.2f'%valorParcela)
if(parcela == 3):
    juros3 = (valor/100)*5
    valorFinal = juros3 + valor
    valorParcela = valorFinal/parcela
    print('%.2f'%valorFinal, '%.2f'%valorParcela)
if(parcela == 4):
    juros = (valor/100)*10
    valorFinal = juros+valor
    valorParcela = valorFinal/parcela
    print('%.2f'%valorFinal, '%.2f'%valorParcela)