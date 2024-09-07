from flask import Flask, jsonify, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'estoque.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
        db.commit()

def row_to_dict(row):
    return dict(row)

@app.route('/')
def index():
    db = get_db()
    cursor = db.execute('SELECT * FROM estoque')
    estoque = [row_to_dict(row) for row in cursor.fetchall()]
    return render_template('index.html', estoque=estoque)

@app.route('/buscar')
def buscar():
    query = request.args.get('query')
    if query:
        db = get_db()
        cursor = db.execute('SELECT * FROM estoque WHERE id = ? OR nome LIKE ?', (query, f'%{query}%'))
        filtrado = [row_to_dict(row) for row in cursor.fetchall()]
        return render_template('resultados.html', estoque=filtrado)
    return redirect(url_for('index'))

@app.route('/adicionar', methods=['POST'])
def adicionar():
    item_id = int(request.form['id'])
    quantidade = int(request.form['quantidade'])
    nome = request.form.get('nome', '')

    db = get_db()
    cursor = db.execute('SELECT * FROM estoque WHERE id = ?', (item_id,))
    item = cursor.fetchone()

    if item:
        db.execute('UPDATE estoque SET quantidade = quantidade + ? WHERE id = ?', (quantidade, item_id))
    else:
        db.execute('INSERT INTO estoque (id, nome, quantidade) VALUES (?, ?, ?)', (item_id, nome, quantidade))
    db.commit()
    return redirect(url_for('index'))

@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    nome = request.form['nome']
    quantidade = int(request.form['quantidade'])

    db = get_db()
    db.execute('UPDATE estoque SET nome = ?, quantidade = ? WHERE id = ?', (nome, quantidade, id))
    db.commit()
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    db = get_db()
    db.execute('DELETE FROM estoque WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/vender', methods=['POST'])
def vender():
    item_id = int(request.form['id'])
    quantidade = int(request.form['quantidade'])

    db = get_db()
    cursor = db.execute('SELECT * FROM estoque WHERE id = ?', (item_id,))
    item = cursor.fetchone()

    if item:
        if item['quantidade'] >= quantidade:
            db.execute('UPDATE estoque SET quantidade = quantidade - ? WHERE id = ?', (quantidade, item_id))
            db.commit()
            return redirect(url_for('index'))
        else:
            return "Quantidade insuficiente", 400
    return "Item não encontrado", 404

if __name__ == '__main__':
    app.run(debug=True)
