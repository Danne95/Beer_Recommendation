
import pandas as pd
from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
from urllib.request import urlopen
import model            #our model.py file

# useful stuff
default_bg_color = "black"          # developer green: bg="#263D42" 
#background beer image url:
displayLabels = []
scrlst = [5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5, 0]
reviewCounter = 0
reviewInputs = []
dispState = True

# datasheet 
data = pd.read_csv(r"beer_reviews.csv")
data = data.dropna()

# return all reviewers names
def beerList():
    reviewers = data['beer_name'].unique().tolist()
    reviewers.sort()
    return reviewers

#hide or return first screen widgets

# click to reset inputs
def resetClick():
    global reviewCounter
    global dispState
    global displayLabels
    global reviewInputs
    global dispState
    reviewCounter = 0
    lbl7.config(text = '(0)')
    if(dispState == False):
        for i in displayLabels:
            i.destroy()
        lbl0.grid(row=1, column=0,columnspan=8, sticky=W)
        lbl1.grid(row=2, column=0, sticky=W)
        lbl2.grid(row=2, column=1, sticky=W)
        lbl3.grid(row=2, column=2, sticky=W)
        lbl4.grid(row=2, column=3, sticky=W)
        lbl5.grid(row=2, column=4, sticky=W)
        lbl6.grid(row=2, column=5, sticky=W)
        lbl7.grid(row=3, column=6, padx=60)
        btn1.grid(row=3, column=6, padx=10, sticky=W)
        btn2.grid(row=3, column=7, sticky=W)
        userChoice1.grid(row=3, column=0, sticky=W)
        userChoice2.grid(row=3, column=1, sticky=W)
        userChoice3.grid(row=3, column=2, sticky=W)
        userChoice4.grid(row=3, column=3, sticky=W)
        userChoice5.grid(row=3, column=4, sticky=W)
        userChoice6.grid(row=3, column=5, sticky=W)
        dispState = True
    displayLabels.clear()
    reviewInputs.clear()

# click to add beer review
def addClick():
    global reviewCounter
    global reviewInputs
    reviewCounter += 1
    lbl7.config(text = '('+str(reviewCounter)+')')
    temp = data.loc[data['beer_name'] == boxChoice1.get()].iloc[0]
    reviewInputs.append({"beer_name":boxChoice1.get(),"review_appearance":float(boxChoice2.get()),"review_aroma":float(boxChoice3.get()),"review_palate":float(boxChoice4.get()),"review_taste":float(boxChoice5.get()),"review_overall":float(boxChoice6.get()),
                         "brewery_name":temp['brewery_name'],"beer_style":temp['beer_style'],"beer_abv":temp['beer_abv']})

# click event display modifications
def submitClick():
    global dispState
    global displayLabels
    suggestions = model.userInput(reviewInputs)
    
    # clear first display
    lbl0.grid_forget()
    lbl1.grid_forget()
    lbl2.grid_forget()
    lbl3.grid_forget()
    lbl4.grid_forget()
    lbl5.grid_forget()
    lbl6.grid_forget()
    lbl7.grid_forget()
    btn1.grid_forget()
    btn2.grid_forget()
    userChoice1.grid_forget()
    userChoice2.grid_forget()
    userChoice3.grid_forget()
    userChoice4.grid_forget()
    userChoice5.grid_forget()
    userChoice6.grid_forget()
    dispState = False
    
    # clear last display
    for i in displayLabels:
        i.destroy()
    
    for x in suggestions:
        for i in range((suggestions[x].shape)[0]):
            if(i>7):
                break
            # Frame
            if (x == 'users'):
                displayLabels.append(LabelFrame(window, text="CF suggestion no."+str(i+1), cursor="heart", relief=RIDGE, bg=default_bg_color, fg="gold", font="none 16 italic"))
                displayLabels[-1].grid(row=5, column=3*(i%3), padx=50, pady=50, sticky=W)
            elif (x == 'items'):
                displayLabels.append(LabelFrame(window, text="CBF suggestion no."+str(i+1), cursor="heart", relief=RIDGE, bg=default_bg_color, fg="gold", font="none 16 italic"))
                displayLabels[-1].grid(row=6, column=3*(i%3), padx=50, pady=50, sticky=W)
            else:
                displayLabels.append(LabelFrame(window, text="Cold suggestion no."+str(i+1), cursor="heart", relief=RIDGE, bg=default_bg_color, fg="gold", font="none 16 italic"))
                displayLabels[-1].grid(row=5+2*(i//3), column=3*(i%3), padx=50, pady=50, sticky=W)
            
            #   beer name + abv
            tmp = str(suggestions[x].at[i,'beer_name']) + "   (" + str(suggestions[x].at[i,'beer_abv']) + "% abv)"
            frmLbl = Label(displayLabels[-1], text=tmp, bg=default_bg_color, fg="white", font="none 16 bold")
            frmLbl.grid(row=0, column=0, sticky=W)
            
            #   beer style
            tmp = "beer style: " + str(suggestions[x].at[i,'beer_style'])
            frmLb2 = Label(displayLabels[-1], text=tmp, bg=default_bg_color, fg="white", font="none 12")
            frmLb2.grid(row=1, column=0, sticky=W)
            
            #   beer brewery
            tmp = "brewery name: " + str((data.loc[data['beer_name'] == boxChoice1.get()].iloc[0])['brewery_name'])
            frmLb3 = Label(displayLabels[-1], text=tmp, bg=default_bg_color, fg="white", font="none 12")
            frmLb3.grid(row=2, column=0, sticky=W)
            
            #   frame image
            """i give up !"""

# exiting and closing window function
def closeWindow():
    window.destroy
    exit()

# main GUI window setup
window = Tk()
window.title("Beer Suggestion Application")

# setting background and default widget background color
try:
    img = Image.open(urlopen('https://wallpaper.dog/large/20483358.jpg'))
    img = ImageTk.PhotoImage(img)
    window.geometry("1956x1240")
    bg = Label(window, image=img, bd=0)
    bg.place(x=0, y=0)
except:
    default_bg_color = "#263D42"
    window.configure(background=default_bg_color)

# first label
lbl0 = Label(window, text="please enter reviews for beers you had from the list below and score them 0(bad) ~ 5(good)", bg=default_bg_color, fg="white", font="none 16 bold")
lbl0.grid(row=1, column=0,columnspan=8, sticky=W)

# input labels
lbl1 = Label(window, text="beer name", bg=default_bg_color, fg="white", font="none 16")
lbl1.grid(row=2, column=0, sticky=W)

lbl2 = Label(window, text="appearance", bg=default_bg_color, fg="white", font="none 16")
lbl2.grid(row=2, column=1, sticky=W)

lbl3 = Label(window, text="aroma", bg=default_bg_color, fg="white", font="none 16")
lbl3.grid(row=2, column=2, sticky=W)

lbl4 = Label(window, text="palate", bg=default_bg_color, fg="white", font="none 16")
lbl4.grid(row=2, column=3, sticky=W)

lbl5 = Label(window, text="taste", bg=default_bg_color, fg="white", font="none 16")
lbl5.grid(row=2, column=4, sticky=W)

lbl6 = Label(window, text="overall", bg=default_bg_color, fg="white", font="none 16")
lbl6.grid(row=2, column=5, sticky=W)

# input comboboxes
boxChoice1 = StringVar()
userChoice1 = Combobox(window, width=30, textvariable=boxChoice1)
userChoice1['values'] = beerList()
userChoice1['state'] = 'readonly'
userChoice1.grid(row=3, column=0, sticky=W)
userChoice1.current(0)

boxChoice2 = StringVar()
userChoice2 = Combobox(window, width=30, textvariable=boxChoice2)
userChoice2['values'] = scrlst
userChoice2['state'] = 'readonly'
userChoice2.grid(row=3, column=1, sticky=W)
userChoice2.current(0)

boxChoice3 = StringVar()
userChoice3 = Combobox(window, width=30, textvariable=boxChoice3)
userChoice3['values'] = scrlst
userChoice3['state'] = 'readonly'
userChoice3.grid(row=3, column=2, sticky=W)
userChoice3.current(0)

boxChoice4 = StringVar()
userChoice4 = Combobox(window, width=30, textvariable=boxChoice4)
userChoice4['values'] = scrlst
userChoice4['state'] = 'readonly'
userChoice4.grid(row=3, column=3, sticky=W)
userChoice4.current(0)

boxChoice5 = StringVar()
userChoice5 = Combobox(window, width=30, textvariable=boxChoice5)
userChoice5['values'] = scrlst
userChoice5['state'] = 'readonly'
userChoice5.grid(row=3, column=4, sticky=W)
userChoice5.current(0)

boxChoice6 = StringVar()
userChoice6 = Combobox(window, width=30, textvariable=boxChoice6)
userChoice6['values'] = scrlst
userChoice6['state'] = 'readonly'
userChoice6.grid(row=3, column=5, sticky=W)
userChoice6.current(0)

# add button and counter
btn1 = Button(window, text="add", width=6, command=addClick)
btn1.grid(row=3, column=6, padx=10, sticky=W)
lbl7 = Label(window, text="(0)", bg=default_bg_color, fg="grey", font="none 16")
lbl7.grid(row=3, column=6, padx=60)

# submit button
btn2 = Button(window, text="get results", width=10, command=submitClick)
btn2.grid(row=3, column=7, sticky=W)

# reset button
btn3 = Button(window, text="reset", width=6, command=resetClick)
btn3.grid(row=997, column=0, padx=10)

# exit
extlbl= Label(window, text="Exit with this useful button:", bg=default_bg_color, fg="white", font="none 12 bold")
extlbl.grid(row=998, column=0, pady=5)
extbtn = Button(window, text = "Exit", width=14, font="none 8 bold", command=closeWindow)
extbtn.grid(row=999, column=0)

# run GUI
window.mainloop()
