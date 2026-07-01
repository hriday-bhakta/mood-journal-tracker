def date_verify(date):
    try:
        day, month, year = map(int, date.split('-'))
        if 1 <= day <= 31 and 1 <= month <= 12 and 99 >= year >= 0:
            return True
        else:
            return False
    except (ValueError, EOFError):
        return False
    
def check_mood(entry):
    mood_keywords = {
        "happy": ["happy", "joyful", "excited", "content"],
        "sad": ["sad", "unhappy", "depressed"],
        "angry": ["angry", "frustrated", "annoyed", "irritated"],
        "anxious": ["anxious", "nervous", "worried", "stressed"]
    }

    entry_lower = entry.lower()
    
    for mood, keywords in mood_keywords.items():
        for keyword in keywords:
            if keyword in entry_lower:
                return mood
    return None

def write():
    file_write = open("journal.txt", "a")
    while True:
        date = input("Enter the date (DD-MM-YY): ")
        if date_verify(date):
            break
        else:
            print("Invalid date format. Please try again.")
            continue

    entry = input("Write your journal entry: ")
    mood = check_mood(entry)

    file_write.write(f"Date: {date}\nMood: {mood if mood else 'Neutral'}\nEntry: {entry}\n\n")
    file_write.close()
    return


def view(date=None, keyword=None):
    try:
        with open("journal.txt", "r") as file_read:
            entries = file_read.read().strip().split("\n\n")
            filtered_entries = []

            for entry in entries:
                if date and f"Date: {date}" not in entry:
                    continue
                if keyword and keyword.lower() not in entry.lower():
                    continue
                filtered_entries.append(entry)

            if not filtered_entries:
                print("No entries found for the given criteria.")
            else:
                for entry in filtered_entries:
                    print(entry)
                    print("-" * 40)

    except FileNotFoundError:
        print("No journal entries found. Please write a new entry first.")
    return

def analytics():
    try:
        with open("journal.txt", "r") as file_read:
            entries = file_read.read().strip().split("\n\n")
            mood_count = {"happy": 0, "sad": 0, "angry": 0, "anxious": 0, "neutral": 0}

            for entry in entries:
                mood_line = next((line for line in entry.split("\n") if line.startswith("Mood:")), None)
                if mood_line:
                    mood = mood_line.split(": ")[1].lower()
                    if mood in mood_count:
                        mood_count[mood] += 1
                    else:
                        mood_count["neutral"] += 1

            print("Mood Analytics:")
            for mood, count in mood_count.items():
                if count > 0:
                    print(f"You were {mood.capitalize()} for {count} day(s).")

    except FileNotFoundError:
        print("No journal entries found. Please write a new entry first.")
    return

# main loop
while True:
    try:
        choice = int(input("\n\nEnter your choice:\n1. Write a new journal entry\n2. View Past Entries\n3. View Mood Analytics\n4. Exit\nChoice: "))
        
    except (ValueError, EOFError):
        print("Invalid input. Please enter a number.")
        continue
    
    except KeyboardInterrupt:
        sure = input("\nAre you sure you want to exit? (Type Y or yes to exit and anything else to continue): ")
        if sure.lower() == 'y' or sure.lower() == 'yes':
            print("Exiting the journal application. Goodbye!")
            break   
        else:
            continue

    else:
        if choice == 4:
            print("Exiting the journal application. Goodbye!")
            break

        elif choice == 1:
            write()
        elif choice == 2:
            while True:
                date = input("Enter the date to view entries for (DD-MM-YY), or press Enter to view all entries: ")
                if date_verify(date) or date=="":
                    break
                else:
                    print("Invalid date format. Please try again.")
                    continue
            keyword = input("Enter a keyword to search for, or press Enter to view all entries: ")
            view(date if date else None, keyword if keyword else None)
                   
                
        elif choice == 3:
            analytics()
            
        else:
            print("Invalid choice. Please select a valid option.")
            continue