# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_dht
import tkinter as tk

from datetime import datetime

# Time internval for reading sensor data
dTimeMilisecond = 1000

# Initial the dht device, with data pin connected to:
#dhtDevice = adafruit_dht.DHT22(board.D4)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

GUI = tk.Tk()
GUI.title('Temp/Humidity')
GUI.geometry("330x300")

scrollbar = tk.Scrollbar(GUI)
scrollbar.pack( side = tk.RIGHT, fill = tk.Y)
mylist = tk.Listbox(GUI)

def readHumidity():    
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        # Print time
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")
        
        mylist.insert(tk.END, "Temp: {:.1f} F / {:.1f} C    Humidity: {}%".format(temperature_f, temperature_c, humidity))
        mylist.insert(tk.END, "Current Timestamp : {}".format(timestampStr))
        mylist.insert(tk.END, "-")
        mylist.pack(side = tk.LEFT, fill = tk.BOTH, expand=True)        
        mylist.see(tk.END)
        
        mylist.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = mylist.yview)
        

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        #print(error.args[0])        
        time.sleep(1.0)
    except Exception as error:
        dhtDevice.exit()
        raise error
    GUI.after(dTimeMilisecond, readHumidity)  # reschedule event in  miliseconds

GUI.after(dTimeMilisecond, readHumidity)
GUI.mainloop()
