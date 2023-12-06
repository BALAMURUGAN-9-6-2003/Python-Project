import phonenumbers

from phonenumbers import carrier
from opencage.geocoder import OpenCageGeocode
import folium
from tkinter import *
from tkinter import messagebox

def findloc():
    from phonenumbers import geocoder
    phone_number=str(entry.get())
    parse=phonenumbers.parse(phone_number)
    loction=geocoder.description_for_number(parse,"en")
    key="86f9210b79d14c73b7e3943c3d91e8d7"
    geocoder=OpenCageGeocode(key)
    res=geocoder.geocode(loction)
    service_pro=carrier.name_for_number(parse,"en")
    lat=res[0]['geometry']['lat']
    lng=res[0]['geometry']['lng']
    my =folium.Map(location=[lat,lng],zoom_start=9)
    folium.Marker([lat,lng],popup=loction).add_to(my)
    messagebox.showinfo("info",("Country : "+str(loction)+"\nService provider : "+str(service_pro)+"\nLatitude : "+str(lat)+"\nLongitude : "+str(lng)))
    
def clear():
    entry.delete(0,len(entry.get()))


tk=Tk()
tk.geometry("300x200")
tk.title("Phone number Location")
Label(tk,text="Welcome to track phone number Location",font=("Bold",11),padx=10,pady=20).grid(row=0,columnspan=2)
Label(tk,text="Enter the phone number : ",pady=20).grid(row=1,column=0)
entry=Entry(tk)
entry.grid(row=1,column=1)
Button(text="Find",command=findloc).grid(row=2,column=0)
Button(text="Clear",command=clear).grid(row=2,column=1)
tk.mainloop()

