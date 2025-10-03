import os
from datetime import datetime

# ---------------- CONFIG ----------------
DATA_FILE = "tracker.txt"

CATEGORY_EMOJI_DEFAULT = {
    "task": "📝",
    "habit": "💪",
    "expense": "💰"
}

# Habit-to-unit mapping
HABIT_UNITS = {
    "water": "glasses",
    "gym": "sessions",
    "alcohol": "drinks"
}

# ---------------- ANSI COLOR CODES ----------------
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"

# ---------------- UTILITY FUNCTIONS ----------------
def progress_bar(current, target, length=10):
    filled_len = int(round(length * current / float(target)))
    bar = '█' * filled_len + '-' * (length - filled_len)
    return f"[{bar}] {current}/{target}"

def get_emoji(category, text):
    text = text.lower()
    if category == "habit":
        if "alcohol" in text: return "🍺"
        if "water" in text: return "💧"
        if "gym" in text: return "🏋️"
        return "💪"
    if category == "expense":
        if "food" in text: return "🍔"
        if "bill" in text: return "💡"
        if "transport" in text: return "🚗"
    return CATEGORY_EMOJI_DEFAULT.get(category.lower(), "📌")

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

# ---------------- LOAD DATA ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    items = []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        parts = line.strip().split(" | ")
        if len(parts) == 5:  # Habit
            category, text, due, current, target = parts
            items.append({"category": category, "text": text, "due": due, "current": int(current), "target": int(target), "priority":"Medium","unit":"times"})
        elif len(parts) == 3:
            category, text, due = parts
            items.append({"category": category, "text": text, "due": due, "priority":"Medium"})
    return items

# ---------------- SAVE DATA ----------------
def priority_icon(priority):
    return {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(priority,"🟡")

def save_data(items):
    categories = ["task", "habit", "expense"]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for cat in categories:
            cat_items = [item for item in items if item['category'].lower() == cat]
            if not cat_items:
                continue
            emoji = CATEGORY_EMOJI_DEFAULT.get(cat, "")
            f.write(f"\n========== {cat.upper()}S {emoji} ==========\n")
            for item in cat_items:
                due_str = item.get('due', "")
                if due_str:
                    try:
                        due_date = datetime.strptime(due_str, "%d/%m/%Y")
                        if due_date < datetime.today():
                            due_str += " ⚠️ Overdue"
                    except ValueError:
                        pass
                f.write("───────────────────────────────\n")
                f.write(f"Description : {item.get('text','')} {get_emoji(item['category'], item['text'])}\n")
                if due_str:
                    f.write(f"Due Date : {due_str}\n")
                if cat=="habit" and "current" in item and "target" in item:
                    unit = item.get("unit","times")
                    f.write(f"Progress : {progress_bar(item['current'], item['target'])} {unit}\n")
                f.write(f"Priority : {item.get('priority','Medium')} ({priority_icon(item.get('priority','Medium'))})\n")
                f.write("───────────────────────────────\n\n")

# ---------------- FORMAT ITEMS WITH COLORS ----------------
def format_item_colored(item, idx):
    cat = item['category'].lower()
    cat_color = CYAN if cat=="task" else GREEN if cat=="habit" else YELLOW
    due_str = item.get('due',"")
    if due_str:
        try:
            due_date = datetime.strptime(due_str, "%d/%m/%Y")
            if due_date < datetime.today():
                due_str += f" {RED}⚠️ Overdue{RESET}"
        except ValueError:
            pass
    progress_str = ""
    if cat=="habit" and "current" in item and "target" in item:
        unit = item.get("unit","times")
        progress_str = f" {BLUE}{progress_bar(item['current'], item['target'])} {unit}{RESET}"
    priority = item.get('priority','Medium')
    priority_icon_str = {"High": f"{RED}🔴{RESET}", "Medium": f"{YELLOW}🟡{RESET}", "Low": f"{GREEN}🟢{RESET}"}.get(priority, f"{YELLOW}🟡{RESET}")
    return f"{cat_color}{idx}. {get_emoji(item['category'], item['text'])} {item['text']} (Due: {due_str}){progress_str} Priority: {priority_icon_str} {priority}{RESET}"

# ---------------- CORE FUNCTIONS ----------------
def add_items(items):
    valid_categories = ["task", "habit", "expense"]
    while True:
        category = input("Enter category (Task/Habit/Expense): ").strip().lower()
        if category in valid_categories:
            break
        print("⚠️ Invalid category! Please enter Task, Habit, or Expense.")
    
    print("Enter item(s). Type one per line, Enter blank to finish:")
    entered_items = []

    while True:
        text = input("> ").strip()
        if not text:
            break

        due = input("Enter due date (DD/MM/YYYY) or leave blank: ").strip()
        if due and not validate_date(due):
            print("⚠️ Invalid date format! Skipping due date.")
            due = ""

        priority = input("Enter priority (High/Medium/Low, default Medium): ").strip().title()
        if priority not in ["High","Medium","Low"]:
            priority = "Medium"

        if category == "habit":
            # Detect unit
            unit = "times"  # default
            for key, u in HABIT_UNITS.items():
                if key in text.lower():
                    unit = u
                    break
            try:
                target = int(input(f"Enter target ({unit}): "))
                current_input = input(f"Enter current progress (default 0 {unit}): ").strip()
                current = int(current_input) if current_input else 0
            except ValueError:
                print(f"⚠️ Invalid number! Setting current=0, target=1 {unit}")
                current, target = 0,1
            entered_items.append({
                "category": category,
                "text": text,
                "due": due,
                "current": current,
                "target": target,
                "priority": priority,
                "unit": unit
            })
        else:
            entered_items.append({
                "category": category,
                "text": text,
                "due": due,
                "priority": priority
            })

    if not entered_items:
        print("❌ No items entered.")
    else:
        items.extend(entered_items)
        for i, item in enumerate(entered_items, start=len(items)-len(entered_items)+1):
            print(f"✅ Added: {format_item_colored(item, i)}")
        save_data(items)

def list_items(items):
    if not items:
        print("📂 No items yet!")
        return
    for idx, item in enumerate(items,1):
        print(format_item_colored(item,idx))

def update_item(items):
    list_items(items)
    if not items: return
    try:
        idx = int(input("Enter item number to update: "))
        if 1<=idx<=len(items):
            item = items[idx-1]
            item['text'] = input("Enter new description: ").strip()
            if item['category']=="habit" and "current" in item and "target" in item:
                try:
                    item['current'] = int(input(f"Enter current progress (0-{item['target']}): "))
                except ValueError:
                    print("⚠️ Invalid input, keeping previous progress.")
            item['priority'] = input("Enter priority (High/Medium/Low, default Medium): ").title() or item.get('priority','Medium')
            print("✅ Item updated!")
            save_data(items)
        else:
            print("⚠️ Invalid number")
    except ValueError:
        print("⚠️ Enter a valid number")

def delete_item(items):
    if not items:
        print("📂 No items to delete!")
        return
    while True:
        print("\n🗑️ DELETE MENU")
        print("1. Delete Single Item")
        print("2. Delete Multiple Items")
        print("3. Delete All Items")
        print("4. Back to Main Menu")

        choice = input("Choose option (1-4): ").strip()
        if choice=="1":
            for idx, item in enumerate(items,1): print(format_item_colored(item,idx))
            try:
                idx = int(input("Enter item number to delete: "))
                if 1<=idx<=len(items):
                    removed = items.pop(idx-1)
                    save_data(items)
                    print(f"🗑️ Deleted: {removed['text']}")
                else: print("⚠️ Invalid number")
            except ValueError:
                print("⚠️ Enter a valid number")
        elif choice=="2":
            for idx, item in enumerate(items,1): print(format_item_colored(item,idx))
            nums = input("Enter numbers to delete (comma-separated): ").strip()
            try:
                indices = sorted({int(n)-1 for n in nums.split(",") if n.strip().isdigit()}, reverse=True)
                for i in indices:
                    if 0<=i<len(items):
                        removed = items.pop(i)
                        print(f"🗑️ Deleted: {removed['text']}")
                save_data(items)
            except Exception as e:
                print(f"⚠️ Error deleting items: {e}")
        elif choice=="3":
            confirm = input("⚠️ Are you sure you want to delete ALL items? (Y/N): ").strip().lower()
            if confirm=="y":
                items.clear()
                save_data(items)
                print("🗑️ All items deleted!")
        elif choice=="4":
            break
        else:
            print("⚠️ Invalid choice, try again!")

def search_items(items):
    keyword = input("Enter keyword to search: ").strip().lower()
    results = [item for item in items if keyword in item['text'].lower()]
    if results:
        for idx, item in enumerate(results,1):
            print(format_item_colored(item,idx))
    else:
        print("❌ No match found.")

def view_stats(items):
    total = len(items)
    tasks = sum(1 for i in items if i['category']=="task")
    habits = sum(1 for i in items if i['category']=="habit")
    expenses = sum(1 for i in items if i['category']=="expense")
    print(f"Total Records: {total} | Tasks: {tasks} | Habits: {habits} | Expenses: {expenses}")

# ---------------- MAIN LOOP ----------------
def show_menu():
    print("\n1. Add Item(s)\n2. List items\n3. Update item\n4. Delete item\n5. Search items\n6. View Stats\n7. Exit")

def main():
    items = load_data()
    while True:
        show_menu()
        choice = input("Choose option (1-7): ").strip()
        if choice=="1": add_items(items)
        elif choice=="2": list_items(items)
        elif choice=="3": update_item(items)
        elif choice=="4": delete_item(items)
        elif choice=="5": search_items(items)
        elif choice=="6": view_stats(items)
        elif choice=="7":
            save_data(items)
            print("💾 Data saved. Goodbye!")
            break
        else:
            print("⚠️ Invalid option, try again!")

if __name__=="__main__":
    main()
