def sacar(*, saldo, valor_saque, extrato, qtd_saque_diario, numero_saques, limite_valor_saque):
    if qtd_saque_diario < numero_saques:
        if valor_saque > 0:
            if valor_saque <= limite_valor_saque:
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

    return saldo, extrato, qtd_saque_diario

def depositar(saldo, valor_deposito, extrato, /):
    if valor_deposito > 0:
        saldo += valor_deposito
        extrato += f"Depósito: R$ {valor_deposito:.2f}\n"
        print("Depósito realziado com sucesso!")
    else:
        print("Informe um valor maior que zero!")
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print()
    print("\n================ EXTRATO ================")
    print()
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print()
    print("==========================================")

def cadastrar_usuario(usuarios):
    cpf = input("Informe o CPF: ")
    consulta = consulta_usuario(cpf, usuarios)
    if consulta:
        print("Usuario já cadastrado!")
    else:
        nome = input("Informe o nome do usuario: ")
        data_nasc = input("Informe a data de nascimento do usuario: ")
        logradouro = input("Informe o logradouro: ")
        numero = input("Informe o número: ")
        bairro = input("Informe o bairro: ")
        cidade = input("Informe a cidade: ")
        uf = input("Informe a sigla do estado: ")
        endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{uf}"
        usuarios.append({"nome": nome, "data_nascimento": data_nasc, "cpf": cpf, "endereco": endereco})
        print("usuario criado com sucesso!")
        
def listar_usuarios(usuarios):
    for usuario in usuarios:
        print(f"Nome: {usuario['nome']}")
        print(f"CPF: {usuario['cpf']}")
        print(f"Data Nascimento: {usuario['data_nascimento']}")
        print(f"Endereço: {usuario['endereco']}")
        print("==============================\n")

def consulta_usuario(cpf, usuarios):
    #usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            usuario_encontrado = [usuario]
            return usuario_encontrado[0] if usuario_encontrado else None

def listar_contas(contas):
    for conta in contas:
        print(f"Nome: {conta['usuario']['nome']}")
        print(f"Agência: {conta['agencia']}")
        print(f"Conta: {conta['conta']}")
        print("==============================\n")

def cadastrar_conta(contas, usuarios, agencia, numero_conta):
    cpf = input("Informe o CPF: ")
    usuario = consulta_usuario(cpf, usuarios)
    if usuario:
        contas.append({"usuario": usuario, "agencia": agencia, "conta": numero_conta+1}) 
        print("Conta criada com sucesso!")
        numero_conta+=1
        return numero_conta
    else:
        print("Usuario não cadastrado! Cadastre o usuário.")
        


print()
print("Seja bem vindo ao banco Cunhão!")
print("Selecione uma das opções abaixo:")
menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo Usuário
[lu] Listar Usuários
[nc] Nova Conta
[lc] Listar Contas
[q] Sair

=> """

def man():
    saldo = 1000
    extrato = ""
    qtd_saque_diario = 0
    QTD_SAQUES = 3
    LIMITE_VALOR_SAQUE = 500
    AGENCIA = "0001"
    numero_conta = 0
    usuarios = []
    contas = []


    while True:
        opcao = input(menu)
        if opcao in ("d", "D"):
            valor_deposito = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor_deposito, extrato)
            print(f"Saldo atual = {saldo}")
            
        elif opcao in ("s", "S"):
            valor_saque = float(input("Informe o valor do saque: "))
            saldo, extrato, qtd_saque_diario = sacar(

                valor_saque=valor_saque, 
                saldo=saldo, 
                extrato=extrato, 
                numero_saques=QTD_SAQUES,
                qtd_saque_diario=qtd_saque_diario, 
                limite_valor_saque=LIMITE_VALOR_SAQUE
            )
            print(f"Saldo atual = {saldo}")
            
        elif opcao in ("e", "E"):
            exibir_extrato(saldo, extrato=extrato)
        
        elif opcao in ("nu", "NU"):
            cadastrar_usuario(usuarios)
            
        elif opcao in ("lu", "LU"):
            listar_usuarios(usuarios)
        
        elif opcao in ("nc", "NC"):
            numero_conta = cadastrar_conta(contas, usuarios, AGENCIA, numero_conta)
            
        elif opcao in ("lc", "LC"):
            listar_contas(contas)
            
        elif opcao in ("q", "Q"):
            break
        else:
            print("Opção inválida!")

man()