import tkinter as tk
import time
#define o tabuleiro

largura=800
altura=800
ladoQuadrado=100
nH= largura//ladoQuadrado
nV=altura//ladoQuadrado

tela = tk.Tk()


canvas = tk.Canvas(tela,width=largura,height=altura)

tabuleiro=[]
    for j in range(nV):
        linha=[]
        for i in range(nH):
        #print(i,j)#imprimindo os valores de i e j usados na mapeação

            q=canvas.create_rectangle(i*ladoQuadrado,j*ladoQuadrado,(i+1)*ladoQuadrado,(j+1)*ladoQuadrado)
            linha.append(q)
            if (i%2==0 and j%2==0) or (i%2!=0 and j%2!=0) :
            canvas.itemconfig(q, fill='black')
        else:
        canvas.itemconfig(q, fill='white')

def set_color(i,j,cor)  :
    canvas.itemconfig(tabuleiro[j][i],fill=cor)
def set_color(i,j)  :
    canvas.itemconfig(tabuleiro[j][i],'fill')
def get_cor(i,j):
    return canvas.itemget(tabuleiro[j][i],'fill')
def set_padrao(i0,j0,padrao,cor)
    for j in range(len(padrao)):
        linha = padrao[j]
        for i in range(len(linha)):
            if linha[i]==1
            set_cor(i,j,'cor')

set_padrao(letraB,'red')
canvas.pack()


tela.update()
input("Tecle enter:")
