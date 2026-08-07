#PARTE DE JOS
import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox 

from model.categoria import Categoria 
from model.producto import Producto

class AppWindow(tk.Tk):
    def __init__(self, category_service, product_service):
        super().__init__()

        self.category_service = category_service
        self.product_service = product_service

        self.title("Sistema de Gestion de Inventario - IT Solutions")
        self.geometry("900x600")
        self.minsize(800, 500)

        # Diccionario para almacenar el nombre de la categoria y su UUID en los ComboBox
        self.categories_map = {}

        self.setup_ui()
        self.refresh_categories()
        self.refresh_products()

    def setup_ui(self):
        # Notebook (Pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Crear pestañas 
        self.tab_products = ttk.Frame(self.notebook)
        self.tab_categories = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_products, text="Productos")
        self.notebook.add(self.tab_categories, text="Categorías")

        # LLAMADA A LA CONSTRUCCIÓN DE CADA PESTAÑA
        self._build_products_tab()
        self._build_categories_tab()

    def _build_products_tab(self):
        # Formulario de entrada de productos
        frame_form = ttk.LabelFrame(self.tab_products, text="Datos del producto", padding=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_prod_nombre = ttk.Entry(frame_form, width=25)
        self.entry_prod_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Precio ($):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_prod_precio = ttk.Entry(frame_form, width=25)
        self.entry_prod_precio.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="stock:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_prod_stock = ttk.Entry(frame_form, width=25)
        self.entry_prod_stock.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Categoria:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.combo_prod_categoria = ttk.Combobox(frame_form, width=25)
        self.combo_prod_categoria.grid(row=3, column=1, padx=5, pady=5)

        # Boton de Acciones
        frame_btn = ttk.Frame(self.tab_products)
        frame_btn.pack(fill="x", padx=10, pady=5)

        btn_add = ttk.Button(frame_btn, text="Agregar Producto", command=self.add_product)
        btn_add.pack(side="left", padx=5, pady=5)

        btn_delete = ttk.Button(frame_btn, text="Eliminar Producto", command=self.delete_product)
        btn_delete.pack(side="left", padx=5, pady=5)

        btn_clear = ttk.Button(frame_btn, text="Limpiar Campos", command=self.clear_prod_entries)
        btn_clear.pack(side="left", padx=5, pady=5)

        # Tabla (Treeview) de productos
        frame_table = ttk.Frame(self.tab_products)
        frame_table.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("uuid", "nombre", "precio", "stock", "categoria")
        self.tree_products = ttk.Treeview(frame_table, columns=columns, show="headings")

        self.tree_products.heading("uuid", text="UUID")
        self.tree_products.heading("nombre", text="Nombre")
        self.tree_products.heading("precio", text="Precio ($)")
        self.tree_products.heading("stock", text="Stock")
        self.tree_products.heading("categoria", text="Categoría")

        self.tree_products.column("uuid", width=100, anchor="center")
        self.tree_products.column("nombre", width=200)
        self.tree_products.column("precio", width=100, anchor="e")
        self.tree_products.column("stock", width=100, anchor="center")
        self.tree_products.column("categoria", width=180)

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree_products.yview)
        self.tree_products.configure(yscroll=scrollbar.set)

        self.tree_products.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh_products(self):
        for item in self.tree_products.get_children():
            self.tree_products.delete(item)

        products = self.product_service.get_all_products()
        for prod in products:
            cat_name = "Sin categoría"
            if prod.categoria_uuid:
                try: 
                    cat = self.category_service.get_category_by_id(prod.categoria_uuid)
                    cat_name = cat.nombre
                except ValueError:
                    cat_name = "Categoría no encontrada"

            # Inserción fuera del if prod.categoria_uuid
            self.tree_products.insert("", "end", values=(
                prod.uuid[:8] + "...", 
                prod.nombre,
                f"${prod.precio:.2f}",
                prod.stock,
                cat_name
            ), tags=(prod.uuid,))

    def add_product(self):
        try:
            nombre = self.entry_prod_nombre.get().strip()
            precio = float(self.entry_prod_precio.get() or 0) 
            stock = int(self.entry_prod_stock.get() or 0)

            cat_selected = self.combo_prod_categoria.get()
            cat_uuid = self.categories_map.get(cat_selected, None)

            nuevo_producto = Producto( 
                nombre=nombre,
                precio=precio, 
                stock=stock, 
                categoria_uuid=cat_uuid
            )

            self.product_service.create_product(nuevo_producto)
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
            self.clear_prod_entries()
            self.refresh_products()

        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al agregar el producto: {str(e)}")

    def delete_product(self):
        selected = self.tree_products.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar.")
            return
        
        item = self.tree_products.item(selected[0])
        prod_uuid = item["tags"][0]  

        if messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar este producto?"):
            try:
                self.product_service.delete_product(prod_uuid)
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
                self.refresh_products()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al eliminar el producto: {str(e)}")

    def clear_prod_entries(self):
        self.entry_prod_nombre.delete(0, tk.END)
        self.entry_prod_precio.delete(0, tk.END)
        self.entry_prod_stock.delete(0, tk.END)
        self.combo_prod_categoria.set("")

    # PESTAÑA: CATEGORIAS
    def _build_categories_tab(self):
        frame_form = ttk.LabelFrame(self.tab_categories, text="Datos de la categoría", padding=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_form, text="Nombre de categoria:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_cat_nombre = ttk.Entry(frame_form, width=30)
        self.entry_cat_nombre.grid(row=0, column=1, padx=5, pady=5)

        btn_add = ttk.Button(frame_form, text="Crear categoria", command=self.add_category)
        btn_add.grid(row=0, column=2, padx=5, pady=5)

        btn_delete = ttk.Button(frame_form, text="Eliminar Seleccionada", command=self.delete_category)
        btn_delete.grid(row=0, column=3, padx=5, pady=5)

        # Tabla Categorias 
        frame_table = ttk.Frame(self.tab_categories)
        frame_table.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("uuid", "nombre")
        self.tree_categories = ttk.Treeview(frame_table, columns=columns, show="headings")

        self.tree_categories.heading("uuid", text="UUID")
        self.tree_categories.heading("nombre", text="Nombre de la categoría")

        self.tree_categories.column("uuid", width=250, anchor="center")
        self.tree_categories.column("nombre", width=400)

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree_categories.yview)
        self.tree_categories.configure(yscroll=scrollbar.set)

        self.tree_categories.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh_categories(self):
        for item in self.tree_categories.get_children():
            self.tree_categories.delete(item)

        categories = self.category_service.get_all_categories()
        self.categories_map.clear()  

        for cat in categories:
            self.tree_categories.insert("", "end", values=(cat.uuid, cat.nombre), tags=(cat.uuid,))
            self.categories_map[cat.nombre] = cat.uuid 

        # Actualizar el ComboBox en la pestaña de productos
        self.combo_prod_categoria['values'] = list(self.categories_map.keys())

    def add_category(self):
        try:
            nombre = self.entry_cat_nombre.get().strip()
            nueva_categoria = Categoria(nombre=nombre)

            self.category_service.create_category(nueva_categoria)
            messagebox.showinfo("Éxito", "Categoría creada correctamente.")
            self.entry_cat_nombre.delete(0, tk.END)

            self.refresh_categories()
            self.refresh_products()  

        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))

    def delete_category(self):
        selected = self.tree_categories.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione una categoría de la lista.")
            return

        item = self.tree_categories.item(selected[0])
        cat_uuid = item["tags"][0]  

        if messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar esta categoría?"):
            try:
                self.category_service.delete_category(cat_uuid)
                messagebox.showinfo("Éxito", "Categoría eliminada correctamente.")
                self.refresh_categories()
                self.refresh_products()  
            except ValueError as e:
                messagebox.showerror("Error", str(e))
           
