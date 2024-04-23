import psycopg2


class conecta_no_banco:
    def connect_banco(script, bd, opção=['fetchall','fetchone','insert' or 'update' ]):
        banco = psycopg2.connect(database= bd, user='postgres', password='1804')
        cursor= banco.cursor()
        cursor.execute(script)

        if opção == 'fetchall':
            response = cursor.fetchall()

        elif opção == 'fetchone':
            response = cursor.fetchone()
        
        elif opção == 'insert':
            response = banco.commit()
            print('usuario cadastrado')
        elif opção == 'update':
            response = banco.commit()
            print('usuario atualizado')

        return response
    
    