import socket
import threading
from datetime import datetime

class Quadra:
    def _init_(self, id, tipo, nome):
        self.id = id
        self.tipo = tipo
        self.nome = nome

class Cliente:
    def _init_(self, id, nome, telefone, email):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email

    def _str_(self):
        return f"ID: {self.id}, Nome: {self.nome}, Telefone: {self.telefone}, Email: {self.email}"

class Reserva:
    def _init_(self, cliente, quadra, data_hora):
        self.cliente = cliente
        self.quadra = quadra
        self.data_hora = data_hora

    def _str_(self):
        return f"Cliente: {self.cliente.nome}, Quadra: {self.quadra.nome}, Data e Hora: {self.data_hora}"

class SistemaDeAluguel:
    def _init_(self):
        self.quadras = []
        self.clientes = []
        self.reservas = []

    def cadastrar_quadra(self, id, tipo, nome):
        quadra = Quadra(id, tipo, nome)
        self.quadras.append(quadra)
        return f"Quadra {nome} cadastrada com sucesso!"

    def listar_quadras(self):
        quadras_str = ""
        for quadra in self.quadras:
            quadras_str += f"ID: {quadra.id}, Tipo: {quadra.tipo}, Nome: {quadra.nome}\n"
        return quadras_str

    def cadastrar_cliente(self, id, nome, telefone, email):
        cliente = Cliente(id, nome, telefone, email)
        self.clientes.append(cliente)
        return f"Cliente {nome} cadastrado com sucesso!"

    def listar_clientes(self):
        clientes_str = ""
        for cliente in self.clientes:
            clientes_str += f"{cliente}\n"
        return clientes_str

    def reservar_quadra(self, id_cliente, id_quadra, data_hora):
        cliente = next((cliente for cliente in self.clientes if cliente.id == id_cliente), None)
        quadra = next((quadra for quadra in self.quadras if quadra.id == id_quadra), None)
        if cliente and quadra:
            reserva = Reserva(cliente, quadra, data_hora)
            self.reservas.append(reserva)
            return f"Reserva feita com sucesso para {cliente.nome} na quadra {quadra.nome} para {data_hora}!"
        else:
            return "Cliente ou quadra não encontrados."

    def listar_reservas(self):
        reservas_str = ""
        for reserva in self.reservas:
            reservas_str += f"{reserva}\n"
        return reservas_str

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 65432       # Porta do servidor

sistema = SistemaDeAluguel()

# Função para lidar com conexões de clientes
def handle_client(conn, addr):
    print(f"Conectado a {addr}")
    with conn:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            command = data.split()
            response = ""
            if command[0] == 'CADASTRAR_QUADRA':
                response = sistema.cadastrar_quadra(int(command[1]), command[2], command[3])
            elif command[0] == 'LISTAR_QUADRAS':
                response = sistema.listar_quadras()
            elif command[0] == 'CADASTRAR_CLIENTE':
                response = sistema.cadastrar_cliente(int(command[1]), command[2], command[3], command[4])
            elif command[0] == 'LISTAR_CLIENTES':
                response = sistema.listar_clientes()
            elif command[0] == 'RESERVAR_QUADRA':
                data_hora = datetime.strptime(command[3], '%Y-%m-%dT%H:%M')
                response = sistema.reservar_quadra(int(command[1]), int(command[2]), data_hora)
            elif command[0] == 'LISTAR_RESERVAS':
                response = sistema.listar_reservas()
            else:
                response = "Comando desconhecido."
            conn.sendall(response.encode('utf-8'))

# Iniciando o servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor rodando em {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
