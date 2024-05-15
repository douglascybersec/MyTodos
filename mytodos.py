# Modules
import customtkinter
from CTkMessagebox import CTkMessagebox
from CTkListbox import *


# myApp setting & more..
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("Dark-Theme.json")
myApp = customtkinter.CTk()
myApp.title("MyTodos")
myApp.geometry(f"{800}x{600}")
myApp.resizable(False, False)

# Fonts
tite_font = customtkinter.CTkFont(family="Montserrat",size=60,weight="bold")
todos_font = customtkinter.CTkFont(family="Roboto",size=21,weight="bold")
todos_font_checked = customtkinter.CTkFont(family="Roboto",size=25,weight="bold", overstrike=True)

# (List) -->Store todos data
todos_data = []

# ---FUNCTIONS---

# ---> Create todos_frame for each todo
def create_frame():
    
    # Length of child_widgets
    num_children = len(todos_listbox.winfo_children())
    row_num = num_children
    
    todos_frame = customtkinter.CTkFrame(master=todos_listbox, height=350, border_color="#586b78", border_width=1)
    todos_frame.grid(row=row_num, column=0, padx=5, pady=5)
    
    return todos_frame
    
# ---> Add todo to listbox(can also use scrollableframe)
def add_todo():

    todo = todos_entry.get()
    
    if todo:
        todos_frame = create_frame()
        
        todos_checkbox = customtkinter.CTkCheckBox(master=todos_frame, text=todo, command=lambda:checked(todos_checkbox),
                                                   font=todos_font, width=555, height=50, checkbox_height=50, checkbox_width=50)
        todos_checkbox.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")
        todos_data.append((todo, todos_checkbox, todos_frame))
        
        edit_button = customtkinter.CTkButton(master=todos_frame, text="Edit", command=lambda index=len(todos_data)-1: edit_todo(index),
                                              font=todos_font, corner_radius=8, width=75, height=50, cursor="hand2")
        edit_button.grid(row=0, column=1, pady=5, padx=5, sticky="nswe")

        remove_button = customtkinter.CTkButton(master=todos_frame, text="Remove", fg_color="#a70f0f", hover_color="#e00000", command=lambda :remove_todo(todos_frame),
                                                font=todos_font, corner_radius=8, width=75, height=50,  cursor="hand2")
        remove_button.grid(row=0, column=2, pady=5, padx=5, sticky="nswe")

        todos_entry.delete(0, customtkinter.END)
        
        show_progress()
        save_todos()
        
    else:
        
        # Error MsgBox
        error_msg = CTkMessagebox(title="MyTodos-Error", 
                  message="Check you! Add a todo.",
                  fg_color="#000000", 
                  icon="cancel", 
                  width=300, height=150)
        error_msg = error_msg.get()
        
        
# ---> Cross/Uncross when todo is checked/done  
def checked(todos_checkbox):
    checkbox_state = todos_checkbox.get()
    if not checkbox_state:
        todos_checkbox.configure(font=todos_font)    
    else:
        todos_checkbox.configure(font=todos_font_checked)
    show_progress()
    save_todos()

# ---> Remove todo & destroy parent_frame
def remove_todo(todos_frame):
    
    # Locate Index to remove & do notthing if not found
    for index, (todo, todos_checkbox, frame) in enumerate(todos_data):
        if frame == todos_frame:
            break
    else:
        return

    # Check for unmarked & prompt to cancel or proceed
    try:
        todos_checkbox = todos_frame.winfo_children()[0] 
        
        if not todos_checkbox.get():
            
            # Confirmation MsgBox
            response = CTkMessagebox(title="MyTodos-Confirm", 
                                     message="Check you! todo's not done. Remove anyway?",
                                     fg_color="#000000", 
                                     icon="warning", 
                                     option_1="Yes", option_2="No",
                                     width=300, height=150)
            response = response.get()

            # Remove frame if yes from todos_data
            if response == "Yes":
                todos_frame.destroy()
                todos_data.pop(index)
                
                # Refresh & reposition remaining frames, & update progress_button
                for i, (todo, todos_checkbox, todos_frame) in enumerate(todos_data):                      
                    todos_frame.grid(row=i, column=0, padx=5, pady=5)
                show_progress()
                save_todos()
            else:
                pass 
        else:
            todos_frame.destroy()
            todos_data.pop(index)
            
            # Refresh & reposition remaining frames, & update progress_button
            for i, (todo, todos_checkbox, todos_frame) in enumerate(todos_data):                  
                todos_frame.grid(row=i, column=0, padx=5, pady=5)
            show_progress()
            save_todos()
    
    # Tried & no frame found, remove nothing from todos_data
    except IndexError:
        todos_frame.destroy()
             
        # Refresh & reposition remaining frames
        for i, (todo, todos_checkbox, todos_frame) in enumerate(todos_data):    
            todos_frame.grid(row=i, column=0, padx=5, pady=5)
        show_progress()
        save_todos()


# ---> Edit todo
def edit_todo(index):
    current_todo, todos_checkbox, todos_frame = todos_data[index]
    new_todo = customtkinter.CTkInputDialog(text="Edit Todo here:", title="MyTodos-Editor").get_input()
    if new_todo:
        todos_checkbox.configure(text=new_todo)
        todos_data[index] = (new_todo, todos_checkbox, todos_frame)
    save_todos()

# ---> Remove all done todos
def remove_done_todos():
    
    # Track done_todos
    done_todos = False
    
    # Reverse iterate, del marked checkbox's master & update data
    for i in range(len(todos_data) - 1, -1, -1):
        todo, todos_checkbox, todos_frame = todos_data[i]
        if todos_checkbox.get():
            todos_frame.destroy()
            todos_data.pop(i)
            done_todos = True
            
    # Refresh & reposition remaining frames
    for i, (todo, todos_checkbox, todos_frame) in enumerate(todos_data):
        todos_frame.grid(row=i, column=0, padx=5, pady=5)
    
    # Msgbox if no done & empty listbox
    if not done_todos:
        msg= "Oops! There's no todos yet!" if not todos_data else "Oops! There's no completed todos yet!"
        CTkMessagebox(title="MyTodos-Info", 
                      message=msg,
                      fg_color="#000000", 
                      icon="info", 
                      width=300, height=150).get()
    show_progress()
    save_todos()

# ---> save todos in txt file -todos.txt (use pickle or sqlite)
def save_todos():
    ...

# ---> Load todos from saved txt file
def load_todos():
    ...

# # ---> Show todos_progress, update dynamically
def show_progress():
    total_todos = len(todos_data)
    done_todos = sum(todo_checkbox.get() for todo, todo_checkbox, todo_frame in todos_data)
    progress_button.configure(text=f"{done_todos} of {total_todos} done")
    
# ---WIDGETS---

# Frames
entry_label_frame = customtkinter.CTkFrame(myApp, height=300)
entry_label_frame.pack(side="top", expand=True, fill="both", padx=5, pady=5)

todos_listbox = CTkListbox(myApp,
                           width=800, 
                           height=350, 
                           border_color="#586b78", 
                           border_width=2)
todos_listbox.pack(expand=True, fill="both", padx=5, pady=5)

control_progress_frame = customtkinter.CTkFrame(myApp, height=100)
control_progress_frame.pack(side="bottom", expand=True, fill="both", padx=5, pady=5)

# myApp name/label
myApp.name = customtkinter.CTkLabel(master=entry_label_frame, text="MyTodos", font=tite_font, anchor="center", cursor="hand2")
myApp.name.grid(row=0, column=0, pady=10, padx=10, sticky="nswe", columnspan=5)

# Todos Entry & Buttons
todos_entry = customtkinter.CTkEntry(master=entry_label_frame, font=todos_font, placeholder_text="Type a ToDo here...", corner_radius=8, width=670, height=50)
todos_entry.grid(row=1, column=0, pady=5, padx=5, sticky="nswe")

add_button = customtkinter.CTkButton(master=entry_label_frame, text="Add", command=add_todo, font=todos_font, corner_radius=8, width=100, height=50, cursor="hand2")
add_button.grid(row=1, column=1, pady=5, padx=5, sticky="nswe")

progress_button = customtkinter.CTkButton(master=control_progress_frame, fg_color="#32CD32", text=f"{0} of {0} done", command=show_progress, font=todos_font, corner_radius=8, height=50, width=300, cursor="hand2", state="disabled")
progress_button.pack(side="left", pady=5, padx=10)

remove_all_button = customtkinter.CTkButton(master=control_progress_frame, text="Remove All Done", fg_color="#a70f0f", hover_color="#e00000", command=remove_done_todos, font=todos_font, corner_radius=8, height=50, width=300, cursor="hand2")
remove_all_button.pack(side="right", pady=5, padx=10)

# Load todos at startup
load_todos()

# Update progress
show_progress()

# Run myApp(as admin😁)
myApp.mainloop()