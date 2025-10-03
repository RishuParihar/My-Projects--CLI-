# 📌 Personal Task, Habit & Expense Tracker (CLI)

This is a Python-based command-line tracker that helps you manage Tasks, Habits, and Expenses in one place. You can add, list, update, delete, and search items, track habit progress with dynamic units (e.g., glasses for water, sessions for gym), and view basic statistics. The program saves all data to a text file (tracker.txt) so your records persist between sessions.

**How to Run**

1. Make sure you have Python 3.x installed on your system.

2. Save the script file (e.g., app.py) and keep tracker.txt in the same folder (the file is created automatically if it doesn’t exist).

3. ⚠️ Requires **Python 3.7+**

4. Open a terminal, navigate to the folder containing the script, and run:

       ''' python app.py '''


5. Follow the menu prompts to add tasks, habits, or expenses. Habits automatically detect relevant units when adding items (like Drink Water → glasses) and show progress with units in the CLI and saved file.


## 🚀 Features
- Add, List, Update, Delete items
- Supports three categories: **Tasks, Habits, Expenses**
- **Due Date validation** (DD/MM/YYYY format)
- **Habit progress tracking** with progress bar
- **Priority levels** (High, Medium, Low with icons)
- Colorful CLI output (ANSI codes)
- Save & load data from `tracker.txt`
- Search by keyword
- View statistics (total tasks, habits, expenses)

---



2. Run the Python script
   '''
   python app.py
   
   '''


## 📂 Project Structure
```

│── app.py       # Main program
│── tracker.txt      # Saved data (auto-created)
│── README.md        # Project documentation
```

---

## 📖 Usage Guide

### Main Menu
```
1. Add Item(s)
2. List Items
3. Update Item
4. Delete Item
5. Search Items
6. View Stats
7. Exit
```

### Delete Sub-Menu
```
🗑️ DELETE MENU
1. Delete Single Item
2. Delete Multiple Items
3. Delete All Items
4. Back to Main Menu
```

---

## 📊 Example
### Adding a Habit:
```
Enter category (Task/Habit/Expense): habit
Enter item(s). Type one per line, Enter blank to finish:
> Drink Water
Enter due date (DD/MM/YYYY) or leave blank: 05/10/2025
Enter priority (High/Medium/Low, default Medium): High
Enter target (e.g., 8 glasses/sessions): 8
Enter current progress (default 0): 2
✅ Added: 💧 Drink Water (Due: 05/10/2025) [██--------] 2/8 glasses Priority: 🔴 High
```

---

## 📌 Future Improvements 
- Export reports in CSV/Excel
- Add recurring habits/tasks
- Add authentication (user-specific data)
- Graphical dashboard (Tkinter / Web app)

---
## 🤖 AI Assistance / Help

💡 AI assistance is integrated — the tracker can suggest habit units and emojis automatically based on your input.

## 👨‍💻 Developed by :
- Rishu Parihar
- Stage 2 Project Submission
