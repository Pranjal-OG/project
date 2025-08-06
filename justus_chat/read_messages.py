import sqlite3

conn = sqlite3.connect("messages.db")
cursor = conn.cursor()

cursor.execute("SELECT sender, message, timestamp FROM messages ORDER BY id ASC")
rows = cursor.fetchall()

if rows:
    for row in rows:
        print(f"[{row[2]}] {row[0]}: {row[1]}")

    # Print the last message again
    last_sender, last_message, last_timestamp = rows[-1]
    print("\n👉 Last Message: [{}] {}: {}".format(last_timestamp, last_sender, last_message))
else:
    print("⚠️ No messages found in the database.")

conn.close()
print("✅ Messages read successfully!")
