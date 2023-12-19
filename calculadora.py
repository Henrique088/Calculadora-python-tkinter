import tkinter as tk
import re
from tkinter.colorchooser import askcolor
from tkinter.scrolledtext import *

#função para mudar a cor de fundo
def change_color(frame2):
    colors = askcolor(title="Tkinter Color Chooser")
    root.configure(bg=colors[1])
    frame2.configure(bg=colors[1])
    ScrolledText.configure(root,bg=colors[1])

def sobre():
    sobre = """
    Essa é uma calculadora simples que apenas resolve contas básicas, sendo:
    1. Somar
    2. Dimuir
    3. Multiplicação
    4. Divisão
        """

    janela_regras = tk.Toplevel()
    janela_regras.title("Sobre Calculadora")

    caixa_texto = tk.Text(janela_regras, wrap=tk.WORD)
    caixa_texto.pack()
    caixa_texto.insert("0.0", sobre)
    caixa_texto['state'] = 'disabled'

def Menus(root, frame2):
    Menubar = tk.Menu(root)
    root.config(menu=Menubar)
    filemenu = tk.Menu(Menubar)
    filemenu2 = tk.Menu(Menubar)

    def Quit():root.destroy()

    Menubar.add_cascade(label="opções", menu=filemenu)
    Menubar.add_cascade(label="Funções", menu=filemenu2)

    filemenu.add_command(label="sobre", command=lambda: sobre())
    filemenu.add_command(label="Sair", command=Quit)

    filemenu2.add_command(label='Mudar cor', command=lambda : change_color(frame2))


# Adiciona o valor do numero apertado nas teclas da calculadora
def adicionar_valor(valor):

    caixa_texto.configure(state='normal') # abilita o visor ("caixa-texto")
    caixa_texto.insert(tk.END, valor) #insere o valor
    caixa_texto.configure(state='disabled') #desabilita o visor ("caixa-texto")

# impede do usuario digitar um operador no inicio e chama a função adiciona_valor caso for certo
def botao_clique(valor):
    vet = ['.', '+', '-', '*', '/', '=']

    if (len(caixa_texto.get("1.0", "end-1c")) == 0 and valor in vet ): #averigua se a caixa está vazia e se o digitado é um operador
        pass
    else:
        adicionar_valor(valor)


#verifica se a expressão digitada é coerente, pora não aceitar isso: 5++5 ou 3- ou 8*/89
def verifica_expressao ():
    vet = ['.', '+', '-', '*', '/']


    conteudo = caixa_texto.get("1.0", "end-1c")
    linhas = conteudo.split('\n') #quebra todo o contéudo da caixa dexto em linhas
    conteudo = linhas[-2] if linhas[-1] == '' else linhas[-1] # pega somente a ultima linha
    elementos = re.findall(r'[-+]?\d*\.\d+|\d+|[-+*/]', conteudo) #expressão regular para separar a expressão em numero e operadores

    #for para percorrer elementos e averiguar a expressão
    for x in range(len(elementos)):
        if(x != len(elementos)-1):
            if(elementos[x] in vet and elementos[x+1] in vet): #se tiver dois operadores seguidos já printa erro e retorna false

                caixa_texto.insert(tk.END, "\nExpressão errada\n")
                return False

            elif(elementos[x] in vet ):
                pass
        elif(x == len(elementos)-1 and elementos[x] in vet):
            caixa_texto.insert(tk.END, "\nExpressão errada\n")
            return False
    return elementos, conteudo
def calcula():
    caixa_texto.configure(state='normal')
    vet_expre, conta = verifica_expressao()
    resultado = 0
    divi_por_0 = True
    vet = ['*', '/']


    if(vet_expre):


        while (len(vet_expre)>1): #se vet_expre tiver apenas um dado quer dizer que temos o resultado final

            for x in range(len(vet_expre)):

                if(vet_expre[x] in vet):
                    aux = 1 #controla a precedência dos operadores
                    break
                else:
                    aux = 0


            for x in range(len(vet_expre)):
                #calcula e remove do vetor e deixa apenas o resultado no lugar e vai repetindo até sobrar apenas o resultado final. A cada calculo ele volta no while e retorna no for
                if(vet_expre[x] == '*' and aux == 1):
                    resultado = float(vet_expre[x-1] )* float(vet_expre[x+1])
                    vet_expre.pop(x)
                    vet_expre.pop(x)
                    vet_expre.pop(x-1)
                    vet_expre.insert(x-1,resultado)

                    break


                elif(vet_expre[x] == '/' and aux == 1):
                    try:
                        resultado = float(vet_expre[x-1] ) / float(vet_expre[x+1])

                    except:
                        resultado = 0
                        divi_por_0 = False


                    vet_expre.pop(x)
                    vet_expre.pop(x)
                    vet_expre.pop(x - 1)
                    vet_expre.insert(x-1,resultado)
                    break


                elif (vet_expre[x] == '+' and aux == 0):
                    resultado = float(vet_expre[x-1] ) + float(vet_expre[x+1])
                    vet_expre.pop(x)
                    vet_expre.pop(x)
                    vet_expre.pop(x - 1)
                    vet_expre.insert(x-1,resultado)
                    break

                elif (vet_expre[x] == '-' and aux == 0):
                    resultado = float(vet_expre[x-1] ) - float(vet_expre[x+1])
                    vet_expre.pop(x)
                    vet_expre.pop(x)
                    vet_expre.pop(x - 1)
                    vet_expre.insert(x-1,resultado)
                    break
        if (divi_por_0):
            caixa_texto.delete(1.0, tk.END) #apga  o conteudo ca caixa texto
            caixa_texto.insert(tk.END, f'{conta}\n')
            caixa_texto.insert(tk.END, f'\n= {resultado}\n')
            caixa_texto.configure(state='disabled')
            return resultado

        else:
            caixa_texto.delete(1.0, tk.END)  # apga  o conteudo ca caixa texto
            caixa_texto.insert(tk.END, f'{conta}\n')
            caixa_texto.insert(tk.END, f'\nNão é possivel divir por 0\n')
            caixa_texto.configure(state='disabled')
            return resultado

def soma (num_1, num_2):
    return num_1 + num_2


def diminui(num_1, num_2):
    return num_1 - num_2

def multiplica(num_1, num_2):
    return num_1 * num_2

def divisao(num_1, num_2):

    if num_2 ==0:
        return False

    return num_1 / num_2


if(__name__ == "__main__"):

    root = tk.Tk()
    root.title('Calculadora')
    root.geometry('350x450')
    root.resizable(False, False)
    root.configure(background="#fff")
    root.maxsize(width=850, height=700)
    root.minsize(width=400, height=300)


    frame1 = tk.Frame(root, borderwidth=4, bg="#fff",
                      highlightbackground="#fff", highlightthickness=3)
    frame1.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=0.20)

    frame2 = tk.Frame(root, borderwidth=4, bg="#fff",
                      highlightbackground="#fff", highlightthickness=1)
    frame2.place(relx=0.0, rely=0.21, relwidth=1.0, relheight=0.79)

    caixa_texto = tk.Text(frame1, width=50, height=22)
    caixa_texto.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
    caixa_texto.configure(state='disabled')

    Menus(root, frame2)


    botoes = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        '0', '.', '=', '+'
    ]

    x = 0.02
    y = 0.13
    relw= 0.22
    relhei = 0.15
    cont = 0


    for botao in botoes:

        if botao != '=':

            (tk.Button(frame2, text=botao, width=5, height=2,
                      command=lambda valor=botao: botao_clique(valor), background="#fff").
                      place(relx=x, rely=y, relwidth=relw, relheight=relhei))
        else:
            (tk.Button(frame2, text=botao, width=5, height=2,
                       command=lambda: calcula()).
             place(relx=x, rely=y, relwidth=relw, relheight=relhei))

        cont +=1
        if cont < 4:
            x += 0.25
        else:
            cont = 0
            x = 0.02
            y += 0.2

    root.mainloop()