# Ambiente de Rede com Políticas de Segurança

Ambiente virtualizado (Docker Compose) para a disciplina CIC0201 - Segurança Computacional, com mecanismos de segurança em diferentes camadas da arquitetura TCP/IP.

## Módulo 1: Comunicação insegura (HTTP)

Serviço web acessível por HTTP, com captura do tráfego para mostrar que usuário, senha e cookie circulam em texto claro.

## Arquitetura

| Serviço | Função |
|---|---|
| `web` | Nginx, proxy reverso na porta 80 |
| `app` | Aplicação Flask (login e área protegida) |
| `cliente` | Contêiner com `curl` que gera as requisições |
| `monitor` | `tcpdump` capturando o tráfego do `web` |


## Pré-requisitos

- Docker e Docker Compose
- Wireshark (instalado no host, para analisar o `.pcap`)

## Instalação de dependências (Ubuntu/Debian)

```bash
sudo apt install docker.io docker-compose-v2 docker-buildx
sudo usermod -aG docker $USER
```

Faça logout e login novamente para usar o Docker sem `sudo`. O `docker-buildx` é opcional, mas remove o aviso do Bake no build.

## Como reproduzir

Clone o repositório e entre na pasta:

```bash
git clone <url-do-repositorio>
cd Politicas_de_Seguranca
```

1. Subir o ambiente:

```bash
docker compose up -d --build
docker compose ps
docker compose logs monitor
```

O `monitor` usa `tcpdump` para gravar o tráfego automaticamente em `Capturas/Modulo1/http_inseguro.pcap`.

2. Gerar o tráfego a partir do cliente:

```bash
docker compose exec cliente curl -v http://web/
docker compose exec cliente curl -v -d "usuario=user&senha=123456" http://web/login
docker compose exec cliente curl -v -H "Cookie: sessao=abc123" http://web/admin
```

O primeiro acessa a página de login, o segundo envia as credenciais (resposta `302`) e o terceiro reutiliza o cookie, simulando um atacante que o capturou.

3. Encerrar e finalizar a captura:

```bash
docker compose down
```

## Análise no Wireshark

Abra `Capturas/Modulo1/http_inseguro.pcap` e use:

| Filtro | O que mostra |
|---|---|
| `http.request.method == "POST"` | Credenciais no corpo do login |
| `http.set_cookie` / `http.cookie` | Cookie de sessão |
| `tcp.flags.syn == 1` | Handshake TCP |

Se o arquivo ficar com dono root: `sudo chown $USER Capturas/Modulo1/*.pcap`.

## Estrutura do projeto

```text
.
├── docker-compose.yml
├── Servidor/
├── Cliente/
├── Firewall/
├── Scripts/
└── Capturas/
```