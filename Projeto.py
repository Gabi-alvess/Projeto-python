import socket

# Configurações do cliente
HOST = '192.168.43.36'  # Endereço IP do servidor
PORT = 65432       # Porta do servidor

# Função para exibir o menu e lidar com a entrada do usuário
def exibir_menu():
    print("Menu de Opções:")
    print("1. Reservar Quadra")
    print("2. Cancelar Reserva")
    print("3. Sair")

# Função para enviar comandos ao servidor e receber a resposta
def enviar_comando(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command.encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
        return data

# Função principal do cliente
def main():
    print("Bem-vindo ao sistema de reservas de quadras!")
    while True:
        exibir_menu()
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            id_cliente = input("Digite o ID do cliente: ")
            id_quadra = input("Digite o ID da quadra: ")
            data_hora = input("Digite a data e hora da reserva (YYYY-MM-DDTHH:MM): ")
            print(type(data_hora))
            command = f'RESERVAR {id_cliente} {id_quadra} {data_hora}'
            resposta = enviar_comando(command)
            print("Servidor:", resposta)
        elif escolha == '2':
            id_cliente = input("Digite o ID do cliente: ")
            id_quadra = input("Digite o ID da quadra: ")
            data_hora = input("Digite a data e hora da reserva a cancelar (YYYY-MM-DDTHH:MM): ")
            command = f'CANCELAR {id_cliente} {id_quadra} {data_hora}'
            resposta = enviar_comando(command)
            print("Servidor:", resposta)
        elif escolha == '3':
            print("Saindo...")
            break
        else:
            print("Opção inválida, por favor escolha novamente.")

if __name__ == "__main__":
    main()
