import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phần mềm quản lý thông tin sinh viên")
        self.conn = None

        # Database connection fields
        self.db_name = tk.StringVar(value='dbtest')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='sinhvien')

        # Data fields
        self.column_mssv = tk.StringVar()
        self.column_hoten = tk.StringVar()
        self.column_tuoi = tk.StringVar()
        self.column_diachi = tk.StringVar()
        self.column_quequan = tk.StringVar()
        self.column_chuyennganh = tk.StringVar()
        self.delete_mssv = tk.StringVar()
        self.search_mssv = tk.StringVar()

        # Create the GUI elements
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Connection section
        connection_frame = tk.Frame(self.root)
        connection_frame.pack(pady=10)

        tk.Label(connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)

        tk.Button(connection_frame, text="Connect", command=self.connect_db).grid(row=5, columnspan=2, pady=10)

        # Action buttons for table operations
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=10)

        tk.Button(action_frame, text="Create Table", command=self.create_table).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(action_frame, text="Delete Table", command=self.delete_table).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(action_frame, text="Delete Data", command=self.delete_data).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(action_frame, text="Load Data", command=self.load_data).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(action_frame, text="Search Data", command=self.search_data).grid(row=0, column=4, padx=5, pady=5)

        # Query section
        query_frame = tk.Frame(self.root)
        query_frame.pack(pady=10)

        tk.Label(query_frame, text="Table Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(query_frame, textvariable=self.table_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(query_frame, text="MSSV to Delete:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(query_frame, textvariable=self.delete_mssv).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(query_frame, text="MSSV to Search:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(query_frame, textvariable=self.search_mssv).grid(row=2, column=1, padx=5, pady=5)
        

        self.data_display = tk.Text(self.root, height=10, width=50)
        self.data_display.pack(pady=10)

        # Insert section
        insert_frame = tk.Frame(self.root)
        insert_frame.pack(pady=10)

        tk.Label(insert_frame, text="MSSV:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column_mssv).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Họ tên:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column_hoten).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Tuổi:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column_tuoi).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Địa chỉ:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column_diachi).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Quê quán:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column_quequan).grid(row=4, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Chuyên ngành:").grid(row=5, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column_chuyennganh).grid(row=5, column=1, padx=5, pady=5)

        tk.Button(insert_frame, text="Insert Data", command=self.insert_data).grid(row=6, columnspan=2, pady=10)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to the database successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")

    def create_table(self):
        try:
            create_query = sql.SQL(
                """
                CREATE TABLE IF NOT EXISTS {} (
                    id SERIAL PRIMARY KEY,
                    mssv VARCHAR(20),
                    ho_ten VARCHAR(100),
                    tuoi INT,
                    dia_chi VARCHAR(100),
                    que_quan VARCHAR(100),
                    chuyen_nganh VARCHAR(100)
                )
                """
            ).format(sql.Identifier(self.table_name.get()))
            self.cur.execute(create_query)
            self.conn.commit()
            messagebox.showinfo("Success", "Table created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error creating table: {e}")

    def delete_table(self):
        try:
            delete_query = sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(delete_query)
            self.conn.commit()
            messagebox.showinfo("Success", "Table deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting table: {e}")

    def delete_data(self):
        try:
            mssv_value = self.delete_mssv.get().strip()
            if not mssv_value:
                raise ValueError("MSSV cannot be empty.")

            delete_data_query = sql.SQL("DELETE FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(delete_data_query, (mssv_value,))
            self.conn.commit()
            messagebox.showinfo("Success", f"Data for MSSV {mssv_value} deleted successfully!")
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid input: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting data: {e}")

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            self.data_display.delete(1.0, tk.END)
            for row in rows:
                self.data_display.insert(tk.END, f"{row}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def search_data(self):
        try:
            mssv_value = self.search_mssv.get().strip()
            if not mssv_value:
                raise ValueError("MSSV không được để trống.")
            search_query = sql.SQL("SELECT * FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(search_query, (mssv_value,))
            result = self.cur.fetchone()  # Lấy 1 hàng dữ liệu
            self.data_display.delete(1.0, tk.END)
            if result:
                self.data_display.insert(tk.END, f"Thông tin MSSV {mssv_value}: {result}\n")
            else:
                self.data_display.insert(tk.END, f"Không tìm thấy dữ liệu cho MSSV: {mssv_value}\n")
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid input: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Error searching data: {e}")


    def insert_data(self):
        try:
            if not self.column_tuoi.get().isdigit():
                raise ValueError("Tuổi phải là một số nguyên hợp lệ.")

            insert_query = sql.SQL(
                "INSERT INTO {} (mssv, ho_ten, tuoi, dia_chi, que_quan, chuyen_nganh) VALUES (%s, %s, %s, %s, %s, %s)"
            ).format(sql.Identifier(self.table_name.get()))

            data_to_insert = (
                self.column_mssv.get(),
                self.column_hoten.get(),
                int(self.column_tuoi.get()),
                self.column_diachi.get(),
                self.column_quequan.get(),
                self.column_chuyennganh.get()
            )

            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid input: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")

    def on_closing(self):
        if self.conn:
            self.conn.close()
        self.root.destroy()