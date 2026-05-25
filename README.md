# Hexa Bot – Readme 

## Project Overview

Hexa Bot is a desktop-based AI assistant application built using Python and Tkinter. It provides features like Wikipedia search, Google search, web search, text-to-speech, translation, and search history management through a simple graphical interface.

The project combines GUI development with internet-based utilities to create a smart virtual assistant experience.



---

# Features

* Wikipedia search with summaries
* Google and Bing web search
* Text-to-speech output
* Language translation support
* Search history storage
* Feedback submission system
* Animated GUI interface
* Background image support

---

# Technologies Used

* Python
* Tkinter
* Pillow (PIL)
* Wikipedia API
* pyttsx3
* googletrans / google_trans_new
* Webbrowser module

---

# Required Libraries

Install the required libraries using:

```bash
pip install pillow wikipedia pyttsx3 googletrans==4.0.0-rc1
```

If googletrans does not work:

```bash
pip install google_trans_new
```

---

# Project Structure

```text
Hexa-Bot/
│
├── main.py
├── SUNSET-AI-1112023TH.png
├── search_history.txt
├── feedback.txt
└── README.md
```

---

# How to Run

1. Install Python 3.x
2. Install required libraries
3. Place the background image in the project folder
4. Run the program:

```bash
python main.py
```

---

# Functionalities

## Search

Searches Wikipedia and displays a short summary.

## Speak

Reads the displayed result using text-to-speech.

## Translate

Translates output text into English.

## Web Search

Opens Bing search in browser.

## Google Search

Opens Google search in browser.

## Search History

Stores previous searches locally.

## Feedback System

Allows users to submit feedback saved in a text file.

---

# Advantages

* Easy to use interface
* Beginner-friendly project
* Useful for learning GUI programming
* Combines multiple Python libraries
* Interactive virtual assistant

---

# Future Improvements

* Voice recognition support
* ChatGPT API integration
* Dark/Light themes
* More language support
* AI conversation mode

---

# Author

Developed by Omer Ayoub

---

# License

This project is for educational purposes only.
