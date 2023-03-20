import tkinter as tk
import time
tela = tk.Tk()
largura=1000
altura=500

canvas = tk.Canvas(tela,width=largura,height=altura)

canvas.pack()

objeto = canvas.create_oval(0,0,20,20,fill='green')

t=0
vy = 300
vx = 100
g = 10

while t<200:
    delT=0.00025
    t=t+delT
    vy = vy + g * delT
    canvas.move(objeto,vx*delT,vy*delT)
    coord_objeto=canvas.coords(objeto)

    if coord_objeto[3] > altura and vy >0:
        vy = -0.9*vy
    if coord_objeto[1] < 0 and  vy <0:
        vy = -0.9*vy
    if coord_objeto[2] > largura and vx >0:
        vx = -0.9*vx
    if coord_objeto[0] < 0 and vx <0:
        vx = -0.9*vx

    tela.update()


tela.update()



input()
