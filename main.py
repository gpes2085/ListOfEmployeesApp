import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):

        # Панель инструментов
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Добавить сотрудника
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_open_dialog = tk.Button(
            toolbar, bg='#d7d8e0', bd=0,
            image=self.add_img,
            command=self.open_dialog
        )
        btn_open_dialog.pack(side=tk.LEFT)

        # Обновить (или изменить) сотрудника
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_open_update_dialog = tk.Button(
            toolbar, bg='#d7d8e0', bd=0,
            image=self.update_img,
            command=self.open_update_dialog
        )
        btn_open_update_dialog.pack(side=tk.LEFT)

        # Поиск сотрудников по имени
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_open_search_dialog = tk.Button(
            toolbar, bg='#d7d8e0', bd=0,
            image=self.search_img,
            command=self.open_search_dialog
        )
        btn_open_search_dialog.pack(side=tk.LEFT)

        # Обновить список сотрудников
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(
            toolbar, bg='#d7d8e0', bd=0,
            image=self.refresh_img,
            command=self.view_records
        )
        btn_refresh.pack(side=tk.LEFT)

        # Удалить выбранных сотрудников
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(
            toolbar, bg='#d7d8e0', bd=0,
            image=self.delete_img,
            command=self.delete_records
        )
        btn_delete.pack(side=tk.RIGHT)

        # # Конец панели инструментов

        # Таблица (или список) сотрудников
        self.tree = ttk.Treeview(
            self, columns=['ID', 'name', 'tel', 'email', 'salary'],
            height=45, show='headings'
        )

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Заработная плата')

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack()

    def open_dialog(self):
        Child()

    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    def view_records(self):
        # Обновление списка сотрудников
        self.db.c.execute('''
        SELECT * FROM db
        ''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
            for row in self.db.c.fetchall()]

    def open_search_dialog(self):
        # Открытие дополнительного окна для произведения поиска сотрудников
        Search()

    def search_records(self, name):
        # Сам поиск и вывод найденных сотрудников в таблицу
        name = ('%' + name + '%')
        self.db.c.execute('''
        SELECT * FROM db WHERE name LIKE ?
        ''', (name,))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
            for row in self.db.c.fetchall()]

    def open_update_dialog(self):
        # Открытие дополнительного окна для обновления сотрудника
        if len(self.tree.selection()) == 1:
            Update()
        elif len(self.tree.selection()) > 1:
            messagebox.showerror(
                'Ошибка изменения строки',
                'Изменение позиции невозможно, '
                'должна быть выделена только одна строка.'
            )

    def update_record(self, name, tel, email, salary):
        # Само обновление сотрудника
        self.db.conn.execute('''
        UPDATE db SET name=?, tel=?, email=?, salary=? WHERE id=?
        ''', (
            name, tel, email, salary,
            self.tree.set(self.tree.selection()[0], '#1')
        ))
        self.db.conn.commit()
        self.view_records()

    def delete_records(self):
        # Само удаление выделенных записей
        for selection_item in self.tree.selection():
            self.db.c.execute('''
            DELETE FROM db WHERE id=?
            ''', (self.tree.set(selection_item, '#1'),))
            self.db.conn.commit()
        self.view_records()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_child()

    def init_child(self):
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail')
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text='Заработная плата')
        label_salary.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=80)

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)

        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        self.button_cancel = ttk.Button(self, text='Закрыть',
                                        command=self.destroy)
        self.button_cancel.place(x=280, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=170, y=170)
        self.btn_ok.bind(
            '<Button-1>',
            lambda event: app.records(
                self.entry_name.get(),
                self.entry_tel.get(),
                self.entry_email.get(),
                self.entry_salary.get()
            )
        )


class Update(Child):
    def __init__(self):
        super().__init__()
        self.view = app
        self.db = db
        self.init_edit()
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=160, y=170)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_record(self.entry_name.get(),
                                              self.entry_tel.get(),
                                              self.entry_email.get(),
                                              self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda event:
                      self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''
        SELECT * FROM db WHERE id=?
        ''', (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.view = app
        self.init_search()

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=80, y=50)
        btn_search.bind('<Button-1>', lambda event:
                        self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
        self.c.execute('''
        CREATE TABLE IF NOT EXISTS db (
            id INTEGER PRIMARY KEY,
            name TEXT,
            tel TEXT,
            email TEXT,
            salary REAL
        )
        ''')
        self.conn.commit()

    def insert_data(self, name, tel, email, salary):
        # Само добавление сотрудника
        self.c.execute('''
        INSERT INTO db (name, tel, email, salary) VALUES (?, ?, ?, ?)
        ''', (name, tel, email, salary))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('815x450')
    root.resizable(False, False)
    root.mainloop()
