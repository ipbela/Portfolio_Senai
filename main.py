import http
import os
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import parse_qs 

class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            #tenta abrir o arquivo index.html
            f = open(os.path.join(path, 'home.html'), 'r', encoding='utf-8')
            #se existir, envia o conteudo do arquivo
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close()
            return None
        except FileNotFoundError:
            print('Erro!')

        return super().list_directory(path)

    def do_GET(self):
        if self.path == '/login':
            #tenta abrir o arquivo login.html
            try:
                with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                    content = login_file.read()

                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8')) #frase esta sendo representada como bytes
            except FileNotFoundError:
                self.send_error(404, 'File not found')

        else:
            #se nao for a rota '/login', continua com o comportamento padrao
            super().do_GET()

    def do_POST(self):
        #verifica se a rota é /enviar_login
        if self.path == '/enviar_login':
            #obtem o comprimento do corpo da requisição
            content_length = int(self.headers['Content-Length'])
            #lê o corpo da requisição
            body = self.rfile.read(content_length).decode('utf-8')
            #parseia os dados do formulário
            form_data = parse_qs(body)

            #exibe os dados no terminal
            print('Dados do formulário: ')
            print('Email: ', form_data.get('email', [''])[0])
            print('Senha: ', form_data.get('senha', [''])[0])

            #responde ao cliente
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('Dados recebidos com sucesso!'.encode('utf-8'))
        else:
            #se nao for a rota '/submit_login', continua com o comportamento
            super(MyHandler, self).do_POST()
            print('erro')

#define a porta a ser utilizada
#define o IP
endereco_ip = '0.0.0.0'
porta = 8000

#configura o manipulador (handler) para o servidor
handler = http.server.SimpleHTTPRequestHandler

#cria um servidor na porta especificada
with socketserver.TCPServer((endereco_ip, porta), MyHandler) as httpd:
    print(f'Servidor iniciado em {endereco_ip}:{porta}')
    #mantem o servidor em execução
    httpd.serve_forever()
