import os
import customtkinter
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("750x500")
saved_notes_folder = "saved-notes"

os.makedirs(saved_notes_folder, exist_ok=True)

notes_dict = {}

left_panel_selection = customtkinter.StringVar()

def create_note():
    note_name_input.pack(pady=10, padx=10, fill="x")
    text_editor.pack(pady=10, padx=10, fill="both", expand=True)
    save_button.pack(side="bottom", pady=10, padx=10)
    
def save_note():
    note_name = note_name_input.get()
    note_content = text_editor.get("1.0", "end-1c")
    file_path = os.path.join(saved_notes_folder, f"{note_name}.txt")
    with open(file_path, "w") as file:
        file.write(note_content)
    notes_dict[note_name] = file_path
    update_left_panel()
    note_name_input.pack_forget()
    text_editor.pack_forget()
    save_button.pack_forget()
    
def update_note():
    selected_note_name = left_panel_selection.get()
    
    if not selected_note_name:
        print("Please select a note to update.")
        return
    
    note_content = text_editor.get("1.0", "end-1c")
    
    file_path = notes_dict.get(selected_note_name, "")
    
    if file_path and os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write(note_content)
        
        notes_dict[selected_note_name] = file_path
        update_left_panel()
        note_name_input.pack_forget()
        text_editor.pack_forget()
        update_button.pack_forget()
    else:
        print(f"File not found: {file_path}")
    
def update_left_panel():
    for widget in left_frame.winfo_children():
        widget.pack_forget()
    create_note_button = customtkinter.CTkButton(master=left_frame, text="Create Note", command=create_note)
    create_note_button.pack(pady=10, padx=10, anchor='n')  
    load_existing_notes()
    
def load_note(note_name):
    file_path = notes_dict.get(note_name, "")
    if file_path and os.path.exists(file_path):
        with open(file_path, "r") as file:
            note_content = file.read()
        text_editor.delete("1.0", "end")
        text_editor.insert("1.0", note_content)
        text_editor.pack(pady=10, padx=10, fill="both", expand=True)
        update_button.pack(side="bottom", pady=10, padx=10, fill="x")
        left_panel_selection.set(note_name)
    
def load_existing_notes():
    for file_name in os.listdir(saved_notes_folder):
        if file_name.endswith(".txt"):
            note_name = os.path.splitext(file_name)[0]
            notes_dict[note_name] = os.path.join(saved_notes_folder, file_name)
            note_name_button = customtkinter.CTkButton(master=left_frame, text=note_name, command=lambda n=note_name: load_note(n))
            note_name_button.pack(pady=5, padx=5, fill="x")
    
left_frame = customtkinter.CTkFrame(master=root)
left_frame.pack(side="left", fill="y")

create_note_button = customtkinter.CTkButton(master=left_frame, text="Create Note", command=create_note)
create_note_button.pack(pady=10, padx=10)

main_frame = customtkinter.CTkFrame(master=root)
main_frame.pack(side="right", fill="both", expand=True)

label = customtkinter.CTkLabel(master=main_frame, text="DashNote", font=("Roboto", 30))
label.pack(pady=12, padx=10)

note_name_input = customtkinter.CTkEntry(master=main_frame, placeholder_text="Enter Note Name")

text_editor = customtkinter.CTkTextbox(master=main_frame)

save_button = customtkinter.CTkButton(master=main_frame, text="Save", command=save_note)

update_button = customtkinter.CTkButton(master=main_frame, text="Update", command=update_note)

load_existing_notes()

root.mainloop()