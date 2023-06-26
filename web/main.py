import os
from flask import Flask, Blueprint, redirect, url_for, session, render_template, request
from web.db import get_db

bp = Blueprint('main', __name__, url_prefix='/main')

# @bp.route('/inicio')
# def inicio():
#    return render_template('public/index.html')


@bp.route('/instrumentos', methods=['GET','POST'])
def instrumentos():
    db, c = get_db()
    c.execute(
        'select id_instrumento, nombre, marca, tipo_instrumento,'
        'valor, cantidad from instrumento;'
    )
    instrumentos = c.fetchall()
    return render_template('public/instrumentos.html', instrumentos=instrumentos)

@bp.route('/carrito')
def carrito():
    return render_template('public/carrito.html')

"""
@bp.route('/add', methods=['POST'])
def add_product_to_cart():
 try:
  _cantidad = int(request.form['cantidad'])
  _id_instrumento = request.form['id_instrumento']
  # validate the received values
  if _cantidad and _id_instrumento and request.method == 'POST':
    db, c = get_db()
    c.execute(
        'SELECT id_instrumento, nombre, marca,'
        'valor, FROM instrumento WHERE id_instrumento=%s;', (_id_instrumento,)
    )
    row = c.fetchone()
    
    itemArray = { row['id_instrumento'] : {'nombre' : row['nombre'], 'marca' : row['marca'], 'id_instrumento' : row['id_instrumento'], 'cantidad' : _cantidad, 'valor' : row['valor'], 'total_price': _cantidad * row['valor']}}
    
    valor_total = 0
    total_cantidad = 0
        
    session.modified = True
    if 'cart_item' in session:
        if row['id_instrumento'] in session['cart_item']:
            for key, value in session['cart_item'].items():
                if row['id_instrumento'] == key:
                    old_cantidad = session['cart_item'][key]['cantidad']
                    total_cantidad = old_cantidad + _cantidad
                    session['cart_item'][key]['cantidad'] = total_cantidad
                    session['cart_item'][key]['total_price'] = total_cantidad * row['valor']
        else:
            session['cart_item'] = array_merge(session['cart_item'], itemArray)
    
        for key, value in session['cart_item'].items():
            individual_cantidad = int(session['cart_item'][key]['cantidad'])
            item_price = float(session['cart_item'][key]['total_price'])
            total_cantidad = total_cantidad + individual_cantidad
            valor_total = valor_total + item_price
    else:
        session['cart_item'] = itemArray
        total_cantidad = total_cantidad + _cantidad
        valor_total = valor_total + _cantidad * row['valor']
        
    session['total_cantidad'] = total_cantidad
    session['valor_total'] = valor_total
        
    return redirect(url_for('main.carrito'))
  else:
    return 'Error al incluir un item'
 except Exception as e:
    print(e)
"""
@bp.route('/add', methods=['POST'])
def add_product_to_cart():
    try:
        _cantidad = int(request.form['cantidad'])
        _id_instrumento = request.form['id_instrumento']
        
        # Validate the received values
        if _cantidad and _id_instrumento and request.method == 'POST':
            db, c = get_db()
            c.execute(
                'SELECT id_instrumento, nombre, marca, valor FROM instrumento WHERE id_instrumento=%s;',
                (_id_instrumento,)
            )
            row = c.fetchone()

            item = {
                'nombre': row['nombre'],
                'marca': row['marca'],
                'id_instrumento': row['id_instrumento'],
                'cantidad': _cantidad,
                'valor': row['valor'],
                'total_price': _cantidad * row['valor']
            }

            session.modified = True

            if 'cart_item' in session:
                if row['id_instrumento'] in session['cart_item']:
                    session['cart_item'][row['id_instrumento']]['cantidad'] += _cantidad
                    session['cart_item'][row['id_instrumento']]['total_price'] += _cantidad * row['valor']
                else:
                    session['cart_item'][row['id_instrumento']] = item
            else:
                session['cart_item'] = {row['id_instrumento']: item}

            total_cantidad = sum(item['cantidad'] for item in session['cart_item'].values())
            valor_total = sum(item['total_price'] for item in session['cart_item'].values())

            session['total_cantidad'] = total_cantidad
            session['valor_total'] = valor_total

            return redirect(url_for('main.carrito'))
        else:
            return 'Error al incluir un item'
    except Exception as e:
        print(e)

@bp.route('/empty')
def empty_cart():
 try:
  session.clear()
  return redirect(url_for('main.instrumento'))
 except Exception as e:
  print(e)
 

@bp.route('/delete/<string:code>')
def delete_product(code):
 try:
  valor_total = 0
  total_cantidad = 0
  session.modified = True
   
  for item in session['cart_item'].items():
   if item[0] == code:    
    session['cart_item'].pop(item[0], None)
    if 'cart_item' in session:
     for key, value in session['cart_item'].items():
      individual_cantidad = int(session['cart_item'][key]['cantidad'])
      individual_price = float(session['cart_item'][key]['total_price'])
      total_cantidad = total_cantidad + individual_cantidad
      valor_total = valor_total + individual_price
    break
   
  if total_cantidad == 0:
   session.clear()
  else:
   session['total_cantidad'] = total_cantidad
   session['valor_total'] = valor_total
   
  return redirect(url_for('main.carrito'))
 except Exception as e:
  print(e)
   

def array_merge( first_array , second_array ):
 if isinstance( first_array , list ) and isinstance( second_array , list ):
  return first_array + second_array
 elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
  return dict( list( first_array.items() ) + list( second_array.items() ) )
 elif isinstance( first_array , set ) and isinstance( second_array , set ):
  return first_array.union( second_array )
 return False
