import meu_modulo as mm


valor_a = int(input('Insira o ano atual: '))
valor_b = int(input('Insira que você nasce: '))

print('Sua idade é: ')
print(mm.soma(valor_a,valor_b))


anoAtual = int(input('Insira o ano atual: '))
anoNascimento = int(input('Insira que você nasce: '))

print(f'Voce têm {mm.calcularIdade(anoAtual, anoNascimento)} anos')