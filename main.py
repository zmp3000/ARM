import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="curs",
            user="postgres",
            password="1133",
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка подключения", f"Ошибка: {e}")
        return None

def create_weapon(weapon_data):
    try:
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Оружие ("Название модели", "Тип оружия", "Страна производства", "Калибр")
                VALUES (%s, %s, %s, %s)
            """, weapon_data)
            conn.commit()
            messagebox.showinfo("Успешно", "Запись успешно создана")
            conn.close()
            update_listboxes()
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка: {e}")

def create_recipient(recipient_data):
    try:
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Получатели ("Название", "Страна")
                VALUES (%s, %s)
            """, recipient_data)
            conn.commit()
            messagebox.showinfo("Успешно", "Запись успешно создана")
            conn.close()
            update_recipient_listbox()
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка: {e}")

def view_weapons():
    try:
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Оружие")
            weapons = cursor.fetchall()
            conn.close()
            return weapons
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка: {e}")
        return []

def view_recipients():
    try:
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Получатели")
            recipients = cursor.fetchall()
            conn.close()
            return recipients
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка: {e}")
        return []

def delete_weapon(record_id):
    try:
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Оружие WHERE \"ID_оружия\" = %s", (record_id,))
            conn.commit()
            messagebox.showinfo("Успешно", "Запись успешно удалена")
            conn.close()
            update_listboxes()
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка: {e}")

def delete_recipient(record_id):
    try:
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Получатели WHERE \"ID_получателя\" = %s", (record_id,))
            conn.commit()
            messagebox.showinfo("Успешно", "Запись успешно удалена")
            conn.close()
            update_recipient_listbox()
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка: {e}")

def edit_weapon(weapon_data):
    try:
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Оружие
                SET "Название модели" = %s, "Тип оружия" = %s, "Страна производства" = %s, "Калибр" = %s
                WHERE "ID_оружия" = %s
            """, weapon_data)
            conn.commit()
            messagebox.showinfo("Успешно", "Запись успешно отредактирована")
            conn.close()
            update_listboxes()
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка: {e}")

def edit_recipient(recipient_data):
    try:
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Получатели
                SET "Название" = %s, "Страна" = %s
                WHERE "ID_получателя" = %s
            """, recipient_data)
            conn.commit()
            messagebox.showinfo("Успешно", "Запись успешно отредактирована")
            conn.close()
            update_recipient_listbox()
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка: {e}")

def create_weapon_handler():
    weapon_data = (
        entry_model.get(),
        entry_type.get(),
        entry_country.get(),
        entry_caliber.get()
    )
    create_weapon(weapon_data)

def create_recipient_handler():
    recipient_data = (
        entry_recipient_name.get(),
        entry_recipient_country.get()
    )
    create_recipient(recipient_data)

def delete_weapon_handler():
    selected_item = listbox_weapons.curselection()
    if selected_item:
        record_id = listbox_weapons.get(selected_item)[0]
        delete_weapon(record_id)
    else:
        messagebox.showwarning("Ошибка", "Выберите запись для удаления")

def delete_recipient_handler():
    selected_item = listbox_recipients.curselection()
    if selected_item:
        record_id = listbox_recipients.get(selected_item)[0]
        delete_recipient(record_id)
    else:
        messagebox.showwarning("Ошибка", "Выберите запись для удаления")

def edit_weapon_handler():
    record_id = entry_edit_weapon_id.get()
    if record_id:
        weapon_data = (
            entry_model.get(),
            entry_type.get(),
            entry_country.get(),
            entry_caliber.get(),
            record_id
        )
        edit_weapon(weapon_data)
    else:
        messagebox.showwarning("Ошибка", "Введите ID записи для редактирования")

def edit_recipient_handler():
    record_id = entry_edit_recipient_id.get()
    if record_id:
        recipient_data = (
            entry_recipient_name.get(),
            entry_recipient_country.get(),
            record_id
        )
        edit_recipient(recipient_data)
    else:
        messagebox.showwarning("Ошибка", "Введите ID записи для редактирования")

def update_listboxes():
    listbox_weapons.delete(0, tk.END)
    weapons = view_weapons()
    for weapon in weapons:
        listbox_weapons.insert(tk.END, weapon)

def update_recipient_listbox():
    listbox_recipients.delete(0, tk.END)
    recipients = view_recipients()
    for recipient in recipients:
        listbox_recipients.insert(tk.END, recipient)

root = tk.Tk()
root.geometry("1000x800")
root.title("Управление оружием и получателями")

frame_weapon = ttk.LabelFrame(root, text="Создать запись оружия")
frame_weapon.grid(row=0, column=0, padx=10, pady=5, sticky="w")

label_model = ttk.Label(frame_weapon, text="Название модели:")
label_type = ttk.Label(frame_weapon, text="Тип оружия:")
label_country = ttk.Label(frame_weapon, text="Страна производства:")
label_caliber = ttk.Label(frame_weapon, text="Калибр:")

entry_model = ttk.Entry(frame_weapon)
entry_type = ttk.Entry(frame_weapon)
entry_country = ttk.Entry(frame_weapon)
entry_caliber = ttk.Entry(frame_weapon)

button_create_weapon = ttk.Button(frame_weapon, text="Создать запись", command=create_weapon_handler)

label_model.grid(row=0, column=0, sticky="e", padx=5, pady=2)
label_type.grid(row=1, column=0, sticky="e", padx=5, pady=2)
label_country.grid(row=2, column=0, sticky="e", padx=5, pady=2)
label_caliber.grid(row=3, column=0, sticky="e", padx=5, pady=2)
entry_model.grid(row=0, column=1, padx=5, pady=2)
entry_type.grid(row=1, column=1, padx=5, pady=2)
entry_country.grid(row=2, column=1, padx=5, pady=2)
entry_caliber.grid(row=3, column=1, padx=5, pady=2)
button_create_weapon.grid(row=4, columnspan=2, pady=5)

frame_edit_weapon = ttk.LabelFrame(root, text="Редактировать запись оружия")
frame_edit_weapon.grid(row=0, column=1, padx=10, pady=5, sticky="w")

label_edit_weapon_id = ttk.Label(frame_edit_weapon, text="ID_оружия:")
label_edit_weapon_id.grid(row=0, column=0, sticky="e", padx=5, pady=2)

entry_edit_weapon_id = ttk.Entry(frame_edit_weapon)
entry_edit_weapon_id.grid(row=0, column=1, padx=5, pady=2)

button_edit_weapon = ttk.Button(frame_edit_weapon, text="Редактировать запись", command=edit_weapon_handler)
button_edit_weapon.grid(row=1, columnspan=2, pady=5)

frame_recipient = ttk.LabelFrame(root, text="Создать запись получателя")
frame_recipient.grid(row=1, column=0, padx=10, pady=5, sticky="w")

label_recipient_name = ttk.Label(frame_recipient, text="Название:")
label_recipient_country = ttk.Label(frame_recipient, text="Страна:")

entry_recipient_name = ttk.Entry(frame_recipient)
entry_recipient_country = ttk.Entry(frame_recipient)

button_create_recipient = ttk.Button(frame_recipient, text="Создать запись", command=create_recipient_handler)

label_recipient_name.grid(row=0, column=0, sticky="e", padx=5, pady=2)
label_recipient_country.grid(row=1, column=0, sticky="e", padx=5, pady=2)
entry_recipient_name.grid(row=0, column=1, padx=5, pady=2)
entry_recipient_country.grid(row=1, column=1, padx=5, pady=2)
button_create_recipient.grid(row=2, columnspan=2, pady=5)

frame_edit_recipient = ttk.LabelFrame(root, text="Редактировать запись получателя")
frame_edit_recipient.grid(row=1, column=1, padx=10, pady=5, sticky="w")

label_edit_recipient_id = ttk.Label(frame_edit_recipient, text="ID_получателя:")
label_edit_recipient_id.grid(row=0, column=0, sticky="e", padx=5, pady=2)

entry_edit_recipient_id = ttk.Entry(frame_edit_recipient)
entry_edit_recipient_id.grid(row=0, column=1, padx=5, pady=2)

button_edit_recipient = ttk.Button(frame_edit_recipient, text="Редактировать запись", command=edit_recipient_handler)
button_edit_recipient.grid(row=1, columnspan=2, pady=5)

frame_lists = ttk.LabelFrame(root, text="Список оружия")
frame_lists.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")



listbox_weapons = tk.Listbox(frame_lists, width=50)
listbox_weapons.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")

button_delete_weapon = ttk.Button(frame_lists, text="Удалить запись", command=delete_weapon_handler)
button_delete_weapon.grid(row=1, column=0, pady=5)

frame_recipient_lists = ttk.LabelFrame(root, text="Список получателей" )
frame_recipient_lists.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")

listbox_recipients = tk.Listbox(frame_recipient_lists, width=50)
listbox_recipients.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")

button_delete_recipient = ttk.Button(frame_recipient_lists, text="Удалить запись", command=delete_recipient_handler)
button_delete_recipient.grid(row=1, column=0, pady=5)

def create_delivery(delivery_data):
    try:
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Поставки ("ID_оружия", "ID_получателя", "Дата поставки", "Количество")
                VALUES (%s, %s, %s, %s)
            """, delivery_data)
            conn.commit()
            messagebox.showinfo("Успешно", "Запись успешно создана")
            conn.close()
            update_delivery_listbox()
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка: {e}")

def view_deliveries():
    try:
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Поставки")
            deliveries = cursor.fetchall()
            conn.close()
            return deliveries
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка: {e}")
        return []

def delete_delivery(record_id):
    try:
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Поставки WHERE \"ID_поставки\" = %s", (record_id,))
            conn.commit()
            messagebox.showinfo("Успешно", "Запись успешно удалена")
            conn.close()
            update_delivery_listbox()
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка: {e}")

def edit_delivery(delivery_data):
    try:
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Поставки
                SET "ID_оружия" = %s, "ID_получателя" = %s, "Дата поставки" = %s, "Количество" = %s
                WHERE "ID_поставки" = %s
            """, delivery_data)
            conn.commit()
            messagebox.showinfo("Успешно", "Запись успешно отредактирована")
            conn.close()
            update_delivery_listbox()
    except psycopg2.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка: {e}")

def create_delivery_handler():
    delivery_data = (
        entry_delivery_weapon_id.get(),
        entry_delivery_recipient_id.get(),
        entry_delivery_date.get(),
        entry_delivery_quantity.get()
    )
    create_delivery(delivery_data)

def delete_delivery_handler():
    selected_item = listbox_deliveries.curselection()
    if selected_item:
        record_id = listbox_deliveries.get(selected_item)[0]
        delete_delivery(record_id)
    else:
        messagebox.showwarning("Ошибка", "Выберите запись для удаления")

def edit_delivery_handler():
    record_id = entry_edit_delivery_id.get()
    if record_id:
        delivery_data = (
            entry_delivery_weapon_id.get(),
            entry_delivery_recipient_id.get(),
            entry_delivery_date.get(),
            entry_delivery_quantity.get(),
            record_id
        )
        edit_delivery(delivery_data)
    else:
        messagebox.showwarning("Ошибка", "Введите ID записи для редактирования")

def update_delivery_listbox():
    listbox_deliveries.delete(0, tk.END)
    deliveries = view_deliveries()
    for delivery in deliveries:
        listbox_deliveries.insert(tk.END, delivery)



frame_deliveries = ttk.LabelFrame(root, text="Работа с поставками")
frame_deliveries.grid(row=2, column=0, padx=10, pady=5, sticky="w")

# Названия полей для ввода данных поставки
label_delivery_weapon_id = ttk.Label(frame_deliveries, text="ID_оружия:")
label_delivery_recipient_id = ttk.Label(frame_deliveries, text="ID_получателя:")
label_delivery_date = ttk.Label(frame_deliveries, text="Дата поставки:")
label_delivery_quantity = ttk.Label(frame_deliveries, text="Количество:")

# Поля для ввода данных поставки
entry_delivery_weapon_id = ttk.Entry(frame_deliveries)
entry_delivery_recipient_id = ttk.Entry(frame_deliveries)
entry_delivery_date = ttk.Entry(frame_deliveries)
entry_delivery_quantity = ttk.Entry(frame_deliveries)

# Кнопка для создания записи поставки
button_create_delivery = ttk.Button(frame_deliveries, text="Создать запись", command=create_delivery_handler)

# Кнопка для удаления записи поставки
button_delete_delivery = ttk.Button(frame_deliveries, text="Удалить запись", command=delete_delivery_handler)

# Фрейм для редактирования записи поставки
frame_edit_delivery = ttk.LabelFrame(root, text="Редактировать поставку")
frame_edit_delivery.grid(row=2, column=1, padx=10, pady=2, sticky="w")

# Название поля для ввода ID записи для редактирования
label_edit_delivery_id = ttk.Label(frame_edit_delivery, text="ID записи:")
entry_edit_delivery_id = ttk.Entry(frame_edit_delivery)

# Кнопка для редактирования записи поставки
button_edit_delivery = ttk.Button(frame_edit_delivery, text="Редактировать запись", command=edit_delivery_handler)

# Размещение виджетов для создания записей поставки на форме
label_delivery_weapon_id.grid(row=0, column=0, sticky="e", padx=5, pady=2)
label_delivery_recipient_id.grid(row=1, column=0, sticky="e", padx=5, pady=2)
label_delivery_date.grid(row=2, column=0, sticky="e", padx=5, pady=2)
label_delivery_quantity.grid(row=3, column=0, sticky="e", padx=5, pady=2)
entry_delivery_weapon_id.grid(row=0, column=1, padx=5, pady=2)
entry_delivery_recipient_id.grid(row=1, column=1, padx=5, pady=2)
entry_delivery_date.grid(row=2, column=1, padx=5, pady=2)
entry_delivery_quantity.grid(row=3, column=1, padx=5, pady=2)
button_create_delivery.grid(row=4, columnspan=2, pady=5)
button_delete_delivery.grid(row=5, columnspan=2, pady=5)

# Размещение виджетов для редактирования записи поставки на форме
label_edit_delivery_id.grid(row=0, column=0, sticky="e", padx=5, pady=2)
entry_edit_delivery_id.grid(row=0, column=1, padx=5, pady=2)
button_edit_delivery.grid(row=1, columnspan=2, pady=5)

# Создание списка для отображения данных поставок
frame_deliveries_list = ttk.LabelFrame(root, text="Список поставок", width=100, height=100)
frame_deliveries_list.grid(row=2, column=2, rowspan=2, padx=10, pady=5, sticky="nsew")
frame_deliveries_list.grid_propagate(False)  # Устанавливаем фиксированный размер фрейма
frame_deliveries_list.config(width=100, height=100)


listbox_deliveries = tk.Listbox(frame_deliveries_list, width=50)
listbox_deliveries.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")

# Обновление данных в списках поставок
def update_deliveries_listbox():
    listbox_deliveries.delete(0, tk.END)
    deliveries = view_deliveries()
    for delivery in deliveries:
        listbox_deliveries.insert(tk.END, delivery)

# Вызов функции для обновления данных в списке поставок
update_deliveries_listbox()

# Установка возможности масштабирования и размеров окна
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)












update_listboxes()
update_recipient_listbox()

root.mainloop()
