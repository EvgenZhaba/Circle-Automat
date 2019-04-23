# -*- coding: utf8 -*-

from tkinter import Tk, Canvas
from random import randint
from PIL import Image, ImageTk, ImageDraw
import datetime

WX = 128
WY = 128

def replace(nagval, x, y):
	if (x<0) or (x>=WX) or (y<0) or (y>=WY):
		return
	value = nagval[x][y]
	if value == 0:
		nagval[x][y] = 2
	elif value == 2:
		nagval[x][y] = 0

def tick(tonal, nagval):
	new_nagval = []
	for i, n in enumerate(nagval):
		way = n[2]
		dx = way % 3 - 1
		dy = (way // 3) % 3 - 1
		x = n[0]+dx
		y = n[1]+dy
		if (x == -1) or (x == WX) or (y == -1) or (y == WY) or (n[4]<0): # условия уничтожения сигнала
			nagval.pop(i)
			tonal[n[0]][n[1]] = 0
			continue
		if n[3] == 0: # если ещё не столкнулись
			if tonal[x][y] == 2: # если стена
				replace(tonal, x+dx, y+dy) # перемещение стены визуальное
				nagval[i][3] = 1 # столкновение
				if dy == 0:
					new_way = 7 if dx>0 else 1
					replace(tonal, x, y-1)
					replace(tonal, x, y+1)
					new_nagval += [[x, y, new_way, 0, 0]] # новый сигнал
				if False and dx == 0:
					new_way = 5 if dy>0 else 3
					replace(tonal, x-1, y)
					replace(tonal, x+1, y)
					new_nagval += [[x, y, new_way, 0, 0]] # новый сигнал
				
		else: # если столкнулись
			dx *= -1
			dy *= -1
			x = n[0]+dx
			y = n[1]+dy
			nagval[i][2] = (dy+1)*3 + (dx+1)
			nagval[i][3] = 0
			
		tonal[x][y] = 1 # перемещение точки визуальное
		tonal[n[0]][n[1]] = 0
		nagval[i][0] += dx # перемещение точки логическое
		nagval[i][1] += dy
		nagval[i][4] += 1
	if new_nagval:
		nagval += new_nagval
	
	for i, n in enumerate(nagval):
		for j, m in enumerate(nagval[i+1:]):
			if n[0]==m[0] and n[1]==m[1] and n[2]==m[2]:
				nagval.pop(i)
				nagval.pop(j-1)
				tonal[n[0]][n[1]] = 0
	
	print(len(nagval))

def create_wave(tonal, nagval, x, y, way):
	dx = way % 3 - 1
	dy = (way // 3) % 3 - 1
	if dy == 0:
		tonal[x+1][y] = 2
		tonal[x-1][y] = 2
	if dx == 0:
		tonal[x][y+1] = 2
		tonal[x][y-1] = 2

	nagval += [ [x, y, way, 0, 0] ]
	# x
	# y
	# направление 1 - вверх, 7 - вниз, 3 - налево, 5 - направо
	# столкновение 0 - движение, 1 - столкновение
	# количество столкновений

def leftclick(event):
	global tonal, frames, nagval, STEP, multiverse_nagval, multiverse_tonal

	canvas.delete("all")
	
	image = Image.new("RGB", (WX*2,WY*2), (255,255,255))
	draw = ImageDraw.Draw(image)

	world = [[0 for i in range(WX)] for i in range(WY)]
	for t in range(len(multiverse_tonal)):
		for i in range(WY):
			for j in range(WX):
				if multiverse_tonal[t][i][j] > 1:
					if multiverse_tonal[t][i][j] == 1 and world[i][j] == 0:
						color = 'grey70'
						color_rgb = (179, 179, 179)
						world[i][j] = 1
					if multiverse_tonal[t][i][j] == 2:
						color = 'black'
						color_rgb = (0, 0, 0)
						world[i][j] = 2						
					canvas.create_rectangle((i+1)*2, (j+1)*2, (i+1)*2+1, (j+1)*2+1, outline=color)
					draw.rectangle([(i+1)*2, (j+1)*2, (i+1)*2+1, (j+1)*2+1], color_rgb)
	frames += [image]
	for t in range(len(multiverse_tonal)):
		tick(multiverse_tonal[t], multiverse_nagval[t])
	STEP += 1
	if STEP % 100 == 0:
		new_tonal = [[0 for i in range(WX)] for i in range(WY)]
		new_nagval = []
		create_wave(new_tonal, new_nagval, WX*9//16, WY*9//16, 5)
		create_wave(new_tonal, new_nagval, WX*7//16, WY*9//16, 5)
		create_wave(new_tonal, new_nagval, WX*9//16, WY*7//16, 5)
		create_wave(new_tonal, new_nagval, WX*7//16, WY*7//16, 5)
		multiverse_tonal += [new_tonal]
		multiverse_nagval += [new_nagval]
		

def save(event):
	global frames
	frames[0].save('images/result'+ str(datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")) + '.gif', format='GIF', append_images=frames[1:], save_all=True, duration=50, loop=0)
	print("save!")


frames = []
tonal = [[0 for i in range(WX)] for i in range(WY)]
multiverse_tonal = [tonal]

nagval = [ ] 
multiverse_nagval = [nagval]

STEP = 0
#create_wave(tonal, nagval, WX*8//16, WY*8//16, 5)
create_wave(tonal, nagval, WX*9//16, WY*9//16, 5)
create_wave(tonal, nagval, WX*7//16, WY*9//16, 5)
create_wave(tonal, nagval, WX*9//16, WY*7//16, 5)
create_wave(tonal, nagval, WX*7//16, WY*7//16, 5)
#create_wave(tonal, nagval, WX*8//16, WY*9//16, 5)

if __name__ == "__main__":
	
	root = Tk()
	root.minsize(WX*2, WY*2)
	root.resizable(width=False, height=False)

	canvas = Canvas(root, width=WX*2, height=WY*2, bg="white")
	canvas.pack()
		
	root.bind("<Return>", leftclick)
	root.bind("<S>", save)

	root.mainloop()