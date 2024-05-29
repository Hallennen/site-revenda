from flask import Flask, request, render_template, redirect
from conexao_bd import conecta_no_banco




app = Flask(__name__)


def dados_banco(dados_da_busca=['completo','especifico' and 'like'], tipo=''):
    global valor, dados
    if dados_da_busca == 'completo':
        script = f''' SELECT * FROM produtos_shekina WHERE ativo = 'SIM' ORDER BY tipo_produto ASC'''
        dados = conecta_no_banco.connect_banco(script= script,bd='shekina', opção= 'fetchall')
    
    elif dados_da_busca == 'especifico':
        script = f''' SELECT * FROM produtos_shekina WHERE ativo = 'SIM' AND tipo_produto = '{tipo}'  '''
        dados = conecta_no_banco.connect_banco(script= script,bd='shekina', opção= 'fetchall')
    
    elif dados_da_busca == 'like':
        script = f''' select * from produtos_shekina WHERE ativo = 'SIM' AND descricao_item LIKE '%{tipo}%'  '''
        dados = conecta_no_banco.connect_banco(script= script,bd='shekina', opção= 'fetchall')

    valor = len(dados)
    return dados



def contador(ativo=['SIM', 'NAO']):      
          
    script = script = f''' SELECT COUNT(id_item) FROM produtos_shekina WHERE ativo = '{ativo}' '''
    dados = conecta_no_banco.connect_banco(script= script,bd='shekina', opção= 'fetchone')
    

    return dados[0]







## -------------------- PUBLICO ------------------------- ##

@app.route('/')
def homepage():
  

    return render_template('homepage.html', produto= dados_banco(dados_da_busca='completo'), lista_num = int(valor))



@app.route('/catalogo/pesquisa', methods=['GET','POST'])
def buscar_catalogo_por_pesquisa():
    item_pesquisa = request.form['barra_pesquisa'].capitalize()
    produto = item_pesquisa

    return render_template('homepage.html', produto= dados_banco('like',produto), lista_num = int(valor))




@app.route('/catalogo/<produto>')
def buscar_catalogo_por_produto(produto):


    return render_template('homepage.html', produto= dados_banco('especifico',produto), lista_num = int(valor))




@app.route('/detalhe/<produto>')
def detalhe_produto(produto):
    script= f''' SELECT * FROM produtos_shekina WHERE descricao_item ='{produto}' '''


    detalhe_item = conecta_no_banco.connect_banco(script=script, bd='shekina',opção='fetchone')



    return render_template('detalhe.html', teamplate = 'base', detalhe_descricao_produto = detalhe_item[1] , detalhe_valor_produto = detalhe_item[3], detalhe_imagem_produto = detalhe_item[2], detalhe_tipo_produto=detalhe_item[4])






## --------------------- ADMIN  ---------------------- ##


@app.route('/admin')
def login_admin():
    
    return render_template('login.html', login_incorreto = False)



@app.route('/validacao', methods=['POST'])
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

    script = f''' SELECT * FROM produtos_shekina WHERE ativo = 'SIM' ORDER BY tipo_produto  '''

    lista_de_itens_cadastrados_ativos = conecta_no_banco.connect_banco(script=script,bd='shekina',opção='fetchall')
    
    script = f''' SELECT * FROM produtos_shekina WHERE ativo = 'NAO' '''

    lista_de_itens_cadastrados_desativados = conecta_no_banco.connect_banco(script=script,bd='shekina',opção='fetchall')


    return render_template('cadastro.html', lista_de_itens_cadastrados_ativos= lista_de_itens_cadastrados_ativos, 
                           lista_de_itens_cadastrados_desativados= lista_de_itens_cadastrados_desativados, 
                           numero_ativos = contador(ativo='SIM'), 
                           numero_desativados = contador(ativo='NAO')  )




@app.route('/cadastro-produto=true', methods=['POST'])
def cadastro():
    novo_item_descricao = request.form['novo_item_descricao']
    novo_item_link = request.form['novo_item_link']
    novo_item_valor = request.form['novo_item_valor']
    novo_item_tipo = request.form['novo_item_tipo']
    novo_item_ativo = request.form['novo_item_ativo']
    script = f''' INSERT INTO produtos_shekina (descricao_item, link_imagem_item, valor_item, tipo_produto, ativo) 
                VALUES ('{novo_item_descricao}','{novo_item_link}','{novo_item_valor}','{novo_item_tipo}', '{novo_item_ativo}') '''
    conecta_no_banco.connect_banco(script=script,bd='shekina',opção='insert')

    return redirect('/cadastro-produto')




@app.route('/ativacao',  methods=['POST'])
def ativacao():
    item_id_para_ativar = request.form['id_item_a_ativar']
    try:
        script = f''' UPDATE produtos_shekina SET ativo = 'SIM' WHERE id_item = '{item_id_para_ativar}' '''
        conecta_no_banco.connect_banco(script=script, bd='shekina',opção='update')
    
    except:
        print('Não atualizou')

    return redirect('/cadastro-produto')




@app.route('/desativacao', methods=['POST'])
def desativacao():
    item_id_para_desativar = request.form['id_item_a_desativar']
    try:
        script= f''' UPDATE produtos_shekina SET ativo = 'NAO' WHERE id_item = '{item_id_para_desativar}'  '''
        conecta_no_banco.connect_banco(script, 'shekina', 'update')
    except:
        print('Não atualizou')


    return redirect('/cadastro-produto')




id_respawn = []

@app.route('/edicao', methods=['POST'])
def edicao():
    global id_item

    try:
        id_item = request.form['id_item_a_editar']
        id_respawn.insert(0,int(id_item))
        print(id_respawn)
    except:
        id_item = id_respawn[0]


    script= f''' SELECT * FROM produtos_shekina WHERE id_item = '{id_item}' '''

    detalhe_item = conecta_no_banco.connect_banco(script=script, bd='shekina',opção='fetchone')

    return render_template(['detalhe.html','edicao.html'], teamplate = 'edicao', detalhe_descricao_produto = detalhe_item [1], detalhe_imagem_produto = detalhe_item[2], detalhe_valor_produto= detalhe_item[3], infos = detalhe_item)




@app.route('/edicao=True', methods=['POST'])
def edicao_true():
    descricao_atualizada = request.form['descricao']
    link_atualizado = request.form['link']
    valor_atualizado = request.form['valor']
    tipo_atualizado = request.form['tipo']

    script = f'''UPDATE produtos_shekina SET descricao_item = '{descricao_atualizada}', link_imagem_item = '{link_atualizado}', valor_item = '{valor_atualizado}', tipo_produto = '{tipo_atualizado}' WHERE id_item = '{id_item}' '''
    atualizacao = conecta_no_banco.connect_banco(script, 'shekina', 'update')

    return edicao()





if __name__ == '__main__':
    app.run(host='localhost', port=9001, debug=True)


