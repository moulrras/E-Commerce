import sqlite3
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import json
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'uma_chave_muito_secreta'
produtos_all = [
    # Futebol
    {'id': '1', 'nome': 'Camisa de Futebol', 'preco': 150.00, 'categoria': 'Futebol', 'imagem': 'https://picsum.photos/seed/futebol1/200/200'},
    {'id': '2', 'nome': 'Chuteira', 'preco': 280.00, 'categoria': 'Futebol', 'imagem': 'https://picsum.photos/seed/futebol2/200/200'},
    {'id': '3', 'nome': 'Meião de Futebol', 'preco': 30.00, 'categoria': 'Futebol', 'imagem': 'https://picsum.photos/seed/futebol3/200/200'},
    {'id': '4', 'nome': 'Caneleira', 'preco': 50.00, 'categoria': 'Futebol', 'imagem': 'https://picsum.photos/seed/futebol4/200/200'},
    {'id': '5', 'nome': 'Luva de Goleiro', 'preco': 110.00, 'categoria': 'Futebol', 'imagem': 'https://picsum.photos/seed/futebol5/200/200'},
    {'id': '6', 'nome': 'Bola de Futebol', 'preco': 120.00, 'categoria': 'Futebol', 'imagem': 'https://picsum.photos/seed/futebol6/200/200'},
    {'id': '7', 'nome': 'Agasalho de Treino', 'preco': 180.00, 'categoria': 'Futebol', 'imagem': 'https://picsum.photos/seed/futebol7/200/200'},
    {'id': '8', 'nome': 'Shorts de Futebol', 'preco': 70.00, 'categoria': 'Futebol', 'imagem': 'https://picsum.photos/seed/futebol8/200/200'},
    {'id': '9', 'nome': 'Jaqueta Corta-vento', 'preco': 220.00, 'categoria': 'Futebol', 'imagem': 'https://picsum.photos/seed/futebol9/200/200'},
    {'id': '10', 'nome': 'Corda de Agilidade', 'preco': 45.00, 'categoria': 'Futebol', 'imagem': 'https://picsum.photos/seed/futebol10/200/200'},

    # Corrida
    {'id': '11', 'nome': 'Tênis de Corrida Ultra', 'preco': 450.00, 'categoria': 'Corrida', 'imagem': 'https://picsum.photos/seed/corrida1/200/200'},
    {'id': '12', 'nome': 'Shorts de Corrida', 'preco': 85.00, 'categoria': 'Corrida', 'imagem': 'https://picsum.photos/seed/corrida2/200/200'},
    {'id': '13', 'nome': 'Camiseta Térmica', 'preco': 110.00, 'categoria': 'Corrida', 'imagem': 'https://picsum.photos/seed/corrida3/200/200'},
    {'id': '14', 'nome': 'Relógio de Corrida', 'preco': 700.00, 'categoria': 'Corrida', 'imagem': 'https://picsum.photos/seed/corrida4/200/200'},
    {'id': '15', 'nome': 'Viseira', 'preco': 40.00, 'categoria': 'Corrida', 'imagem': 'https://picsum.photos/seed/corrida5/200/200'},
    {'id': '16', 'nome': 'Meia de Compressão', 'preco': 65.00, 'categoria': 'Corrida', 'imagem': 'https://picsum.photos/seed/corrida6/200/200'},
    {'id': '17', 'nome': 'Squeeze', 'preco': 35.00, 'categoria': 'Corrida', 'imagem': 'https://picsum.photos/seed/corrida7/200/200'},
    {'id': '18', 'nome': 'Jaqueta Corta-Vento', 'preco': 250.00, 'categoria': 'Corrida', 'imagem': 'https://picsum.photos/seed/corrida8/200/200'},
    {'id': '19', 'nome': 'Luz de Sinalização', 'preco': 55.00, 'categoria': 'Corrida', 'imagem': 'https://picsum.photos/seed/corrida9/200/200'},
    {'id': '20', 'nome': 'Cinto de Hidratação', 'preco': 130.00, 'categoria': 'Corrida', 'imagem': 'https://picsum.photos/seed/corrida10/200/200'},

    # Ciclismo
    {'id': '21', 'nome': 'Bicicleta de Montanha', 'preco': 1800.00, 'categoria': 'Ciclismo', 'imagem': 'https://picsum.photos/seed/ciclismo1/200/200'},
    {'id': '22', 'nome': 'Capacete de Ciclismo', 'preco': 200.00, 'categoria': 'Ciclismo', 'imagem': 'https://picsum.photos/seed/ciclismo2/200/200'},
    {'id': '23', 'nome': 'Luzes para Bicicleta', 'preco': 90.00, 'categoria': 'Ciclismo', 'imagem': 'https://picsum.photos/seed/ciclismo3/200/200'},
    {'id': '24', 'nome': 'Luvas de Ciclismo', 'preco': 60.00, 'categoria': 'Ciclismo', 'imagem': 'https://picsum.photos/seed/ciclismo4/200/200'},
    {'id': '25', 'nome': 'Conjunto de Ferramentas', 'preco': 110.00, 'categoria': 'Ciclismo', 'imagem': 'https://picsum.photos/seed/ciclismo5/200/200'},
    {'id': '26', 'nome': 'Garrafa de Água', 'preco': 45.00, 'categoria': 'Ciclismo', 'imagem': 'https://picsum.photos/seed/ciclismo6/200/200'},
    {'id': '27', 'nome': 'Bomba de Ar', 'preco': 75.00, 'categoria': 'Ciclismo', 'imagem': 'https://picsum.photos/seed/ciclismo7/200/200'},
    {'id': '28', 'nome': 'Suporte de Celular', 'preco': 50.00, 'categoria': 'Ciclismo', 'imagem': 'https://picsum.photos/seed/ciclismo8/200/200'},
    {'id': '29', 'nome': 'Jaqueta de Ciclismo', 'preco': 250.00, 'categoria': 'Ciclismo', 'imagem': 'https://picsum.photos/seed/ciclismo9/200/200'},
    {'id': '30', 'nome': 'Kit Reparo de Pneu', 'preco': 40.00, 'categoria': 'Ciclismo', 'imagem': 'https://picsum.photos/seed/ciclismo10/200/200'},

    # Natação
    {'id': '31', 'nome': 'Óculos de Natação', 'preco': 60.00, 'categoria': 'Natação', 'imagem': 'https://picsum.photos/seed/natacao1/200/200'},
    {'id': '32', 'nome': 'Touca de Natação', 'preco': 30.00, 'categoria': 'Natação', 'imagem': 'https://picsum.photos/seed/natacao2/200/200'},
    {'id': '33', 'nome': 'Maiô Competitivo', 'preco': 180.00, 'categoria': 'Natação', 'imagem': 'https://picsum.photos/seed/natacao3/200/200'},
    {'id': '34', 'nome': 'Calção de Natação', 'preco': 90.00, 'categoria': 'Natação', 'imagem': 'https://picsum.photos/seed/natacao4/200/200'},
    {'id': '35', 'nome': 'Prancha de Natação', 'preco': 55.00, 'categoria': 'Natação', 'imagem': 'https://picsum.photos/seed/natacao5/200/200'},
    {'id': '36', 'nome': 'Palmar de Natação', 'preco': 45.00, 'categoria': 'Natação', 'imagem': 'https://picsum.photos/seed/natacao6/200/200'},
    {'id': '37', 'nome': 'Pé de Pato', 'preco': 110.00, 'categoria': 'Natação', 'imagem': 'https://picsum.photos/seed/natacao7/200/200'},
    {'id': '38', 'nome': 'Flutuador de Pernas', 'preco': 35.00, 'categoria': 'Natação', 'imagem': 'https://picsum.photos/seed/natacao8/200/200'},
    {'id': '39', 'nome': 'Protetor de Ouvido', 'preco': 20.00, 'categoria': 'Natação', 'imagem': 'https://picsum.photos/seed/natacao9/200/200'},
    {'id': '40', 'nome': 'Bolsa de Natação', 'preco': 100.00, 'categoria': 'Natação', 'imagem': 'https://picsum.photos/seed/natacao10/200/200'},

    # Acessórios
    {'id': '41', 'nome': 'Mochila Esportiva', 'preco': 120.00, 'categoria': 'Acessórios', 'imagem': 'https://picsum.photos/seed/acessorio1/200/200'},
    {'id': '42', 'nome': 'Garrafa Térmica', 'preco': 95.00, 'categoria': 'Acessórios', 'imagem': 'https://picsum.photos/seed/acessorio2/200/200'},
    {'id': '43', 'nome': 'Joelheira', 'preco': 80.00, 'categoria': 'Acessórios', 'imagem': 'https://picsum.photos/seed/acessorio3/200/200'},
    {'id': '44', 'nome': 'Munhequeira', 'preco': 25.00, 'categoria': 'Acessórios', 'imagem': 'https://picsum.photos/seed/acessorio4/200/200'},
    {'id': '45', 'nome': 'Faixa de Resistência', 'preco': 50.00, 'categoria': 'Acessórios', 'imagem': 'https://picsum.photos/seed/acessorio5/200/200'},
    {'id': '46', 'nome': 'Luvas de Academia', 'preco': 70.00, 'categoria': 'Acessórios', 'imagem': 'https://picsum.photos/seed/acessorio6/200/200'},
    {'id': '47', 'nome': 'Protetor Bucal', 'preco': 35.00, 'categoria': 'Acessórios', 'imagem': 'https://picsum.photos/seed/acessorio7/200/200'},
    {'id': '48', 'nome': 'Cinto de Peso', 'preco': 150.00, 'categoria': 'Acessórios', 'imagem': 'https://picsum.photos/seed/acessorio8/200/200'},
    {'id': '49', 'nome': 'Kit de Primeiros Socorros', 'preco': 120.00, 'categoria': 'Acessórios', 'imagem': 'https://picsum.photos/seed/acessorio9/200/200'},
    {'id': '50', 'nome': 'Capa de Chuva Esportiva', 'preco': 140.00, 'categoria': 'Acessórios', 'imagem': 'https://picsum.photos/seed/acessorio10/200/200'},
]

# Dados simulados para o carrossel (produtos mais vendidos)
produtos_carrossel = [
    {'id': '11', 'nome': 'Tênis de Corrida Ultra', 'preco': 450.00, 'categoria': 'Corrida', 'imagem': 'https://picsum.photos/seed/corrida1/200/200'},
    {'id': '1', 'nome': 'Camisa de Futebol', 'preco': 150.00, 'categoria': 'Futebol', 'imagem': 'https://picsum.photos/seed/futebol1/200/200'},
    {'id': '21', 'nome': 'Bicicleta de Montanha', 'preco': 1800.00, 'categoria': 'Ciclismo', 'imagem': 'https://picsum.photos/seed/ciclismo1/200/200'},
    {'id': '43', 'nome': 'Joelheira', 'preco': 80.00, 'categoria': 'Acessórios', 'imagem': 'https://picsum.photos/seed/acessorio3/200/200'},
    {'id': '31', 'nome': 'Óculos de Natação', 'preco': 60.00, 'categoria': 'Natação', 'imagem': 'https://picsum.photos/seed/natacao1/200/200'},
]

# --- Funções do Banco de Dados ---
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            categoria TEXT NOT NULL,
            preco REAL NOT NULL,
            data_venda TEXT NOT NULL,
            endereco TEXT,
            cpf TEXT,
            metodo_pagamento TEXT
        );
    ''')
    conn.commit()
    conn.close()

# --- Rotas da Aplicação ---
@app.route('/')
def index():
    return render_template('index.html', produtos=produtos_all, carrossel=produtos_carrossel)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        if usuario:
            session['usuario_logado'] = usuario
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('index'))

@app.route('/buscar')
def buscar():
    termo = request.args.get('q', '').lower()
    produtos_encontrados = [p for p in produtos_all if termo in p['nome'].lower() or termo in p['categoria'].lower()]
    return render_template('index.html', produtos=produtos_encontrados, carrossel=produtos_carrossel, termo_busca=termo)

@app.route('/filtrar')
def filtrar():
    categoria = request.args.get('categoria', '')
    if categoria == 'todos':
        produtos_filtrados = produtos_all
    else:
        produtos_filtrados = [p for p in produtos_all if p['categoria'] == categoria]
    return render_template('index.html', produtos=produtos_filtrados, carrossel=produtos_carrossel, categoria_filtro=categoria)

@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html')

@app.route('/checkout')
def checkout():
    total = request.args.get('total', type=float)
    return render_template('checkout.html', total=total)

@app.route('/processar_pagamento', methods=['POST'])
def processar_pagamento():
    dados = request.json
    carrinho_data = dados['carrinho']
    endereco = dados['endereco']
    cpf = dados['cpf']
    metodo_pagamento = dados['metodo_pagamento']

    conn = get_db_connection()
    for item in carrinho_data['itens']:
        categoria = next((p['categoria'] for p in produtos_all if p['id'] == item['id']), 'Outros')
        conn.execute("INSERT INTO vendas (produto, categoria, preco, data_venda, endereco, cpf, metodo_pagamento) VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (item['nome'], categoria, item['preco'], datetime.now().isoformat(), endereco, cpf, metodo_pagamento))
    conn.commit()
    conn.close()

    return jsonify({'status': 'ok'})

@app.route('/gerar_pix', methods=['POST'])
def gerar_pix():
    total = request.json['total']
    
    pix_payload = f"00020126400014br.gov.bcb.pix0118{total:.2f}"
    img = qrcode.make(pix_payload)
    
    buf = BytesIO()
    img.save(buf)
    qr_code_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return jsonify({
        'status': 'ok',
        'qr_code': qr_code_base64
    })

# --- Início da Aplicação ---
if __name__ == '__main__':
    create_database()
    app.run(debug=True)
