#!/usr/bin/env python
# coding: utf-8

# In[38]:


from tkinter import *
import sqlite3
import os
import xlsxwriter
from openpyxl import *

if not os.path.isfile('plyty.db'):
    db = sqlite3.connect('plyty.db')
    cursor=db.cursor()
    cursor.execute("""CREATE TABLE plyty(
        EAN text NOT NULL UNIQUE,
        wykonawca text,
        tytuł text,
        ilość integer,
        adres text)
        """)
    db.commit()
    db.close()
    
root =Tk()
root.title("miniWMS")


def scanwindow():
    scan=Toplevel()
    scan.title("miniWMS scan")
    
    def scanned(event):
        global kod
        kod=ean_Entry.get()
        menu.destroy()
        odstep1.destroy()
        odstep2.destroy()
        odstep3.destroy()
        ean_Label.destroy()
        info_lbl.destroy()
        ean_Entry.destroy()
        scan_button.destroy()
        
        db = sqlite3.connect('plyty.db')
        cursor=db.cursor()
        cursor.execute("SELECT * FROM plyty")
        plyta=cursor.fetchall()
        def nowy():
            def submit(event):
                db = sqlite3.connect('plyty.db')
                cursor=db.cursor()
                if len(zespol.get())>0 and len(tytul.get())>0 and ilosc.get().isnumeric() and len(adres.get())>0: 
                    cursor.execute("INSERT INTO plyty VALUES (:ean,:zespol,:tytul,:ilosc,:adres)",
                    {
                    'ean':kod,
                    'zespol':zespol.get().upper(),
                    'tytul':tytul.get().upper(),
                    'ilosc':ilosc.get(),
                    'adres':adres.get()
                    }              
                    )
    
                    db.commit()
                    db.close()
            
                    scan.destroy()
                    scanwindow()
                else:
                    error=Label(scan, text='Wszystkie pola są wymagane\nilość musi być liczbą')
                    error.grid(row=5, columnspan=2)
        
            db = sqlite3.connect('plyty.db')
            cursor=db.cursor()

            ean2=Label(scan, text=kod)
            ean2.grid(row=0, column=1)
            zespol=Entry(scan, width=30)
            zespol.grid(row=1, column=1)
            tytul=Entry(scan, width=30)
            tytul.grid(row=2, column=1)
            ilosc=Entry(scan, width=30)
            ilosc.grid(row=3, column=1)
            adres=Entry(scan, width=30)
            adres.grid(row=4, column=1)
            zespol.focus_set()

            ean_lbl=Label(scan, text="EAN")
            ean_lbl.grid(row=0, column=0)
            zespol_lbl=Label(scan, text="Wykonawca")
            zespol_lbl.grid(row=1, column=0)
            tytul_lbl=Label(scan, text="Tytuł")
            tytul_lbl.grid(row=2, column=0)
            ilosc_lbl=Label(scan, text="Ilość")
            ilosc_lbl.grid(row=3, column=0)
            adres_lbl=Label(scan, text="Adres")
            adres_lbl.grid(row=4, column=0)
            scan.bind('<Return>', submit)

            submit=Button(scan, text="Zapisz zmiany", command=submit)
            submit_lbl=Label(scan, text='Wciśnij enter aby kontynuować')
            submit_lbl.grid(row=7, columnspan=2)
    
        def ean():
            scan.unbind('<Return>')
            
            def plus(ile_Entry):
                db = sqlite3.connect('plyty.db')
                cursor=db.cursor()
                if zmiana[4]=='---':
                    if len(adres_Entry.get())==0:
                        error=Label(scan, text='Wartość pola "adres" jest wymagana')
                        error.grid(row=19, columnspan=5)
                    else:
                        zmiana[4]=adres_Entry.get()
                else:
                    if len(ile_Entry.get()) == 0:
                        ile=1
                    elif not ile_Entry.get().isnumeric():
                        error=Label(scan, text='Wartość pola "ilość" musi być liczbą dodatnią')
                        error.grid(row=18, columnspan=5)
                    else: 
                        ile=int(ile_Entry.get())
                        ilosc=zmiana[3]
                        ile+=int(ilosc)
                        cursor.execute("UPDATE plyty SET ilość=:ile, adres=:adres WHERE EAN=:kod",
                        {
                            'kod':kod,
                            'adres':zmiana[4],
                            'ile':ile
                        })
                        scan.destroy()
                        scanwindow()
                        db.commit()
                        db.close()
            def minus(ile_Entry):
                if len(ile_Entry.get()) == 0:
                    ile=1
                elif not ile_Entry.get().isnumeric():
                    error=Label(scan, text='Wartość pola "ilość" musi być liczbą dodatnią')
                    error.grid(row=15, columnspan=5)
                elif int(ile_Entry.get())>zmiana[3]:
                    error=Label(scan, text='Nie ma tylu sztuk na stanie')
                    error.grid(row=15, columnspan=5)
                else:
                    ile=int(ile_Entry.get())
                    db = sqlite3.connect('plyty.db')
                    cursor=db.cursor()
                    zmiana[3]-=ile
                    if zmiana[3]==0:
                        zmiana[4]='---'
                    cursor.execute("UPDATE plyty SET ilość=:ile, adres=:adres WHERE EAN=:kod",
                    {
                    'kod':kod,
                    'ile':zmiana[3],
                    'adres':zmiana[4]
                    })
                    scan.destroy()
                    scanwindow()
                    db.commit()
                    db.close()
                    
            ean_label=Label(scan, text="EAN")
            zespol_label=Label(scan, text="Wykonawca")
            tytul_label=Label(scan, text="Tytuł")
            ilosc_label=Label(scan, text="Ilość")
            adres_label=Label(scan, text="Adres")
    
            ean_label.grid(row=7,column=0)
            zespol_label.grid(row=7,column=1)
            tytul_label.grid(row=7,column=2)
            ilosc_label.grid(row=7,column=3)
            adres_label.grid(row=7,column=4)
        
            db = sqlite3.connect('plyty.db')
            cursor=db.cursor()
        
            cursor.execute("SELECT * FROM plyty")
            plyta=cursor.fetchall()
            plyta_val=""
            
            zmiana={}
            for item in plyta:
                j=0
                if kod==item[0]:
                    for data in item:
                        plyta_val=str(data)
                        zmiana[j]=data
                        item_label=Label(scan,text=plyta_val)
                        item_label.grid(row=8, column=j)
                        j+=1
            
            plus_btn=Button(scan, text="Dodaj", command=lambda: plus(ilosc_Entry))
            ilosc_lbl=Label(scan, text="ilość")
            ilosc_Entry=Entry(scan, width=3)
            plus_btn.grid(row=8, column=9)
            ilosc_lbl.grid(row=8, column=5)
            ilosc_Entry.grid(row=8, column=6)
            ilosc_Entry.focus_set()
            if zmiana[3]==0:
                adres_lbl=Label(scan, text="adres:")
                adres_lbl.grid(row=8, column=7)
                adres_Entry=Entry(scan, width=3)
                adres_Entry.grid(row=8, column=8)
            else:
                minus_btn=Button(scan, text="Usuń", command=lambda: minus(ilosc_Entry))
                minus_btn.grid(row=8, column=10)
            
            
            db.commit()
            db.close()
        
        
        i=0
        for item in plyta:
            if kod==item[0]:
                i+=1
        if i>0:
            ean()
        else:
            nowy()
            
    scan.bind('<Return>', scanned)

    menu=Label(scan, text="Skanowanie kodu EAN")

    odstep1=Label(scan, text="      ")
    odstep2=Label(scan, text="      ")
    odstep3=Label(scan, text="      ")

    ean_Label=Label(scan, text="Kod EAN:    ")
    ean_Entry=Entry(scan, width=20)
    ean_Entry.grid(row=3, column=2)
    info_lbl=Label(scan, text='Zeskanuj lub wpisz kod EAN i wciśnij enter\nby kontynuować')
    ean_Entry.focus_set()

    ean_Label.grid(row=3, column=1)
    info_lbl.grid(row=5, column=1, columnspan=2)
    menu.grid(row=1, column=1, columnspan=2)

    odstep1.grid(row=0, column=0)
    odstep2.grid(row=2, column=3)
    odstep3.grid(row=4, column=3)
    
    scan_button=Button(scan, text="Szukaj", command=scanned)
    
def searchwindow():
    search=Toplevel()
    search.title("miniWMS search")
       
    def zespol():
        szukaj=search_Entry.get().upper()
        ean_label=Label(search, text="EAN")
        zespol_label=Label(search, text="Wykonawca")
        tytul_label=Label(search, text="Tytuł")
        ilosc_label=Label(search, text="Ilość")
        adres_label=Label(search, text="Adres")
    
        ean_label.grid(row=7,column=0)
        zespol_label.grid(row=7,column=1)
        tytul_label.grid(row=7,column=2)
        ilosc_label.grid(row=7,column=3)
        adres_label.grid(row=7,column=4)
        
        db = sqlite3.connect('plyty.db')
        cursor=db.cursor()
        
        cursor.execute("SELECT * FROM plyty")
        plyta=cursor.fetchall()
        plyta_val=""
        
        
        i=0
        for item in plyta:
            j=0
            if szukaj in item[1]:
                for data in item:
                    plyta_val=str(data)
                    item_label=Label(search,text=plyta_val)
                    item_label.grid(row=10+i, column=j)
                    j+=1
            i+=1
        
        search_Entry.delete(0, END)
    
        db.commit()
        db.close()
    
    def tytul():
        szukaj=search_Entry.get().upper()
        ean_label=Label(search, text="EAN")
        zespol_label=Label(search, text="Wykonawca")
        tytul_label=Label(search, text="Tytuł")
        ilosc_label=Label(search, text="Ilość")
        adres_label=Label(search, text="Adres")
    
        ean_label.grid(row=7,column=0)
        zespol_label.grid(row=7,column=1)
        tytul_label.grid(row=7,column=2)
        ilosc_label.grid(row=7,column=3)
        adres_label.grid(row=7,column=4)
        
        db = sqlite3.connect('plyty.db')
        cursor=db.cursor()
        
        cursor.execute("SELECT * FROM plyty")
        plyta=cursor.fetchall()
        plyta_val=""
        i=0
        for item in plyta:
            j=0
            if szukaj in item[2]:
                for data in item:
                    plyta_val=str(data)
                    item_label=Label(search,text=plyta_val)
                    item_label.grid(row=10+i, column=j)
                    j+=1
            i+=1
        
        search_Entry.delete(0, END)
    
        db.commit()
        db.close()

    menu=Label(search, text="Wyszukiwanie")

    odstep1=Label(search, text="      ")
    odstep2=Label(search, text="      ")
    odstep3=Label(search, text="      ")

    search_Label=Label(search, text="Szukaj frazy:    ")
    search_Entry=Entry(search, width=20)
    search_Entry.focus_set()

    search_button1=Button(search, text="Szukaj po\nnazwie zespołu", command=zespol)
    search_button2=Button(search, text="Szukaj po\ntytule albumu", command=tytul)
    search_button3=Button(search, text="Powrót do głównego menu", command=search.destroy)

    search_Label.grid(row=3, column=1)
    search_Entry.grid(row=3, column=2)
    menu.grid(row=1, column=1, columnspan=2)

    odstep1.grid(row=0, column=0)
    odstep2.grid(row=2, column=3)
    odstep3.grid(row=4, column=3)

    search_button1.grid(row=5, column=1)
    search_button2.grid(row=5, column=2)
    search_button3.grid(row=6, column=1, columnspan=2)
    
def basewindow():
    db = sqlite3.connect('plyty.db')
    cursor=db.cursor()
    
    workbook = xlsxwriter.Workbook('Baza płyt.xlsx')
    worksheet = workbook.add_worksheet()


    cursor.execute("SELECT wykonawca,tytuł,ilość FROM plyty WHERE NOT ilość=0")
    plyta=cursor.fetchall()
    plyta_val=""
    i=0
    for item in plyta:
        j=0
        for data in item:
            plyta_val=str(data)
            worksheet.write(i, j, plyta_val)
            j+=1
        i+=1
    
    db.commit()
    db.close()
    
    workbook.close()
    
    os.startfile('Baza płyt.xlsx')

def salewindow():
    sale=Toplevel()
    sale.title("miniWMS sprzedaż")
    
    def sold(event):
        kod=ean_Entry.get()
        
        if not 'a' in globals():
            global a
            a=0
        else:
            a+=1
        
        sprzedaz=[]
        db = sqlite3.connect('plyty.db')
        cursor=db.cursor()
        cursor.execute("SELECT * FROM plyty WHERE EAN=:kod",
        {
            'kod':kod
        })
        sprzedaz=cursor.fetchone()
        if sprzedaz[3]==0:
            sold_lbl=Label(sale, text="brak towaru na stanie")
            sold_lbl.grid(row=8+a, column=1, columnspan=4)
        else:
            adres=sprzedaz[4]
            sold_lbl=Label(sale, text=sprzedaz)
            sold_lbl.grid(row=8+a, column=1, columnspan=4)
        
            ean_Entry.delete(0,END)
            ile=sprzedaz[3]-1
            if ile==0:
                 adres='---'
            cursor.execute("UPDATE plyty SET ilość=:ile, adres=:adres WHERE EAN=:kod",
            {
            'kod':kod,
            'ile':ile,
            'adres':adres
            })
            db.commit()
            db.close()
        
    
    menu=Label(sale, text="Sprzedaż")

    odstep1=Label(sale, text="      ")
    odstep2=Label(sale, text="      ")
    odstep3=Label(sale, text="      ")

    ean_Label=Label(sale, text="Kod EAN:    ")
    ean_Entry=Entry(sale, width=20)
    ean_Entry.focus_set()
    sale.bind('<Return>', sold)

    ean_Label.grid(row=3, column=1)
    ean_Entry.grid(row=3, column=2)
    menu.grid(row=1, column=1, columnspan=2)

    odstep1.grid(row=0, column=0)
    odstep2.grid(row=2, column=3)
    odstep3.grid(row=4, column=3)
    
    scan_button=Button(sale, text="Szukaj", command=sold)
    scan_button.grid(row=5, column=1)
    
    
menu=Label(root, text="Menu główne")

spacja1=Label(root, text="     ")
spacja2=Label(root, text="     ")
spacja3=Label(root, text="     ")
spacja4=Label(root, text="     ")
spacja5=Label(root, text="     ")

skan=Button(root, text="Zeskanuj płytę", width=30, command=scanwindow)
szukaj=Button(root, text="Otwórz wyszukiwarkę", width=30, command=searchwindow)
baza=Button(root, text="Otwórz bazę", width=30, command=basewindow)
sprzedaz=Button(root, text="Sprzedaż", width=30, command=salewindow)

spacja1.grid(row=0)
spacja2.grid(row=2)
spacja3.grid(row=4)
spacja4.grid(row=6)
spacja5.grid(row=8)

menu.grid(row=1)
skan.grid(row=3)
szukaj.grid(row=5)
baza.grid(row=7)
sprzedaz.grid(row=9)

root.mainloop()


# In[ ]:





# In[ ]:




