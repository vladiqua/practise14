import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, font

# ---------- Базовый класс Restaurant (из 13 работы) ----------
class Restaurant:
    def __init__(self, restaurant_name, cuisine_type, rating=0):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type
        self.rating = rating

    def describe_restaurant(self):
        print(f"Ресторан '{self.restaurant_name}' | Кухня: {self.cuisine_type} | Рейтинг: {self.rating}")

    def open_restaurant(self):
        print(f"{self.restaurant_name} открыт!")

    def update_rating(self, new_rating):
        self.rating = new_rating
        print(f"Рейтинг ресторана '{self.restaurant_name}' обновлён до {self.rating}")

# ---------- Класс IceCreamStand (14.1 и 14.2) ----------
class IceCreamStand(Restaurant):
    def __init__(self, name, location, hours, cuisine_type='мороженое'):
        super().__init__(name, cuisine_type)
        self.location = location
        self.hours = hours
        self.flavors = ['ваниль', 'шоколад', 'клубника', 'пломбир']

        # Типы мороженого (задание 14.2)
        self.ice_cream_types = {
            'рожок': self.flavors.copy(),
            'стаканчик': self.flavors.copy(),
            'эскимо': ['шоколад', 'пломбир', 'крем-брюле']
        }

    def display_flavors(self):
        print("Сорта мороженого:")
        for f in self.flavors:
            print(f"- {f}")

    def add_flavor(self, flavor):
        if flavor not in self.flavors:
            self.flavors.append(flavor)
            print(f"Добавлен сорт '{flavor}'")
        else:
            print(f"Сорт '{flavor}' уже есть")

    def remove_flavor(self, flavor):
        if flavor in self.flavors:
            self.flavors.remove(flavor)
            print(f"Удалён сорт '{flavor}'")
        else:
            print(f"Сорт '{flavor}' не найден")

    def check_flavor(self, flavor):
        exists = flavor in self.flavors
        print(f"Сорт '{flavor}': {'есть' if exists else 'нет'}")
        return exists

    def add_flavor_to_type(self, ice_type, flavor):
        if ice_type in self.ice_cream_types:
            if flavor not in self.ice_cream_types[ice_type]:
                self.ice_cream_types[ice_type].append(flavor)
                print(f"В тип '{ice_type}' добавлен вкус '{flavor}'")
            else:
                print(f"Вкус '{flavor}' уже есть в типе '{ice_type}'")
        else:
            print(f"Тип '{ice_type}' не поддерживается. Доступные: {list(self.ice_cream_types.keys())}")

    def remove_flavor_from_type(self, ice_type, flavor):
        if ice_type in self.ice_cream_types:
            if flavor in self.ice_cream_types[ice_type]:
                self.ice_cream_types[ice_type].remove(flavor)
                print(f"Из типа '{ice_type}' удалён вкус '{flavor}'")
            else:
                print(f"Вкус '{flavor}' не найден в типе '{ice_type}'")
        else:
            print(f"Тип '{ice_type}' не поддерживается")

    def show_menu_by_type(self):
        print(f"\nКафе '{self.restaurant_name}' ({self.location}, {self.hours})")
        for t, flavors in self.ice_cream_types.items():
            print(f"{t.capitalize()}: {', '.join(flavors)}")

# ---------- 14.3 Цветной GUI с цветком ----------
class IceCreamGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 Кафе-мороженое Сластёна 🌸")
        self.root.geometry("550x600")
        self.root.configure(bg='#FFF0F5')  # Лавандово-розовый фон

        # 1. Сначала создаём объект кафе (чтобы он был доступен для update_listbox и других методов)
        self.shop = IceCreamStand("Сластёна", "ул. Центральная, 10", "10:00–22:00")

        # Яркие цвета
        self.bg_color = '#FFF0F5'      # нежно-розовый
        self.btn_color = '#FFB6C1'     # светло-розовый
        self.btn_active = '#FF69B4'    # горячий розовый
        self.fg_color = '#8B4513'      # коричневый (текст)
        self.listbox_bg = '#FFFFE0'    # кремовый
        self.header_font = font.Font(family='Comic Sans MS', size=14, weight='bold')
        self.normal_font = font.Font(family='Segoe UI', size=10)

        # --- Цветок в правом верхнем углу (эмодзи) ---
        flower_label = tk.Label(root, text="🌸", font=("Segoe UI", 28, "bold"), bg=self.bg_color, fg='#FF1493')
        flower_label.place(relx=0.95, rely=0.02, anchor='ne')

        # --- Заголовок ---
        title = tk.Label(root, text="🍦 Добро пожаловать в наше кафе! 🍧",
                         font=self.header_font, bg=self.bg_color, fg='#D2691E')
        title.pack(pady=10)

        # --- Список вкусов ---
        tk.Label(root, text="🍨 Наши сорта мороженого", font=self.normal_font, bg=self.bg_color, fg=self.fg_color).pack(pady=5)
        frame_list = tk.Frame(root, bg=self.bg_color)
        frame_list.pack(pady=5)
        self.listbox = Listbox(frame_list, width=40, height=8, font=self.normal_font,
                               bg=self.listbox_bg, fg=self.fg_color, selectbackground='#FFB6C1')
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar = Scrollbar(frame_list, command=self.listbox.yview, bg=self.btn_color)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.update_listbox()   # теперь shop уже существует

        # --- Поле ввода ---
        tk.Label(root, text="🍭 Название вкуса:", font=self.normal_font, bg=self.bg_color, fg=self.fg_color).pack(pady=5)
        self.entry = tk.Entry(root, width=30, font=self.normal_font, bg='#FFFFFF', relief='groove')
        self.entry.pack()

        # --- Кнопки управления вкусами ---
        btn_frame = tk.Frame(root, bg=self.bg_color)
        btn_frame.pack(pady=10)
        self.create_button(btn_frame, "➕ Добавить", self.add_flavor, '#98FB98')
        self.create_button(btn_frame, "➖ Удалить", self.remove_flavor, '#FFA07A')
        self.create_button(btn_frame, "🔍 Проверить", self.check_flavor, '#87CEFA')

        # --- Управление типами мороженого ---
        tk.Label(root, text="🍧 Типы мороженого (рожок / стаканчик / эскимо)",
                 font=self.normal_font, bg=self.bg_color, fg=self.fg_color).pack(pady=10)
        type_frame = tk.Frame(root, bg=self.bg_color)
        type_frame.pack()
        self.type_entry = tk.Entry(type_frame, width=12, font=self.normal_font, bg='#FFFACD')
        self.type_entry.insert(0, "тип")
        self.type_entry.pack(side=tk.LEFT, padx=5)
        self.flavor_type_entry = tk.Entry(type_frame, width=12, font=self.normal_font, bg='#FFFACD')
        self.flavor_type_entry.insert(0, "вкус")
        self.flavor_type_entry.pack(side=tk.LEFT, padx=5)

        self.create_button(type_frame, "➕ Добавить в тип", self.add_to_type, '#DDA0DD')
        self.create_button(type_frame, "➖ Удалить из типа", self.remove_from_type, '#F0E68C')
        self.create_button(root, "📋 Показать всё меню по типам", self.show_types, '#FFDAB9', pady=10)

    def create_button(self, parent, text, command, color, pady=0):
        btn = tk.Button(parent, text=text, command=command, font=self.normal_font,
                        bg=color, fg='#4B0082', activebackground='#FF69B4',
                        relief='raised', bd=3, padx=10, pady=3)
        if pady:
            btn.pack(pady=pady)
        else:
            btn.pack(side=tk.LEFT, padx=5)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for f in self.shop.flavors:
            self.listbox.insert(tk.END, f)

    def add_flavor(self):
        name = self.entry.get().strip().lower()
        if name:
            self.shop.add_flavor(name)
            self.update_listbox()
            messagebox.showinfo("Успех", f"Сорт '{name}' добавлен!")
        else:
            messagebox.showwarning("Ошибка", "Введите название вкуса")

    def remove_flavor(self):
        name = self.entry.get().strip().lower()
        if name:
            self.shop.remove_flavor(name)
            self.update_listbox()
            messagebox.showinfo("Успех", f"Сорт '{name}' удалён")
        else:
            messagebox.showwarning("Ошибка", "Введите название вкуса")

    def check_flavor(self):
        name = self.entry.get().strip().lower()
        if name:
            exists = self.shop.check_flavor(name)
            messagebox.showinfo("Результат", f"Сорт '{name}': {'✅ есть' if exists else '❌ нет'}")
        else:
            messagebox.showwarning("Ошибка", "Введите название вкуса")

    def add_to_type(self):
        t = self.type_entry.get().strip().lower()
        f = self.flavor_type_entry.get().strip().lower()
        if t and f:
            self.shop.add_flavor_to_type(t, f)
            messagebox.showinfo("Успех", f"В тип '{t}' добавлен вкус '{f}'")
        else:
            messagebox.showwarning("Ошибка", "Заполните оба поля")

    def remove_from_type(self):
        t = self.type_entry.get().strip().lower()
        f = self.flavor_type_entry.get().strip().lower()
        if t and f:
            self.shop.remove_flavor_from_type(t, f)
            messagebox.showinfo("Успех", f"Из типа '{t}' удалён вкус '{f}'")
        else:
            messagebox.showwarning("Ошибка", "Заполните оба поля")

    def show_types(self):
        msg = f"🍦 Меню кафе '{self.shop.restaurant_name}':\n\n"
        for t, flavors in self.shop.ice_cream_types.items():
            msg += f"🍨 {t.capitalize()}: {', '.join(flavors)}\n"
        messagebox.showinfo("Типы мороженого", msg)

# ---------- Демонстрация 14.1 и 14.2 (консоль) ----------
def demo_1412():
    print("=== 14.1 Демонстрация ===")
    cafe = IceCreamStand("Морозко", "ул. Ленина, 15", "09:00–21:00")
    cafe.display_flavors()

    print("\n=== 14.2 Работа со вкусами ===")
    cafe.add_flavor("фисташка")
    cafe.remove_flavor("клубника")
    cafe.check_flavor("ваниль")

    print("\n=== 14.2 Работа с типами ===")
    cafe.add_flavor_to_type("эскимо", "фисташка")
    cafe.remove_flavor_from_type("стаканчик", "шоколад")
    cafe.show_menu_by_type()

if __name__ == "__main__":
    print("Запуск консольной демонстрации заданий 14.1 и 14.2:")
    demo_1412()
    print("\n" + "="*50)
    print("Запуск цветного графического интерфейса (задание 14.3).")
    root = tk.Tk()
    app = IceCreamGUI(root)
    root.mainloop()
