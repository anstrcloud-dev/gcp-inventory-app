from flask import Flask, render_template, request, redirect, url_for
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client()

@app.route('/')
def index():
    items_ref = db.collection('inventory')
    items = [{'id': doc.id, **doc.to_dict()} for doc in items_ref.stream()]
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form.get('name')
    quantity = int(request.form.get('quantity'))
    category = request.form.get('category')
    db.collection('inventory').add({
        'name': name,
        'quantity': quantity,
        'category': category
    })
    return redirect(url_for('index'))

@app.route('/update/<item_id>', methods=['POST'])
def update_item(item_id):
    quantity = int(request.form.get('quantity'))
    db.collection('inventory').document(item_id).update({'quantity': quantity})
    return redirect(url_for('index'))

@app.route('/delete/<item_id>', methods=['POST'])
def delete_item(item_id):
    db.collection('inventory').document(item_id).delete()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)