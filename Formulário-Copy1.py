#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter  
from openpyxl import load_workbook
from datetime import datetime
from tkinter import messagebox
import re
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
import cv2


# In[11]:


class Login():
    
    def __init__(self,janela,df_usuarios,aba_usuarios):
        self.janela = janela
        self.df_usuarios = df_usuarios
        self.aba_usuarios = aba_usuarios
        self.configuracao_janela_loguin()
        self.tela_loguin()
        
        
    def configuracao_janela_loguin(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()
        pos_x = int(largura_tela/2 - 400/2)
        pos_y = int(altura_tela/2 - 300/2)
        self.janela.geometry(f'{400}x{300}+{pos_x}+{pos_y}')
        self.janela.title('Login')
        self.janela.resizable('False','False')


    def tela_loguin(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        texto_loguin = customtkinter.CTkLabel(janela,text='Usuário', font=('Arial Arrow',15,'bold'))
        texto_loguin.place(x=115,y=40)
        texto_senha = customtkinter.CTkLabel(janela,text='Senha', font=('Arial Arrow',15,'bold'))
        texto_senha.place(x=115,y=100)
        self.entry_loguin = customtkinter.CTkEntry(self.janela, placeholder_text='Insira o seu usuário aqui',font=('Arial Arrow', 12), width=170)
        self.entry_loguin.place(x=110,y=65)
        self.entry_senha = customtkinter.CTkEntry(self.janela, placeholder_text='Insira a sua senha aqui', font=('Arial Arrow', 12), width=170,show="*")
        self.entry_senha.place(x=110,y=125)
        self.botao_loguin = customtkinter.CTkButton(self.janela,text='Login',width=80,command=self.fazer_login)
        self.botao_loguin.place(x=110,y=200)
        self.botao_cadastro = customtkinter.CTkButton(self.janela,text='Cadastre-se',width=80,command=self.tela_cadastro)
        self.botao_cadastro.place(x=200,y=200)
        self.checkbox = customtkinter.CTkCheckBox(self.janela,text='Mostrar Senha',font=('Arial Arrow',12,'bold'),command=self.mostrar_senha)
        self.checkbox.place(x=110,y=160)
    
    
    def tela_cadastro(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        texto_loguin_cadastro = customtkinter.CTkLabel(janela,text='Usuário', font=('Arial Arrow',15,'bold'))
        texto_loguin_cadastro.place(x=115,y=40)
        texto_senha_cadastro = customtkinter.CTkLabel(janela,text='Senha', font=('Arial Arrow',15,'bold'))
        texto_senha_cadastro.place(x=115,y=100)
        texto_confirmar_senha = customtkinter.CTkLabel(janela,text='Confirmar Senha', font=('Arial Arrow',15,'bold'))
        texto_confirmar_senha.place(x=110, y=155)
        self.entry_loguin_cadastro = customtkinter.CTkEntry(self.janela, placeholder_text='Insira o seu usuário aqui',font=('Arial Arrow', 12), width=170)
        self.entry_loguin_cadastro.place(x=110,y=65)
        self.entry_senha_cadastro = customtkinter.CTkEntry(self.janela, placeholder_text='Crie a sua senha aqui', font=('Arial Arrow', 12), width=170,show="*")
        self.entry_senha_cadastro.place(x=110,y=125)
        self.entry_confirmar_senha = customtkinter.CTkEntry(self.janela, placeholder_text='Confirme a sua senha aqui', font=('Arial Arrow', 12), width=170,show="*")
        self.entry_confirmar_senha.place(x=110,y=180)
        self.botao_cadastro = customtkinter.CTkButton(self.janela,text='Cancelar',width=80,command=self.tela_loguin)
        self.botao_cadastro.place(x=110,y=220)
        self.botao_cancelar = customtkinter.CTkButton(self.janela,text='Cadastrar',width=80,command=self.cadastrar_usuario)
        self.botao_cancelar.place(x=200,y=220)
        
    
    def salvar_base_de_dados(self):
        with pd.ExcelWriter('usuarios.xlsx') as writer:
            self.df_usuarios.to_excel(writer,sheet_name=self.aba_usuarios,index=False)
            
    
    def mostrar_senha(self):
        if self.checkbox.get():
            self.entry_senha.configure(show='')
        else:
            self.entry_senha.configure(show='*')
                 
                
    def verificar_senha(self,senha):
        return all([len(senha) >= 8, re.search("[A-Z]", senha), re.search("[0-9]{3,}", senha), re.search("[@#$%^&+=]", senha)])

    
    def cadastrar_usuario(self):
        usuario = self.entry_loguin_cadastro.get()
        senha =self.entry_senha_cadastro.get()
        confirmar_senha = self.entry_confirmar_senha.get()
        cadastro = {'User': usuario,'Senha':senha}
        if usuario in self.df_usuarios['User'].tolist():#transforma pf.Series em uma lista e olha item por item
            tkinter.messagebox.showinfo(title='Erro de Cadastro', message='Esse nome de usuário já existe, tente outro.')
            return
        if not self.verificar_senha(senha):
            mensagem = '''
            A sua senha deve conter:
            - Deve ter no mínimo 8 caracteres
            - Deve ter pelo menos uma letra maiúscula
            - Deve ter pelo menos 3 números
            - Deve ter pelo menos um caractere especial (@, #, $, %, ^, &, +, ou =)
            '''
            tkinter.messagebox.showinfo(title='Erro de Cadastro', message=mensagem)
            return
        if senha != confirmar_senha:
            tkinter.messagebox.showinfo(title='Erro de Cadastro',message='As senhas não condizem. Certifique-se que são iguais.') 
            return
        tkinter.messagebox.showinfo(title='Cadastro',message='Cadastro feito com sucesso!') 
        df_cadastro = pd.DataFrame(cadastro, index=[0])
        self.df_usuarios = pd.concat([self.df_usuarios, df_cadastro], ignore_index=True)
        self.salvar_base_de_dados()
        self.tela_loguin()
        
        
    def fazer_login(self):
        usuario = self.entry_loguin.get()
        senha = self.entry_senha.get()
        if not usuario in self.df_usuarios['User'].tolist():
            tkinter.messagebox.showinfo(title='Erro de Login', message='Usuário não encontrado.')
            return
        if senha != self.df_usuarios.loc[self.df_usuarios['User'] == usuario, 'Senha'].values[0]:
            tkinter.messagebox.showinfo(title='Erro de Login', message='Senha incorreta.')
            return
        tkinter.messagebox.showinfo(title='Login', message='Login feito com sucesso!.')
        self.abrir_formulario()
        
    
    def abrir_formulario(self):
        self.janela.destroy() # Fecha a janela de login
        formulario = Formulario_cadastro(self.janela,img,df_cadastro)
        formulario.janela.mainloop()


# In[12]:


class Formulario_cadastro():

    def __init__(self, janela, img,df_cadastro):
        self.janela = janela
        self.img = None  # definir self.img como None
        self.df_cadastro = df_cadastro
        self.configuracao_janela_formlario()
        self.janela_formulario()
        self.entry_cep.bind('<FocusOut>', self.preencher_entrys)
        self.imagem_padrao()
        

    def configuracao_janela_formlario(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.janela = customtkinter.CTk()
        self.janela.resizable('False','False')
        self.janela.title('Formulário de Cadastro')
        self.janela.update_idletasks()
        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()
        pos_x = int(largura_tela/2 - 600/2)
        pos_y = int(altura_tela/2 - 600/2)
        self.janela.geometry(f'{600}x{600}+{pos_x}+{pos_y}')

    def janela_formulario(self):
        frame = tkinter.Frame(self.janela,width=600,height=50, bg='#1F538D')
        frame.place(x=0,y=0)
        texto = customtkinter.CTkLabel(self.janela,text='Formulário de Cadastro', font=('Arial Arrow',30,'bold'), fg_color='#1F538D')
        texto.pack(padx=10, pady=5)
        self.canvas = Canvas(self.janela, width=150, height=150, highlightthickness=0)
        self.canvas.place(x=430, y=75)
        
        
        
        
        self.botao_adicionar_imagem = customtkinter.CTkButton(self.janela, text='Adicionar Imagem', font=('Arial', 15), width=150, command=self.carregar_imagem)
        self.botao_adicionar_imagem.place(x=430, y=235)
        self.tirar_foto = customtkinter.CTkButton(self.janela, text='Tirar Foto', font=('Arial', 15), width=150,command=WebCam)
        self.tirar_foto.place(x=430, y=275)
        self.botao_limpar_campos = customtkinter.CTkButton(self.janela, text='Limpar Campos', font=('Arial', 15), width=150,command=self.limpar_entrys)
        self.botao_limpar_campos.place(x=430, y=315)
        self.botao_salvar_dados = customtkinter.CTkButton(self.janela, text='Salvar Dados', font=('Arial', 15), width=150,command=self.salvar_dados)
        self.botao_salvar_dados.place(x=430, y=355)
        
        
        
        
        
        
        
        
        texto_nome = customtkinter.CTkLabel(self.janela, text='Nome', font=('Arial', 15, 'bold'))
        texto_nome.place(x=20, y=60)
        self.entry_nome = customtkinter.CTkEntry(self.janela, placeholder_text='Insira o seu nome completo', font=('Arial', 15), width=300)
        self.entry_nome.place(x=20, y=85)
        texto_idade = customtkinter.CTkLabel(self.janela, text='Idade', font=('Arial', 15, 'bold'))
        texto_idade.place(x=20,y=120)
        self.entry_idade = customtkinter.CTkEntry(self.janela, placeholder_text='Insira a sua idade', font=('Arial', 15), width=130)
        self.entry_idade.place(x=20,y=145)
        texto_genero = customtkinter.CTkLabel(self.janela, text='Gênero', font=('Arial', 15, 'bold'))
        texto_genero.place(x=180,y=120)
        self.entry_genero = customtkinter.CTkComboBox(self.janela)
        self.entry_genero.place(x=180,y=145)
        self.entry_genero.set('')
        self.entry_genero.configure(values=['Masculino','Feminino','Outros'])
        texto_email = customtkinter.CTkLabel(self.janela, text='E-mail', font=('Arial', 15, 'bold'))
        texto_email.place(x=20,y=180)
        self.entry_email = customtkinter.CTkEntry(self.janela, placeholder_text='Insira o seu e-mail', font=('Arial', 15), width=300)
        self.entry_email.place(x=20,y=205)
        texto_celular = customtkinter.CTkLabel(self.janela, text='Celular com DDD', font=('Arial', 15, 'bold'))
        texto_celular.place(x=20,y=240)
        self.entry_celular = customtkinter.CTkEntry(self.janela, placeholder_text='Insira o seu número', font=('Arial', 15), width=150)
        self.entry_celular.place(x=20,y=265)
        texto_cep = customtkinter.CTkLabel(self.janela, text='CEP', font=('Arial', 15, 'bold'))
        texto_cep.place(x=190,y=240)
        self.entry_cep = customtkinter.CTkEntry(self.janela, placeholder_text='Insira o seu cep', font=('Arial', 15), width=130)
        self.entry_cep.place(x=190,y=265)
        texto_cidade = customtkinter.CTkLabel(self.janela, text='Cidade', font=('Arial', 15, 'bold'))
        texto_cidade.place(x=20,y=300)
        self.entry_cidade = customtkinter.CTkEntry(self.janela, placeholder_text='Insira a sua cidade', font=('Arial', 15), width=150)
        self.entry_cidade.place(x=20,y=325)
        texto_bairro =customtkinter.CTkLabel(self.janela, text='Bairro', font=('Arial', 15, 'bold')) 
        texto_bairro.place(x=190,y=300)
        self.entry_bairro = customtkinter.CTkEntry(self.janela, placeholder_text='Insira o seu bairro', font=('Arial', 15), width=130)
        self.entry_bairro.place(x=190,y=325)
        texto_rua = customtkinter.CTkLabel(self.janela, text='Rua', font=('Arial', 15, 'bold'))
        texto_rua.place(x=20,y=360)
        self.entry_rua = customtkinter.CTkEntry(self.janela, placeholder_text='Insira a sua rua', font=('Arial', 15), width=200)
        self.entry_rua.place(x=20,y=385)
        texto_uf =customtkinter.CTkLabel(self.janela, text='UF', font=('Arial', 15, 'bold'))
        texto_uf.place(x=230,y=360)
        self.entry_uf = customtkinter.CTkEntry(self.janela, placeholder_text='Insira a UF', font=('Arial', 15), width=90)
        self.entry_uf.place(x=230,y=385)
        texto_inforcames_adicionais = customtkinter.CTkLabel(self.janela, text='Informações Adicionais', font=('Arial', 15, 'bold'))
        texto_inforcames_adicionais.place(x=20,y=420)
        self.entry_inforcoes_adicionais = customtkinter.CTkTextbox(self.janela, width=300, height= 140,font=('Arial Arrow',15))
        self.entry_inforcoes_adicionais.place(x=20,y=450)
        
    
    def preencher_entrys(self, _):
        self.entry_cidade.delete(0, 'end')
        self.entry_bairro.delete(0, 'end')
        self.entry_rua.delete(0, 'end')
        self.entry_uf.delete(0, 'end')
        try:
            cep = self.entry_cep.get()
            url = f"https://viacep.com.br/ws/{cep}/json/"
            response = requests.get(url)
            dicionario = response.json()
            if response.status_code == 200:
                rua = dicionario['logradouro']
                bairro = dicionario['bairro']
                cidade = dicionario['localidade']
                estado = dicionario['uf']
                self.entry_cidade.insert(0, cidade)
                self.entry_bairro.insert(0, bairro)
                self.entry_rua.insert(0, rua)
                self.entry_uf.insert(0, estado)
        except:
            pass
        
        
    def carregar_imagem(self):
        global img
        self.caminho_imagem = filedialog.askopenfilename()
        # Carregar a imagem selecionada
        img = Image.open(self.caminho_imagem)
        img = img.resize((150, 150)) # Redimensionar a imagem para 150x150
        self.img = ImageTk.PhotoImage(img)

        # Exibir a imagem no quadro
        self.canvas.delete('all') # Limpar qualquer imagem anterior do quadro
        self.canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.canvas.image = self.img
    
    def imagem_padrao(self):
        img = Image.open("camera3.png")
        img = img.resize((150, 150)) # Redimensionar a imagem para 150x150
        self.img = ImageTk.PhotoImage(img)

        # Exibir a imagem no quadro
        self.canvas.delete('all') # Limpar qualquer imagem anterior do quadro
        self.canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.canvas.image = self.img
            
        
        
    def limpar_entrys(self):
        self.entry_nome.delete(0, 'end')
        self.entry_idade.delete(0, 'end')
        self.entry_genero.set('')
        self.entry_email.delete(0, 'end')
        self.entry_celular.delete(0, 'end')
        self.entry_cep.delete(0, 'end')
        self.entry_cidade.delete(0, 'end')
        self.entry_bairro.delete(0, 'end')
        self.entry_rua.delete(0, 'end')
        self.entry_uf.delete(0, 'end')
        self.entry_inforcoes_adicionais.delete("1.0", "end")
        self.imagem_padrao()
        
        
    def salvar_dados(self):
        if self.entry_nome.get() == '' or self.entry_idade.get() == '' or self.entry_genero.get() == '' or self.entry_email.get() == '' or self.entry_celular.get() == '' or  self.entry_cep.get() == '' or  self.entry_cidade.get() == '' or self.entry_bairro.get() == '' or self.entry_rua.get() == '' or self.entry_uf.get() == '':
            tkinter.messagebox.showinfo(title='Erro de Cadastro', message='Preencha todos os campos para realizar o cadastro.')
        else:
             nova_cadastro = {
            'Nome': self.entry_nome.get(),
            'Idade': self.entry_idade.get(),
            'Gênero': self.entry_genero.get(), 
            'E-mail': self.entry_email.get(),
            'Celular': self.entry_celular.get(),
            'CEP': self.entry_cep.get(),
            'Cidade': self.entry_cidade.get(),
            'Bairro': self.entry_bairro.get(),
            'Rua': self.entry_rua.get(),
            'UF': self.entry_uf.get(),
            'Informações Adicionais': self.entry_inforcoes_adicionais.get("1.0", END),
            'Foto': self.caminho_imagem
        } 
        df_nova_cadastro = pd.DataFrame(nova_cadastro, index=[0])
        self.df_cadastro = pd.concat([self.df_cadastro, df_nova_cadastro], ignore_index=True)
        with pd.ExcelWriter('cadastro.xlsx') as writer:
            self.df_cadastro.to_excel(writer,index=False)
        tkinter.messagebox.showinfo(title='Cadastro', message='Cadastro realizado com sucesso.')
        self.limpar_entrys()


# In[ ]:


img = None
aba_usuarios = 'usuarios'
df_usuarios = pd.read_excel('Usuarios.xlsx',sheet_name=aba_usuarios,engine='openpyxl')
df_cadastro = pd.read_excel('cadastro.xlsx')
janela= customtkinter.CTk()
Login(janela,df_usuarios,aba_usuarios)
janela.mainloop()

