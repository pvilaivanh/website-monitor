import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

# Database connection
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="monitor_db",
        user="user",
        password="password"
    )

# Refresh table data
def refresh():
    for row in tree.get_children():
        tree.delete(row)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT w.url, l.status, l.response_time, l.checked_at
        FROM logs l
        JOIN websites w ON l.website_id = w.id
        ORDER BY l.checked_at DESC
        LIMIT 20;
    """)

    data = cur.fetchall()

    for row in data:
        status_text = "UP" if row[1] == 200 else "DOWN"

        tree.insert("", "end", values=(
            row[0],
            status_text,
            f"{row[2]:.2f}s",
            row[3]
        ))

    cur.close()
    conn.close()

def auto_refresh():
    refresh()
    root.after(2000, auto_refresh)

# Add website
def add_website():
    url = url_entry.get().strip()

    if not url:
        messagebox.showerror("Error", "Enter a valid URL")
        return

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO websites (url)
            VALUES (%s)
            ON CONFLICT (url) DO NOTHING;
        """, (url,))
        conn.commit()
        messagebox.showinfo("Success", "Website added")
    except Exception as e:
        messagebox.showerror("Error", str(e))

    cur.close()
    conn.close()

    url_entry.delete(0, tk.END)
    refresh()

# Remove website
def remove_website():
    selected = tree.focus()

    if not selected:
        messagebox.showerror("Error", "Select a website to remove")
        return

    values = tree.item(selected, "values")
    url = values[0]

    conn = get_connection()
    cur = conn.cursor()

    try:
        # Get website ID
        cur.execute("SELECT id FROM websites WHERE url = %s", (url,))
        result = cur.fetchone()

        if result:
            website_id = result[0]

            # Delete logs first
            cur.execute("DELETE FROM logs WHERE website_id = %s", (website_id,))

            # Then delete website
            cur.execute("DELETE FROM websites WHERE id = %s", (website_id,))

            conn.commit()
            messagebox.showinfo("Success", "Website removed")
    except Exception as e:
        messagebox.showerror("Error", str(e))

    cur.close()
    conn.close()

    refresh()

# GUI window
root = tk.Tk()
root.title("Website Monitor Dashboard")
root.geometry("800x500")

# Table
columns = ("Website", "Status", "Response Time", "Checked At")

tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(fill=tk.BOTH, expand=True, pady=10)

# Input field
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

tk.Button(button_frame, text="Add Website", command=add_website).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Remove Website", command=remove_website).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Refresh", command=refresh).grid(row=0, column=2, padx=5)

# Initial load
auto_refresh()

# Run app
root.mainloop()