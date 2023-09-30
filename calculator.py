import tkinter as tk

FONTLARGE = ("Arial", 30, "bold")
FONTSMALL = ("Arial", 12)
FONTDIGIT = ("Arial", 18, "bold")
DEFAULTFONT = ("Arial", 15)
OFFWHITE = "#F8FAFF"
BLUE = "#CCEDFF"
WHITE = "#FFFFFF"
GRAY = "#F5F5F5"
LBLCOLOR = "#25265E"

class Calculadora:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("320x505")
        self.window.maxsize(320, 505)
        self.window.resizable(0,0)
        self.window.title("Calculadora")
        
        self.totalExp = ""
        self.currentExp = ""
        self.displayFrame = self.createDisplayFrame()

        self.totalLabel, self.label = self.createDisplayLabels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9:(1, 3),
            4: (2, 1), 5: (2, 2), 6:(2, 3),
            1: (3, 1), 2: (3, 2), 3:(3, 3),
            0: (4, 2), '.': (4, 1)
        }

        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.btnFrame = self.createBtnFrame()

        self.btnFrame.rowconfigure(0, weight=1)

        for x in range(1, 5):
            self.btnFrame.rowconfigure(x, weight=1)
            self.btnFrame.columnconfigure(x, weight=1)
        self.createDigitBtn()
        self.createOperatorBtn()
        self.createSpecialBtn()
        self.bindKeys()

    def bindKeys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())

        for key in self.digits:
            self.window.bind(str(key), lambda event,digit=key: self.addToExp(digit))
        
        for key in self.operations:
            self.window.bind(key, lambda event,operation=key: self.addToExp(operation))

    def createSpecialBtn(self):
        self.createClearBtn()
        self.createEqualBtn()

    def createDisplayLabels(self):
        totalLabel = tk.Label(self.displayFrame, text=self.totalExp, anchor=tk.E, bg=GRAY, fg=LBLCOLOR, padx=18, font=FONTSMALL)
        totalLabel.pack(expand=True, fill="both")
        
        label = tk.Label(self.displayFrame, text=self.currentExp, anchor=tk.E, bg=GRAY, fg=LBLCOLOR, padx=18, font=FONTLARGE)
        label.pack(expand=True, fill="both")
        return totalLabel, label

    def createDisplayFrame(self):
        frame = tk.Frame(self.window, height=167, bg=GRAY)
        frame.pack(expand=True, fill="both")
        return frame
    
    def addToExp(self, value):
        self.currentExp += str(value)
        self.updateLabel()
    
    def createOperatorBtn(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.btnFrame, text=symbol, bg=OFFWHITE, fg=LBLCOLOR, font=DEFAULTFONT, 
                                borderwidth=0, command=lambda x=operator: self.appendOperator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i+=1

    def createDigitBtn(self):
        for digit, gridValue in self.digits.items():
            button = tk.Button(self.btnFrame, text=str(digit), bg=WHITE, fg=LBLCOLOR, font=FONTDIGIT,
                                borderwidth=0, command=lambda x=digit: self.addToExp(x))
            button.grid(row=gridValue[0], column=gridValue[1], sticky=tk.NSEW)
    
    def appendOperator(self, operator):
        self.currentExp += operator
        self.totalExp += self.currentExp
        self.currentExp = ""
        self.updateTotalLabel()
        self.updateLabel()
    
    def clear(self):
        self.currentExp = ""
        self.totalExp = ""
        self.updateTotalLabel()
        self.updateLabel()
    
    def createClearBtn(self):
        button = tk.Button(self.btnFrame, text="C", bg=OFFWHITE, fg=LBLCOLOR, font=DEFAULTFONT, 
                            borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, columnspan=3, sticky=tk.NSEW)

    def evaluate(self):
        self.totalExp += self.currentExp
        self.updateTotalLabel()

        try:
            self.currentExp = str(eval(self.totalExp))

            self.totalExp = ""

        except Exception as e:
            self.currentExp = "ERRO"
        
        finally:
            self.updateLabel()

    def createEqualBtn(self):
        button = tk.Button(self.btnFrame, text="=", bg=BLUE, fg=LBLCOLOR, font=DEFAULTFONT, 
                            borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def createBtnFrame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame
    
    def updateTotalLabel(self):
        exp = self.totalExp
        for operator, symbol in self.operations.items():
            exp = exp.replace(operator, f'{symbol}')
        self.totalLabel.config(text=exp)

    def updateLabel(self):
        self.label.config(text=self.currentExp[:11])
    
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculadora()
    calc.run()
