from flask import Flask, request, render_template, redirect
from conexao_bd import conecta_no_banco




app = Flask(__name__)


def dados_banco(dados_da_busca=['completo','especifico' and 'like'], tipo=''):
    global valor, dados
    if dados_da_busca == 'completo':
        script = f''' SELECT * FROM produtos_shekina ORDER BY tipo_produto '''
        dados = conecta_no_banco.connect_banco(script= script,bd='shekina', opção= 'fetchall')
    
    elif dados_da_busca == 'especifico':
        script = f''' SELECT * FROM produtos_shekina WHERE tipo_produto = '{tipo}'  '''
        dados = conecta_no_banco.connect_banco(script= script,bd='shekina', opção= 'fetchall')
    
    elif dados_da_busca == 'like':
        script = f''' select * from produtos_shekina WHERE descricao_item LIKE '%{tipo}%'  '''
        dados = conecta_no_banco.connect_banco(script= script,bd='shekina', opção= 'fetchall')



    valor = len(dados)
    return dados







## -------------------- PUBLICO ------------------------- ##

@app.route('/')
def homepage():
   

    return render_template('homepage.html', produto= dados_banco(dados_da_busca='completo'), lista_num = int(valor) )



@app.route('/catalogo/pesquisa', methods=['POST'])
def buscar_catalogo_por_pesquisa():
    item_pesquisa = request.form['barra_pesquisa']
    produto = item_pesquisa

    return render_template('homepage.html', produto= dados_banco('like',produto), lista_num = int(valor))


@app.route('/catalogo/<produto>')
def buscar_catalogo_por_produto(produto):


    return render_template('homepage.html', produto= dados_banco('especifico',produto), lista_num = int(valor))


@app.route('/detalhe/<produto>')
def detalhe_produto(produto):
    script= f''' SELECT * FROM produtos_shekina WHERE descricao_item ='{produto}' '''


    detalhe_item = conecta_no_banco.connect_banco(script=script, bd='shekina',opção='fetchone')



    return render_template('detalhe.html', detalhe_descricao_produto = detalhe_item[1] , detalhe_valor_produto = detalhe_item[3], detalhe_imagem_produto = detalhe_item[2])






## --------------------- ADMIN  ---------------------- ##


@app.route('/admin')
def login_admin():
    
    return render_template('login.html', login_incorreto = False)



@app.route('/validacao', methods=['GET', 'POST'])
def pegar_credenciais():
    global senha, email
    email = request.form['email_admin']
    senha = request.form['senha_admin']

    return valida_login(email , senha)

def valida_login(email, senha):
    try:
        script= f'''SELECT email FROM logins WHERE email = '{email}' '''
        retorno_email = conecta_no_banco.connect_banco(script, 'user', 'fetchone')

        script= f'''SELECT senha FROM logins WHERE email = '{email}' '''
        retorno_senha = conecta_no_banco.connect_banco(script,'user', 'fetchone')        

        if email == retorno_email[0] and senha == retorno_senha[0]:
            
            return redirect('/cadastro-produto' )
        else:
            return render_template('login.html', login_incorreto = True)
    except:
        return('erro de parametro')




@app.route('/cadastro-produto', methods=['GET','POST'])
def cadastroPage():
  
    
    
    return render_template('cadastro.html')


@app.route('/cadastro-produto=true', methods=['GET','POST'])
def cadastro():
    novo_item_descricao = request.form['novo_item_descricao']
    novo_item_link = request.form['novo_item_link']
    novo_item_valor = request.form['novo_item_valor']
    novo_item_tipo = request.form['novo_item_tipo']
    script = f''' INSERT INTO produtos_shekina (descricao_item, link_imagem_item, valor_item, tipo_produto) 
                VALUES ('{novo_item_descricao}','{novo_item_link}','{novo_item_valor}','{novo_item_tipo}') '''
    conecta_no_banco.connect_banco(script=script,bd='shekina',opção='insert')

    return render_template('cadastro.html')



app.run(host='localhost', port=9001, debug=True)
