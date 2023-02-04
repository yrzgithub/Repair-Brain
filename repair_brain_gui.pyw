from tkinter import *
from PIL import Image
from PIL.ImageTk import PhotoImage
from pickle import load,dump 
from datetime import datetime
from os.path import isfile,expanduser,getsize,isdir
from os import listdir,system,remove,mkdir
from threading import Thread
from time import sleep
from random import choice
from tkinter.filedialog import askopenfilenames
from shutil import copy
from winsound import MessageBeep
from easygui import msgbox
from webbrowser import open_new_tab
import pyperclip
import vlc


box_titile = "Repair Brain"
screen_name = "Repair Brain"

key_lastly_opened = "lastly_opened"
key_lastly_relapsed = "lastly_relapsed"
key_lastly_noted_change = "lastly_noted_change"
key_lastly_noted_side_effect = "lastly_noted_side_effect"
key_start_time = "start_time"
key_next_step = "next_step"

file_name = "pkls\\data.pkl"
icon_name = "icon\\favicon.ico"
txt_file_path = "text\\data_txt.txt"
txt_changes = "text\\changes.txt"
txt_effects = "text\\effects.txt"
txt_next_step = "text\\next_step.txt"

bgm_folder = "bgm"

contact_data = {"Instagram":"https://www.instagram.com/alpha_yr/","Linked In":"https://www.linkedin.com/in/sanjay-kumar-y-r-6a88b6207","Github":"https://github.com/yrzgithub","FaceBook":"https://www.facebook.com/y.r.kumar.1232"}
git_link = "https://github.com/yrzgithub/Repair-Brain"
yt_coding_channel_link = "https://www.youtube.com/channel/UCPOkSZ7GGwgVjVQqP2MjviA"
yt_personal_channel = "https://www.youtube.com/channel/UC6wZDLRN5RPimxqIdoR6g_g"
developer_mail = "seenusanjay20102002@gmail.com"

message_format = "Time gone : {diff_days} days {diff_hours} hours {diff_minutes} min {diff_seconds} sec"


bgms = listdir(bgm_folder)
bgm = choice(bgms)

print("Selected BGM : ",bgm)

dir_list = ("pkls","text")
for dir in dir_list:
    if not isdir(dir):
        mkdir(dir)
        print(dir," created")

vlc_instane = vlc.Instance()
player = vlc_instane.media_player_new()
media = vlc_instane.media_new(f"bgm\\{bgm}")
player.set_media(media)


MessageBeep()

root = Tk()
root.wm_minsize(600,450)
root.wm_iconbitmap(bitmap=icon_name)
root.wm_title(box_titile)

free_img = Image.open(fp="images\\free.jpg").resize(size=(230,230))
free_img = PhotoImage(image=free_img)

hand_cuffed_img = Image.open(fp="images\\hand_cuffed.jpg").resize(size=(230,230))
hand_cuffed_img = PhotoImage(image=hand_cuffed_img)

top_string = StringVar()
top_string.set("Are you Free or Addicted?")

edit_button_var = StringVar()
done_button_var = StringVar()


def time_manager():
    start_time = data[key_start_time]
    root_exists = True
    while root_exists:
        time_now = datetime.now()
        diff = time_now - start_time
        diff_days = diff.days
        diff_seconds = diff.total_seconds()
        diff_hours = int(diff_seconds//3600) % 24
        hours_float = diff_seconds % 3600
        diff_minutes = int(hours_float//60)
        diff_seconds = int(hours_float%60)
        print("thread running")
        message = message_format.format(diff_days=diff_days,diff_hours=diff_hours,diff_minutes=diff_minutes,diff_seconds=diff_seconds)
        try:
            root_exists = root.winfo_exists()
            top_string.set(message)
        except:
            break
        sleep(1)


def data_file(mode="rb",path=file_name,to_write=None):
    out = None
    with open(path,mode) as file:
        if mode=="rb":
            out = load(file)
        elif mode == "wb":
            dump(to_write,file)
        elif mode=="r":
            out = file.read()
        else:
            file.write(to_write)
        file.close()
    return out


def next():
    global lastly_relapsed_label,lastly_noted_change_label,lastly_noted_side_effect_label

    relapsed_button.destroy()
    no_button.destroy()

    lastly_relapsed = data[key_lastly_relapsed]
    last_change = data[key_lastly_noted_change]
    last_side_effect = data[key_lastly_noted_side_effect]
    next_step = data[key_next_step]

    lastly_relapsed_format = "Not Found"
    if type(lastly_relapsed) == datetime:lastly_relapsed_format = lastly_relapsed.strftime("%d:%m:%y")

    top.config(font=("Times New Roman",19),justify=LEFT)
    top.place(relx=.5,rely=.08,anchor=CENTER)

    lastly_relapsed_label = Label(text=f"Lastly relapsed : {lastly_relapsed_format}",font=("Times New Roman",18),anchor=CENTER)
    lastly_relapsed_label.place(relx=.5,rely=.18,anchor=CENTER)

    next_step = Label(text=f"Next Step : {next_step}",font=("Times New Roman",18),anchor=CENTER)
    next_step.place(relx=.5,rely=.28,anchor=CENTER)

    lastly_noted_change_label = Label(text=f"Lastly noted + ve effect : {last_change}",font=("Times New Roman",18),anchor=CENTER)
    lastly_noted_change_label.place(relx=.5,rely=.37,anchor=CENTER)

    lastly_noted_side_effect_label = Label(text=f"Lastly noted side effect : {last_side_effect}",font=("Times New Roman",18),anchor=CENTER)
    lastly_noted_side_effect_label.place(relx=.5,rely=.47,anchor=CENTER)

    change_entry.place(relx=.28,rely=.6,anchor=CENTER,relwidth=.4,relheight=.08)
    side_effect_entry.place(relx=.72,rely=.6,anchor=CENTER,relwidth=.4,relheight=.08)

    next_step_entry.place(relx=.5,rely=.73,anchor=CENTER,relwidth=.7,relheight=.08)

    show_changes_side_effects.place(relx=.37,rely=.88,anchor=CENTER,relwidth=.155,relheight=.09)
    ok_button.place(relx=.63,rely=.88,anchor=CENTER,relwidth=.155,relheight=.09)


def relaped_click():   # addicted
    data[key_lastly_relapsed] = data[key_start_time] = data[key_lastly_opened] = datetime.now()
    next()
    time_manager_thread = Thread(target=time_manager)
    time_manager_thread.start()


def no_button_click():   # free
    root.bind("<space>",stop_player)
    player.play()
    next()
    time_manager_thread = Thread(target=time_manager)
    time_manager_thread.start()


def save_current_effect_change_data():
    side_effect = side_effect_entry.get().strip()
    change = change_entry.get().strip()
    next_step = next_step_entry.get().strip()
    if side_effect != "Enter the side effect" and side_effect!="" and not side_effect.isspace(): 
        data[key_lastly_noted_side_effect] =  side_effect
        side_effect += time_now.strftime(" (%d : %m : %y)")
        data_file(mode="a",path=txt_effects,to_write = f"* {side_effect}\n")

    if change != "Enter the positive effect" and change!="" and not change.isspace(): 
        data[key_lastly_noted_change] = change
        change += time_now.strftime(" (%d : %m : %y)")
        data_file(mode="a",path=txt_changes,to_write = f"* {change}\n")
        
    if next_step != "Enter the next step" and next_step!="" and not next_step.isspace():
        data[key_next_step] = next_step
        next_step += time_now.strftime(" (%d : %m : %y)")
        data_file(mode="a",path=txt_next_step,to_write=f"* {next_step}\n")


def show_changes_side_effects_click(destroy=True):
    global next_steps,effects,changes,edit_button,text_widget,done_button

    player.stop()
    root.unbind(stop_player)

    if destroy:
        save_current_effect_change_data()

        top.destroy()
        lastly_relapsed_label.destroy()
        lastly_noted_change_label.destroy()
        lastly_noted_side_effect_label.destroy()
        change_entry.destroy()
        side_effect_entry.destroy()
        ok_button.destroy()
        show_changes_side_effects.destroy()

    edit_button_var.set("Edit")
    done_button_var.set("Done")
    
    edit_button = Button(textvariable=edit_button_var,command = lambda : edit_steps(),font=("Times New Roman",18,"bold"),cursor="hand2",background="blue",foreground="white",activeforeground="white",activebackground="blue")
    edit_button.place(relx=.4,anchor=CENTER,rely=.95,relheight=.08)

    done_button = Button(textvariable=done_button_var,command = lambda : on_window_close(),font=("Times New Roman",18,"bold"),cursor="hand2",background="blue",foreground="white",activeforeground="white",activebackground="blue")
    done_button.place(relx=.6,anchor=CENTER,rely=.95,relheight=.08)

    next_steps = data_file(mode="r",path=txt_next_step).replace("\n","\n   ")
    effects = data_file(mode="r",path=txt_effects).replace("\n","\n   ")
    changes = data_file(mode="r",path=txt_changes).replace("\n","\n   ")

    txt_format = f" Next Step :\n\n   {next_steps}\n\n\n Positive Effects :\n\n   {changes}\n\n\n Side Effects :\n\n   {effects}"
    text_widget = Text(font=("Times New Roman",20),padx=5,pady=5)
    text_widget.insert(END,txt_format)
    text_widget.configure(state=DISABLED)
    text_widget.place(relheight=.9,relwidth=1)


def edit_steps():
    # save_button = Button(text="Save",font=("Times New Roman",18,"bold"),cursor="hand2",background="blue",foreground="white",activeforeground="white",activebackground="blue")
    done_button_var.set("Next")
    edit_button_var.set("Save")
    text_widget.bind("<Button-1>",func=lambda e : edit_button_var.set("Save"))
    text_widget.configure(state=NORMAL)
    text_widget.delete(1.0,END)
    text_widget.insert(END,f" Next Step :\n\n   {next_steps}")
    edit_button.configure(command = lambda : save_txt(txt_next_step))
    done_button.configure(command = lambda : edit_changes())


def edit_changes():
    done_button_var.set("Next")
    edit_button_var.set("Save")
    text_widget.delete(1.0,END)
    text_widget.insert(END,f" Positive Effects :\n\n   {changes}")
    edit_button.configure(command = lambda : save_txt(txt_changes))
    done_button.configure(command = lambda : edit_effects())


def edit_effects():
    done_button_var.set("Next")
    edit_button_var.set("Save")
    text_widget.delete(1.0,END)
    text_widget.insert(END,f" Side Effects :\n\n   {effects}")
    done_button_var.set("Done")
    done_button.configure(command = lambda :on_window_close())
    edit_button.configure(command=lambda : save_txt(txt_effects))


def save_txt(file_name):
    widget_data = text_widget.get(2.0,END).strip("\n").strip()
    print("Widget data : ",widget_data)
    if not widget_data.isspace() and widget_data!="":
        txt_data = widget_data + "\n"
        print("Text data : ",txt_data)
        data_file(mode="w",path=file_name,to_write=txt_data)

    if file_name==txt_effects:
        if edit_button_var.get()=="Show":
            show_all()
        else:
            edit_button_var.set("Show")
        
    else:
        edit_button_var.set("Saved")


def show_all():
    done_button.destroy()
    edit_button.destroy()
    show_changes_side_effects_click(False)


def ok_button_click():
    save_current_effect_change_data()
    on_window_close()    


def on_window_close():
    player.stop()
    time_now = datetime.now()
    data[key_lastly_opened] = time_now
    formated_time_now = time_now.strftime("%d-%m-%y %H:%M:%S")
    txt_file_write_data = f"{formated_time_now} :: {data}\n"
    print(txt_file_write_data)
    data_file(mode="a",path=txt_file_path,to_write=txt_file_write_data)
    data_file("wb",to_write=data)
    root.destroy()
    print("Window closed")


def entry_button_click(entry):
    player.stop()
    entry.delete(0,END)
    entry.configure(fg="black")


def stop_player(event):
    player.pause()


def show_main_menu(event):
    main_menu.tk_popup(x = event.x_root+10,y=event.y_root+5)


def add_songs():
    MessageBeep()
    bgm_files = listdir(bgm_folder)
    ask_files_path = askopenfilenames(title="Select music files",filetypes=[("Audio files","*.mp3")])

    if len(ask_files_path)==0:
        MessageBeep()
        msgbox(title=box_titile,msg="No song selected")
        return 

    for file_path in ask_files_path:
        file_name = file_path.rsplit("/",1)[-1]
        if file_name not in bgm_files:
            dst = copy(file_path,bgm_folder)
            print(f"{file_name} copied to {dst}")
        else:
            print(f"{file_name} - File already found")
        
    MessageBeep()
    msgbox(title=box_titile,msg="Songs Added")


def run_on_start():
    MessageBeep()
    start_up_folder_path = expanduser("~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")
    system("explorer.exe "+start_up_folder_path)
    msgbox(root=root,title=box_titile,msg="Create shortcut for .pyw or .exe file here (start up folder)")


def contact_developer(media_name):
    if media_name=="Email":
        pyperclip.copy(developer_mail)
    else:
        open_new_tab(url=contact_data[media_name])


def reset():
    player.stop()
    delete_files = [txt_next_step,txt_changes,txt_effects,txt_file_path,file_name]
    for file_d in delete_files:
        print(f"{file_d} deleted")
        remove(file_d)
    root.destroy()
    MessageBeep()
    msgbox(title=box_titile,root=root,msg="Successfully reseted")



time_now = datetime.now()


if not isfile(file_name):
    data = {}
    data[key_lastly_opened] = data[key_start_time] =  time_now
    data[key_lastly_relapsed] = data[key_lastly_noted_change] = data[key_lastly_noted_side_effect] = data[key_next_step] = "Not Found"
    data_file(mode="wb",to_write=data)

else:
    data = data_file()


if not isfile(txt_file_path):
    started_date = "Started Date (date,month,year) : " + time_now.strftime("%d-%m-%y")
    started_time = "Started Time (hours,mins,secs) : " + time_now.strftime("%H:%M:%S")

    data_file(mode="a",path=txt_file_path,to_write=f"{started_date}\n{started_time}\n\nWriting Format : Date-Month-Year Hours:Minutes:Seconds :: data\n\n")

else:
    txt_file_size = getsize(txt_file_path)
    print("Data file size : ",txt_file_size)
    if txt_file_size>10**5:
        remove(txt_file_path)
        print("Data file deleted")


create_file_names = (txt_effects,txt_changes,txt_next_step)
for name in create_file_names:
    if not isfile(name):
        data_file(mode="a",path=name,to_write="")



contact_developer_menu = Menu(root,tearoff=0,font=("Times New Roman",12))

youtube_menu = Menu(contact_developer_menu,tearoff=0,font=("Times New Roman",12))
youtube_menu.add_command(label="Coding",command=lambda : open_new_tab(yt_coding_channel_link))
youtube_menu.add_command(label="Info & Fun",command = lambda : open_new_tab(yt_personal_channel))

contact_developer_menu.add_command(label="Instagram",command= lambda : contact_developer("Instagram"))
contact_developer_menu.add_command(label="Linked In",command= lambda : contact_developer("Linked In"))
contact_developer_menu.add_cascade(label="Youtube",menu=youtube_menu)
contact_developer_menu.add_command(label="Github",command= lambda : contact_developer("Github"))
contact_developer_menu.add_command(label="Facebook",command= lambda : contact_developer("FaceBook"))

email_menu = Menu(contact_developer_menu,tearoff=0,font=("Times New Roman",12))
email_menu.add_command(label="copy Mail ID",command=lambda : contact_developer("Email"))
contact_developer_menu.add_cascade(label="Email",menu=email_menu)

main_menu = Menu(root,tearoff=0,font=("Times New Roman",12))  
main_menu.add_command(label="Add songs",command=add_songs)  
main_menu.add_command(label="Run on start",command=run_on_start) 
main_menu.add_command(label="Reset",command=reset)
main_menu.add_command(label="Open in Github",command=lambda : open_new_tab(git_link))
main_menu.add_cascade(label="Developer Contact",menu=contact_developer_menu)  

top = Label(textvariable=top_string,font=("Times New Roman",38),anchor=CENTER)

addicted_button = Button(cursor="hand2",image=hand_cuffed_img,border=0,command=relaped_click)
free_button = Button(cursor="hand2",image=free_img,border=0,command=no_button_click)
ok_button = Button(text="Done",font=("Times New Roman",18,"bold"),cursor="hand2",background="blue",foreground="white",activeforeground="white",activebackground="blue",command=ok_button_click)
show_changes_side_effects = Button(text="Effects",font=("Times New Roman",18,"bold"),cursor="hand2",background="blue",foreground="white",activeforeground="white",activebackground="blue",command=show_changes_side_effects_click)

relapsed_button = addicted_button
no_button = free_button

change_entry = Entry(font=("Times New Roman",15),fg="grey",justify=CENTER)
side_effect_entry = Entry(font=("Times New Roman",15),fg="grey",justify=CENTER)
next_step_entry = Entry(font=("Times New Roman",15),fg="grey",justify=CENTER)

change_entry.insert(0,"Enter the positive effect")
side_effect_entry.insert(0,"Enter the side effect")
next_step_entry.insert(0,"Enter the next step")

change_entry.bind("<Button>",lambda event : entry_button_click(change_entry))
side_effect_entry.bind("<Button>",lambda event : entry_button_click(side_effect_entry))
next_step_entry.bind("<Button>",lambda event : entry_button_click(next_step_entry))

top.place(relx=.5,rely=.16,anchor=CENTER,relwidth=1)

no_button.place(relx=.27,rely=.6,anchor=CENTER)
relapsed_button.place(relx=.73,rely=.6,anchor=CENTER)

root.bind("<Button-3>",show_main_menu)
root.protocol("WM_DELETE_WINDOW",on_window_close)
root.mainloop()