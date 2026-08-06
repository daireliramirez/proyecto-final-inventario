#PARTE DE YOENMY
from repository.inventario_repository import ProductRepository, CategoryRepository
from service.inventario_service import CategoryService, ProductService
from ui.app_window import AppWindow

def main():
    product_repository = ProductRepository()
    category_repository = CategoryRepository()
    Category_service = CategoryService(category_repository)
    Product_service = ProductService(product_repository, category_repository)
    

    app_window = AppWindow(Category_service,Product_service)

    app_window.mainloop()


if __name__ == "__main__":
    main()
