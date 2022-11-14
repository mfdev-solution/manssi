from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from threading import Thread
import time


class Dactylo(Tk):

	def __init__(self):
		super().__init__()
		self.title("TapFaster")
		#self.geometry("620x480")
		#self.resizable(width=False, height=False)
		menuBar = Menu(self)

		menu1 = Menu(menuBar, tearoff=0)
		self.niv = menu1.add_command(label="Charger", command=self.importer)
		menuBar.add_cascade(label="Fichier", menu=menu1)

		menu2 = Menu(menuBar, tearoff=0)
		menu2.add_command(label="niveau 1", command=self.importer)
		menuBar.add_cascade(label="Options", menu=menu2)

		menu3 = Menu(menuBar, tearoff=0)
		menu3.add_command(label="niveau 1", command=self.importer)
		menuBar.add_cascade(label="Aide", menu=menu3)


		self.config(menu=menuBar)
		self.container()


	def container(self):
		self.frame1 = Frame(self, height=300, bg='lightgrey')
		self.notifLabel = Label(self.frame1, bg="light grey")
		self.notifLabel.pack()
		self.value = StringVar()
		self.ecran = Entry(self.frame1, textvariable=self.value, state="readonly")
		self.ecran.pack(fill=X, padx=5)
		self.ent_value = StringVar()
		self.entree = Entry(self.frame1, textvariable=self.ent_value, state="readonly")
		self.entree.pack(fill=X, padx=5, pady=10)
		self.touche = Label(self.frame1, height=3, bg="light grey")
		self.touche.pack()

		self.frame2 = Frame(self, borderwidth=5, bg='red')
		self.frame1.pack(fill=BOTH)
		self.draw_touch()

		self.frame3 = Frame(self)
		self.carac = Label(self.frame3, text="Caractère: ")
		self.faute = Label(self.frame3, text="Fautes: ")
		self.temps = Label(self.frame3, text="Temps: ", fg="red")
		self.vitesse = Label(self.frame3, text="Vitesse: ")

		self.carac.pack(side=LEFT, padx=10)
		self.vitesse.pack(side=RIGHT, padx=100)
		self.faute.pack(side=None)
		self.temps.pack(side=None)

		self.frame3.pack(fill=X)



	def draw_touch(self):
		liste_bouton = [["1 &", "2 é", "3 \"", "4 '", "5 (", "6 -", "7 è", "8 _", "9 ç", "0 à", ") °", "= +"],
						 ["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P", "¨^", "$ £"],
							["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M", "ù %", "* µ"],
								["W", "X", "C", "V", "B", "N", ", ?", "; .", ": /", "! §"],
									       [       "Espace"     ]                      ]
		liste_sframe = []
		self.bouton = {}

		for i in range(len(liste_bouton)):
			liste_sframe.append(Frame(self.frame2, bg='red'))
			for j in range(len(liste_bouton[i])):
				self.bout = Button(liste_sframe[i], width=2, height=2, text=liste_bouton[i][j])
				self.bout.grid(padx=3, row=0, column=j)
				if len(liste_bouton[i][j]) > 1 and liste_bouton[i][j]!="Espace":
					self.bouton[liste_bouton[i][j][0].upper()] = self.bout
					self.bouton[liste_bouton[i][j][-1].upper()] = self.bout
				else:
					self.bouton[liste_bouton[i][j].upper()] = self.bout


			liste_sframe[i].grid(row=i, pady=5, padx=i)
		self.bouton["ESPACE"].config(width=60)
		self.bouton[" "] = self.bouton["ESPACE"]
		self.frame2.pack(fill=X)


	def importer(self):
		filename = askopenfilename(title="Ouvrir un fichier", filetypes=[('txt files','.txt'),('all files','.*')])
		self.file = open(filename, "r")
		self.ligne = self.file.readline()
		self.value.set(self.ligne)
		self.ent_value.set("")
		self.ecran.config(state="readonly")
		self.lt = 0
		self.nb_c = 0
		self.nb_f = 0
		self.clear_color()
		self.time = Thread(target=self.timeit)
		self.insert_text() 


	def insert_text(self, event=None):
		if event==None:
			self.bouton[self.ligne[self.lt].upper()].config(bg="green")
		self.bind("<Key>", self.insert_text)
		if event!=None:
			try:
				self.time.start()
			except: pass

			if self.ligne[self.lt] == event.char:
				self.ent_value.set(self.ent_value.get()+event.char)
				self.bouton[self.ligne[self.lt].upper()].config(bg="white")
				self.lt+=1
				self.nb_c+=1
				self.carac.config(text="Caractère: {}".format(self.nb_c))
				if self.ligne[self.lt] == "\n":
					self.value.set(self.file.readline())
					self.ligne = self.file.readline()
					self.value.set(self.ligne)
					self.ent_value.set("")
					self.lt=0
				self.bouton[self.ligne[self.lt].upper()].config(bg="green")
			else:
				if event.keycode != 20:
					self.nb_f+=1
					self.faute.config(text="Faute(s): {}".format(self.nb_f))


	def clear_color(self):
		for bouton in self.bouton.values():
			bouton.config(bg="white")


	def timeit(self):
		big = time.time()
		while 1:
			now = (round(time.time()-big))
			self.temps.config(text="Temps: {}".format(now))
			self.vitesse.config(text="Vitesse: {} Carac/Sec".format(self.nb_c//((now+1)/60)))
			time.sleep(1)

if __name__ == "__main__":
	fen = Dactylo()
	fen.mainloop()
