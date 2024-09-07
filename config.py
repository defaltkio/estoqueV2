from flask import Flask, jsonify, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('estoque.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE,
                quantidade INTEGER,
                preco REAL
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect('estoque.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos')
        produtos = cursor.fetchall()
    return render_template('index.html', estoque=produtos)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome']
    quantidade = int(request.form['quantidade'])
    preco = float(request.form['preco'])

    with sqlite3.connect('estoque.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)', (nome, quantidade, preco))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Produto já existe no estoque.", 400
    return redirect(url_for('index'))

@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    quantidade = request.form.get('quantidade', None)
    preco = request.form.get('preco', None)

    with sqlite3.connect('estoque.db') as conn:
        cursor = conn.cursor()
        if quantidade is not None:
            cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (int(quantidade), id))
        if preco is not None:
            cursor.execute('UPDATE produtos SET preco = ? WHERE id = ?', (float(preco), id))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/remover/<int:id>')
def remover(id):
    with sqlite3.connect('estoque.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM produtos WHERE id = ?', (id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
