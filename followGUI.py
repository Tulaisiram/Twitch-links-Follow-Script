from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import sys
import time
import tkinter as tk
from tkinter.filedialog import askopenfilename

#twitch-links csv file
root = tk.Tk()
root.withdraw()
filename = askopenfilename()
root.destroy()
df = pd.read_csv(filename)
df.dropna(subset = ['Channel Names'], inplace=True)
keep_col = ['Channel Names','Did I Follow them?']
newFile = df[keep_col]
newList = newFile.values.tolist()
followed, notFollowed = [],[]

#Selenium
options = webdriver.ChromeOptions()
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

driver = webdriver.Chrome(resource_path('./driver/chromedriver.exe'))

#Login
driver.get("https://www.twitch.tv/")

#Username
def getName():
    global name
    name = entry.get()
    window.destroy()

def getDone():
    canvas.create_window(200, 120, window=label2)
    canvas.create_window(200, 160, window=entry)
    canvas.create_window(200, 200, window=doneButton2)

window = tk.Tk()
canvas = tk.Canvas(width = 400, height = 250, relief = 'raised')
label1 = tk.Label(text='Press Done once you\'ve logged in')
label1.config(font=('helvetica', 14))
label2 = tk.Label(text='Enter your Twitch Username')
label2.config(font=('helvetica', 14))
entry = tk.Entry(window) 
doneButton1 = tk.Button(text='Done',command=getDone, bg='blue', fg='white', font=('helvetica', 9, 'bold'))
doneButton2 = tk.Button(text='Done',command=getName, bg='blue', fg='white', font=('helvetica', 9, 'bold'))

canvas.pack()
canvas.create_window(200, 25, window=label1)
canvas.create_window(200, 70, window=doneButton1)

window.mainloop()

#Follow Script
for x in newList:
    if x[1] == "Not Followed":
        if x[0] != name:
            counter = 0
            while counter < 2:
                link = "https://www.twitch.tv/" + x[0]
                driver.get(link)

                try:
                    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "eyrwSW, euIPFy")))
                    time.sleep(1)
                    try:
                        button1 = driver.find_element_by_class_name('eyrwSW')
                        ActionChains(driver).click(button1).perform()
                        button2 = driver.find_element_by_class_name('euIPFy')
                        ActionChains(driver).click(button2).perform()
                        time.sleep(1)
                        followed.append(x[0])
                        counter = 3
                    except:
                        pass
                except:
                    counter = counter + 1
                    if counter == 2: notFollowed.append(x[0])
driver.close()
file = open("Results.txt", "w")
file.write("Followed :   " + str(len(followed) + "\n"))
file.write("Not Followed :   " + str(len(notFollowed) + "\n"))
for x in notFollowed:
    file.write(notFollowed)
    file.write("\n")