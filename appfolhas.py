import PySimpleGUI as sg
import mysql.connector

class AppFolhas:
    def Conectar(self):
        self.con = mysql.connector.connect(host='localhost', database='your-database', user = 'your-user-mysql', password = 'your-senha-mysql')

        if self.con.is_connected():
            print('Conectado!')

        self.cursor = self.con.cursor()

    def Iniciar(self):
        self.Conectar()

        self.parar =True

        estilo = [
            [sg.Button('Ver Nomes')],
            [sg.Text('Escreva o nome',size=(39,0))],
            [sg.Input(size=(39,0),key='nome',focus=True)],
            [sg.Text('Escreva a quantidade de folhas usadas',size=(39,0))],
            [sg.Input(size=(39,0),key='qtd',do_not_clear=False,)],
            [sg.Button('Inserir'),sg.Button('Deletar')],
            [sg.Output(size=(50,10), key = '_output_')],
            [sg.Button('Limpar Historico',)]
        ]        
        self.janela = sg.Window('AppFolhas',layout=estilo)   

        while self.parar:

            self.eventos, self.valores = self.janela.Read()
            self.cursor.execute(f'SELECT * FROM prof WHERE (nome = "{self.valores["nome"].upper()}" )')
            dados =self.cursor.fetchall()           
            
            if self.eventos == 'Inserir': 
                if len(self.valores["nome"]) > 0 and len(self.valores["qtd"])>0:

                    if len(dados)==0:
                    
                        self.cursor.execute(f'INSERT INTO prof (nome, folhasdisponiveis) VALUES ("{self.valores["nome"].upper()}","{self.valores["qtd"]}" )')

                        self.con.commit()                
                        
                        print(f'Nome inserido: {self.valores["nome"].upper()}. Quantidade de folhas {self.valores["qtd"]} \n')
                    
                    elif int(self.valores["qtd"]) + int(dados[0][2]) >0:
                        
                        novoValor = int(dados[0][2]) + int(self.valores["qtd"])
                        self.cursor.execute(f'UPDATE prof SET folhasdisponiveis = {novoValor} WHERE (nome = "{self.valores["nome"].upper()}");') 
                        self.con.commit()
                        print(f'Valor atualizado! Novo valor para {dados[0][1]} é de {novoValor} \n')

                    elif int(self.valores["qtd"]) + int(dados[0][2]) <0:
                        print(f"A quantidade de folhas disponiveis é de apenas {dados[0][2]} \n")
                
                else:
                    sg.popup('Algum dado está faltando!')

            if self.eventos == 'Ver Nomes':
               
               self.cursor.execute('SELECT * FROM prof')
               dunico = self.cursor.fetchall()
               
               for i in dunico:
                   print(i,'\n')    

            if self.eventos == 'Deletar':
                if len(dados)>0:
                
                    self.cursor.execute(f'DELETE FROM prof WHERE (nome = "{self.valores["nome"].upper()}");')
                    self.con.commit()
                    print(f'{self.valores["nome"].upper()} foi deletado(a)\n')
            
                else:
                    print(f'{self.valores["nome"].upper()} não existe!\n')
            
            if self.eventos == 'Limpar Historico':
                self.janela.FindElement('_output_').Update('')

            elif self.eventos == sg.WIN_CLOSED:
                
                self.parar = False
                self.con.close()




folha = AppFolhas()
folha.Iniciar()

