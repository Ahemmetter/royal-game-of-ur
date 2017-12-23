# -*- coding: utf-8 -*-

from Tkinter import *
from random import randint
import tkMessageBox
import os
import rgoudicts as rg

# Parameters and Variables
root = Tk()  # makes empty window
root.resizable(0,0)
size = 64                                   # size of one square in px
squares = []                                # list that holds rectangles
pad = 10                                    # padding around fishki (unused)
fsize = 32                                  # size of one fishka
bf = []                                     # black fishki list
wf = []                                     # white fishki list
bpos = [-1, -1, -1, -1, -1, -1, -1]         # positions of black fishki
wpos = [-1, -1, -1, -1, -1, -1, -1]         # positions of white fishki
rosettes = [0, 2, 10, 14, 16]               # red squares, on which you can move again
stone = 0                                   # ID of selected fishka
clicked = 0                                 # ID of clicked fishka
steps = 0                                   # rolled number with dice
whiteturn = True                            # keeps track of whose turn it is
wdone = 0                                   # number of fishki that are finished already
bdone = 0
color = "b"                                 # AI will play black (b) or white (w)

bluec = "#374D7D"                           # flat colors
brownc = "#8F7260"
redc = "#C43730"
blackc = "#2B2B2B"
whitec = "#ECF0F1"
lightredc = "#EC4A42"
lightbluec = "#4F669D"
yellowc = "#FFCB46"

# Paths of black and white fishki

bpath = [-1, 9, 6, 3, 0, 1, 4, 7, 10, 12, 13, 15, 16, 19, 18, 17, 14, 99]
wpath = [-1, 11, 8, 5, 2, 1, 4, 7, 10, 12, 13, 15, 14, 17, 18, 19, 16, 99]


def restart_game():
    python = sys.executable
    os.execl(python, python, * sys.argv)


class Game:

    def __init__(self, root):
        self.root = root
        self.lang = StringVar()
        self.lang.set("en")
        self.rulesexp = StringVar()


        def setup_text():
            self.startbutton = Button(board, text=rg.roll[self.lang.get()], command=self.throw_dice, state="normal")
            self.startbutton.place(x=336, y=80, height=32, width=96)

            self.startbutton = Button(board, text=rg.roll[self.lang.get()], command=self.throw_dice, state="normal")
            self.startbutton.place(x=336, y=80, height=32, width=96)

            menu.entryconfigure(0, label=rg.gamestr[self.lang.get()])
            gamemenu.entryconfigure(0, label=rg.newgame[self.lang.get()])
            gamemenu.entryconfigure(2, label=rg.preferences[self.lang.get()])
            gamemenu.entryconfigure(3, label=rg.rules[self.lang.get()])
            gamemenu.entryconfigure(4, label=rg.aboutgame[self.lang.get()])
            gamemenu.entryconfigure(6, label=rg.exit[self.lang.get()])

        def open_settings():
            global lang
            self.settings = Toplevel()
            settings = self.settings

            settings.deiconify()

            def close_settings():
                root.title(rg.rgou[self.lang.get()])
                setup_text()
                settings.withdraw()
                root.wait_window(settings)

            Radiobutton(settings, text="English", padx=20, variable=self.lang,
                        value="en").grid(row=0, column=0, sticky=W)
            Radiobutton(settings, text="Deutsch", padx=20, variable=self.lang,
                        value="de").grid(row=1, column=0, sticky=W)
            Radiobutton(settings, text="Русский", padx=20, variable=self.lang,
                        value="ru").grid(row=2, column=0, sticky=W)
            Radiobutton(settings, text="Français", padx=20, variable=self.lang,
                        value="fr").grid(row=0, column=1, sticky=W)
            Radiobutton(settings, text="Español", padx=20, variable=self.lang,
                        value="es").grid(row=1, column=1, sticky=W)
            Radiobutton(settings, text="Esperanto", padx=20, variable=self.lang,
                        value="eo").grid(row=2, column=1, sticky=W)

            self.okbutton = Button(settings, text="Ok", command=close_settings).grid(row=8, column=0)

        def open_rules():
            global lang
            self.rules = Toplevel()
            rules = self.rules
            rules.deiconify()

            S = Scrollbar(rules)
            S.grid(row=0, column=1)

            ruletextdisplay = Text(rules, height=15, width=70, bd=0, padx=20, pady=20, wrap=WORD)
            ruletextdisplay.insert(INSERT, rg.ruletext[self.lang.get()])
            ruletextdisplay.grid(row=0, column=0)
            S.config(command=ruletextdisplay.yview)
            ruletextdisplay.config(yscrollcommand=S.set)
            ruletextdisplay.config(state=DISABLED)

            def close_rules():
                root.title(rg.rgou[self.lang.get()])
                self.startbutton = Button(board, text=rg.roll[self.lang.get()], command=self.throw_dice, state="normal")
                self.startbutton.place(x=336, y=80, height=32, width=96)
                rules.withdraw()
                root.wait_window(rules)

            self.closebutton = Button(rules, text="Ok", command=close_rules)
            self.closebutton.grid(row=1, column=0)

        root.title(rg.rgou[self.lang.get()])
        # root.iconbitmap("crown.icns")
        menu = Menu(root)
        root.config(menu=menu)

        self.message = StringVar()
        self.rolled = StringVar()
        self.skipper = StringVar()
        self.message.set(rg.whitebegins[self.lang.get()])
        self.rolled.set("")
        self.skipper.set("")

        def gameinfo():
            tkMessageBox.showinfo(rg.aboutgame[self.lang.get()], rg.info[self.lang.get()])

        status = Label(root, textvariable=self.message, bd=1, relief=SUNKEN, anchor=W)
        status.pack(side=BOTTOM, fill=X)

        self.draw_board()
        board.pack()
        self.create_fishki(bpos, wpos)
        self.startbutton = Button(board, text=rg.roll[self.lang.get()], command=self.throw_dice, state="normal")
        self.startbutton.place(x=336, y=80, height=32, width=96)

        self.skipbutton = Button(board, text=rg.skip[self.lang.get()], command=self.change_turn, state="normal")
        self.skipbutton.place(x=336, y=80, height=32, width=96)
        self.skipbutton.place_forget()

        gamemenu = Menu(menu)
        menu.add_cascade(label=rg.gamestr[self.lang.get()], menu=gamemenu)
        gamemenu.add_command(label=rg.newgame[self.lang.get()], command=restart_game)
        gamemenu.add_separator()
        gamemenu.add_command(label=rg.preferences[self.lang.get()], command=open_settings)
        gamemenu.add_command(label=rg.rules[self.lang.get()],  command=open_rules)
        gamemenu.add_command(label=rg.aboutgame[self.lang.get()], command=gameinfo)
        gamemenu.add_separator()
        gamemenu.add_command(label=rg.exit[self.lang.get()], command=root.quit)

        self.rollednumber = Label(board, textvariable=self.rolled, font=("Courier", 40))
        self.rollednumber.place(x=336, y=212, height=32, width=96)

    def draw_board(self):
        """Draws the grid of squares onto a canvas"""

        posx = range(1, 9)
        posy = range(1, 4)

        for x in posx:
            for y in posy:
                if not ((x == 5 or x == 6) and (y == 1 or y == 3)):
                    squares.append(board.create_rectangle(x * 64, y * 64,
                                                          x * 64 + size,
                                                          y * 64 + size,
                                                          fill=bluec,
                                                          outline=brownc,
                                                          width=8, tags=("clickable", "square")))

        for n in [0, 2, 10, 14, 16]:
            board.itemconfig(squares[n], fill=redc,
                             tags=("clickable", "square"))

        return squares

    def redraw_board(self):
        """Redraws the grid of squares onto a canvas"""

        for n in range(0, 20):
            board.itemconfig(squares[n], fill=bluec)
        for n in [0, 2, 10, 14, 16]:
            board.itemconfig(squares[n], fill=redc)

        return squares

    def create_fishki(self, bpos, wpos):
        """Draws available fishki onto the side of the board.
        Runs only in the beginning of a game."""

        for b in range(0, 7):
            bf.append(board.create_oval(b * 32 + 64, 16, b * 32 +
                                        fsize + 64, 16 + fsize, fill=blackc, outline=blackc, tags=("clickable", "fishka")))

        for w in range(0, 7):
            wf.append(board.create_oval(w * 32 + 64, 272, w * 32 +
                                        fsize + 64, 272 + fsize, fill=whitec, outline=whitec, tags=("clickable", "fishka")))

    def find_position(self, i):
        """Calculates the coordinates from the square number"""

        if i <= 11:
            x = (i / 3 + 1) * 64 + 16
            y = (i % 3 + 1) * 64 + 16
        elif i == 12 or i == 13:
            x = 320 + 16 + (64 * (i - 12))
            y = 128 + 16
        else:
            x = ((i - 14) / 3 + 1) * 64 + 16 + 384
            y = ((i - 14) % 3 + 1) * 64 + 16
        return x, y

    def throw_dice(self):
        """Rolls 4 tetrahedrons (like coin flips)"""
        global steps
        steps = randint(0, 1) + randint(0, 1) + randint(0, 1) + randint(0, 1)
        self.rolled.set(str(steps))
        if steps == 0:
            print "0 gewürfelt"
            # root.after(800, self.change_turn())
            self.change_turn()
            self.startbutton.config(state="active")
            # self.throw_dice()
        else:
            self.startbutton.config(state="disabled")
            if whiteturn:
                self.click()

    def select(self, event):
        """Gets widget ID by clicking on fishka"""
        item = board.find_closest(event.x, event.y)
        tags = board.itemcget(item, "tags")
        if "clickable" in tags:
            if int(item[0]) >= 1 and int(item[0]) <= 20:
                global clicked
                clicked = int(item[0])
                self.move()
            elif int(item[0]) >= 21 and int(item[0]) <= 34:
                global stone
                stone = int(item[0])
                self.show_moves(bpos, wpos, squares)
            else:
                self.message.set(rg.outofbounds[self.lang.get()])
        else:
            self.message.set(rg.notclickable[self.lang.get()])

    def click(self):
        value = 0
        board.tag_bind("clickable", "<ButtonPress-1>", self.select)
        return value

    def show_moves(self, bpos, wpos, squares):
        self.redraw_board()
        if not whiteturn and (stone >= 21) and (stone <= 27):     # black
            black_goal = bpath[bpath.index(bpos[stone - 21]) + steps]
            if (black_goal != 99) and (black_goal not in bpos):
                if (black_goal in wpos):
                    if black_goal not in rosettes:
                        board.itemconfig(squares[black_goal], fill=lightbluec)
                        self.click()
                else:
                    if black_goal in rosettes:
                        board.itemconfig(squares[black_goal], fill=lightredc)
                        self.click()
                    else:
                        board.itemconfig(squares[black_goal], fill=lightbluec)
                        self.click()
            elif black_goal == 99:
                board.itemconfig(bf[stone - 21], fill=yellowc, outline=yellowc)
                global bdone
                bdone += 1
                board.coords(bf[stone - 21], bdone * 32 + 320, 16, bdone * 32 + fsize + 320, 16 + fsize)
                bpos[stone - 21] = 99
                self.redraw_board()
                self.startbutton.config(state="normal")
                self.find_winner()
                self.change_turn()
                # self.ai3()
                # board.tag_unbind("clickable", "<ButtonPress-1>")
                self.click()
                return bpos, wpos
            # else:
                # print rg.notallowed[self.lang.get()]

        elif whiteturn and stone >= 28 and stone <= 34:     # white
            white_goal = wpath[wpath.index(wpos[stone - 28]) + steps]

            skip = True
            for i in range(28, 34):
                if wpath[wpath.index(wpos[i - 28]) + steps] in wpos:
                    if (wpath[wpath.index(wpos[i - 28]) + steps] in rosettes) and (wpath[wpath.index(wpos[i - 28]) + steps] in bpos):
                        self.message.set(rg.skipmove[self.lang.get()])
                        skip = True
                    else:
                        skip = False
                        break
                else:
                    skip = False
                    break

            if skip == False:
                if (white_goal != 99) and (white_goal not in wpos):
                    if (white_goal in bpos):
                        if white_goal not in rosettes:
                            board.itemconfig(squares[white_goal], fill=lightbluec)
                            self.click()
                    else:
                        if white_goal in rosettes:
                            board.itemconfig(squares[white_goal], fill=lightredc)
                            self.click()
                        else:
                            board.itemconfig(squares[white_goal], fill=lightbluec)
                            self.click()
                elif white_goal == 99:
                    board.itemconfig(wf[stone - 28], fill=yellowc, outline=yellowc)
                    global wdone
                    wdone += 1
                    board.coords(wf[stone - 28], wdone * 32 + 320, 272, wdone * 32 + fsize + 320, 272 + fsize)
                    wpos[stone - 28] = 99
                    self.redraw_board()
                    self.startbutton.config(state="normal")
                    self.find_winner()
                    self.change_turn()
                    # board.tag_unbind("clickable", "<ButtonPress-1>")
                    self.ai3()
                    return bpos, wpos
                    # self.click()
                else:
                    self.message.set(rg.notallowed[self.lang.get()])
            else:
                print "Ok, now we need to skip the move"
                self.startbutton.place_forget()
                self.skipbutton.place(x=336, y=80, height=32, width=96)

    def move(self):
        x, y = self.find_position(clicked - 1)
        if stone >= 21 and stone <= 27:     # black
            # print stone
            if bpath.index(bpos[stone - 21]) + steps <= 17:
                black_goal = bpath[bpath.index(bpos[stone - 21]) + steps]
                # if clicked square is target square and is not occupied by black fishka..
                # print black_goal
                if (clicked - 1 == black_goal) and (black_goal not in bpos):
                    # and if target square has white fishka..
                    if (black_goal in wpos):
                        # and is not a rosette..
                        if (black_goal not in rosettes):
                            # then move there, kick it
                            board.coords(wf[wpos.index(black_goal)], wpos.index(black_goal) * 32 + 64,
                                         272, wpos.index(black_goal) * 32 + fsize + 64, 272 + fsize)
                            wpos[wpos.index(black_goal)] = -1
                            board.coords(bf[stone - 21], x, y, x + fsize, y + fsize)
                            bpos[stone - 21] = clicked - 1
                            self.redraw_board()
                            self.rolled.set("")
                            self.startbutton.config(state="normal")
                            self.change_turn()
                            board.tag_unbind("clickable", "<ButtonPress-1>")
                            return bpos, wpos
                        # and is a rosette..
                        else:
                            self.redraw_board()
                            self.rolled.set("")
                            self.startbutton.config(state="normal")
                            self.change_turn()
                            return bpos, wpos
                    else:
                        if (black_goal in rosettes):
                            # move and go again
                            board.coords(bf[stone - 21], x, y, x + fsize, y + fsize)
                            bpos[stone - 21] = clicked - 1
                            self.redraw_board()
                            self.rolled.set("")
                            self.startbutton.config(state="normal")
                            self.ai3()

                            return bpos, wpos
                        else:
                            # move like always
                            board.coords(bf[stone - 21], x, y, x + fsize, y + fsize)
                            bpos[stone - 21] = clicked - 1
                            self.redraw_board()
                            self.rolled.set("")
                            self.startbutton.config(state="normal")
                            self.change_turn()
                            board.tag_unbind("clickable", "<ButtonPress-1>")
                            return bpos, wpos
                else:
                    self.message.set(rg.youcant[self.lang.get()])
                    # print whiteturn
            else:
                self.message.set(rg.notallowed[self.lang.get()])
                self.change_turn()

        if stone >= 28 and stone <= 34:     # white
            if wpath.index(wpos[stone - 28]) + steps <= 17:
                white_goal = wpath[wpath.index(wpos[stone - 28]) + steps]
                # if clicked square is target square and is not occupied by black fishka..
                if (clicked - 1 == white_goal) and (white_goal not in wpos):
                    # and if target square has white fishka..
                    if (white_goal in bpos):
                        # and is not a rosette..
                        if (white_goal not in rosettes):
                            # then move there, kick it
                            board.coords(bf[bpos.index(white_goal)], bpos.index(white_goal) * 32 +
                                         64, 16, bpos.index(white_goal) * 32 + fsize + 64, 16 + fsize)
                            bpos[bpos.index(white_goal)] = -1
                            board.coords(wf[stone - 28], x, y, x + fsize, y + fsize)
                            wpos[stone - 28] = clicked - 1
                            self.redraw_board()
                            self.rolled.set("")
                            self.startbutton.config(state="normal")
                            self.change_turn()
                            board.tag_unbind("clickable", "<ButtonPress-1>")
                            return bpos, wpos
                        # and is a rosette..
                        else:
                            self.redraw_board()
                            self.rolled.set("")
                            self.startbutton.config(state="normal")
                            self.change_turn()
                            # board.tag_unbind("clickable", "<ButtonPress-1>")
                            return bpos, wpos
                    else:
                        if (white_goal in rosettes):
                            # move and go again
                            board.coords(wf[stone - 28], x, y, x + fsize, y + fsize)
                            wpos[stone - 28] = clicked - 1
                            self.redraw_board()
                            self.rolled.set("")
                            self.startbutton.config(state="normal")
                            # board.tag_unbind("clickable", "<ButtonPress-1>")
                            return bpos, wpos
                        else:
                            # move like always
                            board.coords(wf[stone - 28], x, y, x + fsize, y + fsize)
                            wpos[stone - 28] = clicked - 1
                            self.redraw_board()
                            self.rolled.set("")
                            self.startbutton.config(state="normal")
                            self.change_turn()
                            board.tag_unbind("clickable", "<ButtonPress-1>")
                            return bpos, wpos
                else:
                    self.message.set(rg.youcant[self.lang.get()])
            else:
                self.message.set(rg.notallowed[self.lang.get()])
                self.change_turn()

    def change_turn(self):
        global whiteturn
        if whiteturn:
            whiteturn = False
            self.message.set(rg.blacksturn[self.lang.get()])
            self.ai3()
        else:
            whiteturn = True
            self.message.set(rg.whitesturn[self.lang.get()])
            self.startbutton.config(state="normal")

    def find_winner(self):
        if wdone == 7:
            tkMessageBox.showinfo(rg.wehaveawinner[self.lang.get()], rg.whitewins[self.lang.get()])
            root.quit()
        elif bdone == 7:
            tkMessageBox.showinfo(rg.wehaveawinner[self.lang.get()], rg.blackwins[self.lang.get()])
            root.quit()

    def ai3(self):
        if color == "b":
            if not whiteturn:
                self.throw_dice()
                found = -99
                found_stone = -99
                if steps != 0:
                    for i in range(0, 7):
                        # kick someone
                        if bpath.index(bpos[i]) + steps <= 17:
                            black_goal = bpath[bpath.index(bpos[i]) + steps]
                            if (black_goal in wpos) and (black_goal not in rosettes) and (black_goal not in bpos):
                                found = black_goal
                                found_stone = i + 21
                                break
                    if found == -99:
                        for i in range(0, 7):
                            # finish piece
                            if bpath.index(bpos[i]) + steps == 17:
                                global bdone
                                bdone += 1
                                board.coords(bf[i], bdone * 32 + 320, 16, bdone * 32 + fsize + 320, 16 + fsize)
                                bpos[i] = 99
                                found = 99
                                found_stone = i + 21
                                board.itemconfig(bf[i], fill=yellowc, outline=yellowc)
                                self.redraw_board()
                                self.startbutton.config(state="normal")
                                self.find_winner()
                                self.change_turn()
                                board.tag_unbind("clickable", "<ButtonPress-1>")
                                return bpos, wpos
                                break
                        if found == -99:
                            for i in range(0, 7):
                                # get rosette
                                if bpath.index(bpos[i]) + steps <= 17:
                                    black_goal = bpath[bpath.index(bpos[i]) + steps]
                                    if (black_goal not in wpos) and (black_goal in rosettes) and (black_goal not in bpos):
                                        found = black_goal
                                        found_stone = i + 21
                                        break
                            if found == -99:
                                for i in range(0, 7):
                                    # other square
                                    if bpath.index(bpos[i]) + steps <= 17:
                                        black_goal = bpath[bpath.index(bpos[i]) + steps]
                                        if (black_goal not in wpos) and (black_goal not in rosettes) and (black_goal not in bpos):
                                            found = black_goal
                                            found_stone = i + 21
                                            break
                if found != -99 and found != 99:
                    global clicked
                    clicked = found + 1
                    global stone
                    stone = found_stone
                    # self.move()
                    root.after(800, self.move)
                else:
                    self.message.set(rg.skipmove[self.lang.get()])
                    self.change_turn()


board = Canvas(root, width=640, height=320)

gameapp = Game(root)
root.lift()
root.attributes("-topmost", True)
root.after_idle(root.attributes, '-topmost', False)
root.mainloop()
