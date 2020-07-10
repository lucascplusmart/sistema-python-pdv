from tkinter import messagebox
import sqlite3
from tkinter import *
from tkinter import ttk
import datetime
import math
import tkinter

connection = sqlite3.connect('systemdata.db')
cursor = connection.cursor()

produto_preco = []
listVt=[]
 # -> testa tela cadastrar produtos
# -> testa a tela de venda

date = datetime.datetime.now().date()

# transformando a lista de tupla em dicionario
# idx -> key
# col -> colunas
def dict_factory(cursor, row):
    dicionario = {}
    for idx, col in enumerate(cursor.description):
        dicionario[col[0]] = row[idx]
    return dicionario
class WindowVenda():
    def __init__(self):
        self.index=0
        self.ckek_car = False
        self.master = Tk()
        self.AppBar = Frame(self.master, width=1350,
                            height=100, bg='black', bd=9, relief="raise")
        self.AppBar.pack(side=TOP, fill=X)

        self.bordy = Frame(self.master, width=500, height=500)
        self.bordy.pack(fill=BOTH, expand=True)

        self.container = Frame(self.bordy, width=500,
                               height=500, bd=9, relief="raise")
        self.container.pack(anchor=CENTER, pady=50)

     

        self.menu = Menu(self.master, tearoff=0)
        self.menuBar = Menu(self.menu, tearoff=0)

        self.menuBar2 = Menu(self.menu)

        self.menuBar.add_command(
            label="cadastrar produtos", command=self.window_cadastrar_produtos)
        self.menuBar.add_command(label="Limpar tudo", command=self.limpar)
        self.menuBar.add_separator()
        self.menuBar.add_command(label="Sair", command=self.window_login)

        self.menu.add_cascade(label="opção", menu=self.menuBar)
        self.master.config(menu=self.menu)

        self.menu.add_cascade(label="Excluir Produto da Lista",command=self.remove_listproduto)
        self.master.config(menu=self.menu)

        self.lb_title = Label(self.AppBar, text='TELA DE VENDA',
                              fg='white', bg='black', font="Times 50 bold italic")
        self.lb_title.pack(anchor=CENTER)

        self.lb_data_1 = Label(
            self.container, text='Data:' + str(date), font=["arial", 16], anchor=CENTER)
        self.lb_data_1.grid(row=0, column=0, sticky='n')

        # label produto
        self.inserir = Label(self.container, text='Digite o nome :', font=[
                             "arial", 16], anchor='w', padx="5", pady="25")
        self.inserir.grid(row=1, column=0)
        # Entry produtos:
        self.entry_inserir = Entry(self.container, font=["arial", 16], bd=5)
        self.entry_inserir.grid(row=1, column=1)
        
        self.produtonome = Label(self.container,text="")
        self.produtonome.grid(row=2, column=0)

        self.preco = Label(self.container, text="")
        self.preco.grid(row=3, column=0)

        # self.button_pesq = Button(self.container,text="Pesquisar",fg="black",relief='flat',font="arial 12 bold ", command= self.pesq)
        # self.button_pesq.grid(row=1,column=2,padx=5)

        self.imagemBotton = PhotoImage(file="lupa.png")
        self.button_pesq = Button(
            self.container, image=self.imagemBotton, relief='flat', command=self.pesq)
        self.button_pesq.grid(row=1, column=2,padx=5)

       


        self.master.wm_iconbitmap("iconepy.ico")
        self.master.title("Tela de Venda")
        #self.master["bg"] = "black"
        self.master.mainloop()

    def pesq(self):
  
        self.search_name = self.entry_inserir.get()
        
        if self.search_name =='':
                messagebox.showwarning(title='INFO', message='campo de pesquisar vazio')
        else:
            try:
                cursor.row_factory = dict_factory
                cursor.execute(
                    'SELECT  *FROM produtos WHERE  nome = "{}"'.format(self.search_name))
                result = cursor.fetchall()
                

                self.get_nome = result[0]['nome']
                self.get_preco = result[0]['preco_venda']
                self.get_estoque = result[0]['stock']   
                   

            except:
                messagebox.showwarning(title='INFO', message='Erro ao realizar consultar')

            self.produtonome['text']= "Nome:"+str(self.get_nome)
            self.produtonome ["font"]=["arial", 16]
            self.produtonome["padx"],self.produtonome["pady"] = 5 , 15

            self.preco.config(text='Preço R$:' + str(self.get_preco),
                            padx=5, pady=15, font=["arial", 16])

            self.quantidade = Label(
                self.container, text='Quantidade:', font=["arial", 16])
            self.quantidade.grid(row=4, column=0, padx=5, pady=15)

            self.quantidade_ed = Entry(
                self.container, width=25, font=["arial", 16])
            self.quantidade_ed.grid(row=4, column=1, padx=5, pady=15)

            self.quantidade_ed.focus()

            self.desconto = Label(
                self.container, text='Desconto:', font=["arial", 16])
            self.desconto.grid(row=5, column=0, padx=5, pady=15)

            self.desconto_ed = Entry(self.container, width=25, font=["arial", 16])
            self.desconto_ed.grid(row=5, column=1, padx=5, pady=15)

            self.desconto_ed.insert(END, 0)

            self.total_pago = Label(
                self.container, text='Total Pago:', font=["arial", 16])
            self.total_pago.grid(row=6, column=0, padx=5, pady=15)

            self.total_pago_ed = Entry(
                self.container, width=25, font=["arial", 16])
            self.total_pago_ed.grid(row=6, column=1, padx=5, pady=15)

            self.tree = ttk.Treeview(self.container, selectmode="browse", column=(
                "column1", "column2", "column3"), show='headings')

            # self.tree.column("column1", width=40, minwidth=500, stretch=NO)
            # self.tree.heading('#1', text='ID')

            self.tree.column("column1", width=200, minwidth=500, stretch=NO)
            self.tree.heading('#1', text='Nome')

            self.tree.column("column2", width=100, minwidth=500,
                            stretch=NO, anchor=CENTER)
            self.tree.heading('#2', text='quantidade')

            self.tree.column("column3", width=100, minwidth=500,
                            stretch=NO, anchor=CENTER)
            self.tree.heading('#3', text='Preço de venda')

            self.tree.grid(row=0, column=4, columnspan=3, rowspan=6, sticky='nse')

            self.yscrollbar = ttk.Scrollbar(self.container, orient='vertical', command=self.tree.yview)
            self.tree.configure(yscrollcommand=self.yscrollbar.set)
            self.yscrollbar.grid(row=0, column=7, sticky='nse', padx=1, rowspan=5)
            self.yscrollbar.grid_configure(rowspan=6)
            self.yscrollbar.configure(command=self.tree.yview)
            self.vt_view()


            self.button_add = Button(self.container, text="ADD", width=15, font="arial 12 bold ", command=self.car)
            self.button_add.grid(row=7, column=0, padx=5, pady=5)

            self.button_total = Button(self.container, text="Total", width=15, font="arial 12 bold ",command=self.botao_total)
            self.button_total.grid(row=7, column=1, padx=5, pady=5)

            self.button_limapar = Button(
                self.container, text="Limpar", width=15, font="arial 12 bold ",command=self.limpar)
            self.button_limapar.grid(row=8, column=0, padx=5, pady=5)

            self.button_troco = Button(
                self.container, text="Calcular Troco", width=15, font="arial 12 bold ",command=self.troco)
            self.button_troco.grid(row=8, column=1, padx=5, pady=5)

            self.c_total= Label(self.container,text='', font=["arial", 16])
            self.c_total.grid(row=7,column=4)

            self.c_troco= Label(self.container,text='', font=["arial", 16])
            self.c_troco.grid(row=7,column=5)

            #=>Alternativa para mostra o troco e o total com a text da tkinter.
            #self.textbox = Text(self.container, height=6, width=50)
            #self.textbox.grid(row=7,column=4,sticky='nse')

            #self.yscrollbartext = ttk.Scrollbar(
            #self.container,orient='vertical', command=self.textbox.yview)
            #self.yscrollbartext.grid(row=7,column=6,columnspan=3,sticky='nse')

            #self.textbox.config(yscrollcommand=self.yscrollbartext.set)

    def vt_view(self):

        self.tree.delete(*self.tree.get_children())
        linhaV = []
        for linha in  listVt:
            linhaV.append(linha['nome'])
            linhaV.append(linha['quantidade'])
            linhaV.append(linha['preco'])
            self.tree.insert("", END, values=linhaV, iid=linha['id'], tag='1')
            linhaV.clear()

    def window_cadastrar_produtos(self):
        self.master.destroy()
        WindowCadastrarProdutos()
    def window_login(self):
        self.master.destroy()
        WindowLogin()
    def troco(self):
        if self.ckek_car:
            self.quantidade_valores = int(self.quantidade_ed.get())
            if self.quantidade_valores > int(self.get_estoque):
                messagebox.showinfo(title='INFOR', message='Quantidade acima do estoque')
            else:
                self.valor_recebido = float(self.total_pago_ed.get())
                self.total_troco = float(sum(produto_preco))
                self.valor_cliente = self.valor_recebido - (self.total_troco - float(self.desconto_ed.get()))
            self.c_troco.config(text='Troco R$:'+str(self.valor_cliente), font='arial 16')
            connection.commit()
        else:
            messagebox.showwarning(title='INFOR', message='adicioner o produto no carrinho precionando o botão add')
        self.ckek_car = False
    def botao_total(self):

        if self.ckek_car:
            soma_produto = sum(produto_preco) - float(self.desconto_ed.get())
            self.c_total.config(text='Total R$:'+str(soma_produto)) 
        else:
            messagebox.showwarning(title='INFOR', message='adicioner o produto no carrinho precionando o botão add')
    def limpar(self):
        self.desconto_ed.delete(0,END)
        self.quantidade_ed.delete(0,END)
        self.quantidade_ed.delete(0,END)
        self.entry_inserir.delete(0,END)
        self.total_pago_ed.delete(0,END)
        self.tree.delete(*self.tree.get_children())  
        produto_preco.clear()
        listVt.clear()
        self.index = 0
        
    def car(self): 
        self.quantidade_valores = self.quantidade_ed.get()

        if self.quantidade_valores == '':
            messagebox.showwarning(title='INFOR', message='informe a quantidade do produto')


        elif int(self.quantidade_valores) > int(self.get_estoque):
            messagebox.showinfo(
                title='INFOR', message='Quantidade acima do estoque')
        else:
            
            self.ckek_car = True
           # self.final_preco = (float(self.quantidade_valores) * float(self.get_preco)) - (float(self.desconto_ed.get()))
            self.final_preco = (float(self.quantidade_valores) * float(self.get_preco))
                                
            produto_preco.append(self.final_preco)
            dicprod = {"id":self.index,"nome":self.get_nome,"quantidade":self.quantidade_valores,"preco":self.final_preco}
            listVt.append(dicprod)
          
            self.vt_view()
            self.index=self.index+1
    def relatoriodaVenda(self):
        pass
    def remove_listproduto(self):
        try:
            indexDeletar = int(self.tree.selection()[0])
            listVt.pop(indexDeletar)
            produto_preco.pop(indexDeletar)
            self.vt_view()
        except AttributeError:
            messagebox.showinfo("INFO","Selecione o Produto, Para Excluir da Lista")        
class WindowCadastrarProdutos():
    def __init__(self):
        self.clickSelecionar = False

        self.master = Tk()
        self.AppBar = Frame(self.master, width=400, height=30,bg='black', bd=9, relief="raise")
        self.AppBar.pack(side=TOP, fill=X)
        
        self.menu = Menu(self.master,tearoff = 0)
        self.menuBar = Menu(self.menu,tearoff = 0)

        self.menuBar.add_command(label="Tela de Venda",command=self.windowvenda)
    
        self.menuBar.add_separator()
        self.menuBar.add_command(label="Sair",command=self.sair_cadastroproduto)
        self.menu.add_cascade(label="opção",menu=self.menuBar)
        
        self.menu.add_cascade(label="selecionar para atualizar",command=self.selecionar_produtos_atualizar)
        self.menu.add_cascade(label="limpar campos",command=self.limpar_campos)
        

        self.master.config(menu=self.menu)


        self.bordy = Frame(self.master, width=500, height=500, bg="#524f4f")
        self.bordy.pack(fill=BOTH, expand=True)
        # ===========label===================
        self.lb_color = "#524f4f"

        self.lb_title = Label(self.AppBar, text='Cadastra Produtos',
                              fg='white', bg='black', font="Times 20 bold italic",)
        self.lb_title.pack(anchor=CENTER)

        
        self.lb_nome_produto = Label(self.bordy, text='Nome:',fg='white',bg=self.lb_color,font=["arial", 12],)
        self.lb_nome_produto.grid(row=0, column=0, columnspan=1, padx=5, pady=5)
        
        self.lb_estoque_produto = Label(self.bordy, text='Estoque:',fg='white',bg=self.lb_color,font=["arial", 12])
        self.lb_estoque_produto.grid(row=1, column=0, columnspan=1, padx=5, pady=5)
        

        self.lb_precoCusto_produto = Label(self.bordy, text='Preço de Custo:',fg='white',bg=self.lb_color,font=["arial", 12])
        self.lb_precoCusto_produto.grid(row=2, column=0, columnspan=1, padx=5, pady=5)
        

        
        self.lb_precoVenda_produto = Label(self.bordy, text='Preço de Venda:',fg='white',bg=self.lb_color,font=["arial", 12])
        self.lb_precoVenda_produto.grid(row=3, column=0, columnspan=1, padx=5, pady=5)
        

        self.lb_forncecedor_produto = Label(self.bordy, text='Fornecedor:',fg='white',bg=self.lb_color,font=["arial", 12])
        self.lb_forncecedor_produto.grid(row=4, column=0, columnspan=1, padx=5, pady=5)
        

        self.lb_telforncecedor_produto = Label(self.bordy, text='Tel Fornecedor:',fg='white',bg=self.lb_color,font=["arial", 12])
        self.lb_telforncecedor_produto.grid(row=5, column=0, columnspan=1, padx=5, pady=5)
        
        # ================Entry========================
        self.entry_nome_produto = Entry(self.bordy,bd = 5)
        self.entry_nome_produto.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        self.entry_estoque_produto = Entry(self.bordy,bd = 5)
        self.entry_estoque_produto.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        
        self.entry_precoCusto_produto = Entry(self.bordy,bd = 5)
        self.entry_precoCusto_produto.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        self.entry_precoVenda_produto = Entry(self.bordy,bd = 5)
        self.entry_precoVenda_produto.grid(row=3, column=1, columnspan=2, padx=5, pady=5)


        self.entry_fornecedor_produto = Entry(self.bordy,bd = 5)
        self.entry_fornecedor_produto.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

        self.entry_telfornecedor_produto = Entry(self.bordy,bd = 5)
        self.entry_telfornecedor_produto.grid(row=5, column=1, columnspan=2, padx=5, pady=5)
        # ==========BOTÃO===================================================
        self.button_cadastrar_produtos = Button(self.bordy,  text='Cadastrar', width=15, bg='gray', relief='flat', highlightbackground='#524f4f',command=self._cadastrar_produtos)
        self.button_cadastrar_produtos.grid(row=6, column=0,padx=5, pady=5)

        self.button_atualizar_produtos = Button(self.bordy,  text='Atualizar', width=15, bg='gray', relief='flat', highlightbackground='#524f4f',command=self.atualizar_produtos)
        self.button_atualizar_produtos.grid(row=6, column=1, padx=5, pady=5)

        
        self.button_excluir_produtos = Button(self.bordy,  text='Excluir', width=15, bg='gray', relief='flat', highlightbackground='#524f4f',command=self.RemoverCadastrosBackEnd)
        self.button_excluir_produtos.grid(row=7, column=0,padx=5, pady=5)
        
        self.button_limpar_produtos = Button(self.bordy,  text='Limpar',width=15, bg='gray', relief='flat', highlightbackground='#524f4f',command=self._deletar_produtos)
        self.button_limpar_produtos.grid(row=7, column=1,padx=5, pady=5)

        # ===============treeViem===========
        self.tree = ttk.Treeview(self.bordy, selectmode="browse", column=(
            "column1", "column2", "column3","column4","column5","column6","column7","column8","column9"), show='headings')

        # self.tree.column("column1", width=40, minwidth=500, stretch=NO)
        # self.tree.heading('#1', text='ID')

        self.tree.column("column1", width=200, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='Nome')

        self.tree.column("column2", width=60, minwidth=500, stretch=NO,anchor=CENTER)
        self.tree.heading('#2', text='Estoque')

        self.tree.column("column3", width=100, minwidth=500, stretch=NO,anchor=CENTER)
        self.tree.heading('#3', text='Preço de Custo')

        self.tree.column("column4", width=100, minwidth=500, stretch=NO,anchor=CENTER)
        self.tree.heading('#4', text='Preço de venda')

        self.tree.column("column5", width=100, minwidth=500, stretch=NO,anchor=CENTER)
        self.tree.heading('#5', text='Fornecedor')

        self.tree.column("column6", width=100, minwidth=500, stretch=NO,anchor=CENTER)
        self.tree.heading('#6', text='Tel_Fornecedorr')

        self.tree.column("column7", width=100, minwidth=500, stretch=NO,anchor=CENTER)
        self.tree.heading('#7', text='Total Custo')

        self.tree.column("column8", width=100, minwidth=500, stretch=NO,anchor=CENTER)
        self.tree.heading('#8', text='Total Venda')

        self.tree.column("column9", width=60, minwidth=500, stretch=NO,anchor=CENTER)
        self.tree.heading('#9', text='lucro')




        self.tree.grid(row=0, column=4, pady=10, columnspan=3,rowspan=6,sticky='ne')  

        self.yscrollbar = ttk.Scrollbar(self.bordy, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.yscrollbar.set)
        self.yscrollbar.grid(row=0, column=7, sticky='nse',padx=1,pady=10,rowspan=5)
        self.yscrollbar.grid_configure(rowspan=6)
        self.yscrollbar.configure(command=self.tree.yview)

        self._vizualizar_backend_produtos()

        self.master.title("Cadastra Produtos")
        self.master.wm_iconbitmap("iconepy.ico")
        self.master.resizable(FALSE, FALSE)
        self.master.mainloop()

    def _vizualizar_backend_produtos(self):
        try:
            cursor.row_factory = dict_factory
            cursor.execute('select * from produtos')
            result = cursor.fetchall()
        except:
            messagebox.showerror("INFO","Erro ao fazer consultar ao banco de dados")
  
        self.tree.delete(*self.tree.get_children())

        linhaV = []
        for linha in result:
            linhaV.append(linha['nome'])
            linhaV.append(linha['stock'])
            linhaV.append(linha['preco_custo'])
            linhaV.append(linha['preco_venda'])
            linhaV.append(linha['fornecedor'])
            linhaV.append(linha['tel_fornecedor'])
            linhaV.append(linha['total_custo'])
            linhaV.append(linha['total_venda'])
            linhaV.append(linha['lucro'])

            self.tree.insert("", END, values=linhaV, iid=linha['id'], tag='1')
            linhaV.clear()
    def  _cadastrar_produtos(self):
            nome = self.entry_nome_produto.get()
            stock = self.entry_estoque_produto.get()
            preco_custo =self.entry_precoCusto_produto.get()
            preco_venda =self.entry_precoVenda_produto.get()
            fornecedor = self.entry_fornecedor_produto.get()
            tel_fornecedor = self.entry_telfornecedor_produto.get()

            total_custo = float(preco_custo) * float(stock)
            total_venda = float(preco_venda) * float(stock)
            lucro = float(preco_venda) - float(preco_custo)
            
            if nome != '' and stock != '' and preco_custo != '' and  preco_venda != '':
                
                cursor.execute('''insert into produtos 
                (nome,stock,preco_custo,preco_venda,fornecedor,tel_fornecedor,total_custo,total_venda,lucro)
                values
                (?,?,?,?,?,?,?,?,?)''',
                (nome,stock,preco_custo,preco_venda,fornecedor,tel_fornecedor,total_custo,total_venda,lucro))
                connection.commit()
                messagebox.showinfo(title='INFO', message='produto cadastrado com sucesso')
                self._vizualizar_backend_produtos()  
                 
            else:
                messagebox.showinfo(title='!', message='preencar todos os campos')
             
    def RemoverCadastrosBackEnd(self):

        idDeletar = int(self.tree.selection()[0])
        try:
            cursor.execute('delete from produtos where id = {}'.format(idDeletar))
            connection.commit()
        
        except:
             messagebox.showerror(title='INFO', message='ERRO ao excluir Produto')
             
        self._vizualizar_backend_produtos()
    def _deletar_produtos(self):
        if messagebox.askokcancel('Deletar dados CUIDADO!!', 'DESEJA EXCLUIR TODOS OS DADOS DA TABELA ? NAO HÁ VOLTA'):
            try:
                with connection.cursor() as cursor:
                    cursor.execute('DELETE FROM table produtos')
                    connection.commit()
            except:
                messagebox.showinfo(title='INFO', message='Erro ao Deletar Todos os Produto')
            self._vizualizar_backend_produtos()
    def selecionar_produtos_atualizar(self):
        try:
            idAtualizar = int(self.tree.selection()[0])
            cursor.row_factory = dict_factory
            cursor.execute('SELECT * FROM produtos WHERE id = {}'.format(idAtualizar))
            result = cursor.fetchall()
        except IndexError:
            messagebox.showinfo("INFO","o produto não está selecionado")
        except:
            messagebox.showerror("INFO","erro ao consultar o banco de dados")
        
        self.limpar_campos()

        self.entry_nome_produto.insert(0,str(result[0]["nome"]))
        self.entry_estoque_produto.insert(0,str(result[0]["stock"]))
        self.entry_precoCusto_produto.insert(0,str(result[0]["preco_custo"]))
        self.entry_precoVenda_produto.insert(0,str(result[0]["preco_venda"]))
        self.entry_fornecedor_produto.insert(0,str(result[0]["fornecedor"]))
        self.entry_telfornecedor_produto.insert(0,str(result[0]["tel_fornecedor"]))

        self.clickSelecionar = True
    def atualizar_produtos(self):
        if self.clickSelecionar:
            nome = self.entry_nome_produto.get()
            stock = self.entry_estoque_produto.get()
            preco_custo =self.entry_precoCusto_produto.get()
            preco_venda =self.entry_precoVenda_produto.get()
            fornecedor = self.entry_fornecedor_produto.get()
            tel_fornecedor = self.entry_telfornecedor_produto.get()
            
            idup = int(self.tree.selection()[0])
            
            if nome != '' and stock != '' and preco_custo != '' and  preco_venda != '':

                total_custo = float(preco_custo) * float(stock)
                total_venda = float(preco_venda) * float(stock)
                lucro = float(preco_venda) - float(preco_custo)

                cursor.execute('''UPDATE produtos SET
                nome =?,stock=?,preco_custo=?,preco_venda=?,fornecedor=?,tel_fornecedor=?,total_custo=?,total_venda=?,lucro=? where  id = ?''',
                (nome,stock,preco_custo,preco_venda,fornecedor,tel_fornecedor,total_custo,total_venda,lucro,idup))
                connection.commit()
                messagebox.showinfo(title='INFO', message='produto atualizado cadastrado com sucesso')
                self._vizualizar_backend_produtos()
            else:
                messagebox.showinfo(title='!', message='preencar todos os campos')
             
        else:
            messagebox.showinfo(title='INFO-COMO FAZER ALTERAÇÃO', message='''selecione o produto que se deseja fazer alteração,seguee o passo-a-passo:\n
                1º) click na parte superio em,\"Selecionar para atualizar"\n
                2º) faça as alterações\n
                3º) com as alteraçõe e click do botão atualizar\n
            \t\tfim (:''')
    def limpar_campos(self):
        self.entry_nome_produto.delete(0,END)
        self.entry_estoque_produto.delete(0,END)
        self.entry_precoCusto_produto.delete(0,END)
        self.entry_precoVenda_produto.delete(0,END)
        self.entry_fornecedor_produto.delete(0,END)
        self.entry_telfornecedor_produto.delete(0,END)     
    def windowvenda(self):
        self.master.destroy()
        WindowVenda()
    def sair_cadastroproduto(self):
        self.master.destroy()
        WindowLogin()
class WindowEditarCadastro():
    def __init__(self):
        self.clickSelecionar = False
        self.master = Tk()
        self.us = IntVar() # #=> 0 ,começa marcado 1, começa desmarcado
        self.AppBar = Frame(self.master, width=1350,
                            height=100, bg='black', bd=9, relief="raise")
        self.AppBar.pack(side=TOP, fill=X)

        self.bordy = Frame(self.master, width=500, height=500)
        self.bordy.pack(fill=BOTH, expand=True)

        self.menu = Menu(self.master,tearoff = 0)
        self.master.config(menu=self.menu)
        self.menu.add_cascade(label="Sair",command=self.sair_editarcadastro)
        self.menu.add_cascade(label="Selecionar para atualizar",command=self.selecionar_login_atualizar)
        self.menu.add_cascade(label="Limpar campos",command=self.limpar_login_campos)
        self.menu.add_cascade(label="Deletar Dados", command=self.deletar_login_todos)

        self.lb_title = Label(self.AppBar, text='Cadastros', fg='white', bg='black', font="Times 20 bold italic")
        self.lb_title.pack(anchor=CENTER)
        self.lb_usuario = Label(
        self.bordy, text='Usuario:', font="Times 15 bold italic", padx="5")
        self.lb_usuario.grid(row=0, column=0)
        self.lb_senha = Label(self.bordy, text='Senha:',font="Times 15 bold italic")
        self.lb_senha.grid(row=1, column=0)
        self.lb_nivel = Label(self.bordy, text='Nivel:',font="Times 15 bold italic")
        self.lb_nivel.grid(row=2, column=0)
        # entry
        self.entry_usuario = Entry(self.bordy)
        self.entry_usuario.grid(row=0, column=1)
        self.entry_senha = Entry(self.bordy)
        self.entry_senha.grid(row=1, column=1)
          
        self.entry_nivel_normal = Radiobutton(self.bordy,text='Usuario Normal', value=0, variable=self.us)
        self.entry_nivel_normal.grid(row=3, column=1)

        self.entry_nivel_master = Radiobutton(self.bordy,text='Usuario Master', value=1, variable=self.us)
        self.entry_nivel_master.grid(row=2, column=1)
      
       
        self.button_atulizar = Button(self.bordy, text='Atualizar', width=10, bg='springGreen2', fg='black', font=["arial", 12],command=self.upadate_login)
        self.button_atulizar.grid(row=4,column=0,padx=5)
        self.button_excluir = Button(self.bordy, text='Excluir', width=10, bg='#b30000',fg='black', font=["arial", 12],command=self.excluir_login)
        self.button_excluir.grid(row=4,column=1)

        self.tree = ttk.Treeview(self.bordy, selectmode="browse", column=(
            "column1", "column2", "column3", "column4"), show='headings')

        self.tree.column("column1", width=40, minwidth=500, stretch=NO,anchor=CENTER)
        self.tree.heading('#1', text='ID')

        self.tree.column("column2", width=100, minwidth=500, stretch=NO,anchor=CENTER)
        self.tree.heading('#2', text='Usuario')

        self.tree.column("column3", width=100, minwidth=500, stretch=NO,anchor=CENTER)
        self.tree.heading('#3', text='Senha')

        self.tree.column("column4", width=40, minwidth=500, stretch=NO,anchor=CENTER)
        self.tree.heading('#4', text='Nivel')

        self.tree.grid(row=0, column=2, pady=10, columnspan=3,rowspan=6,sticky='ne',padx=5) 
        self.backend_vizualizarCadastro()


        self.master.title("Visualizar Cadastro")
        self.master.wm_iconbitmap("iconepy.ico")
        self.master.resizable(FALSE, FALSE)
        self.master.mainloop()
    

    def backend_vizualizarCadastro(self):
        try:
            cursor.row_factory = dict_factory
            cursor.execute('select * from cadastros')
            result = cursor.fetchall()
        except:
            messagebox.showerror("INFO","Erro ao fazer consultar ao banco de dados")
        #finally:
            #cursor.close()
        # apagando tudo que estar dentro da tree view
        self.tree.delete(*self.tree.get_children())

        linhaV = []
        for linha in result:
            linhaV.append(linha['id'])
            linhaV.append(linha['nome'])
            linhaV.append(linha['senha'])
            linhaV.append(linha['nivel'])
            self.tree.insert("", END, values=linhaV, iid=linha['id'], tag='1')
            linhaV.clear()

    def selecionar_login_atualizar(self):
        try:
            idAtualizar = int(self.tree.selection()[0])
            cursor.row_factory = dict_factory
            cursor.execute('SELECT * FROM cadastros WHERE id = {}'.format(idAtualizar))
            result = cursor.fetchall()
        except IndexError:
            messagebox.showinfo("INFO","o usuario não está selecionado")
        except:
            messagebox.showerror("INFO","erro ao consultar o banco de dados")

        self.limpar_login_campos()

        self.entry_usuario.insert(0,str(result[0]["nome"]))
        self.entry_senha.insert(0,str(result[0]["senha"]))
        self.clickSelecionar = True

    def upadate_login(self):
        if self.clickSelecionar:
            nivel = self.us.get()
            print(nivel)
            
            usuario= self.entry_usuario.get()
            senha = self.entry_senha.get()
            idtualizar = int(self.tree.selection()[0])
         
         
                
            if usuario != '' and senha !='' and nivel !='' :
                try:
                    cursor.execute('''UPDATE cadastros SET
                    nome =?,senha =?,nivel=? where id = ?''',
                    (usuario,senha,nivel,idtualizar))
                    connection.commit()
                    messagebox.showinfo(title='INFO', message='usuario atualizado cadastrado com sucesso')
                    self.backend_vizualizarCadastro()
                except:
                    messagebox.showerror(title='ERRO', message='Erro com ao conectar ao banco de dados')  
            else:
               messagebox.showinfo(title='!', message='preencar todos os campos') 
        else:
            messagebox.showinfo(title='INFO', message='''selecione o usuario que se deseja fazer alteração,segue passo-a-passo\n
            1º)click na parte superio em, \"Selecionar para atualizar"\n
            2º) faça as alterações\n
            3º) com as alteraçõe e click do botão atualizar\n
            \t\tfim (:''')

        self.clickSelecionar = False

    def limpar_login_campos(self):
        self.entry_usuario.delete(0,END)
        self.entry_senha.delete(0,END)
    def deletar_login_todos(self):
        if messagebox.askokcancel('Deletar dados CUIDADO!!', 'DESEJA EXCLUIR TODOS OS DADOS DA TABELA ? NAO HÁ VOLTA'):
            try:
                cursor.execute('DELETE FROM cadastros')
                connection.commit()
            except:
                messagebox.showinfo(title='INFO', message='Erro ao Deletar Todos os Cadastros')
            
        self.backend_vizualizarCadastro()
    def excluir_login(self):
        idexcluir = int(self.tree.selection()[0])
        try:
            cursor.execute('delete from cadastros where id = {}'.format(idexcluir))
            connection.commit()
        
        except:
             messagebox.showerror(title='INFO', message='ERRO ao excluir Produto')
             
        self.backend_vizualizarCadastro()
    def sair_editarcadastro(self):
        self.master.destroy()
        WindowLogin()
'''
class WindowADM():
    def __init__(self):
        self.master = Tk()
        self.AppBar = Frame(self.master, width=400, height=30,
                            bg='black', bd=9, relief="raise")
        self.AppBar.pack(side=TOP, fill=X)
        self.bordy = Frame(self.master, width=400, height=320)
        self.bordy.pack(fill=BOTH)
        # label
        self.lb_title = Label(self.AppBar, text='Adimistrador',
                              fg='white', bg='black', font="Times 20 bold italic")
        self.lb_title.pack(anchor=CENTER)
        
        self.button_window_venda = Button(self.bordy, text='Tela de Venda', width=20, bg='springGreen2', fg='black', font=[ "arial", 12], command=self.venda)
        self.button_window_venda.grid(row=0, column=0, padx=10,  pady=10)

        self.button_window_produto = Button(self.bordy, text='Cadastrar Produto', width=20, bg='springGreen2', fg='black', font=[ "arial", 12], command=self.cadastros_produtos)
        self.button_window_produto.grid(row=1, column=0, padx=10,  pady=10)

        self.button_usuario_cadastro = Button(self.bordy, text='Cadastros Usuario', width=20, bg='springGreen2', fg='black', font=[ "arial", 12], command=self.cadastros_usuarios)
        self.button_usuario_cadastro.grid(row=2, column=0, padx=10,  pady=10)

        self.button_novo_usuario = Button(self.bordy, text='Novo Usuario', width=20, bg='springGreen2', fg='black', font=[ "arial", 12], command=self.novo_usuario)
        self.button_novo_usuario.grid(row=3, column=0, padx=10,  pady=10)

        self.master.title("ADM")
        self.master.resizable(FALSE, FALSE)
        self.master.wm_iconbitmap("iconepy.ico")
        self.master.mainloop()
      
    def cadastros_usuarios(self):
        self.master.destroy()
        WindowEditarCadastro()
    def novo_usuario(self):
        self.master.destroy()
        WindowCadastrar()
    def cadastros_produtos(self):
        self.master.destroy()
        WindowCadastrarProdutos()
    def venda(self):
        self.master.destroy()
        WindowVenda()'''
class WindowCadastrar():
    def __init__(self):
        # container --> Frames
        self.master = Tk()

        self.menu = Menu(self.master,tearoff = 0)
        self.menu.add_cascade(label="Sair",command=self.sair_cadastro)
        
        

        self.master.config(menu=self.menu)

        self.AppBar = Frame(self.master, width=400, height=30,
                            bg='black', bd=9, relief="raise")
        self.AppBar.pack(side=TOP, fill=X)
        self.bordy = Frame(self.master, width=400, height=320)
        self.bordy.pack(fill=BOTH)
        # label
        self.lb_title = Label(self.AppBar, text='Tela de Cadastro',
                              fg='white', bg='black', font="Times 20 bold italic")
        self.lb_title.pack(anchor=CENTER)

        self.lb_usuario = Label(
            self.bordy, text='Usuario:', font="Times 15 bold italic", padx="5", pady="25")
        self.lb_usuario.grid(row=0, column=0)
        self.lb_senha = Label(self.bordy, text='Senha:',
                              font="Times 15 bold italic", padx="5")
        self.lb_senha.grid(row=1, column=0)
        self.lb_chaveSeguranca = Label(
            self.bordy, text='Chave de Segurança :', font="Times 15 bold italic", padx="5", pady="25")
        self.lb_chaveSeguranca.grid(row=2, column=0)
        # entry
        self.entry_usuario = Entry(self.bordy)
        self.entry_usuario.grid(row=0, column=1)
        self.entry_senha = Entry(self.bordy, show="*")
        self.entry_senha.grid(row=1, column=1)
        self.entry_chaveSeguranca = Entry(self.bordy)
        self.entry_chaveSeguranca.grid(row=2, column=1)
        # botão
        self.button_cadastrar = Button(self.bordy, text='cadastrar', width=20, bg='springGreen2', fg='black', font=[
                                       "arial", 12], command=self.CadastroBackEnd)
        self.button_cadastrar.grid(
            row=3, column=0, columnspan=3, padx=10,  pady=10)

        self.master.title("Cadastro")
        self.master.geometry("400x300+500+200")
        self.master.wm_iconbitmap("iconepy.ico")
        self.master.resizable(FALSE, FALSE)
        self.master.mainloop()
    def CadastroBackEnd(self):
        codigoPadrao = '123'
        if self.entry_chaveSeguranca.get() == codigoPadrao:
            if len(self.entry_usuario.get()) <= 20:

                if len(self.entry_senha.get()) <= 50:
                    nome = self.entry_usuario.get()
                    senha = self.entry_senha.get()
                    try:
                        cursor.execute('insert into cadastros (nome, senha, nivel) values (?, ?, ?)', (nome, senha, 0))
                        connection.commit()
                        messagebox.showinfo('Cadastro', 'Usuario cadastrado com sucesso')
                        self.master.destroy()
                        WindowLogin()
                    except:
                        messagebox.showerror('INFO',"ERRO ao conectar ao banco de dados")          
                    #finally:
                        #cursor.close()
                else:
                    messagebox.showinfo(
                        'ERRO', 'Por favor insira um senha com 50 ou menos caracteres')
            else:
                messagebox.showinfo(
                    'ERRO', 'Por favor insira um nome com 20 ou menos caracteres')
        else:
            messagebox.showinfo('ERRO', 'Erro no codigo de segurança')
    def sair_cadastro(self):
        self.master.destroy()
        WindowLogin()
class WindowLogin():
    def __init__(self):
            # container Frames
        self.master = Tk()

        self.AppBar = Frame(self.master, width=400, height=30,
                            bg='black', bd=9, relief="raise")
        self.AppBar.pack(side=TOP, fill=X)
        self.bordy = Frame(self.master, width=400, height=320)
        self.bordy.pack(fill=BOTH)
        # label
        self.lb_title = Label(self.AppBar, text='Tela de Login',
                              fg='white', bg='black', font="Times 20 bold italic")
        self.lb_title.pack(anchor=CENTER)

        self.lb_usuario = Label(
            self.bordy, text='Usuario:', font="Times 15 bold italic", padx="5", pady="25")
        self.lb_usuario.grid(row=0, column=0)
        self.lb_senha = Label(self.bordy, text='Senha:',
                              font="Times 15 bold italic", padx="5")
        self.lb_senha.grid(row=1, column=0)
        # entry
        self.entry_usuario = Entry(self.bordy,bd = 5)
        self.entry_usuario.grid(row=0, column=1,)
        self.entry_senha = Entry(self.bordy, show="*",bd = 5)
        self.entry_senha.grid(row=1, column=1)
        # botão
        self.button_cadastra = Button(self.bordy, text='cadastra-se', width=10,
                                      bg="orange3", fg='black', font=["arial", 12], command=self.cadastra)
        self.button_cadastra.grid(row=2, column=0, padx=10,  pady=10)

        self.button_login = Button(self.bordy, text='login', bg="springGreen2", width=10, fg='black', font=[
                                   "arial", 12], command=self.logar)
        self.button_login.grid(row=2, column=1,  padx=10,  pady=10)
        self.CheckVar1 = IntVar()
        self.chek_button = Checkbutton(self.bordy, text="adm", variable=self.CheckVar1, offvalue=0,
                                       onvalue=1, width=20)
        self.chek_button.grid(row=0, column=2, padx=10,  pady=10)

        self.master.title("Tela de Login")
        self.master.geometry("400x250+500+200")
        self.master.wm_iconbitmap("iconepy.ico")
        self.master.resizable(FALSE, FALSE)
        self.master.mainloop()
    def logar(self):
        autenticado = False
        nivel = self.CheckVar1.get()
        userMaster = False
        
        try:
            cursor.row_factory = dict_factory
            cursor.execute('select * from cadastros')
            result = cursor.fetchall()
        except:
            messagebox.showerror("INFO","Erro ao fazer consultar ao banco de dados")

        user = self.entry_usuario.get()
        password = self.entry_senha.get()

        for linha in result:
            if user == linha['nome'] and password == linha['senha']:
                #print(nivel)
                #print(linha['nivel']) 
                # => melhorar as condições.
                if linha['nivel']==nivel and linha['nivel'] == 1:#usuario master

                    messagebox.showinfo(title='INFO', message='usuario master')
                    autenticado = True
                    userMaster = True
                    break

                if linha['nivel']==nivel and linha['nivel'] ==0 :#usuario não é master
                    messagebox.showinfo(title='INFO', message='usuario não é master')
                    autenticado = True
                    break
            else:
                autenticado = False
    
        if autenticado:
            if userMaster:
                self.master.destroy()
                WindowEditarCadastro()
            else:
                self.master.destroy()
                WindowVenda()
        else:
            messagebox.showwarning(
            title='INFO', message='Erro, usuario ou senha iválido')
    def cadastra(self):
        self.master.destroy()
        WindowCadastrar()
if __name__ =='__main__':
        GUUEST = WindowLogin()


