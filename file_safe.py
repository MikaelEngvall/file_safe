import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
from encryption import encrypt_message, decrypt_message, generate_key

def validate_choice(ok_list, choice):
    return choice in ok_list

def create_folder(folder_name):
    os.makedirs(folder_name, exist_ok=True)
    messagebox.showinfo("Success", f"Folder '{folder_name}' created successfully.")

def choose_folder():
    folder = filedialog.askdirectory()
    return folder

def create_file(folder):
    file_name = simpledialog.askstring("Input", "Enter the name of the new file:")
    content = simpledialog.askstring("Input", "Enter the content for the file:")
    if content is not None:
        content += '\n'  # Add a newline character at the end
        key = generate_key()
        encrypted_content = encrypt_message(content, key)
        with open(os.path.join(folder, file_name), 'wb') as f:
            f.write(encrypted_content)
        with open(os.path.join(folder, file_name + '.key'), 'wb') as key_file:
            key_file.write(key)
        messagebox.showinfo("Success", f"File '{file_name}' created successfully in folder '{folder}'.")

def read_file(folder):
    file_name = filedialog.askopenfilename(initialdir=folder, title="Select file")
    try:
        with open(file_name, 'rb') as f:
            encrypted_content = f.read()
        with open(file_name + '.key', 'rb') as key_file:
            key = key_file.read()
        decrypted_content = decrypt_message(encrypted_content, key)
        
        # Create a new window to display the content
        content_window = tk.Toplevel()
        content_window.title(f"Content of {os.path.basename(file_name)}")
        
        # Create a Text widget to display the content
        text_widget = tk.Text(content_window, wrap='word')
        text_widget.insert('1.0', decrypted_content)
        text_widget.pack(expand=True, fill='both')
        
        # Add a scrollbar to the Text widget
        scrollbar = tk.Scrollbar(content_window, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{file_name}' not found in folder '{folder}'.")

def add_to_file(folder):
    file_name = filedialog.askopenfilename(initialdir=folder, title="Select file")
    additional_content = simpledialog.askstring("Input", "Enter the additional content:")
    if additional_content is not None:
        additional_content += '\n'  # Add a newline character at the end
        try:
            with open(file_name + '.key', 'rb') as key_file:
                key = key_file.read()
            with open(file_name, 'rb') as f:
                existing_encrypted_content = f.read()
            decrypted_existing_content = decrypt_message(existing_encrypted_content, key)
            new_content = decrypted_existing_content + additional_content
            encrypted_content = encrypt_message(new_content, key)
            with open(file_name, 'wb') as f:
                f.write(encrypted_content)
            messagebox.showinfo("Success", f"Content added to file '{os.path.basename(file_name)}' in folder '{folder}'.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"File '{file_name}' not found in folder '{folder}'.")

def delete_file(folder):
    file_name = filedialog.askopenfilename(initialdir=folder, title="Select file")
    try:
        os.remove(file_name)
        os.remove(file_name + '.key')
        messagebox.showinfo("Success", f"File '{os.path.basename(file_name)}' deleted successfully from folder '{folder}'.")
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{file_name}' not found in folder '{folder}'.")

def main():
    root = tk.Tk()
    root.title("File Safe")
    root.geometry("400x300")

    main_frame = ttk.Frame(root, padding="10 10 10 10")
    main_frame.pack(expand=True, fill='both')

    def on_create_folder():
        folder_name = simpledialog.askstring("Input", "Enter the name for the new folder:")
        if folder_name:
            create_folder(folder_name)

    def on_choose_folder():
        folder = choose_folder()
        if folder:
            folder_menu(folder)

    def folder_menu(folder):
        folder_window = tk.Toplevel(root)
        folder_window.title(f"Folder: {folder}")
        folder_window.geometry("400x300")

        folder_frame = ttk.Frame(folder_window, padding="10 10 10 10")
        folder_frame.pack(expand=True, fill='both')

        ttk.Button(folder_frame, text="Create a new file", command=lambda: create_file(folder)).pack(pady=5)
        ttk.Button(folder_frame, text="Read an existing file", command=lambda: read_file(folder)).pack(pady=5)
        ttk.Button(folder_frame, text="Add to a file", command=lambda: add_to_file(folder)).pack(pady=5)
        ttk.Button(folder_frame, text="Delete a file", command=lambda: delete_file(folder)).pack(pady=5)
        ttk.Button(folder_frame, text="Go back to main menu", command=folder_window.destroy).pack(pady=5)

    ttk.Button(main_frame, text="Create a new folder", command=on_create_folder).pack(pady=5)
    ttk.Button(main_frame, text="Choose an existing folder", command=on_choose_folder).pack(pady=5)
    ttk.Button(main_frame, text="Exit", command=root.quit).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()