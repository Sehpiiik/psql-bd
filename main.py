from sqlalchemy.util import column_set

from imports import *


class Application:
    window_width = 1200
    window_height = 500

    def __init__(self, root):
        self.root = root
        self.root.title('Приложение для работы с базой данных')
        self.root.geometry(
            f'{self.window_width}x{self.window_height}+{(self.root.winfo_screenwidth() - self.window_width) // 2}+{(self.root.winfo_screenheight() - self.window_height) // 2}')
        self.root.resizable(False, False)
        self.root.iconbitmap(default='icon.ico')
        self.create_db_frame()

    def create_db_frame(self):
        self.clear_window()
        create_frame = ttk.Frame(self.root)
        create_frame.pack(fill=BOTH)
        label_create = ttk.Label(create_frame, text='Создать базу данных(Удалит предыдущую!)', font=("Arial", 12))
        label_create.pack(anchor="n", pady=15)
        button_create = ttk.Button(create_frame, text="", width=10, command=self.create_db)
        button_create.pack(anchor="n", pady=0)
        label_next = ttk.Label(create_frame, text='Перейти к редактированию', font=("Arial", 12))
        label_next.pack(anchor="s", pady=15)
        button_next = ttk.Button(create_frame, text="", width=10, command=self.manipulate_db_frame)
        button_next.pack(anchor="s", pady=0)

    def create_db(self):
        try:
            engine = create_engine(f'postgresql+psycopg://{user}:{password}@{host}/{db_name}', echo=True)
            try:
                Session = sessionmaker(bind=engine)
                with Session() as session:
                    session.query(func.public.create_tables()).all()
                    session.commit()
                messagebox.showinfo("Ура", "База данных успешно создана")
                self.manipulate_db_frame()
            except:
                Session = sessionmaker(bind=engine)
                with Session() as session:
                    session.execute(
                        text("SELECT delete_tables('list_of_films','artists','film_genres','film_roles');"))
                    session.commit()
                messagebox.showerror("Error::code 1", "Ошибка при создании базы данных. Удаляю существующую")
        except:
           messagebox.showerror("Error::code 0", "Неверные данные подключения")

    def manipulate_db_frame(self):
        try:
            engine = create_engine(f'postgresql+psycopg://{user}:{password}@{host}/{db_name}', echo=True)
        except:
            messagebox.showerror("Error::code 0", "Неверные данные подключения")
            self.create_db_frame()
        metadata = MetaData()
        metadata.reflect(bind=engine)
        remaining_tables = len(metadata.tables.keys())
        if remaining_tables == 0:
            messagebox.showerror("Error::code -1", "Вы еще не создали базу данных")
        else:
            self.clear_window()
            main_frame = ttk.Frame(self.root)
            main_frame.pack(fill=BOTH)

            label_delete = ttk.Label(main_frame, text='Очистить содержимое таблиц(ы)', font=("Arial", 12))
            label_delete.pack(anchor="n", pady=15)
            button_delete = ttk.Button(main_frame, text="", width=10, command=self.delete_db_frame)
            button_delete.pack(anchor="n", pady=0)

            label_select = ttk.Label(main_frame, text='Вывести содержимое таблиц', font=("Arial", 12))
            label_select.pack(anchor="n", pady=15)
            button_select = ttk.Button(main_frame, text="", width=10, command=self.select_frame)
            button_select.pack(anchor="n", pady=0)

            label_insert = ttk.Label(main_frame, text='Добавить новые данные в таблицы', font=("Arial", 12))
            label_insert.pack(anchor="n", pady=15)
            button_insert = ttk.Button(main_frame, text="", width=10, command=self.insert_select_frame)
            button_insert.pack(anchor="n", pady=0)

            label_update = ttk.Label(main_frame, text='Обновить содержимое таблиц', font=("Arial", 12))
            label_update.pack(anchor="n", pady=15)
            button_update = ttk.Button(main_frame, text="", width=10, command=self.update_select_frame)
            button_update.pack(anchor="n", pady=0)

    def delete_db_frame(self):
        self.clear_window()
        delete_frame = ttk.Frame(self.root)
        delete_frame.pack(fill=BOTH)
        position = {'padx': 6, 'pady': 6, 'anchor': NW}
        label_delete = ttk.Label(delete_frame, text='Выберите, какие таблицы хотите удалить', font=("Arial", 12))
        label_delete.pack(anchor="n", pady=15)

        table1_check = IntVar()
        table2_check = IntVar()
        table3_check = IntVar()
        table4_check = IntVar()
        table_check = [table1_check, table2_check, table3_check, table4_check]

        table1_checkbutton = ttk.Checkbutton(delete_frame, text="list_of_films", variable=table1_check)
        table1_checkbutton.pack(**position)

        table2_checkbutton = ttk.Checkbutton(delete_frame, text="artists", variable=table2_check)
        table2_checkbutton.pack(**position)

        table3_checkbutton = ttk.Checkbutton(delete_frame, text="film_genres", variable=table3_check)
        table3_checkbutton.pack(**position)

        table4_checkbutton = ttk.Checkbutton(delete_frame, text="film_roles", variable=table4_check)
        table4_checkbutton.pack(**position)

        button_delete = ttk.Button(delete_frame, text="Удалить", width=10, command=lambda: self.delete_db(table_check))
        button_delete.pack(anchor="n", pady=0)

        button_back = ttk.Button(delete_frame, text="Вернуться назад", width=20,
                                 command=lambda: self.manipulate_db_frame())
        button_back.pack(anchor="nw")

    def delete_db(self, table_check):
        try:
            engine = create_engine(f'postgresql+psycopg://{user}:{password}@{host}/{db_name}', echo=True)
            table_names = {'list_of_films': table_check[0].get(), 'artists': table_check[1].get(),
                           'film_genres': table_check[2].get(), 'film_roles': table_check[3].get()}
            to_delete = []
            try:
                Session = sessionmaker(bind=engine)
                for name in table_names:
                    if table_names[name] == 1:
                        to_delete.append(name)
                    else:
                        to_delete.append('')
                with Session() as session:
                    session.execute(text(
                        f"SELECT delete_tables('{to_delete[0]}','{to_delete[1]}','{to_delete[2]}','{to_delete[3]}');"))
                    session.commit()
                metadata = MetaData()
                metadata.reflect(bind=engine)
                remaining_tables = len(metadata.tables.keys())
                match remaining_tables:
                    case 0:
                        messagebox.showinfo("Ура", "База данных успешно удалена")
                        self.create_db_frame()
                    case 3:
                        messagebox.showinfo("Ура", f"Вы успешно удалили 1 таблицу")
                    case _:
                        messagebox.showinfo("Ура", f"Вы успешно удалили {4 - remaining_tables} таблиц")
            except:
                messagebox.showerror("Error::code 2", "Ошибка при удалении")
        except:
            messagebox.showerror("Error::code 0", "Неверные данные подключения")
            
    def select_frame(self):
        self.clear_window()
        position = {'padx': 6, 'pady': 6, 'anchor': NW}
        select_frame = ttk.Frame(self.root)
        select_frame.pack(fill=BOTH)
        label_select = ttk.Label(select_frame, text='Выберите, какие таблицы хотите вывести', font=("Arial", 12))
        label_select.pack(anchor="n", pady=15)

        select = StringVar()

        table1 = ttk.Radiobutton(select_frame, text="list_of_films", value="list_of_films", variable=select)
        table1.pack(**position)

        table2 = ttk.Radiobutton(select_frame, text="artists", value="artists", variable=select)
        table2.pack(**position)

        table3 = ttk.Radiobutton(select_frame, text="film_genres", value="film_genres", variable=select)
        table3.pack(**position)

        table4 = ttk.Radiobutton(select_frame, text="film_roles", value="film_roles", variable=select)
        table4.pack(**position)

        button_select = ttk.Button(select_frame, text="Вывести", width=10,
                                   command=lambda: self.displaying_frame(select))
        button_select.pack(anchor="n", pady=0)

        button_back = ttk.Button(select_frame, text="Вернуться назад", width=20,
                                 command=lambda: self.manipulate_db_frame())
        button_back.pack(anchor="nw")

    def displaying_frame(self, select):
        if select.get() == '':
            messagebox.showerror("Error::code 4", "Выберите хотя бы 1 таблицу")
        else:
            try:
                engine = create_engine(f'postgresql+psycopg://{user}:{password}@{host}/{db_name}', echo=True)
            except:
                messagebox.showerror("Error::code 0", "Неверные данные подключения")
                self.create_db_frame()
            metadata = MetaData()
            metadata.reflect(bind=engine)
            remaining_tables = metadata.tables.keys()
            if select.get() not in remaining_tables:
                messagebox.showerror("Error::code 4", "Такой таблицы нет")
            else:
                self.clear_window()
                displaying_frame = ttk.Frame(self.root)
                displaying_frame.pack(fill=BOTH)

                table_name = metadata.tables[select.get()]
                columns = tuple(table_name.columns.keys())
                table = ttk.Treeview(displaying_frame, columns=columns, show='headings')
                for column in columns:
                    table.heading(column, text=column)

                Session = sessionmaker(bind=engine)
                with Session() as session:
                    data = session.query(table_name)

                rows = data.all()
                for row in rows:
                    row = tuple(row)
                    table.insert('', 'end', values=row)

                table.pack()
                button_back = ttk.Button(displaying_frame, text="Вернуться назад", width=20,
                                         command=lambda: self.select_frame())
                button_back.pack(anchor="nw")

    def insert_select_frame(self):
        self.clear_window()
        position = {'padx': 6, 'pady': 6, 'anchor': NW}
        insert_select_frame = ttk.Frame(self.root)
        insert_select_frame.pack(fill=BOTH)
        label_select_insert = ttk.Label(insert_select_frame, text='Выберите, в какую таблицу вы хотите добавить данные',
                                        font=("Arial", 12))
        label_select_insert.pack(anchor="n", pady=15)

        select = StringVar()

        table1_btn = ttk.Radiobutton(insert_select_frame, text="list_of_films", value="list_of_films", variable=select)
        table1_btn.pack(**position)

        table2_btn = ttk.Radiobutton(insert_select_frame, text="artists", value="artists", variable=select)
        table2_btn.pack(**position)

        table3_btn = ttk.Radiobutton(insert_select_frame, text="film_genres", value="film_genres", variable=select)
        table3_btn.pack(**position)

        table4_btn = ttk.Radiobutton(insert_select_frame, text="film_roles", value="film_roles", variable=select)
        table4_btn.pack(**position)

        button_select = ttk.Button(insert_select_frame, text="Выбрать", width=10,
                                   command=lambda: self.inserting_frame(select))
        button_select.pack(anchor="n", pady=0)

        button_back = ttk.Button(insert_select_frame, text="Вернуться назад", width=20,
                                 command=lambda: self.manipulate_db_frame())
        button_back.pack(anchor="nw")

    def inserting_frame(self, select):
        if select.get() == '':
            messagebox.showerror("Error::code 4", "Выберите хотя бы 1 таблицу")
        else:
            try:
                engine = create_engine(f'postgresql+psycopg://{user}:{password}@{host}/{db_name}', echo=True)
            except:
                messagebox.showerror("Error::code 0", "Неверные данные подключения")
                self.create_db_frame()
            metadata = MetaData()
            metadata.reflect(bind=engine)
            remaining_tables = metadata.tables.keys()
            if select.get() not in remaining_tables:
                messagebox.showerror("Error::code 4", "Такой таблицы нет")
            else:
                self.clear_window()
                inserting_frame = ttk.Frame(self.root)
                inserting_frame.pack(fill=BOTH)

                table_name = metadata.tables[select.get()]
                columns = table_name.columns.keys()
                columns.pop(0)
                if select.get() == 'artists':
                    columns.pop(4)
                columns = tuple(columns)
                widgets = []
                for column in columns:
                    column_label = ttk.Label(inserting_frame, text=column, font=("Arial", 12))
                    entry = ttk.Entry(inserting_frame, width=100, justify=LEFT, font=("Arial", 12))
                    widgets.append((column_label, entry))

                for label, entry in widgets:
                    label.pack(anchor="nw")
                    entry.pack(anchor="nw")

                button_add = ttk.Button(inserting_frame, text="Добавить", width=20,
                                        command=lambda: self.add_raw(select.get(), widgets))
                button_add.pack(anchor="nw")

                button_back = ttk.Button(inserting_frame, text="Вернуться назад", width=20,
                                         command=lambda: self.insert_select_frame())
                button_back.pack(anchor="nw")

    def add_raw(self, table_name, widgets):
        try:
            engine = create_engine(f'postgresql+psycopg://{user}:{password}@{host}/{db_name}', echo=True)
        except:
            messagebox.showerror("Error::code 0", "Неверные данные подключения")
            self.create_db_frame()
        try:
            columns = []
            entries = []
            for label, entry in widgets:
                column = "'" + label.cget('text') + "'"
                value = "'" + entry.get() + "'"
                columns.append(column)
                entries.append(value)
            col_ins = ','.join(columns)
            entr_ins = ','.join(entries)
            Session = sessionmaker(bind=engine)
            with Session() as session:
                session.execute(text(
                    f"SELECT dynamic_insert('{table_name}',ARRAY[{col_ins}],ARRAY[{entr_ins}]);"))
                session.commit()
            messagebox.showinfo("Ура", "Вставка прошла успешно")
        except:
            messagebox.showerror("Error::code 5", "Ошибка при вставке")

    def update_select_frame(self):
        self.clear_window()
        position = {'padx': 6, 'pady': 6, 'anchor': NW}
        update_select_frame = ttk.Frame(self.root)
        update_select_frame.pack(fill=BOTH)
        label_select_insert = ttk.Label(update_select_frame, text='Выберите, в какой таблице вы хотите обновить данные',
                                        font=("Arial", 12))
        label_select_insert.pack(anchor="n", pady=15)

        select = StringVar()

        table1_btn = ttk.Radiobutton(update_select_frame, text="list_of_films", value="list_of_films", variable=select)
        table1_btn.pack(**position)

        table2_btn = ttk.Radiobutton(update_select_frame, text="artists", value="artists", variable=select)
        table2_btn.pack(**position)

        table3_btn = ttk.Radiobutton(update_select_frame, text="film_genres", value="film_genres", variable=select)
        table3_btn.pack(**position)

        table4_btn = ttk.Radiobutton(update_select_frame, text="film_roles", value="film_roles", variable=select)
        table4_btn.pack(**position)

        button_select = ttk.Button(update_select_frame, text="Выбрать", width=10,
                                   command=lambda: self.updating_frame(select))
        button_select.pack(anchor="n", pady=0)

        button_back = ttk.Button(update_select_frame, text="Вернуться назад", width=20,
                                 command=lambda: self.manipulate_db_frame())
        button_back.pack(anchor="nw")

    def updating_frame(self, select):
        if select.get() == '':
            messagebox.showerror("Error::code 4", "Выберите хотя бы 1 таблицу")
        else:
            try:
                engine = create_engine(f'postgresql+psycopg://{user}:{password}@{host}/{db_name}', echo=True)
            except:
                messagebox.showerror("Error::code 0", "Неверные данные подключения")
                self.create_db_frame()
            metadata = MetaData()
            metadata.reflect(bind=engine)
            remaining_tables = metadata.tables.keys()
            if select.get() not in remaining_tables:
                messagebox.showerror("Error::code 4", "Такой таблицы нет")
            else:
                self.clear_window()
                updating_frame = ttk.Frame(self.root)
                updating_frame.pack(fill=BOTH)

                table_name = metadata.tables[select.get()]
                columns = table_name.columns.keys()
                id_name = columns[0]
                columns.pop(0)
                if select.get() == 'artists':
                    columns.pop(4)
                columns = tuple(columns)
                widgets = []
                for column in columns:
                    column_label = ttk.Label(updating_frame, text=column, font=("Arial", 12))
                    entry = ttk.Entry(updating_frame, width=100, justify=LEFT, font=("Arial", 12))
                    widgets.append((column_label, entry))

                for label, entry in widgets:
                    label.pack(anchor="nw")
                    entry.pack(anchor="nw")

                id_select_label = ttk.Label(updating_frame,
                                            text=f"Введите значение {id_name}, которое вы хотите обновить",
                                            font=("Arial", 12))
                id_select_label.pack(anchor="nw")
                id_entry = ttk.Entry(updating_frame, width=100, justify=LEFT, font=("Arial", 12))
                id_entry.pack(anchor="nw")

                button_up = ttk.Button(updating_frame, text="Обновить", width=20,
                                        command=lambda: self.update_raw(select.get(), widgets,id_name,id_entry.get()))
                button_up.pack(anchor="nw")

                button_back = ttk.Button(updating_frame, text="Вернуться назад", width=20,
                                         command=lambda: self.update_select_frame())
                button_back.pack(anchor="nw")

    def update_raw(self, table_name, widgets,id_name,id_entry):
        try:
            engine = create_engine(f'postgresql+psycopg://{user}:{password}@{host}/{db_name}', echo=True)
            try:
                id_name = "'" + id_name + "'"
                id_entry = "'" + id_entry + "'"
                columns = []
                entries = []
                for label, entry in widgets:
                    column = "'" + label.cget('text') + "'"
                    value = "'" + entry.get() + "'"
                    columns.append(column)
                    entries.append(value)
                col_up = ','.join(columns)
                entr_up = ','.join(entries)
                Session = sessionmaker(bind=engine)
                with Session() as session:
                    session.execute(text(
                        f"SELECT dynamic_update('{table_name}',{id_name},{id_entry},ARRAY[{col_up}],ARRAY[{entr_up}]);"))
                    session.commit()
                messagebox.showinfo("Ура", "Обновление прошло успешно")
            except:
                messagebox.showerror("Error::code 6", "Ошибка при обновлении")
                self.create_db_frame()
        except:
            messagebox.showerror("Error::code 0", "Неверные данные подключения")
            self.create_db_frame()


    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start(self):
        self.root.mainloop()


def main():
    root = Tk()
    app = Application(root)
    app.start()


if __name__ == "__main__":
    main()
