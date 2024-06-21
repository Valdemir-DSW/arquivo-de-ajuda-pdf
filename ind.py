import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import ttk
import webbrowser
class HelpWizardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Arapuca Help Wizard")

        self.project_name = ""
        self.page_style = ""
        self.topics = []
        self.pdf_folder = ""

        self.create_widgets()

    def create_widgets(self):
        # Project Name
        self.lbl_project = tk.Label(self.root, text="Project Name:")
        self.lbl_project.grid(row=0, column=0, padx=5, pady=5)
        self.entry_project = tk.Entry(self.root)
        self.entry_project.grid(row=0, column=1, padx=5, pady=5)

        # Page Style
        self.lbl_style = tk.Label(self.root, text="Page Style:")
        self.lbl_style.grid(row=1, column=0, padx=5, pady=5)
        self.combo_style = ttk.Combobox(self.root, values=["Modern", "Classic", "Dark"])
        self.combo_style.grid(row=1, column=1, padx=5, pady=5)

        # Topics List
        self.lbl_topics = tk.Label(self.root, text="Topics:")
        self.lbl_topics.grid(row=2, column=0, padx=5, pady=5)
        self.listbox_topics = tk.Listbox(self.root, width=30)  # Definindo uma largura inicial para a lista
        self.listbox_topics.grid(row=2, column=1, padx=5, pady=5)

        # Filter Entry
        self.lbl_filter = tk.Label(self.root, text="Filter:")
        self.lbl_filter.grid(row=3, column=0, padx=5, pady=5)
        self.entry_filter = tk.Entry(self.root)
        self.entry_filter.grid(row=3, column=1, padx=5, pady=5)
        self.entry_filter.bind("<KeyRelease>", self.filter_topics)

        # Add Topic Button
        self.btn_add_topic = tk.Button(self.root, text="Add Topic", command=self.add_topic)
        self.btn_add_topic.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.btn_delete_topic = tk.Button(self.root, text="Delete Topic", command=self.delete_topic)
        self.btn_delete_topic.grid(row=5, column=0, columnspan=2, pady=10)

        # Save Button
        self.btn_save = tk.Button(self.root, text="Save Project", command=self.save_project)
        self.btn_save.grid(row=6, column=0, columnspan=2, pady=10)
        self.btn_load = tk.Button(self.root, text="Load Project", command=self.load_project)
        self.btn_load.grid(row=7, column=0, columnspan=2, pady=10)

        self.btnhelp = tk.Button(self.root,text="Criar arquivo PDF online",command=self.helpte)
        self.btnhelp.grid(row=8, column=0, columnspan=2, pady=10)
        self.btnhelp = tk.Button(self.root,text="Como usar",command=self.helpte2)
        self.btnhelp.grid(row=9, column=0, columnspan=2, pady=10)

    def helpte(self):   
        webbrowser.open("https://docs.google.com/document/u/0/") 
    def helpte2(self):   
        webbrowser.open(os.path.abspath("index.html")) 
        print(os.path.abspath("index.html"))    
    def delete_topic(self):
        selected_topic_index = self.listbox_topics.curselection()
        if selected_topic_index:
            selected_topic_index = selected_topic_index[0]
            self.listbox_topics.delete(selected_topic_index)
            del self.topics[selected_topic_index]
    def filter_topics(self, event):
        filter_text = self.entry_filter.get().lower()
        self.listbox_topics.delete(0, tk.END)
        for topic, _ in self.topics:
            if filter_text in topic.lower():
                self.listbox_topics.insert(tk.END, topic)

    def add_topic(self):
        topic_name = simpledialog.askstring("Topic Name", "Enter the topic name:")
        if topic_name:
            pdf_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if pdf_file:
                self.topics.append((topic_name, pdf_file))
                self.listbox_topics.insert(tk.END, topic_name)

    def save_project(self):
        self.project_name = self.entry_project.get()
        self.page_style = self.combo_style.get()

        if not self.project_name or not self.page_style:
            messagebox.showwarning("Input Error", "Please enter the project name and select a page style.")
            return

        save_dir = filedialog.askdirectory()
        if not save_dir:
            return

        project_dir = os.path.join(save_dir, self.project_name)
        os.makedirs(project_dir, exist_ok=True)
        self.pdf_folder = os.path.join(project_dir, "pdfs")
        os.makedirs(self.pdf_folder, exist_ok=True)
        if not os.path.exists(project_dir):
         os.makedirs(project_dir)

        project_data_file = os.path.join(project_dir, "project_data.txt")
        
        with open(project_data_file, "w") as f:
            f.write(f"{self.project_name}\n")
            f.write(f"{self.page_style}\n")
            for topic, pdf_file in self.topics:
                f.write(f"{topic},{pdf_file}\n")

        for topic, pdf_file in self.topics:
            pdf_dest = os.path.join(self.pdf_folder, os.path.basename(pdf_file))
            shutil.copy(pdf_file, pdf_dest)

        self.generate_html(project_dir)

        messagebox.showinfo("Success", "Project saved successfully!")
    def load_project(self):
        project_dir = filedialog.askdirectory()
        if not project_dir:
            return

        # Load project data from project_dir (replace with actual loading logic)
        project_data_file = os.path.join(project_dir, "project_data.txt")
        if not os.path.isfile(project_data_file):
            messagebox.showerror("Error", "Project data file not found.")
            return

        with open(project_data_file, "r") as f:
            lines = f.readlines()
            if len(lines) < 2:
                messagebox.showerror("Error", "Invalid project data format.")
                return

            self.project_name = lines[0].strip()
            self.page_style = lines[1].strip()

            # Clear current topics and load from project data
            self.topics = []
            self.listbox_topics.delete(0, tk.END)
            for line in lines[2:]:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    topic_name = parts[0].strip()
                    pdf_file = parts[1].strip()
                    self.topics.append((topic_name, pdf_file))
                    self.listbox_topics.insert(tk.END, topic_name)

        messagebox.showinfo("Success", f"Project '{self.project_name}' loaded successfully!")

    def generate_html(self, project_dir):
        styles = {
            "Modern": """
                body { font-family: 'Helvetica', sans-serif; background-color: #f9f9f9; margin: 0; display: flex; }
                .sidebar { width: 20%; background: #333; color: white; padding: 10px; height: 100vh; }
                .sidebar a { color: white; text-decoration: none; display: block; padding: 5px; }
                .sidebar a:hover { background: #575757; }
                .content { flex: 1; padding: 10px; }
                .filter { margin-bottom: 10px; padding: 5px; width: calc(100% - 12px); }
                iframe { width: 100%; height: calc(100vh - 20px); border: none; }
            """,
            "Classic": """
                body { font-family: 'Times New Roman', serif; background-color: #ffffff; margin: 0; display: flex; }
                .sidebar { width: 20%; background: #eee; padding: 10px; height: 100vh; }
                .sidebar a { color: #333; text-decoration: none; display: block; padding: 5px; }
                .sidebar a:hover { background: #ddd; }
                .content { flex: 1; padding: 10px; }
                .filter { margin-bottom: 10px; padding: 5px; width: calc(100% - 12px); }
                iframe { width: 100%; height: calc(100vh - 20px); border: none; }
            """,
            "Dark": """
                body { font-family: 'Arial', sans-serif; background-color: #121212; color: #e0e0e0; margin: 0; display: flex; }
                .sidebar { width: 20%; background: #1e1e1e; color: #e0e0e0; padding: 10px; height: 100vh; }
                .sidebar a { color: #e0e0e0; text-decoration: none; display: block; padding: 5px; }
                .sidebar a:hover { background: #333; }
                .content { flex: 1; padding: 10px; }
                .filter { margin-bottom: 10px; padding: 5px; width: calc(100% - 12px); background: #333; color: #e0e0e0; border: none; }
                iframe { width: 100%; height: calc(100vh - 20px); border: none; }
            """
        }

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{self.project_name}</title>
            <style>
                {styles.get(self.page_style, styles["Modern"])}
            </style>
        </head>
        <body>
            <div class="sidebar">
                <input class="filter" type="text" id="filter" onkeyup="filterTopics()" placeholder="Filter topics...">
                <ul id="topicList">
                    {" ".join([f'<li><a href="pdfs/{os.path.basename(pdf)}" target="contentFrame">{topic}</a></li>' for topic, pdf in self.topics])}
                </ul>
            </div>
            <div class="content">
                <iframe name="contentFrame"></iframe>
            </div>
            <script>
                function filterTopics() {{
                    var filter = document.getElementById('filter').value.toLowerCase();
                    var topics = document.getElementById('topicList').getElementsByTagName('li');
                    for (var i = 0; i < topics.length; i++) {{
                        var topic = topics[i].innerText.toLowerCase();
                        if (topic.includes(filter)) {{
                            topics[i].style.display = "";
                        }} else {{
                            topics[i].style.display = "none";
                        }}
                    }}
                }}
            </script>
        </body>
        </html>
        """

        with open(os.path.join(project_dir, "index.html"), "w") as html_file:
            html_file.write(html_content)


if __name__ == "__main__":
    root = tk.Tk()
    app = HelpWizardApp(root)
    root.mainloop()
