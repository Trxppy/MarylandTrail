import os
import keyboard
import tkinter
import random
import math
from PIL import Image, ImageTk
from tkinter import messagebox

class Interface(object):
    """handles graphical interface"""
    window = None
    loader = None
    window_width =  None
    window_height = None
    dynamic_frame = None
    toolbar_frame = None
    toolbar_buttons = None
    scenes = {}
    players = {}
    stats = {}
    inventory = []
    visited_scenes = []
    random_events_experienced = []
    scene_cursor = 'scene1'
    location = None

    def __init__(self, loader):
        # initalize window and loader
        self.window = tkinter.Tk()
        self.loader = loader
        self.window_width = self.window.winfo_screenwidth()
        self.window_height = self.window.winfo_screenheight()
        # create dynamic frame
        self.dynamic_frame = tkinter.Frame(self.window, bg="#1a1a1a")
        self.dynamic_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
        # set window properties
        self.window.attributes('-fullscreen', True)
        # create menu frame (toolbar)
        self.toolbar_frame = tkinter.Frame(self.window, bg="#000")
        self.toolbar_frame.place(relwidth=.2, relheight=1)
        self.toolbar_buttons = {}
        self.toolbar_buttons['inventory'] = tkinter.Button(self.toolbar_frame, text = 'view inventory', command=self.open_inventory)
        self.toolbar_buttons['inventory'].place(relwidth=0.9, relheight=0.08, relx=0.05, rely=0.75)
        self.toolbar_buttons['exit'] = tkinter.Button(self.toolbar_frame, text = 'exit', command=self.close)
        self.toolbar_buttons['exit'].place(relwidth=0.9, relheight=0.08, relx=0.05, rely=0.85)
        # self.toolbar image
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/welcome_maryland.png")
        self.toolbar_buttons['image'] = {}
        self.toolbar_buttons['image']['welcome_sign'] = Image.open(filepath)
        self.toolbar_buttons['image']['welcome_sign'] = self.toolbar_buttons['image']['welcome_sign'].resize((round(self.window_width * 0.1), round(self.window_height * 0.2)), Image.ANTIALIAS)
        self.toolbar_buttons['image']['welcome_sign_widget'] = ImageTk.PhotoImage(self.toolbar_buttons['image']['welcome_sign'])
        self.toolbar_buttons['image']['label'] = tkinter.Label(image=self.toolbar_buttons['image']['welcome_sign_widget'], borderwidth=0)
        self.toolbar_buttons['image']['label'].image = self.toolbar_buttons['image']['welcome_sign_widget']
        self.toolbar_buttons['image']['label'].place(relx=0.05, rely=0.05)
        self.toolbar_buttons['image']['heading'] = tkinter.Label(bg="#000", text="The Maryland Trail", fg="#fff", font=("Arial", 20))
        self.window.update() # updates window dimensions
        self.toolbar_buttons['image']['heading'].place(x=(self.toolbar_frame.winfo_width() - self.toolbar_buttons['image']['label'].winfo_width())/4, y=round(self.window_height * 0.2) + round(self.window_height * 0.05) + 5)
        # self.toolbar stats
        self.toolbar_buttons['stats'] = {}
        self.toolbar_buttons['stats']['fun'] = tkinter.Label(self.toolbar_frame, bg="#000", text="Fun: 5/100", fg="#e35454", font=("Arial", 16), justify="center")
        self.toolbar_buttons['stats']['fun'].place(rely=0.4, relx=0.1, relwidth=0.8)
        self.toolbar_buttons['stats']['hunger'] = tkinter.Label(self.toolbar_frame, bg="#000", text="Hunger: 20/20", fg="#94f086", font=("Arial", 15), justify="center")
        self.toolbar_buttons['stats']['hunger'].place(rely=0.45, relx=0.1, relwidth=0.8)
        self.toolbar_buttons['stats']['rest'] = tkinter.Label(self.toolbar_frame, bg="#000", text="Rest: 20/20", fg="#94f086", font=("Arial", 16), justify="center")
        self.toolbar_buttons['stats']['rest'].place(rely=0.5, relx=0.1, relwidth=0.8)
        self.toolbar_buttons['stats']['money'] = tkinter.Label(self.toolbar_frame, bg="#000", text="Money: $0", fg="#94f086", font=("Arial", 15), justify="center")
        self.toolbar_buttons['stats']['money'].place(rely=0.55, relx=0.1, relwidth=0.8)
        self.toolbar_buttons['stats']['time'] = tkinter.Label(self.toolbar_frame, bg="#000", text="120 hours left", fg="#fff", font=("Arial", 16), justify="center")
        self.toolbar_buttons['stats']['time'].place(rely=0.6, relx=0.1, relwidth=0.8)
        # create scene 1 (game intro)
        self.window.update() # updates window dimensions
        self.scenes['scene1'] = {}
        self.scenes['scene1']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene1']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        self.scenes['scene1']['text'] = "Welcome to the Maryland Trail!\n\nOn your journey you will have the opportunity to explore the Old Line State\n in all of its grandeur, with YOU deciding what to explore and how to explore it.\n\nMake wise decisions and make the most of your trip.\n\nSafe travels!\n"
        self.scenes['scene1']['text_label'] = tkinter.Label(self.scenes['scene1']['frame'], bg="#1a1a1a", text=self.scenes['scene1']['text'], fg="#fff", font=("Arial", 16))
        self.scenes['scene1']['text_label'].pack()
        self.scenes['scene1']['continue_label'] = tkinter.Label(self.scenes['scene1']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene1']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene2'))  
        self.scenes['scene1']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        # create scene 2 (player count)
        self.window.update() # updates window dimensions
        self.scenes['scene2'] = {}
        self.scenes['scene2']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene2']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        self.scenes['scene2']['text'] = "How many people will be traveling with you?\n\nPlease enter a value between 0-7"
        self.scenes['scene2']['text_label'] = tkinter.Label(self.scenes['scene2']['frame'], bg="#1a1a1a", text=self.scenes['scene2']['text'], fg="#fff", font=("Arial", 20))
        self.scenes['scene2']['text_label'].pack()
        self.scenes['scene2']['continue_label'] = tkinter.Label(self.scenes['scene2']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene2']['input1'] = tkinter.Entry(self.scenes['scene2']['frame'], fg="#fff", bg="#1a1a1a", borderwidth=1, relief="sunken", font=("Arial", 16), justify="center")
        self.scenes['scene2']['input1'].place(relx=0.35, rely=0.2, relheight=0.08, relwidth=0.3)
        self.scenes['scene2']['continue_label'].bind("<Button>", lambda e:self.create_players())  
        self.scenes['scene2']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene2']['frame'].place_forget()
        # finish window creation
        self.window.mainloop()

    # creates (and validates number of) players (scene2)
    def create_players(self):
        if(not self.scenes['scene2']['input1'].get().isnumeric()):
            messagebox.showinfo("Oops!", "Please enter a valid number")
        else:
            if(int(self.scenes['scene2']['input1'].get()) > 7 or int(self.scenes['scene2']['input1'].get()) < 0):
                messagebox.showinfo("Oops!", "Please enter a number from 0-7")
            else:
                # if all conditions met, create outline for players
                players_created = 0
                while(players_created < int(self.scenes['scene2']['input1'].get())):
                    self.players[players_created] = {}
                    self.players[players_created]['id'] = players_created
                    players_created += 1
                self.name_players()

    # name players (scene 3)
    def name_players(self):
        # initialize stats
        self.stats["fun"] = 5
        self.stats["hunger"] = 20
        self.stats["rest"] = 20
        self.stats["money"] = 1000 + (500 * len(self.players))
        self.stats["time"] = 120
        self.update_stats()
        if(len(self.players) > 0):
            self.scene_cursor = 'scene3'
            self.scenes['scene3'] = {}
            self.scenes['scene3']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
            self.scenes['scene3']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
            self.scenes['scene3']['text'] = "What are the names of your passengers?"
            self.scenes['scene3']['text_label'] = tkinter.Label(self.scenes['scene3']['frame'], bg="#1a1a1a", text=self.scenes['scene3']['text'], fg="#fff", font=("Arial", 20))
            self.scenes['scene3']['text_label'].pack()
            self.scenes['scene3']['continue_label'] = tkinter.Label(self.scenes['scene3']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
            for x in self.players:
                self.scenes['scene3']['input' + str(x)] = tkinter.Entry(self.scenes['scene3']['frame'], fg="#fff", bg="#1a1a1a", borderwidth=1, relief="sunken", font=("Arial", 16), justify="center")
                self.scenes['scene3']['input' + str(x)].place(relx=0.3, rely=0.2 + (x * .08), relheight=0.08, relwidth=0.4)
            self.scenes['scene3']['continue_label'].bind("<Button>", lambda e:self.choose_vehicles())  
            self.scenes['scene3']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        else:
            self.choose_vehicles()

    # create vehicle selection menu
    def choose_vehicles(self):   
        self.window.update() # updates window dimensions
        self.scene_cursor = 'scene4'
        self.scenes['scene4'] = {}
        self.scenes['scene4']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene4']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        self.scenes['scene4']['text'] = "Select your vehicle!\n\nRemember, your car must be able to\n accomodate you plus ({}) passengers!".format(len(self.players))
        self.scenes['scene4']['text2'] = "\n\n [0]--> VW Bus ($1000, seats 8)\n\n [1]--> Mercedes G Wagon ($1500, seats 7)\n\n [2]--> Toyota Corolla ($400, seats 5)\n\n [3]--> Subaru outback ($550, seats 5)\n\n [4]--> Toyota Highlander ($700, seats 7)\n\n [5]--> RV Camper ($1200, seats 8)"
        self.scenes['scene4']['text_label'] = tkinter.Label(self.scenes['scene4']['frame'], bg="#1a1a1a", text=self.scenes['scene4']['text'], fg="#fff", font=("Arial", 20))
        self.scenes['scene4']['text_label'].pack()
        self.scenes['scene4']['text_label2'] = tkinter.Label(self.scenes['scene4']['frame'], bg="#1a1a1a", text=self.scenes['scene4']['text2'], fg="#fff", font=("Arial", 14), justify="left")
        self.scenes['scene4']['text_label2'].pack()
        self.scenes['scene4']['continue_label'] = tkinter.Label(self.scenes['scene4']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene4']['input1'] = tkinter.Entry(self.scenes['scene4']['frame'], fg="#fff", bg="#1a1a1a", borderwidth=1, relief="sunken", font=("Arial", 16), justify="center")
        self.scenes['scene4']['input1'].place(relx=0.35, rely=0.7, relheight=0.08, relwidth=0.3)
        self.scenes['scene4']['continue_label'].bind( "<Button>", lambda e:self.select_vehicle(self.scenes['scene4']['input1'].get()))  
        self.scenes['scene4']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene4']['frame'].place_forget()
        self.open_scene('scene4')

    # select vehicle (and validate vehicle choice)
    def select_vehicle(self, num):
        vehicle_purchased = False
        accepted_values = ['0', '1','2','3','4','5']
        if(num not in accepted_values):
            messagebox.showinfo("Oops!", "Vehicle not found! Please try again.")
        else:
            if(num == '0' and self.stats["money"] - 1000 >= 0):
                # vw bus
                self.stats["money"] -= 1000
                self.stats["fun"] += 3
                self.inventory.append("Volkswagen Bus") 
                vehicle_purchased = True
            elif(num == '1' and self.stats["money"] - 1500 >= 0):
                # mercedes g-wagon
                self.stats["money"] -= 1500
                self.stats["fun"] += 5
                self.inventory.append("Mercedes G-Wagon") 
                vehicle_purchased = True   
            elif(num == '2' and self.stats["money"] - 400 >= 0):
                # toyota corolla
                self.stats["money"] -= 400
                self.inventory.append("Toyota Corolla") 
                vehicle_purchased = True   
            elif(num == '3' and self.stats["money"] - 550 >= 0):
                # subaru outback
                self.stats["money"] -= 550
                self.inventory.append("Subaru Outback")
                vehicle_purchased = True
            elif(num == '4' and self.stats["money"] - 700 >= 0):
                # toyota highlander
                self.stats["money"] -= 700
                self.inventory.append("Toyota Highlander") 
                vehicle_purchased = True  
            elif(num == '5' and self.stats["money"] - 1200 >= 0):
                # kayak
                self.stats["money"] -= 1200
                self.stats["fun"] += 7
                self.inventory.append("RV Camper") 
                vehicle_purchased = True 
            else:
                messagebox.showinfo("Oops!", "You don't have enough money to purchase that item!")
            if(vehicle_purchased):
                self.choose_items()
            self.update_stats()

    # create store menu
    def choose_items(self):
        self.scene_cursor = 'scene5'
        self.scenes['scene5'] = {}
        self.scenes['scene5']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene5']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        self.scenes['scene5']['text'] = "What items would you like to purchase?"
        self.scenes['scene5']['text2'] = "\n\n [0]--> Spare Tire ($250)\n\n [1]--> Air Pump ($40)\n\n [2]--> First Aid Kit ($20)\n\n [3]--> Tent ($250)\n\n [4]--> Pepper Spray ($5)\n\n [5]--> Kayak ($350)\n\n [6]--> Surfboard ($300)\n\n [7]--> Raft ($250)"
        self.scenes['scene5']['text_label'] = tkinter.Label(self.scenes['scene5']['frame'], bg="#1a1a1a", text=self.scenes['scene5']['text'], fg="#fff", font=("Arial", 20))
        self.scenes['scene5']['text_label'].pack()
        self.scenes['scene5']['text_label2'] = tkinter.Label(self.scenes['scene5']['frame'], bg="#1a1a1a", text=self.scenes['scene5']['text2'], fg="#fff", font=("Arial", 14), justify="left")
        self.scenes['scene5']['text_label2'].pack()
        self.scenes['scene5']['input'] = tkinter.Entry(self.scenes['scene5']['frame'], fg="#fff", bg="#1a1a1a", borderwidth=1, relief="sunken", font=("Arial", 16), justify="center")
        self.scenes['scene5']['input'].place(relx=0.3, rely=0.7, relheight=0.08, relwidth=0.4)
        self.scenes['scene5']['continue_label'] = tkinter.Label(self.scenes['scene5']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene5']['continue_label'].bind("<Button>", lambda e:self.choose_location())  
        self.scenes['scene5']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene5']['confirm_label'] = tkinter.Label(self.scenes['scene5']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONFIRM PURCHASE", fg="#5cecff", font=("Arial", 20))
        self.scenes['scene5']['confirm_label'].bind("<Button>", lambda e:self.buy_item(self.scenes['scene5']['input'].get()))  
        self.scenes['scene5']['confirm_label'].place(relx=.15, rely=.8, relwidth=.7)

    # buy item from menu
    def buy_item(self, num):
        accepted_values = ['0', '1','2','3','4','5','6','7']
        if(num not in accepted_values):
            messagebox.showinfo("Oops!", "Item not found! Please try again.")
        else:
            if(num == '0' and self.stats["money"] - 250 >= 0):
                # spare tire
                self.stats["money"] -= 250
                self.inventory.append("Spare Tire")       
            elif(num == '1' and self.stats["money"] - 40 >= 0):
                # air pump
                self.stats["money"] -= 40
                self.inventory.append("Air Pump")    
            elif(num == '2' and self.stats["money"] - 20 >= 0):
                # first aid kit
                self.stats["money"] -= 20
                self.inventory.append("First Aid Kit")    
            elif(num == '3' and self.stats["money"] - 250 >= 0):
                # tent
                self.stats["money"] -= 250
                self.inventory.append("Tent")
            elif(num == '4' and self.stats["money"] - 5 >= 0):
                # pepper spray
                self.stats["money"] -= 5
                self.inventory.append("Pepper Spray")   
            elif(num == '5' and self.stats["money"] - 350 >= 0):
                # kayak
                self.stats["money"] -= 350
                self.inventory.append("Kayak")    
            elif(num == '6' and self.stats["money"] - 300 >= 0):
                # surfboard
                self.stats["money"] -= 300
                self.inventory.append("Surfboard")
            elif(num == '7' and self.stats["money"] - 250 >= 0):
                # raft
                self.stats["money"] -= 250
                self.inventory.append("Raft")
            else:
                messagebox.showinfo("Oops!", "You don't have enough money to purchase that item!")
            self.update_stats()

    # update toolbar stats
    def update_stats(self):
        # make sure that rest and hunger don't exceed their maximums
        if(self.stats["rest"] > 20):
            self.stats["rest"] = 20
        if(self.stats["hunger"] > 20):
            self.stats["hunger"] = 20
        # reset stat ui components
        self.toolbar_buttons['stats']['fun'].place_forget()
        self.toolbar_buttons['stats']['hunger'].place_forget()
        self.toolbar_buttons['stats']['rest'].place_forget()
        self.toolbar_buttons['stats']['money'].place_forget()
        self.toolbar_buttons['stats']['time'].place_forget()
        # get color for fun stat
        if(self.stats['fun'] < 75 and self.stats['fun'] > 40):
            color = "#ffe033"
        elif(self.stats['fun'] > 74):
            color = "#94f086"
        else:
            color = "#e35454"
        self.toolbar_buttons['stats']['fun'] = tkinter.Label(self.toolbar_frame, bg="#000", text="Fun: {}/100".format(self.stats["fun"]), fg="#e35454", font=("Arial", 16), justify="center")
        self.toolbar_buttons['stats']['fun'].place(rely=0.4, relx=0.1, relwidth=0.8)
        # get color for hunger stat
        if(self.stats['hunger'] < 15 and self.stats['hunger'] > 7):
            color = "#ffe033"
        elif(self.stats['hunger'] > 14):
            color = "#94f086"
        else:
            color = "#e35454"
        self.toolbar_buttons['stats']['hunger'] = tkinter.Label(self.toolbar_frame, bg="#000", text="Hunger: {}/20".format(self.stats["hunger"]), fg="#94f086", font=("Arial", 15), justify="center")
        self.toolbar_buttons['stats']['hunger'].place(rely=0.45, relx=0.1, relwidth=0.8)
        # get color for rest stat
        if(self.stats['rest'] < 13 and self.stats['rest'] > 4):
            color = "#ffe033"
        elif(self.stats['rest'] > 12):
            color = "#94f086"
        else:
            color = "#e35454"
        self.toolbar_buttons['stats']['rest'] = tkinter.Label(self.toolbar_frame, bg="#000", text="Rest: {}/20".format(self.stats["rest"]), fg="#94f086", font=("Arial", 16), justify="center")
        self.toolbar_buttons['stats']['rest'].place(rely=0.5, relx=0.1, relwidth=0.8)
        # get color for money stat
        if(self.stats['money'] > 100):
            color = "#e35454"
        else:
            color = "#ffe033"
        self.toolbar_buttons['stats']['money'] = tkinter.Label(self.toolbar_frame, bg="#000", text="Money: ${}".format(self.stats["money"]), fg="#94f086", font=("Arial", 15), justify="center")
        self.toolbar_buttons['stats']['money'].place(rely=0.55, relx=0.1, relwidth=0.8)
        self.toolbar_buttons['stats']['time'] = tkinter.Label(self.toolbar_frame, bg="#000", text="{} hours left".format(self.stats["time"]), fg="#fff", font=("Arial", 16), justify="center")
        self.toolbar_buttons['stats']['time'].place(rely=0.6, relx=0.1, relwidth=0.8)

    def choose_location(self):
        self.scenes['scene6'] = {}
        self.scenes['scene6']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene6']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        self.scenes['scene6']['text'] = "Where would you like to start?"
        self.scenes['scene6']['text2'] = "\n\n [0]--> Baltimore\n\n [1]--> Frederick\n\n [2]--> The Eastern Shore\n\n [3]--> Annapolis\n\n [4]--> Montgomery County\n\n [5]--> Deep Creek Lake"
        self.scenes['scene6']['text_label'] = tkinter.Label(self.scenes['scene6']['frame'], bg="#1a1a1a", text=self.scenes['scene6']['text'], fg="#fff", font=("Arial", 20))
        self.scenes['scene6']['text_label'].pack()
        self.scenes['scene6']['text_label2'] = tkinter.Label(self.scenes['scene6']['frame'], bg="#1a1a1a", text=self.scenes['scene6']['text2'], fg="#fff", font=("Arial", 14), justify="left")
        self.scenes['scene6']['text_label2'].pack()
        self.scenes['scene6']['input'] = tkinter.Entry(self.scenes['scene6']['frame'], fg="#fff", bg="#1a1a1a", borderwidth=1, relief="sunken", font=("Arial", 16), justify="center")
        self.scenes['scene6']['input'].place(relx=0.3, rely=0.7, relheight=0.08, relwidth=0.4)
        self.scenes['scene6']['continue_label'] = tkinter.Label(self.scenes['scene6']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene6']['continue_label'].bind("<Button>", lambda e:self.select_starting_location(self.scenes['scene6']['input'].get()))  
        self.scenes['scene6']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        # load location scenes and update stats
        self.load_destinations()

    def travel_menu(self, current_location):
        # create travel menu scene
        self.scenes['travel_menu'] = {}
        self.scenes['travel_menu']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['travel_menu']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        self.scenes['travel_menu']['text'] = "Where would you like to travel?"
        self.scenes['travel_menu']['text2'] = "\n\n [0]--> Baltimore\n\n [1]--> Frederick\n\n [2]--> The Eastern Shore\n\n [3]--> Annapolis\n\n [4]--> Montgomery County\n\n [5]--> Deep Creek Lake"
        self.scenes['travel_menu']['text_label'] = tkinter.Label(self.scenes['travel_menu']['frame'], bg="#1a1a1a", text=self.scenes['travel_menu']['text'], fg="#fff", font=("Arial", 20))
        self.scenes['travel_menu']['text_label'].pack()
        self.scenes['travel_menu']['text_label2'] = tkinter.Label(self.scenes['travel_menu']['frame'], bg="#1a1a1a", text=self.scenes['travel_menu']['text2'], fg="#fff", font=("Arial", 14), justify="left")
        self.scenes['travel_menu']['text_label2'].pack()
        self.scenes['travel_menu']['input'] = tkinter.Entry(self.scenes['travel_menu']['frame'], fg="#fff", bg="#1a1a1a", borderwidth=1, relief="sunken", font=("Arial", 16), justify="center")
        self.scenes['travel_menu']['input'].place(relx=0.3, rely=0.7, relheight=0.08, relwidth=0.4)
        self.scenes['travel_menu']['continue_label'] = tkinter.Label(self.scenes['travel_menu']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['travel_menu']['continue_label'].bind("<Button>", lambda e:self.travel_menu_handler(current_location, self.scenes['travel_menu']['input'].get()))  
        self.scenes['travel_menu']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        # scene travel0: baltimore travel scene
        self.scenes['travel0'] = {}
        self.scenes['travel0']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['travel0']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/travel/baltimore.jpg")
        self.scenes['travel0']["image"] = Image.open(filepath)
        self.scenes['travel0']["image_widget"] = ImageTk.PhotoImage(self.scenes['travel0']["image"])
        self.scenes['travel0']["image_label"] = tkinter.Label(self.scenes['travel0']['frame'], image=self.scenes['travel0']["image_widget"], borderwidth=0)
        self.scenes['travel0']['image_label'].image = self.scenes['travel0']["image_widget"]
        self.scenes['travel0']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['travel0']['continue_label'] = tkinter.Label(self.scenes['travel0']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['travel0']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene8'))
        self.scenes['travel0']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['travel0']['frame'].place_forget()
        # scene travel1: frederick travel scene
        self.scenes['travel1'] = {}
        self.scenes['travel1']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['travel1']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/travel/frederick.jpg")
        self.scenes['travel1']["image"] = Image.open(filepath)
        self.scenes['travel1']["image_widget"] = ImageTk.PhotoImage(self.scenes['travel1']["image"])
        self.scenes['travel1']["image_label"] = tkinter.Label(self.scenes['travel1']['frame'], image=self.scenes['travel1']["image_widget"], borderwidth=0)
        self.scenes['travel1']['image_label'].image = self.scenes['travel1']["image_widget"]
        self.scenes['travel1']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['travel1']['continue_label'] = tkinter.Label(self.scenes['travel1']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['travel1']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene8'))
        self.scenes['travel1']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['travel1']['frame'].place_forget()

    def travel_menu_handler(self, current_location, destination):
            if(destination == current_location):
                # if destination and start point is the same, prompt message box
                messagebox.showinfo("Oops!", "You're already in this area! Please choose a different location!")
            else:
                # otherwise, redirect to corresponding travel scene
                self.open_scene("travel" + str(destination))



    # select starting location
    def select_starting_location(self, num):
        accepted_values = ['0', '1','2','3','4','5']
        if(num not in accepted_values):
            messagebox.showinfo("Oops!", "Please enter a valid response to continue!")
        else:
            if(num == '0'):
                # start in baltimore
                self.location = 0
                self.open_scene("scene7")
            elif(num == '1'):
                # start in frederick
                self.location = 1
                self.open_scene("scene8")
            elif(num == '2'):
                # start in eastern shore
                self.location = 2
                self.open_scene("scene9")
            elif(num == '3'):
                # start in annapolis
                self.location = 3
                self.open_scene("scene10")
            elif(num == '4'):
                # start in montgomery county
                self.location = 4
                self.open_scene("scene11")
            elif(num == '5'):
                # start in western maryland
                self.location = 5
                self.open_scene("scene12")  
            self.update_stats()

    # open inventory for player to view
    def open_inventory(self):
        self.window.update() # updates window dimensions
        self.scenes['inventory'] = {}
        self.scenes['inventory']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['inventory']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        self.scenes['inventory']['text1'] = "Your Items\n\n"
        for item in self.inventory:
            self.scenes['inventory']['text1'] = self.scenes['inventory']['text1'] + item + "|"
        self.scenes['inventory']['text_label1'] = tkinter.Label(self.scenes['inventory']['frame'], bg="#1a1a1a", text=self.scenes['inventory']['text1'], fg="#fff", font=("Arial", 16), justify="center")
        self.scenes['inventory']['text_label1'].place(relwidth=0.8, relx=0.1, rely=0.2)
        self.scenes['inventory']['continue_label'] = tkinter.Label(self.scenes['inventory']['frame'], bg="#1a1a1a", text="CLICK HERE TO CLOSE", fg="#fff", font=("Arial", 20))
        self.scenes['inventory']['continue_label'].bind( "<Button>", lambda e:self.open_scene(self.scene_cursor))  
        self.scenes['inventory']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['inventory']['frame'].place_forget()
        self.open_scene("inventory")

    # load all of the location scenes
    def load_destinations(self):
        self.baltimore_creator()
        self.frederick_creator()

    # create baltimore scene
    def baltimore_creator(self):
        self.window.update() # updates window dimensions
        # baltimore menu (scene7)
        random_event_chance = random.randint(1, 10)
        self.scenes['scene7'] = {}
        self.scenes['scene7']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene7']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        self.scenes['scene7']['text1'] = "Welcome to Charm City!\n\n"
        self.scenes['scene7']['text_label1'] = tkinter.Label(self.scenes['scene7']['frame'], bg="#1a1a1a", text=self.scenes['scene7']['text1'], fg="#fff", font=("Arial", 24), justify="center")
        self.scenes['scene7']['text_label1'].pack()
        self.scenes['scene7']['text2'] = "[0]--> Visit National Aquarium\n\n [1]--> Visit Ripley's Museum\n\n [2]-->Explore Inner Harbor\n\n [3]--> Eat at Restaurant (${})\n\n [4]--> Sleep at Hotel (${})\n\n [5]--> Travel to new location".format((len(self.players) + 1) * 17, (len(self.players) + 1) * 80)
        self.scenes['scene7']['text_label2'] = tkinter.Label(self.scenes['scene7']['frame'], bg="#1a1a1a", text=self.scenes['scene7']['text2'], fg="#fff", font=("Arial", 14), justify="left")
        self.scenes['scene7']['text_label2'].pack()
        self.scenes['scene7']['input'] = tkinter.Entry(self.scenes['scene7']['frame'], fg="#fff", bg="#1a1a1a", borderwidth=1, relief="sunken", font=("Arial", 16), justify="center")
        self.scenes['scene7']['input'].place(relx=0.3, rely=0.7, relheight=0.08, relwidth=0.4)
        self.scenes['scene7']['continue_label'] = tkinter.Label(self.scenes['scene7']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene7']['continue_label'].bind( "<Button>", lambda e:self.baltimore_handler(self.scenes['scene7']['input'].get()))  
        self.scenes['scene7']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene7']['frame'].place_forget()
        # scene 7a1: aquarium slideshow (whale shark)
        self.scenes['scene7a1'] = {}
        self.scenes['scene7a1']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene7a1']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/scene7a/aquarium1.jpg")
        self.scenes['scene7a1']["image"] = Image.open(filepath)
        self.scenes['scene7a1']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene7a1']["image"])
        self.scenes['scene7a1']["image_label"] = tkinter.Label(self.scenes['scene7a1']['frame'], image=self.scenes['scene7a1']["image_widget"], borderwidth=0)
        self.scenes['scene7a1']['image_label'].image = self.scenes['scene7a1']["image_widget"]
        self.scenes['scene7a1']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['scene7a1']['continue_label'] = tkinter.Label(self.scenes['scene7a1']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene7a1']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene7a2'))
        self.scenes['scene7a1']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene7a1']['frame'].place_forget()
        # scene 7a2: aquarium slideshow (first turtle)
        self.scenes['scene7a2'] = {}
        self.scenes['scene7a2']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene7a2']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/scene7a/aquarium2.png")
        self.scenes['scene7a2']["image"] = Image.open(filepath)
        self.scenes['scene7a2']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene7a2']["image"])
        self.scenes['scene7a2']["image_label"] = tkinter.Label(self.scenes['scene7a2']['frame'], image=self.scenes['scene7a2']["image_widget"], borderwidth=0)
        self.scenes['scene7a2']['image_label'].image = self.scenes['scene7a2']["image_widget"]
        self.scenes['scene7a2']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['scene7a2']['continue_label'] = tkinter.Label(self.scenes['scene7a2']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene7a2']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene7a3'))
        self.scenes['scene7a2']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene7a2']['frame'].place_forget() 
        # scene 7a3: aquarium slideshow (pufferfish)
        self.scenes['scene7a3'] = {}
        self.scenes['scene7a3']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene7a3']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/scene7a/aquarium3.jpeg")
        self.scenes['scene7a3']["image"] = Image.open(filepath)
        self.scenes['scene7a3']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene7a3']["image"])
        self.scenes['scene7a3']["image_label"] = tkinter.Label(self.scenes['scene7a3']['frame'], image=self.scenes['scene7a3']["image_widget"], borderwidth=0)
        self.scenes['scene7a3']['image_label'].image = self.scenes['scene7a3']["image_widget"]
        self.scenes['scene7a3']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['scene7a3']['continue_label'] = tkinter.Label(self.scenes['scene7a3']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene7a3']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene7a4'))
        self.scenes['scene7a3']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene7a3']['frame'].place_forget() 
        # scene 7a4: aquarium slideshow (turtle 4)
        self.scenes['scene7a4'] = {}
        self.scenes['scene7a4']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene7a4']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/scene7a/aquarium4.png")
        self.scenes['scene7a4']["image"] = Image.open(filepath)
        self.scenes['scene7a4']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene7a4']["image"])
        self.scenes['scene7a4']["image_label"] = tkinter.Label(self.scenes['scene7a4']['frame'], image=self.scenes['scene7a4']["image_widget"], borderwidth=0)
        self.scenes['scene7a4']['image_label'].image = self.scenes['scene7a4']["image_widget"]
        self.scenes['scene7a4']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['scene7a4']['continue_label'] = tkinter.Label(self.scenes['scene7a4']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        if(random_event_chance == 1):
            # (10% chance) slip and fall random event (-2 fun, -2 rest)
            self.scenes['scene7a4']['continue_label'].bind( "<Button>", lambda e:self.random_event_handler("e1", "scene7"))
        else:
            # otherwise, return to baltimore menu
            self.scenes['scene7a4']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene7'))
        self.scenes['scene7a4']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene7a4']['frame'].place_forget() 
        # scene 7b1: believe it or not museum slideshow (whale shark)
        random_event_chance = random.randint(1, 10)
        self.scenes['scene7b1'] = {}
        self.scenes['scene7b1']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene7b1']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/scene7b/1.jpg")
        self.scenes['scene7b1']["image"] = Image.open(filepath)
        self.scenes['scene7b1']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene7b1']["image"])
        self.scenes['scene7b1']["image_label"] = tkinter.Label(self.scenes['scene7b1']['frame'], image=self.scenes['scene7b1']["image_widget"], borderwidth=0)
        self.scenes['scene7b1']['image_label'].image = self.scenes['scene7b1']["image_widget"]
        self.scenes['scene7b1']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['scene7b1']['continue_label'] = tkinter.Label(self.scenes['scene7b1']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene7b1']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene7b2'))
        self.scenes['scene7b1']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene7b1']['frame'].place_forget()
        # scene 7b2: ripley's museum pic 2
        self.scenes['scene7b2'] = {}
        self.scenes['scene7b2']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene7b2']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/scene7b/2.jpg")
        self.scenes['scene7b2']["image"] = Image.open(filepath)
        self.scenes['scene7b2']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene7b2']["image"])
        self.scenes['scene7b2']["image_label"] = tkinter.Label(self.scenes['scene7b2']['frame'], image=self.scenes['scene7b2']["image_widget"], borderwidth=0)
        self.scenes['scene7b2']['image_label'].image = self.scenes['scene7b2']["image_widget"]
        self.scenes['scene7b2']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['scene7b2']['continue_label'] = tkinter.Label(self.scenes['scene7b2']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene7b2']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene7b3'))
        self.scenes['scene7b2']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene7b2']['frame'].place_forget() 
        # scene 7b3: ripley's museum pic 3
        self.scenes['scene7b3'] = {}
        self.scenes['scene7b3']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene7b3']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/scene7b/3.jpg")
        self.scenes['scene7b3']["image"] = Image.open(filepath)
        self.scenes['scene7b3']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene7b3']["image"])
        self.scenes['scene7b3']["image_label"] = tkinter.Label(self.scenes['scene7b3']['frame'], image=self.scenes['scene7b3']["image_widget"], borderwidth=0)
        self.scenes['scene7b3']['image_label'].image = self.scenes['scene7b3']["image_widget"]
        self.scenes['scene7b3']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['scene7b3']['continue_label'] = tkinter.Label(self.scenes['scene7b3']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene7b3']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene7b4'))
        self.scenes['scene7b3']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene7b3']['frame'].place_forget() 
        # scene 7b4: ripley's museum pic 4
        self.scenes['scene7b4'] = {}
        self.scenes['scene7b4']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene7b4']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/scene7b/4.jpg")
        self.scenes['scene7b4']["image"] = Image.open(filepath)
        self.scenes['scene7b4']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene7b4']["image"])
        self.scenes['scene7b4']["image_label"] = tkinter.Label(self.scenes['scene7b4']['frame'], image=self.scenes['scene7b4']["image_widget"], borderwidth=0)
        self.scenes['scene7b4']['image_label'].image = self.scenes['scene7b4']["image_widget"]
        self.scenes['scene7b4']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['scene7b4']['continue_label'] = tkinter.Label(self.scenes['scene7b4']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        if(random_event_chance == 1):
            # (10% chance) slip and fall random event (-2 fun, -2 rest)
            self.scenes['scene7b4']['continue_label'].bind( "<Button>", lambda e:self.random_event_handler("e1", "scene7"))
        else:
            # otherwise, return to baltimore menu
            self.scenes['scene7b4']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene7'))
        self.scenes['scene7b4']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene7b4']['frame'].place_forget() 
        # scene 7c1: explore downtown pic 1
        random_event_chance = random.randint(1, 100)
        self.scenes['scene7c1'] = {}
        self.scenes['scene7c1']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene7c1']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/scene7c/1.jpg")
        self.scenes['scene7c1']["image"] = Image.open(filepath)
        self.scenes['scene7c1']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene7c1']["image"])
        self.scenes['scene7c1']["image_label"] = tkinter.Label(self.scenes['scene7c1']['frame'], image=self.scenes['scene7c1']["image_widget"], borderwidth=0)
        self.scenes['scene7c1']['image_label'].image = self.scenes['scene7c1']["image_widget"]
        self.scenes['scene7c1']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['scene7c1']['continue_label'] = tkinter.Label(self.scenes['scene7c1']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene7c1']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene7c2'))
        self.scenes['scene7c1']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene7c1']['frame'].place_forget()
        # scene 7c2: explore downtown pic 2
        self.scenes['scene7c2'] = {}
        self.scenes['scene7c2']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene7c2']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/scene7c/2.jpg")
        self.scenes['scene7c2']["image"] = Image.open(filepath)
        self.scenes['scene7c2']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene7c2']["image"])
        self.scenes['scene7c2']["image_label"] = tkinter.Label(self.scenes['scene7c2']['frame'], image=self.scenes['scene7c2']["image_widget"], borderwidth=0)
        self.scenes['scene7c2']['image_label'].image = self.scenes['scene7c2']["image_widget"]
        self.scenes['scene7c2']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['scene7c2']['continue_label'] = tkinter.Label(self.scenes['scene7c2']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene7c2']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene7c3'))
        self.scenes['scene7c2']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene7c2']['frame'].place_forget() 
        # scene 7c3: explore downtown pic 3
        self.scenes['scene7c3'] = {}
        self.scenes['scene7c3']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene7c3']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/scene7c/3.jpg")
        self.scenes['scene7c3']["image"] = Image.open(filepath)
        self.scenes['scene7c3']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene7c3']["image"])
        self.scenes['scene7c3']["image_label"] = tkinter.Label(self.scenes['scene7c3']['frame'], image=self.scenes['scene7c3']["image_widget"], borderwidth=0)
        self.scenes['scene7c3']['image_label'].image = self.scenes['scene7c3']["image_widget"]
        self.scenes['scene7c3']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['scene7c3']['continue_label'] = tkinter.Label(self.scenes['scene7c3']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene7c3']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene7c4'))
        self.scenes['scene7c3']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene7c3']['frame'].place_forget() 
        # scene 7c4: downtown pic 4
        self.scenes['scene7c4'] = {}
        self.scenes['scene7c4']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene7c4']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/scene7c/4.jpg")
        self.scenes['scene7c4']["image"] = Image.open(filepath)
        self.scenes['scene7c4']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene7c4']["image"])
        self.scenes['scene7c4']["image_label"] = tkinter.Label(self.scenes['scene7c4']['frame'], image=self.scenes['scene7c4']["image_widget"], borderwidth=0)
        self.scenes['scene7c4']['image_label'].image = self.scenes['scene7c4']["image_widget"]
        self.scenes['scene7c4']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['scene7c4']['continue_label'] = tkinter.Label(self.scenes['scene7c4']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        if(random_event_chance <= 50):
            # (50% chance) "homeless person" random event
            self.scenes['scene7c4']['continue_label'].bind( "<Button>", lambda e:self.random_event_handler("e2", "scene7"))
        elif(random_event_chance <= 5):
            # (5% chance) "robbery" random event
            self.scenes['scene7c4']['continue_label'].bind( "<Button>", lambda e:self.random_event_handler("e3", "scene7"))
        elif(random_event_chance <= 20):
            # (20% chance) "heavy rain" random event
            self.scenes['scene7c4']['continue_label'].bind( "<Button>", lambda e:self.random_event_handler("e4","scene7"))
        else:
            # otherwise, return to baltimore menu
            self.scenes['scene7c4']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene7'))
        self.scenes['scene7c4']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene7c4']['frame'].place_forget() 

    def baltimore_handler(self, num):
        if(num == '0'):
            # visit national aquarium (+5 fun, -2 rest, -3 time, -4 hunger) ; show slideshow (scenes 7a(1-4))
            if("scene7a1" not in self.visited_scenes):
                self.stats["fun"] += 5
                self.stats["rest"] -= 2
                self.stats["time"] -= 3
                self.stats["hunger"] -= 4
                self.visited_scenes.append("scene7a1")
                self.open_scene("scene7a1")
            else:
                messagebox.showinfo("Oops!", "You've already visited this location!\n\nPlease select a different option.")
        elif(num == '1'):
            # visit ripley's museum (+5 fun, -2 rest, -3 time, -4 hunger) ; show slideshow (scenes 7b(1-4))
            if("scene7b1" not in self.visited_scenes):
                self.stats["fun"] += 5
                self.stats["rest"] -= 2
                self.stats["time"] -= 3
                self.stats["hunger"] -= 4
                self.visited_scenes.append("scene7b1")
                self.open_scene("scene7b1")
            else:
                messagebox.showinfo("Oops!", "You've already visited this location!\n\nPlease select a different option.")
        elif(num == '2'):
            # explore downtown (+10 fun, -5 rest, -3 time, -6 hunger) ; show slideshow (scenes 7c(1-4))
            if("scene7c1" not in self.visited_scenes):
                self.stats["fun"] += 10
                self.stats["rest"] -= 5
                self.stats["time"] -= 3
                self.stats["hunger"] -= 6
                self.visited_scenes.append("scene7c1")
                self.open_scene("scene7c1")
            else:
                messagebox.showinfo("Oops!", "You've already visited this location!\n\nPlease select a different option.")
        elif(num == '3'):
            # eat at restaurant in baltimore
            if(self.stats["money"] - (len(self.players) + 1) * 17 > 0):
                self.stats["hunger"] += 10
                self.stats["money"] -= (len(self.players) + 1) * 17
                messagebox.showinfo("Bon appetit!", "Enjoy your meal.\n\n(+ 10 hunger)")
            else:
                msgbox = messagebox.showinfo("Oh no!", "You don't have enough money for this!")
        elif(num == '4'):
            # sleep at hotel in baltimore
            if(self.stats["money"] - (len(self.players) + 1) * 80 > 0):
                self.stats["hunger"] += 10
                self.stats["rest"] += 10
                self.stats["time"] -= 10
                self.stats["money"] -= (len(self.players) + 1) * 80
                messagebox.showinfo("Lord Hotel", "Enjoy your stay at the Lord Hotel.\n\n(+ 10 rest, +10 hunger, -10 time)")
            else:
                msgbox = messagebox.askquestion("Oh no!", "You don't have enough money for this!\n\nWould you like to sleep in your car instead?")
                if(msgbox == 'yes'):
                    self.stats["rest"] += 3
                    self.stats["time"] -= 10
                    messagebox.showinfo("Sweet Dreams!", "It's not ideal, but it gets the job done!\n\n(+ 3 rest, -10 time)")

        elif(num == '5'):
            # travel to new location
            self.travel_menu("0")    
        self.update_stats()


  # create frederick scene
    def frederick_creator(self):
        self.window.update() # updates window dimensions
        # frederick menu (scene8)
        random_event_chance = random.randint(1, 100)
        self.scenes['scene8'] = {}
        self.scenes['scene8']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene8']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        self.scenes['scene8']['text1'] = "Welcome to the City of Clustered Spires!\n\n"
        self.scenes['scene8']['text_label1'] = tkinter.Label(self.scenes['scene8']['frame'], bg="#1a1a1a", text=self.scenes['scene8']['text1'], fg="#fff", font=("Arial", 24), justify="center")
        self.scenes['scene8']['text_label1'].pack()
        self.scenes['scene8']['text2'] = "[0]--> Explore Downtown Frederick\n\n [1]--> Visit Sugarloaf Mountain\n\n [2]--> Visit Catoctin Mountain Park\n\n [3]-->Visit Farmer's Market\n\n [4]--> Travel to new location"
        self.scenes['scene8']['text_label2'] = tkinter.Label(self.scenes['scene8']['frame'], bg="#1a1a1a", text=self.scenes['scene8']['text2'], fg="#fff", font=("Arial", 14), justify="left")
        self.scenes['scene8']['text_label2'].pack()
        self.scenes['scene8']['input'] = tkinter.Entry(self.scenes['scene8']['frame'], fg="#fff", bg="#1a1a1a", borderwidth=1, relief="sunken", font=("Arial", 16), justify="center")
        self.scenes['scene8']['input'].place(relx=0.3, rely=0.7, relheight=0.08, relwidth=0.4)
        self.scenes['scene8']['continue_label'] = tkinter.Label(self.scenes['scene8']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene8']['continue_label'].bind( "<Button>", lambda e:self.frederick_handler(self.scenes['scene8']['input'].get()))  
        self.scenes['scene8']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene8']['frame'].place_forget()
        # scene 8a1: downtown frederick 1
        self.scenes['scene8a1'] = {}
        self.scenes['scene8a1']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene8a1']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/scene8a/1.jpg")
        self.scenes['scene8a1']["image"] = Image.open(filepath)
        self.scenes['scene8a1']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene8a1']["image"])
        self.scenes['scene8a1']["image_label"] = tkinter.Label(self.scenes['scene8a1']['frame'], image=self.scenes['scene8a1']["image_widget"], borderwidth=0)
        self.scenes['scene8a1']['image_label'].image = self.scenes['scene8a1']["image_widget"]
        self.scenes['scene8a1']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['scene8a1']['continue_label'] = tkinter.Label(self.scenes['scene8a1']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene8a1']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene8a2'))
        self.scenes['scene8a1']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene8a1']['frame'].place_forget()
        # scene 8a2: downtown frederick 2
        self.scenes['scene8a2'] = {}
        self.scenes['scene8a2']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene8a2']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/scene8a/2.jpg")
        self.scenes['scene8a2']["image"] = Image.open(filepath)
        self.scenes['scene8a2']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene8a2']["image"])
        self.scenes['scene8a2']["image_label"] = tkinter.Label(self.scenes['scene8a2']['frame'], image=self.scenes['scene8a2']["image_widget"], borderwidth=0)
        self.scenes['scene8a2']['image_label'].image = self.scenes['scene8a2']["image_widget"]
        self.scenes['scene8a2']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['scene8a2']['continue_label'] = tkinter.Label(self.scenes['scene8a2']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene8a2']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene8a3'))
        self.scenes['scene8a2']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene8a2']['frame'].place_forget() 
        # scene 8a3: downtown frederick 3
        self.scenes['scene8a3'] = {}
        self.scenes['scene8a3']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene8a3']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/scene8a/3.jpg")
        self.scenes['scene8a3']["image"] = Image.open(filepath)
        self.scenes['scene8a3']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene8a3']["image"])
        self.scenes['scene8a3']["image_label"] = tkinter.Label(self.scenes['scene8a3']['frame'], image=self.scenes['scene8a3']["image_widget"], borderwidth=0)
        self.scenes['scene8a3']['image_label'].image = self.scenes['scene8a3']["image_widget"]
        self.scenes['scene8a3']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['scene8a3']['continue_label'] = tkinter.Label(self.scenes['scene8a3']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        self.scenes['scene8a3']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene8a4'))
        self.scenes['scene8a3']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene8a3']['frame'].place_forget() 
        # scene 8a4: downtown frederick 4
        self.scenes['scene8a4'] = {}
        self.scenes['scene8a4']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        self.scenes['scene8a4']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(current_dir, "../bin/images/scene8a/4.jpg")
        self.scenes['scene8a4']["image"] = Image.open(filepath)
        self.scenes['scene8a4']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene8a4']["image"])
        self.scenes['scene8a4']["image_label"] = tkinter.Label(self.scenes['scene8a4']['frame'], image=self.scenes['scene8a4']["image_widget"], borderwidth=0)
        self.scenes['scene8a4']['image_label'].image = self.scenes['scene8a4']["image_widget"]
        self.scenes['scene8a4']['image_label'].place(relx=0.02, rely=0.02)
        self.scenes['scene8a4']['continue_label'] = tkinter.Label(self.scenes['scene8a4']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        if(random_event_chance <= 5):
            # (5% chance) robbery random event
            self.scenes['scene8a4']['continue_label'].bind( "<Button>", lambda e:self.random_event_handler("e3", "scene8"))
        elif(random_event_chance <= 20 and random_event_chance > 5):
            # (15% chance) homeless person random event
            self.scenes['scene8a4']['continue_label'].bind( "<Button>", lambda e:self.random_event_handler("e2", "scene8"))
        elif(random_event_chance <= 20 and random_event_chance > 5):
            # (20% chance) heavy rain random event
            self.scenes['scene8a4']['continue_label'].bind( "<Button>", lambda e:self.random_event_handler("e4", "scene8"))
        else:
            # otherwise, return to frederick menu
            self.scenes['scene8a4']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene8'))
        self.scenes['scene8a4']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        self.scenes['scene8a4']['frame'].place_forget() 
        ## scene 8b1: sugarloaf mountain pic 1
        #random_event_chance = random.randint(1, 10)
        #self.scenes['scene8b1'] = {}
        #self.scenes['scene8b1']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        #self.scenes['scene8b1']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        #current_dir = os.path.abspath(os.path.dirname(__file__))
        #filepath = os.path.join(current_dir, "../bin/images/scene8b/1.jpg")
        #self.scenes['scene8b1']["image"] = Image.open(filepath)
        #self.scenes['scene8b1']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene8b1']["image"])
        #self.scenes['scene8b1']["image_label"] = tkinter.Label(self.scenes['scene8b1']['frame'], image=self.scenes['scene8b1']["image_widget"], borderwidth=0)
        #self.scenes['scene8b1']['image_label'].image = self.scenes['scene8b1']["image_widget"]
        #self.scenes['scene8b1']['image_label'].place(relx=0.02, rely=0.02)
        #self.scenes['scene8b1']['continue_label'] = tkinter.Label(self.scenes['scene8b1']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        #self.scenes['scene8b1']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene8b2'))
        #self.scenes['scene8b1']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        #self.scenes['scene8b1']['frame'].place_forget()
        ## scene 8b2: sugarloaf mountain pic 2
        #self.scenes['scene8b2'] = {}
        #self.scenes['scene8b2']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        #self.scenes['scene8b2']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        #current_dir = os.path.abspath(os.path.dirname(__file__))
        #filepath = os.path.join(current_dir, "../bin/images/scene8b/2.jpg")
        #self.scenes['scene8b2']["image"] = Image.open(filepath)
        #self.scenes['scene8b2']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene8b2']["image"])
        #self.scenes['scene8b2']["image_label"] = tkinter.Label(self.scenes['scene8b2']['frame'], image=self.scenes['scene8b2']["image_widget"], borderwidth=0)
        #self.scenes['scene8b2']['image_label'].image = self.scenes['scene8b2']["image_widget"]
        #self.scenes['scene8b2']['image_label'].place(relx=0.02, rely=0.02)
        #self.scenes['scene8b2']['continue_label'] = tkinter.Label(self.scenes['scene8b2']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        #self.scenes['scene8b2']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene8b3'))
        #self.scenes['scene8b2']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        #self.scenes['scene8b2']['frame'].place_forget() 
        ## scene 8b3: sugarloaf mountain pic 3
        #self.scenes['scene8b3'] = {}
        #self.scenes['scene8b3']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        #self.scenes['scene8b3']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        #current_dir = os.path.abspath(os.path.dirname(__file__))
        #filepath = os.path.join(current_dir, "../bin/images/scene8b/3.jpg")
        #self.scenes['scene8b3']["image"] = Image.open(filepath)
        #self.scenes['scene8b3']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene8b3']["image"])
        #self.scenes['scene8b3']["image_label"] = tkinter.Label(self.scenes['scene8b3']['frame'], image=self.scenes['scene8b3']["image_widget"], borderwidth=0)
        #self.scenes['scene8b3']['image_label'].image = self.scenes['scene8b3']["image_widget"]
        #self.scenes['scene8b3']['image_label'].place(relx=0.02, rely=0.02)
        #self.scenes['scene8b3']['continue_label'] = tkinter.Label(self.scenes['scene8b3']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        #self.scenes['scene8b3']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene8b4'))
        #self.scenes['scene8b3']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        #self.scenes['scene8b3']['frame'].place_forget() 
        ## scene 7b4: sugarloaf mountain pic 4
        #self.scenes['scene8b4'] = {}
        #self.scenes['scene8b4']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        #self.scenes['scene8b4']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        #current_dir = os.path.abspath(os.path.dirname(__file__))
        #filepath = os.path.join(current_dir, "../bin/images/scene8b/4.jpg")
        #self.scenes['scene8b4']["image"] = Image.open(filepath)
        #self.scenes['scene8b4']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene8b4']["image"])
        #self.scenes['scene8b4']["image_label"] = tkinter.Label(self.scenes['scene8b4']['frame'], image=self.scenes['scene8b4']["image_widget"], borderwidth=0)
        #self.scenes['scene8b4']['image_label'].image = self.scenes['scene8b4']["image_widget"]
        #self.scenes['scene8b4']['image_label'].place(relx=0.02, rely=0.02)
        #self.scenes['scene8b4']['continue_label'] = tkinter.Label(self.scenes['scene8b4']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        #if(random_event_chance == 1):
        #    # if random event chance occurs (only if equal to 1), show "slip and fall" message (-2 fun, -2 rest)
        #    self.scenes['scene8b4']['continue_label'].bind( "<Button>", lambda e:self.frederick_handler("e1"))
        #else:
        #    # otherwise, return to frederick menu
        #    self.scenes['scene8b4']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene8'))
        #self.scenes['scene8b4']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        #self.scenes['scene8b4']['frame'].place_forget() 
        ## scene 8c1: explore downtown pic 1
        #random_event_chance = random.randint(1, 10)
        #self.scenes['scene8c1'] = {}
        #self.scenes['scene8c1']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        #self.scenes['scene8c1']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        #current_dir = os.path.abspath(os.path.dirname(__file__))
        #filepath = os.path.join(current_dir, "../bin/images/scene8c/1.jpg")
        #self.scenes['scene8c1']["image"] = Image.open(filepath)
        #self.scenes['scene8c1']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene8c1']["image"])
        #self.scenes['scene8c1']["image_label"] = tkinter.Label(self.scenes['scene8c1']['frame'], image=self.scenes['scene8c1']["image_widget"], borderwidth=0)
        #self.scenes['scene8c1']['image_label'].image = self.scenes['scene8c1']["image_widget"]
        #self.scenes['scene8c1']['image_label'].place(relx=0.02, rely=0.02)
        #self.scenes['scene8c1']['continue_label'] = tkinter.Label(self.scenes['scene8c1']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        #self.scenes['scene8c1']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene8c2'))
        #self.scenes['scene8c1']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        #self.scenes['scene8c1']['frame'].place_forget()
        ## scene 7c2: explore downtown pic 2
        #self.scenes['scene8c2'] = {}
        #self.scenes['scene8c2']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        #self.scenes['scene8c2']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        #current_dir = os.path.abspath(os.path.dirname(__file__))
        #filepath = os.path.join(current_dir, "../bin/images/scene8c/2.jpg")
        #self.scenes['scene8c2']["image"] = Image.open(filepath)
        #self.scenes['scene8c2']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene8c2']["image"])
        #self.scenes['scene8c2']["image_label"] = tkinter.Label(self.scenes['scene8c2']['frame'], image=self.scenes['scene8c2']["image_widget"], borderwidth=0)
        #self.scenes['scene8c2']['image_label'].image = self.scenes['scene8c2']["image_widget"]
        #self.scenes['scene8c2']['image_label'].place(relx=0.02, rely=0.02)
        #self.scenes['scene8c2']['continue_label'] = tkinter.Label(self.scenes['scene8c2']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        #self.scenes['scene8c2']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene8c3'))
        #self.scenes['scene8c2']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        #self.scenes['scene8c2']['frame'].place_forget() 
        ## scene 7c3: explore downtown pic 3
        #self.scenes['scene8c3'] = {}
        #self.scenes['scene8c3']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        #self.scenes['scene8c3']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        #current_dir = os.path.abspath(os.path.dirname(__file__))
        #filepath = os.path.join(current_dir, "../bin/images/scene8c/3.jpg")
        #self.scenes['scene8c3']["image"] = Image.open(filepath)
        #self.scenes['scene8c3']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene8c3']["image"])
        #self.scenes['scene8c3']["image_label"] = tkinter.Label(self.scenes['scene8c3']['frame'], image=self.scenes['scene8c3']["image_widget"], borderwidth=0)
        #self.scenes['scene8c3']['image_label'].image = self.scenes['scene8c3']["image_widget"]
        #self.scenes['scene8c3']['image_label'].place(relx=0.02, rely=0.02)
        #self.scenes['scene8c3']['continue_label'] = tkinter.Label(self.scenes['scene8c3']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        #self.scenes['scene8c3']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene8c4'))
        #self.scenes['scene8c3']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        #self.scenes['scene8c3']['frame'].place_forget() 
        ## scene 7c4: downtown pic 4
        #self.scenes['scene8c4'] = {}
        #self.scenes['scene8c4']['frame'] = tkinter.Frame(self.dynamic_frame, bg="#1a1a1a")
        #self.scenes['scene8c4']['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9)
        #current_dir = os.path.abspath(os.path.dirname(__file__))
        #filepath = os.path.join(current_dir, "../bin/images/scene8c/4.jpg")
        #self.scenes['scene8c4']["image"] = Image.open(filepath)
        #self.scenes['scene8c4']["image_widget"] = ImageTk.PhotoImage(self.scenes['scene8c4']["image"])
        #self.scenes['scene8c4']["image_label"] = tkinter.Label(self.scenes['scene8c4']['frame'], image=self.scenes['scene8c4']["image_widget"], borderwidth=0)
        #self.scenes['scene8c4']['image_label'].image = self.scenes['scene8c4']["image_widget"]
        #self.scenes['scene8c4']['image_label'].place(relx=0.02, rely=0.02)
        #self.scenes['scene8c4']['continue_label'] = tkinter.Label(self.scenes['scene8c4']['frame'], bg="#1a1a1a", text="CLICK HERE TO CONTINUE", fg="#fff", font=("Arial", 20))
        #if(random_event_chance == 1):
        #    # if random event chance occurs (only if equal to 1), show "slip and fall" message (-2 fun, -2 rest)
        #    self.scenes['scene8c4']['continue_label'].bind( "<Button>", lambda e:self.frederick_handler("e1"))
        #else:
        #    # otherwise, return to frederick menu
        #    self.scenes['scene8c4']['continue_label'].bind( "<Button>", lambda e:self.open_scene('scene8'))
        #self.scenes['scene8c4']['continue_label'].place(relx=.15, rely=.9, relwidth=.7)
        #self.scenes['scene8c4']['frame'].place_forget() 

    def frederick_handler(self, num):
        if(num == '0'):
            # explore downtown frederick (+5 fun, -2 rest, -3 time, -4 hunger) ; show slideshow (scenes 7a(1-4))
            if("scene8a1" not in self.visited_scenes):
                self.stats["fun"] += 5
                self.stats["rest"] -= 2
                self.stats["time"] -= 3
                self.stats["hunger"] -= 4
                self.visited_scenes.append("scene8a1")
                self.open_scene("scene8a1")
            else:
                messagebox.showinfo("Oops!", "You've already visited this location!\n\nPlease select a different option.")
        elif(num == '1'):
            # visit ripley's museum (+5 fun, -2 rest, -3 time, -4 hunger) ; show slideshow (scenes 7b(1-4))
            if("scene7b1" not in self.visited_scenes):
                self.stats["fun"] += 5
                self.stats["rest"] -= 2
                self.stats["time"] -= 3
                self.stats["hunger"] -= 4
                self.visited_scenes.append("scene7b1")
                self.open_scene("scene7b1")
            else:
                messagebox.showinfo("Oops!", "You've already visited this location!\n\nPlease select a different option.")
        elif(num == '2'):
            # explore downtown (+10 fun, -5 rest, -3 time, -6 hunger) ; show slideshow (scenes 7c(1-4))
            if("scene7c1" not in self.visited_scenes):
                self.stats["fun"] += 10
                self.stats["rest"] -= 5
                self.stats["time"] -= 3
                self.stats["hunger"] -= 6
                self.visited_scenes.append("scene7c1")
                self.open_scene("scene7c1")
            else:
                messagebox.showinfo("Oops!", "You've already visited this location!\n\nPlease select a different option.")
        elif(num == '3'):
            # eat at restaurant in baltimore
            if(self.stats["money"] - (len(self.players) + 1) * 17 > 0):
                self.stats["hunger"] += 10
                self.stats["money"] -= (len(self.players) + 1) * 17
                messagebox.showinfo("Bon appetit!", "Enjoy your meal.\n\n(+ 10 hunger)")
            else:
                msgbox = messagebox.showinfo("Oh no!", "You don't have enough money for this!")
        elif(num == '4'):
            # sleep at hotel in baltimore
            if(self.stats["money"] - (len(self.players) + 1) * 80 > 0):
                self.stats["hunger"] += 10
                self.stats["rest"] += 10
                self.stats["time"] -= 10
                self.stats["money"] -= (len(self.players) + 1) * 80
                messagebox.showinfo("Lord Hotel", "Enjoy your stay at the Lord Hotel.\n\n(+ 10 rest, +10 hunger, -10 time)")
            else:
                msgbox = messagebox.askquestion("Oh no!", "You don't have enough money for this!\n\nWould you like to sleep in your car instead?")
                if(msgbox == 'yes'):
                    self.stats["rest"] += 3
                    self.stats["time"] -= 10
                    messagebox.showinfo("Sweet Dreams!", "It's not ideal, but it gets the job done!\n\n(+ 3 rest, -10 time)")

        elif(num == '5'):
            # travel to new location
            self.travel_menu("0")     
        self.update_stats()

    # random event handler
    def random_event_handler(self, code, redirect_scene):
        if(code == 'e1'):
            # random event scene: slip and fall (-2 fun, -2 energy)
            self.stats["fun"] -= 2
            self.stats["rest"] -= 2
            messagebox.showinfo("Oh no!", "You slipped on the fell outside an exhibit!\n\n(-2 fun, -2 rest)")
        elif(code == 'e2'):
            # random event scene: asked for money by homeless person
            if(self.stats["money"] - 20 >= 0):
                msgbox = messagebox.askquestion("Hello!", "A homeless person has approached you and asked for some money\nCan you spare $20?")
                if(msgbox == "yes"):
                    # if you give him your money, continue
                    self.stats["money"] -= 20
                else:
                    # if not, 10% chance they attack you
                    if(random.randint(1, 10) == 1):
                        if("Pepper Spray" in self.invetory):
                            # if pepper spray in inventory, reduce fun penalty
                            messagebox.showinfo("Oh no!", "The homeless person attacked you, but you used your pepper spray\n\n(5- fun)")
                            self.stats["fun"] -= 5
                        else:
                            # otherwise, incur harsher fun penalty plus energy
                            # penalty
                            messagebox.showinfo("Oh no!", "The homeless person attacked you!\n\n(-10 fun, -2 rest)")
                            self.stats["fun"] -= 10
                            self.stats["rest"] -= 2
            else:
                # if user is broke, 10% chance they attack you
                if(random.randint(1, 10) == 1):
                    if("Pepper Spray" in self.invetory):
                        # if pepper spray in inventory, reduce fun penalty
                        messagebox.showinfo("Oh no!", "A homeless person has approached you and asked for some money\nCan you spare $20?\n\n(You're broke, so you must say no)\n\nHowever, the homeless person attacked you, but you used your pepper spray\n\n(5- fun)")
                        self.stats["fun"] -= 5
                    else:
                        # otherwise, incur harsher fun penalty plus energy penalty
                        messagebox.showinfo("Oh no!", "A homeless person has approached you and asked for some money\nCan you spare $20?\n\n(You're broke, so you must say no)\n\nHowever, the homeless person attacked you!\n\n(-10 fun, -2 rest)")
                        self.stats["fun"] -= 10
                        self.stats["rest"] -= 2
        elif(code == "e3"):
            # random event scene: robbery 
            # w/o pepper spray: (-20 fun, -5 rest, -15% of money)
            # w/ pepper spray: (-10 fun)
            if("Pepper Spray" in self.invetory):
                # if pepper spray in inventory, reduce fun penalty
                messagebox.showinfo("Oh no!", "You wandered into the wrong neighborhood and were robbed!\n\nLuckily, you used pepper spray to fend off the perpetrators!\n\n(-10 fun)")
                self.stats["fun"] -= 10
            else:
                # otherwise, incur harsher fun penalty plus energy and money penalty
                messagebox.showinfo("Oh no!", "You wandered into the wrong neighborhood and were robbed!\n\nLuckily, you used pepper spray to fend off the perpetrators!\n\nThey took ${}!\n\n(-20 fun, -5 rest)".format(math.floor(self.stats["money"] * 15)))
                self.stats["fun"] -= 20
                self.stats["rest"] -= 5
                self.stats["money"] -= math.floor(self.stats["money"] * 15)
        elif(code == "e4"):
            # random event scene: heavy rain
            # w/o rain jacket: (-2 fun)
            # w/ rain jacket: (-5 fun, -2 rest)
            if("Raincoat" in self.invetory):
                # if rain jacket in inventory, reduce fun penalty
                messagebox.showinfo("Oh no!", "A sudden rainstorm appeared out of nowhere!\n\nYou put on your raincoat and countinued exploring in the rain!(-2 fun)")
                self.stats["fun"] -= 2
            else:
                # otherwise, incur harsher fun penalty plus energy and money penalty
                messagebox.showinfo("Oh no!", "A sudden rainstorm appeared out of nowhere!\n\n(-5 fun, -2 rest)")
                self.stats["fun"] -= 5
                self.stats["rest"] -= 2
        self.open_scene(redirect_scene)
        self.random_events_experienced.append(code)     
        self.update_stats()

    # navigate to page
    def open_scene(self, scene_to_open):
        scene_cursor = scene_to_open
        self.hide_frames()
        self.scenes[scene_to_open]['frame'].place(relx=0.1, rely=0.1, relwidth=0.8, relheight=.9) 

    # close window
    def close(self):
        self.window.destroy()

    # hide all pages during navigation
    def hide_frames(self):
        for scene in self.scenes:
            self.scenes[scene]['frame'].place_forget()