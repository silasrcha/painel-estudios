"""
Servidor do painel dos estúdios.

Diferente dos servidores de cada estúdio, este serve a pasta SILAS-CLAUDE
inteira. Com isso o painel e todos os estúdios ficam na MESMA porta, e abrir
um estúdio é só navegar para a subpasta dele — nada de subir um processo por
estúdio e decorar qual porta é qual.

Mesmo motivo dos outros para existir em vez do http.server puro: o padrão
deixa o navegador cachear, e módulo ES cacheado faz você editar o arquivo,
recarregar, e continuar rodando a versão velha sem perceber. Aqui todo
arquivo sai com no-store.

Amarra em 127.0.0.1 de propósito: assim trocar de Wi-Fi não derruba o processo.

    py -3 servidor.py [porta]
"""
import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class SemCache(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, formato, *args):
        # só erros; o log de cada asset polui o terminal
        if args and str(args[1]).startswith(("4", "5")):
            super().log_message(formato, *args)


def main():
    porta = int(sys.argv[1]) if len(sys.argv) > 1 else 8790
    pasta = os.path.dirname(os.path.abspath(__file__))
    servidor = ThreadingHTTPServer(("127.0.0.1", porta), partial(SemCache, directory=pasta))
    print("Painel dos estudios em http://localhost:%d  (pasta: %s)" % (porta, pasta))
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.server_close()


if __name__ == "__main__":
    main()
