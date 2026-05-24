import os
import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
import webbrowser
import wikipedia
from tkinter import messagebox
from urllib.parse import quote_plus
Translator = None
google_translator = None
try:
    from googletrans import Translator as GoogleTranslateTranslator
    Translator = GoogleTranslateTranslator
except ImportError:
    try:
        from google_trans_new import google_translator as GoogleTransNewTranslator
        google_translator = GoogleTransNewTranslator
    except ImportError:
        print("Warning: Google translation modules not installed. Translation functionality will be disabled.")
try:
    import pyttsx3
except ImportError:
    pyttsx3 = None
    print("Warning: The 'pyttsx3' module is not installed. Voice functionality will be disabled.")

class VirtualBuddyApp:
    def __init__(self, root):  # Corrected the method name to __init__
        self.root = root
        self.root.title("Hexa Bot")

        # Set the background color
        self.root.configure(bg='#000000')

        # Correct the image path here
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "SUNSET-AI-1112023TH.png")
        if not os.path.exists(image_path):
            image_path = r"C:\Users\OMER AYOUB\OneDrive\Attachments\Desktop\mini project\Hexa-Bot\SUNSET-AI-1112023TH.png"

        try:
            pil_image = Image.open(image_path)
            pil_image = pil_image.filter(ImageFilter.SHARPEN)  # Apply sharpen filter to enhance image
            self.photo = ImageTk.PhotoImage(pil_image)

            # Create a label to display the full-size image as the background
            self.bg_label = tk.Label(root, image=self.photo)
            self.bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            print(f"Image not found at path: {image_path}")
            messagebox.showerror("Error", "Image file not found. Please check the image path.")

        # Create and configure frames
        self.main_frame = tk.Frame(root, bg='#FC2E20')  # White color for the main frame
        self.main_frame.pack(pady=20)

        # Create an entry widget for user input with shadow effect
        self.entry_label = tk.Label(self.main_frame, text="Hexa Bot", bg='#000000', fg='#ffffff',
                                    font=('Batik Alin', 90, 'bold'))
        self.entry_label.grid(row=0, column=0, padx=20, pady=10, columnspan=3)

        self.entry = tk.Entry(self.main_frame, width=40, font=('Minguwest', 20), bd=5, relief=tk.GROOVE)
        self.entry.grid(row=1, column=0, padx=20, pady=10, columnspan=3, sticky="ew")

        # Create a button to perform the search
        self.search_button = tk.Button(self.main_frame, text="Search", command=self.start_animation,
                                       bg='#000000', fg='#ffffff', font=('Minguwest', 20))
        self.search_button.grid(row=1, column=4, pady=10)

        # Create a "Clear" button
        self.clear_button = tk.Button(self.main_frame, text="Clear", command=self.clear_result,
                                      bg='#000000', fg='#ffffff', font=('Minguwest', 20))
        self.clear_button.grid(row=2, column=4, pady=10)

        # Create a "Speak" button
        self.speak_button = tk.Button(self.main_frame, text="Speak", command=self.speak_output,
                                      bg='#000000', fg='#ffffff', font=('Minguwest', 20))
        self.speak_button.grid(row=3, column=4, pady=10)

        # Create a "Submit Feedback" button
        self.feedback_button = tk.Button(self.main_frame, text="Submit Feedback", command=self.show_feedback_window,
                                         bg='#000000', fg='#ffffff', font=('Minguwest', 20))
        self.feedback_button.grid(row=4, column=4, pady=10)

        # Create a text widget to display the search result with shadow effect
        self.result_text = tk.Text(self.main_frame, height=7, width=35, wrap=tk.WORD, font=('Minguwest', 30), bd=5,
                                   relief=tk.GROOVE)
        self.result_text.grid(row=2, column=0, padx=20, pady=10, columnspan=3, rowspan=2, sticky="ew")

        # Create a "Web Search" button
        self.web_search_button = tk.Button(self.main_frame, text="Web Search", command=self.web_search,
                                           bg='#000000', fg='#ffffff', font=('Minguwest', 20))
        self.web_search_button.grid(row=1, column=5, pady=10)

        # Create a "Translate" button if translation is available
        if Translator:
            self.translate_button = tk.Button(self.main_frame, text="Translate", command=self.translate_result,
                                              bg='#000000', fg='#ffffff', font=('Minguwest', 20))
            self.translate_button.grid(row=2, column=5, pady=10)

        # Create a "Wikipedia Search" button
        self.wikipedia_button = tk.Button(self.main_frame, text="Wikipedia", command=self.wikipedia_search,
                                          bg='#000000', fg='#ffffff', font=('Minguwest', 20))
        self.wikipedia_button.grid(row=3, column=5, pady=10)

        # Create a "Google Search" button
        self.google_search_button = tk.Button(self.main_frame, text="Google Search", command=self.google_search,
                                              bg='#000000', fg='#ffffff', font=('Minguwest', 20))
        self.google_search_button.grid(row=4, column=5, pady=10)

        # Create a search history frame
        self.history_frame = tk.Frame(root, bg='#ffffff')
        self.history_frame.pack(side=tk.RIGHT, pady=20)

        self.history_label = tk.Label(self.history_frame, text="Search History", bg='#ffff00', fg='#000000',
                                      font=('Minguwest', 12, 'bold'))
        self.history_label.pack()

        self.history_listbox = tk.Listbox(self.history_frame, selectbackground='#4285F4', selectforeground='#ffffff',
                                          font=('Minguwest', 14), height=10, selectmode=tk.SINGLE)
        self.history_listbox.pack()
        self.history_listbox.bind("<<ListboxSelect>>", self.on_history_select)

        self.search_history = []
        self.history_file = os.path.join(os.path.dirname(__file__), "search_history.txt")
        self.feedback_file = os.path.join(os.path.dirname(__file__), "feedback.txt")

        self.load_search_history()

        # Initialize animation parameters
        self.alpha = 0.0
        self.fade_in()
        self.initial_greeting = True

        # Initialize text-to-speech
        if pyttsx3:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 150)  # Speed of speech
                voices = self.engine.getProperty('voices')
                if voices:
                    self.engine.setProperty('voice', voices[0].id)
            except Exception as e:
                self.engine = None
                print(f"Warning: pyttsx3 initialization failed: {e}")
        else:
            self.engine = None

    def fade_in(self):
        if self.alpha < 1.0:
            self.alpha += 0.05
            try:
                self.root.attributes('-alpha', self.alpha)
            except Exception:
                pass
            self.root.after(40, self.fade_in)
        else:
            try:
                self.root.attributes('-alpha', 1.0)
            except Exception:
                pass

    def get_query(self):
        query = self.entry.get().strip()
        if not query:
            messagebox.showwarning("Input required", "Please enter a search query.")
            return None
        return query

    def show_result(self, text):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)

    def update_history(self, query):
        if not query or query in self.search_history:
            return
        self.search_history.append(query)
        self.history_listbox.insert(tk.END, query)
        self.history_listbox.yview_moveto(1)
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                for item in self.search_history:
                    f.write(item + '\n')
        except Exception as e:
            print(f"Warning: Could not save search history: {e}")

    def load_search_history(self):
        if not os.path.exists(self.history_file):
            return
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                for line in f:
                    query = line.strip()
                    if query:
                        self.search_history.append(query)
                        self.history_listbox.insert(tk.END, query)
        except Exception as e:
            print(f"Warning: Could not load search history: {e}")

    def start_animation(self):
        query = self.get_query()
        if not query:
            return
        self.update_history(query)
        self.show_result(f"Searching Wikipedia for '{query}'...")
        try:
            summary = wikipedia.summary(query, sentences=3)
            self.show_result(summary)
        except wikipedia.DisambiguationError as e:
            options = ', '.join(e.options[:5])
            self.show_result(
                f"Multiple results found for '{query}'. Try one of: {options}"
            )
        except wikipedia.PageError:
            self.show_result(f"No Wikipedia page found for '{query}'.")
        except Exception as e:
            self.show_result(f"Search failed: {e}")

    def clear_result(self):
        self.entry.delete(0, tk.END)
        self.result_text.delete("1.0", tk.END)

    def speak_output(self):
        if not self.engine:
            messagebox.showerror("Voice not available", "Text-to-speech is not available on this system.")
            return
        text = self.result_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Nothing to speak", "Please perform a search first.")
            return
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            messagebox.showerror("Speech error", f"Could not speak output: {e}")

    def show_feedback_window(self):
        feedback_win = tk.Toplevel(self.root)
        feedback_win.title("Submit Feedback")
        feedback_win.configure(bg='#000000')

        label = tk.Label(feedback_win, text="Your feedback:", bg='#000000', fg='#ffffff', font=('Minguwest', 16))
        label.pack(padx=20, pady=(20, 10))

        feedback_text = tk.Text(feedback_win, height=8, width=50, font=('Minguwest', 14), bd=4, relief=tk.GROOVE)
        feedback_text.pack(padx=20, pady=10)

        def submit_feedback():
            feedback = feedback_text.get("1.0", tk.END).strip()
            if not feedback:
                messagebox.showwarning("Input required", "Please enter your feedback before submitting.")
                return
            try:
                with open(self.feedback_file, 'a', encoding='utf-8') as f:
                    f.write(feedback + '\n---\n')
                messagebox.showinfo("Thank you", "Your feedback has been submitted.")
                feedback_win.destroy()
            except Exception as e:
                messagebox.showerror("Save failed", f"Could not save feedback: {e}")

        submit_button = tk.Button(feedback_win, text="Submit", command=submit_feedback,
                                  bg='#000000', fg='#ffffff', font=('Minguwest', 16))
        submit_button.pack(pady=(0, 20))

    def web_search(self):
        query = self.get_query()
        if not query:
            return
        self.update_history(query)
        url = f"https://www.bing.com/search?q={quote_plus(query)}"
        webbrowser.open(url)

    def translate_result(self):
        if Translator is None and google_translator is None:
            messagebox.showerror("Translation not available", "Translation module is not installed. Install googletrans or google_trans_new.")
            return
        text = self.result_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Nothing to translate", "Please perform a search first.")
            return
        try:
            if Translator is not None:
                translator = Translator()
                translated = translator.translate(text, dest='en')
                result_text = translated.text
            else:
                translator = google_translator()
                result_text = translator.translate(text, lang_tgt='en')
            self.show_result(result_text)
            messagebox.showinfo("Translation", "Result translated to English.")
        except Exception as e:
            messagebox.showerror("Translation failed", f"Could not translate the text: {e}")

    def wikipedia_search(self):
        query = self.get_query()
        if not query:
            return
        self.update_history(query)
        try:
            summary = wikipedia.summary(query, sentences=5)
            self.show_result(summary)
        except wikipedia.DisambiguationError as e:
            options = ', '.join(e.options[:5])
            self.show_result(
                f"Multiple results found for '{query}'. Try one of: {options}"
            )
        except wikipedia.PageError:
            self.show_result(f"No Wikipedia page found for '{query}'.")
        except Exception as e:
            self.show_result(f"Wikipedia search failed: {e}")

    def google_search(self):
        query = self.get_query()
        if not query:
            return
        self.update_history(query)
        url = f"https://www.google.com/search?q={quote_plus(query)}"
        webbrowser.open(url)

    def on_history_select(self, event):
        selection = event.widget.curselection()
        if not selection:
            return
        query = event.widget.get(selection[0])
        self.entry.delete(0, tk.END)
        self.entry.insert(0, query)

# Corrected the check for main execution block
if __name__ == "__main__":  # Corrected the if statement here
    root = tk.Tk()
    app = VirtualBuddyApp(root)
    root.mainloop()  # Corrected the indentation here