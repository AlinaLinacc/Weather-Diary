import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary - Дневник погоды")
        self.root.geometry("850x650")
        self.root.resizable(True, True)
        
        # Данные для хранения записей
        self.entries = []
        self.current_file = None
        self.filtered_entries = None  # Для хранения отфильтрованных записей
        
        # Автоматическая загрузка данных
        self.auto_load_json()
        
        # Создание интерфейса
        self.create_widgets()
        self.update_display()
    
    def auto_load_json(self):
        """Автоматическая загрузка из JSON файла при запуске"""
        json_file = "weather_data.json"
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    self.entries = json.load(f)
                print(f"✓ Автоматически загружено {len(self.entries)} записей из {json_file}")
            except Exception as e:
                print(f"✗ Ошибка загрузки JSON: {e}")
                self.load_default_data()
        else:
            print("ℹ Файл weather_data.json не найден, загружены примеры данных")
            self.load_default_data()
    
    def load_default_data(self):
        """Загрузить пример данных, если нет файла"""
        self.entries = [
            {"date": "2026-05-01", "temperature": 18.5, "description": "Солнечно, легкий ветер", "precipitation": False},
            {"date": "2026-05-02", "temperature": 12.0, "description": "Облачно, пасмурно", "precipitation": True},
            {"date": "2026-05-03", "temperature": 22.0, "description": "Ясно, без осадков", "precipitation": False},
            {"date": "2026-05-04", "temperature": 15.5, "description": "Переменная облачность", "precipitation": False},
            {"date": "2026-05-05", "temperature": 8.0, "description": "Дождь, холодно", "precipitation": True},
            {"date": "2026-05-06", "temperature": -2.0, "description": "Снегопад, метель", "precipitation": True},
            {"date": "2026-05-07", "temperature": 25.0, "description": "Жарко, солнечно", "precipitation": False},
            {"date": "2026-05-08", "temperature": 10.5, "description": "Туман, сыро", "precipitation": True},
            {"date": "2026-05-09", "temperature": 19.0, "description": "Ветрено, но тепло", "precipitation": False},
            {"date": "2026-05-10", "temperature": 14.0, "description": "Гроза, ливень", "precipitation": True}
        ]
    
    def create_widgets(self):
        # Создание стилей
        style = ttk.Style()
        style.theme_use('clam')
        
        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="➕ Добавить новую запись", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Дата
        ttk.Label(input_frame, text="📅 Дата (ГГГГ-ММ-ДД):", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame, width=15, font=("Arial", 10))
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Температура
        ttk.Label(input_frame, text="🌡 Температура (°C):", font=("Arial", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.temp_entry = ttk.Entry(input_frame, width=10, font=("Arial", 10))
        self.temp_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Описание
        ttk.Label(input_frame, text="📝 Описание:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.desc_entry = ttk.Entry(input_frame, width=40, font=("Arial", 10))
        self.desc_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        
        # Осадки
        self.precip_var = tk.BooleanVar()
        ttk.Checkbutton(input_frame, text="☔ Осадки", variable=self.precip_var).grid(row=1, column=3, padx=5, pady=5)
        
        # Кнопка добавления
        add_btn = ttk.Button(input_frame, text="✅ Добавить запись", command=self.add_entry)
        add_btn.grid(row=2, column=0, columnspan=4, pady=10)
        
        # Фрейм для фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="🔍 Фильтрация записей", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        # Фильтр по дате
        ttk.Label(filter_frame, text="📅 По дате:", font=("Arial", 9)).grid(row=0, column=0, padx=5, pady=5)
        self.filter_date = ttk.Entry(filter_frame, width=12, font=("Arial", 9))
        self.filter_date.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(filter_frame, text="Применить", command=self.filter_by_date, width=10).grid(row=0, column=2, padx=5, pady=5)
        
        # Фильтр по температуре
        ttk.Label(filter_frame, text="🌡 Температура >", font=("Arial", 9)).grid(row=0, column=3, padx=5, pady=5)
        self.filter_temp = ttk.Entry(filter_frame, width=8, font=("Arial", 9))
        self.filter_temp.grid(row=0, column=4, padx=5, pady=5)
        ttk.Label(filter_frame, text="°C", font=("Arial", 9)).grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(filter_frame, text="Применить", command=self.filter_by_temp, width=10).grid(row=0, column=6, padx=5, pady=5)
        
        # Кнопка сброса
        ttk.Button(filter_frame, text="🔄 Сбросить фильтр", command=self.reset_filter, width=15).grid(row=0, column=7, padx=5, pady=5)
        
        # Фрейм для кнопок файловых операций
        file_frame = ttk.Frame(self.root)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(file_frame, text="💾 Сохранить в JSON", command=self.save_to_json, width=20).pack(side="left", padx=5)
        ttk.Button(file_frame, text="📂 Загрузить из JSON", command=self.load_from_json, width=20).pack(side="left", padx=5)
        ttk.Button(file_frame, text="🗑 Очистить все записи", command=self.clear_all_entries, width=20).pack(side="left", padx=5)
        
        # Статусная строка
        self.status_label = ttk.Label(self.root, text="Готово", relief="sunken", anchor="w")
        self.status_label.pack(fill="x", padx=10, pady=5)
        
        # Таблица для отображения записей
        columns = ("Дата", "Температура", "Описание", "Осадки")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=20)
        
        # Настройка заголовков и ширины колонок
        self.tree.heading("Дата", text="📅 Дата")
        self.tree.heading("Температура", text="🌡 Температура")
        self.tree.heading("Описание", text="📝 Описание")
        self.tree.heading("Осадки", text="☔ Осадки")
        
        self.tree.column("Дата", width=120)
        self.tree.column("Температура", width=120)
        self.tree.column("Описание", width=400)
        self.tree.column("Осадки", width=100)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Привязка события двойного клика для удаления
        self.tree.bind("<Double-1>", self.delete_selected_entry)
    
    def validate_date(self, date_str):
        """Проверка формата даты"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def add_entry(self):
        """Добавление новой записи"""
        date = self.date_entry.get().strip()
        temp_str = self.temp_entry.get().strip()
        description = self.desc_entry.get().strip()
        precipitation = self.precip_var.get()
        
        # Валидация
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "❌ Неверный формат даты!\nИспользуйте формат: ГГГГ-ММ-ДД\nПример: 2026-05-15")
            return
        
        try:
            temperature = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "❌ Температура должна быть числом!\nПример: 23.5 или -5")
            return
        
        if not description:
            messagebox.showerror("Ошибка", "❌ Описание не может быть пустым!")
            return
        
        # Добавление записи
        self.entries.append({
            "date": date,
            "temperature": temperature,
            "description": description,
            "precipitation": precipitation
        })
        
        # Очистка полей
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)
        
        # Сброс фильтра при добавлении новой записи
        self.reset_filter()
        
        self.update_display()
        self.update_status(f"✓ Запись добавлена: {date}, {temperature}°C, {description}")
        messagebox.showinfo("Успех", "✅ Запись успешно добавлена!")
    
    def update_display(self, entries_to_show=None):
        """Обновление таблицы"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Если нет записей для отображения, показываем все
        if entries_to_show is None:
            entries_to_show = self.entries
        
        # Сортировка по дате
        entries_to_show = sorted(entries_to_show, key=lambda x: x["date"])
        
        # Заполнение таблицы
        for entry in entries_to_show:
            precip_text = "✅ Да" if entry["precipitation"] else "❌ Нет"
            # Цветовая индикация температуры
            temp_display = f"{entry['temperature']:.1f}°C"
            
            self.tree.insert("", "end", values=(
                entry["date"],
                temp_display,
                entry["description"],
                precip_text
            ))
        
        # Обновление статуса
        total_count = len(self.entries)
        displayed_count = len(entries_to_show)
        if total_count == displayed_count:
            self.update_status(f"📊 Всего записей: {total_count}")
        else:
            self.update_status(f"🔍 Показано записей: {displayed_count} из {total_count}")
    
    def filter_by_date(self):
        """Фильтрация по дате"""
        filter_date = self.filter_date.get().strip()
        
        if not filter_date:
            messagebox.showwarning("Предупреждение", "⚠ Введите дату для фильтрации")
            return
        
        if not self.validate_date(filter_date):
            messagebox.showerror("Ошибка", "❌ Неверный формат даты!\nИспользуйте формат: ГГГГ-ММ-ДД")
            return
        
        filtered = [e for e in self.entries if e["date"] == filter_date]
        
        if filtered:
            self.update_display(filtered)
            self.update_status(f"🔍 Фильтр по дате: {filter_date} (найдено {len(filtered)} записей)")
            messagebox.showinfo("Фильтр", f"✅ Найдено {len(filtered)} записей за {filter_date}")
        else:
            self.update_display([])
            self.update_status(f"🔍 Фильтр по дате: {filter_date} (записей не найдено)")
            messagebox.showinfo("Фильтр", f"❌ Записей за {filter_date} не найдено")
    
    def filter_by_temp(self):
        """Фильтрация по температуре"""
        temp_str = self.filter_temp.get().strip()
        
        if not temp_str:
            messagebox.showwarning("Предупреждение", "⚠ Введите значение температуры")
            return
        
        try:
            min_temp = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "❌ Температура должна быть числом!")
            return
        
        filtered = [e for e in self.entries if e["temperature"] > min_temp]
        
        if filtered:
            self.update_display(filtered)
            self.update_status(f"🔍 Фильтр по температуре: > {min_temp}°C (найдено {len(filtered)} записей)")
            messagebox.showinfo("Фильтр", f"✅ Найдено {len(filtered)} записей с температурой выше {min_temp}°C")
        else:
            self.update_display([])
            self.update_status(f"🔍 Фильтр по температуре: > {min_temp}°C (записей не найдено)")
            messagebox.showinfo("Фильтр", f"❌ Записей с температурой выше {min_temp}°C не найдено")
    
    def reset_filter(self):
        """Сброс фильтрации"""
        self.filter_date.delete(0, tk.END)
        self.filter_temp.delete(0, tk.END)
        self.update_display()
        self.update_status("🔄 Фильтр сброшен, показаны все записи")
        messagebox.showinfo("Фильтр", "🔄 Фильтр успешно сброшен")
    
    def save_to_json(self):
        """Сохранение в JSON файл"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Сохранить дневник погоды",
            initialfile="weather_data.json"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.entries, f, indent=4, ensure_ascii=False)
                self.current_file = file_path
                self.update_status(f"💾 Данные сохранены в: {file_path}")
                messagebox.showinfo("Успех", f"✅ Данные успешно сохранены в:\n{file_path}\n\n📊 Сохранено записей: {len(self.entries)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"❌ Не удалось сохранить файл:\n{e}")
    
    def load_from_json(self):
        """Загрузка из JSON файла"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Загрузить дневник погоды"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.entries = json.load(f)
                self.current_file = file_path
                self.reset_filter()
                self.update_status(f"📂 Загружено {len(self.entries)} записей из: {file_path}")
                messagebox.showinfo("Успех", f"✅ Успешно загружено {len(self.entries)} записей из:\n{file_path}")
            except json.JSONDecodeError as e:
                messagebox.showerror("Ошибка", f"❌ Ошибка формата JSON:\n{e}\n\nФайл поврежден или имеет неверный формат")
            except Exception as e:
                messagebox.showerror("Ошибка", f"❌ Не удалось загрузить файл:\n{e}")
    
    def clear_all_entries(self):
        """Очистка всех записей"""
        if messagebox.askyesno("Подтверждение", "⚠ Вы уверены, что хотите удалить ВСЕ записи?\n\nЭто действие нельзя отменить!"):
            self.entries = []
            self.reset_filter()
            self.update_status("🗑 Все записи удалены")
            messagebox.showinfo("Готово", "✅ Все записи успешно удалены")
    
    def delete_selected_entry(self, event):
        """Удаление выбранной записи по двойному клику"""
        selected_item = self.tree.selection()
        if selected_item:
            if messagebox.askyesno("Подтверждение", "🗑 Удалить выбранную запись?"):
                # Получаем значения выбранной записи
                values = self.tree.item(selected_item[0])['values']
                # Находим и удаляем запись из списка
                for i, entry in enumerate(self.entries):
                    if (entry["date"] == values[0] and 
                        f"{entry['temperature']:.1f}°C" == values[1] and
                        entry["description"] == values[2]):
                        del self.entries[i]
                        break
                
                self.reset_filter()
                self.update_status("🗑 Запись удалена")
                messagebox.showinfo("Готово", "✅ Запись успешно удалена")
    
    def update_status(self, message):
        """Обновление статусной строки"""
        self.status_label.config(text=f" {message}")
        print(f"[STATUS] {message}")

def main():
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()

if __name__ == "__main__":
    main()