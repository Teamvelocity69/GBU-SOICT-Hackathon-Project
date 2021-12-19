from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
#import pyqrcode
import mysql.connector
from fpdf import FPDF
import datetime

#the pyqrcode package crashes the project after making the one bill, better we remove this feature for now.

#mysql connectivity is done here only
my=mysql.connector.connect(user="root", password="root123", host="127.0.0.1", database="restaurants")
mydb=my.cursor()

#fdpf connection is made here
pdf=FPDF()

#all the fooditems specified here
givenfooditems=[["Idli Sambhar","60"], ["Medu Vada","50"], ["Momos","40"], ["Aloo Pakoda","50"],
                ["Panner Pakoda","50"],["Payaaz Pakoda", "50"], ["Mixed Pakodas", "60"],
                ["Aloo Parantha","60"],["Pyaaz Parantha","60"],["Paneer Parantha","50"],
                ["Spring Rolls","120"], ["French Toast","110"], ["Grilled Sandwhich","115"]
                ,["Poha", "70"], ["Dalia", "70"],["Dal Makhani", "170"], ["Shahi Paneer", "185"],
                ["Dum Aloo", "170"],["Dal Tadka", "150"],["Naan", "50"], ["Chowmein", "180"],
                ["Manchurian Gravy", "180"], ["Fried Rice", "140"],["Tandoori Roti", "20"],
                ["Choupsey", "190"], ["Aribitta Pasta", "210"], ["Lasagna", "180"],["Pepsi", "30"],
                ["Water","20"], ["Coffee", "30"], ["Tea", "30"], ["Orange juice", "50"], ["Espresso", "70"]
                ,["Ice tea", "60"], ["Lemon Juice","50"], ["Apple juice", "50"]]


#specified the buttons are made here using function
def buttons(win,text, x,y):
    Button(win, text=text, command=lambda:logic(text), width=30).place(x=x, y=y)

#specified the labels are made here using function
def labels(win, text, x,y):
    Label(win, text=text, font=(22)).place(x=x, y=y)

#all the fooditems are inserted into the list in this function
def logic(x):
    for i in givenfooditems:
        if i[0]==x:
            d="                    ".join(i)
            l1.insert(ACTIVE, f"{d}")
        else:
            pass



#it will evaluate the price of all food which is in Listbox
def evaluate():
    m=l1.get(0,END)
    total_amount=0
    for i in m:
        i=i.split("                    ")
        total_amount+=int(i[1])
    amount.set(total_amount)
    netamount.set(int(total_amount+(total_amount*(5/100))+20))

#function made to delete all items from listbox
def deleteall():
    l1.delete(0,END)
    amount.set(0)

#function to delete a specified item from listbox
def selectdelete():
    selection=l1.curselection()
    selection=int(selection[0])
    l1.delete(selection)

#arguements to place order and enter the data in mysql is done here
def place_order():
    messagebox.showinfo("Alright", "PLacing the Order")
    currenttime=datetime.datetime.now()
    billmaking(orderno.get(),name.get(), phone.get(), netamount.get(), ch.get(), ch1.get(), currenttime.year, currenttime.month, currenttime.day, currenttime.hour, currenttime.minute)
    recordentry(orderno.get(),name.get(), phone.get(), netamount.get(), ch.get(), ch1.get(), currenttime.year, currenttime.month, currenttime.day, currenttime.hour, currenttime.minute)
    messagebox.showinfo("Sucessful", "The Order is Placed")
    name.set("")
    phone.set("")
    amount.set("")
    netamount.set("")
    orderno.set("")
    l1.delete(0,END)

#Bill is made here in this function
#Note Date and time can not be entered in this function
def billmaking(orderno,name, phonenum, amount, paymode, mode, year, month, date, hour, minute):
#    qr=pyqrcode.create(f"{orderno}\n{name}\n{l1.insert(0,END)}\n{amount}\n{paymode}")
#    qr.png(f"{orderno}.png", scale=2)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10,txt="Billing Application", align='C', ln=1)
    pdf.cell(200, 10, txt="25, Parliament Road,New Delhi", align='C', ln=2)
    pdf.cell(200, 10, txt="=========================================", align='C', ln=3)
    pdf.cell(200, 10, txt=" ", align='C', ln=4)
    pdf.cell(200, 10, txt=f"Order Number :                {orderno}", align='L', ln=5)
    pdf.cell(200, 10, txt=f"Name of Customer :            {name}", align='L', ln=6)
    pdf.cell(200, 10, txt=f"Phone Number of Customer :    {phonenum}", align='L', ln=7)
    pdf.cell(200, 10, txt=f"Mode of Eating :              {mode}", align='L', ln=8)
    # pdf.cell(200, 10, txt=" ", align='L', ln=9)
    pdf.cell(200, 10, txt=f"Date and Time of issuing Bill : {date}/{month}/{year} , {hour}:{minute}", align='L', ln=10)
    pdf.cell(200, 10, txt=f" ", align='L', ln=10)
    pdf.cell(200, 10, txt=" ", align='L', ln=11)
    pdf.cell(200, 10, txt="Dish_Name                      Price", align='L', ln=12)
    fooditems=l1.get(0,END)
    line=13
    for i in fooditems:
        pdf.cell(200, 10, txt=f"{i}", align='L', ln=line)
        line+=1
    pdf.cell(200, 10, txt=" ", align='L', ln=line+1)
    pdf.cell(200, 10, txt=f"Total Amount with GST : Rs{amount}", align='L', ln=line+2)
    pdf.cell(200, 10, txt=f"Mode of Payment : {paymode}", align='L', ln=line+3)
    pdf.cell(200, 10, txt=" ", align='L', ln=line+4)
    pdf.cell(200, 10, txt="Thank for Visiting/Ordering from us", align='C', ln=line+5)
#    pdf.image(f"{orderno}.png", 170, 200)
    pdf.output(f"{orderno}.pdf")

#record is entered here to mysql
#date and time can't be entered in the mysql
def recordentry(orderno,name, phonenum, amount, paymode, mode, year, month, date, hour, minute):
    mydb.execute(f"insert into r1 values('{orderno}', '{name}',{phonenum},'{year}/{month}/{date}','{hour}:{minute}', '{paymode}', '{mode}', '{amount}')")
    my.commit()

#main menu is declared here
if __name__ == '__main__':
    rt=Tk()
    rt.geometry("1600x1000")
    rt.title(" Billing Application v1.0.0.1")
    #labels here
    labels(rt, "Starters", 360, 0)
    labels(rt, "Main Course", 360, 260)
    labels(rt, "Bevrages", 360, 480)
    labels(rt, "Food_Item                              Price", 1500,30)
    labels(rt, "Name ", 900, 100)
    labels(rt, "Phone ", 900, 150)
    labels(rt, "Total Amount ", 1500, 520)
    labels(rt, "Net Amount", 1500, 560)
    labels(rt, "Payment Mode ", 900, 200)
    labels(rt, "Mode ", 900, 250)
    labels(rt, "GST is 5%. It is included in the total bill ", 900, 300)
    labels(rt, "Service charge is of Rs 20/- ", 900, 325)
    labels(rt, "Order Number ", 900, 50)
    #all func created buttons
    #starters
    buttons(rt,givenfooditems[0][0], 0, 40)
    buttons(rt, givenfooditems[1][0], 270, 40)
    buttons(rt, givenfooditems[2][0], 540, 40)
    buttons(rt, givenfooditems[3][0], 0, 80)
    buttons(rt, givenfooditems[4][0], 270,80)
    buttons(rt, givenfooditems[5][0], 540,80)
    buttons(rt, givenfooditems[6][0], 0,120)
    buttons(rt, givenfooditems[7][0], 270,120)
    buttons(rt, givenfooditems[8][0], 540,120)
    buttons(rt, givenfooditems[9][0], 0,160)
    buttons(rt, givenfooditems[10][0], 270,160)
    buttons(rt, givenfooditems[11][0], 540,160)
    buttons(rt, givenfooditems[12][0], 0,200)
    buttons(rt, givenfooditems[13][0], 270,200)
    buttons(rt, givenfooditems[14][0], 540,200)
    buttons(rt, givenfooditems[15][0], 0,300)
    #main course
    buttons(rt, givenfooditems[16][0], 270,300)
    buttons(rt, givenfooditems[17][0], 540,300)
    buttons(rt, givenfooditems[18][0], 0,340)
    buttons(rt, givenfooditems[19][0], 270,340)
    buttons(rt, givenfooditems[20][0], 540,340)
    buttons(rt, givenfooditems[21][0], 0,380)
    buttons(rt, givenfooditems[22][0], 270,380)
    buttons(rt, givenfooditems[23][0], 540,380)
    buttons(rt, givenfooditems[24][0], 0,420)
    buttons(rt, givenfooditems[25][0], 270,420)
    buttons(rt, givenfooditems[26][0], 540,420)
    #bevrages
    buttons(rt, givenfooditems[27][0], 0,520)
    buttons(rt, givenfooditems[28][0], 270,520)
    buttons(rt, givenfooditems[29][0], 540,520)
    buttons(rt, givenfooditems[30][0], 0,560)
    buttons(rt, givenfooditems[31][0], 270,560)
    buttons(rt, givenfooditems[32][0], 540,560)
    buttons(rt, givenfooditems[33][0], 0,600)
    buttons(rt, givenfooditems[34][0], 270,600)
    buttons(rt, givenfooditems[35][0], 540,600)




    l1=Listbox(rt, width=30, height=20, font=(22), selectmode=MULTIPLE)
    l1.place(x=1500, y=80)
    #self made buttons
    Button(rt, text="Delete", command=selectdelete, width=12).place(x=1700, y=485)
    Button(rt, text="Delete All", command=deleteall, width=12).place(x=1600, y=485)
    Button(rt, text="Evaluate", command=evaluate, width=12).place(x=1500, y=485)
    Button(rt, text="Place order", width=15, command=place_order).place(x=1670, y=600)

    #all textbox variables are declared here
    name=StringVar()
    phone=StringVar()
    amount=StringVar()
    orderno=StringVar()
    netamount=StringVar()
    Entry(rt, font=(22), textvariable=name).place(x=1100, y=100)
    Entry(rt, font=(22), textvariable=phone).place(x=1100, y=150)
    Entry(rt, font=(22), textvariable=amount, width=15).place(x=1650, y=520)
    Entry(rt, font=(22), textvariable=netamount, width=15).place(x=1650, y=560)
    Entry(rt,font=(22), textvariable=orderno).place(x=1100, y=50)

    ch=Combobox(rt, font=(22))
    ch['values']=["Cash-IN", "Visa/Mastercard", "Online Patyment", "Barten saaf karke", "select anyone"]
    ch.current(4)
    ch.place(x=1100, y=200)

    ch1=Combobox(rt, font=(22))
    ch1['values']=["Dinein", "Take Away", "Home Delivery", "select anyone"]
    ch1.current(3)
    ch1.place(x=1100, y=250)

    rt.mainloop()
