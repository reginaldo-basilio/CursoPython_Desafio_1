print()
print("Seja bem vindo ao banco Cunhão!")
print("Selecione uma das opções abaixo:")
menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
extrato = ""
qtd_saque_diario = 0
QTD_SAQUES = 3
LIMITE_VALOR_SAQUE = 500


while True:
    opcao = input(menu)
    if opcao in ("d", "D"):
        valor_deposito = float(input("Informe o valor do depósito: "))
        if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f"Depósito: R$ {valor_deposito:.2f}\n"
            print("Depósito realziado com sucesso!")
        else:
            print("Informe um valor maior que zero!")
    
    elif opcao in ("s", "S"):
        if qtd_saque_diario < QTD_SAQUES:
            valor_saque = float(input("Informe o valor do saque: "))
            if valor_saque > 0:
                if valor_saque <= LIMITE_VALOR_SAQUE:
                    if valor_saque <= saldo:
                        saldo -= valor_saque
                        qtd_saque_diario += 1
                        extrato += f"Saque: R$ {valor_saque:.2f}\n"
                        print("Saque realziado com sucesso!")
                    else:
                        print("Saldo insuficiente!")
                else:
                    print("Valor do saque excedeu o limite!")                    
            else:
                print("Valor do saque deve ser maior que zero!")
        else:
            print("Quantidade de saque diário excedida!")
    elif opcao in ("e", "E"):
        print()
        print("\n================ EXTRATO ================")
        print()
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print()
        print("==========================================")
    elif opcao in ("q", "Q"):
        break
    else:
        print("Opção inválida!")
