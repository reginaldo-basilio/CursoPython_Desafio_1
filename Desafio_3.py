import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nasc, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome   
        self.data_nasc = data_nasc

    def __str__(self):
        return f"""\
            Titular:\t{self.nome}
            CPF:\t\t{self.cpf}
        """
        
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        
        
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        
class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )
    
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print("\nSaldo insuficiente!")
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True
        else:
            print("\nValor informado é inválido!")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
        else:
            print("\nValor informado é inválido!")
            return False
        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_valor_saque=500, limite_qtd_saques=3):
        super().__init__(numero, cliente)
        self. limite_valor_saque = limite_valor_saque
        self.limite_qtd_saques = limite_qtd_saques
    
    def sacar(self, valor):
        qtd_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        excedeu_qtd_saques = qtd_saques >= self.limite_qtd_saques
        excedeu_valor_limite = valor > self.limite_valor_saque
        
        if excedeu_qtd_saques:
            print("\nQuantidade de saques diário excedida!")
        elif excedeu_valor_limite:
            print("\nValor do saque maior que o limite permitido!")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

########

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):

    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print()
    print("\n================ EXTRATO ================")
    print()
    transacoes = conta.historico.transacoes
    impressao = ""
    if not transacoes:
        impressao = "Não foram realizadas movimentações!"
    else:
        for transacao in transacoes:
            impressao += f"\n{transacao['data']}\t{transacao['tipo']}:\tR${transacao['valor']:.2f}"
    
    print(impressao)
    print(f"\nSaldo: \tR$ {conta.saldo:.2f}")
    print()
    print("==========================================")

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJá existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nasc=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\nCliente criado com sucesso!")
        
def listar_clientes(clientes):
    for cliente in clientes:
        print("=" * 100)
        print(textwrap.dedent(str(cliente)))

def filtrar_cliente(cpf, clientes):
    #clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    #return clientes_filtrados[0] if clientes_filtrados else None
    for cliente in clientes:
        if cliente.cpf == cpf:
            clientes_filtrados = [cliente]
            return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print ("\nCliente não possui conta!")

    #Ainda não permite escolher conta
    return cliente.contas[0]

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta) 
    cliente.contas.append(conta)
    print("Conta criada com sucesso!")

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return
    return cliente.contas[0]



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
    clientes = []
    contas = []

    while True:
        opcao = input(menu)
        if opcao in ("d", "D"):
            depositar(clientes)

        elif opcao in ("s", "S"):
            sacar(clientes)
            
        elif opcao in ("e", "E"):
            exibir_extrato(clientes)
        
        elif opcao in ("nu", "NU"):
            criar_cliente(clientes)
            
        elif opcao in ("lu", "LU"):
            listar_clientes(clientes)
        
        elif opcao in ("nc", "NC"):
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
            
        elif opcao in ("lc", "LC"):
            listar_contas(contas)
            
        elif opcao in ("q", "Q"):
            break
        else:
            print("Opção inválida!")

man()