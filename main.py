from __future__ import annotations

from collections import deque
import heapq


class Product:
    def __init__(self, product_id: int, name: str, price: int, category: str) -> None:
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category

    def __str__(self) -> str:
        return f"[{self.product_id}] {self.name:<18} | Rp{self.price:<6} | {self.category}"


class TransactionNode:
    def __init__(self, text: str) -> None:
        self.text = text
        self.next: TransactionNode | None = None


class TransactionHistory:
    def __init__(self) -> None:
        self.head: TransactionNode | None = None

    def insert_head(self, text: str) -> None:
        node = TransactionNode(text)
        node.next = self.head
        self.head = node

    def insert_tail(self, text: str) -> None:
        node = TransactionNode(text)
        if self.head is None:
            self.head = node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = node

    def delete_by_text(self, text: str) -> bool:
        current = self.head
        prev = None
        while current:
            if current.text == text:
                if prev is None:
                    self.head = current.next
                else:
                    prev.next = current.next
                return True
            prev = current
            current = current.next
        return False

    def display(self) -> list[str]:
        result = []
        current = self.head
        while current:
            result.append(current.text)
            current = current.next
        return result


class ActionStack:
    def __init__(self) -> None:
        self.undo_stack: list[Product] = []
        self.redo_stack: list[Product] = []

    def push_action(self, product: Product) -> None:
        self.undo_stack.append(product)
        self.redo_stack.clear()

    def undo(self) -> Product | None:
        if not self.undo_stack:
            return None
        product = self.undo_stack.pop()
        self.redo_stack.append(product)
        return product

    def redo(self) -> Product | None:
        if not self.redo_stack:
            return None
        product = self.redo_stack.pop()
        self.undo_stack.append(product)
        return product

    def snapshot(self) -> tuple[list[Product], list[Product]]:
        return self.undo_stack[:], self.redo_stack[:]


class CategoryNode:
    def __init__(self, name: str) -> None:
        self.name = name
        self.left: CategoryNode | None = None
        self.right: CategoryNode | None = None


class CategoryTree:
    def __init__(self) -> None:
        self.root = CategoryNode("Produk")
        self.root.left = CategoryNode("Makanan")
        self.root.right = CategoryNode("Minuman")
        self.root.left.left = CategoryNode("Snack")
        self.root.left.right = CategoryNode("Roti")
        self.root.right.left = CategoryNode("Kopi")
        self.root.right.right = CategoryNode("Soda")

    def preorder(self, node: CategoryNode | None, result: list[str]) -> None:
        if node is None:
            return
        result.append(node.name)
        self.preorder(node.left, result)
        self.preorder(node.right, result)

    def inorder(self, node: CategoryNode | None, result: list[str]) -> None:
        if node is None:
            return
        self.inorder(node.left, result)
        result.append(node.name)
        self.inorder(node.right, result)

    def postorder(self, node: CategoryNode | None, result: list[str]) -> None:
        if node is None:
            return
        self.postorder(node.left, result)
        self.postorder(node.right, result)
        result.append(node.name)

    def traversals(self) -> dict[str, list[str]]:
        pre, ino, post = [], [], []
        self.preorder(self.root, pre)
        self.inorder(self.root, ino)
        self.postorder(self.root, post)
        return {"Pre-order": pre, "In-order": ino, "Post-order": post}


class BSTNode:
    def __init__(self, product: Product) -> None:
        self.product = product
        self.left: BSTNode | None = None
        self.right: BSTNode | None = None


class ProductBST:
    def __init__(self) -> None:
        self.root: BSTNode | None = None

    def insert(self, product: Product) -> None:
        self.root = self._insert(self.root, product)

    def _insert(self, node: BSTNode | None, product: Product) -> BSTNode:
        if node is None:
            return BSTNode(product)
        if product.price < node.product.price:
            node.left = self._insert(node.left, product)
        else:
            node.right = self._insert(node.right, product)
        return node

    def search_by_price(self, price: int) -> Product | None:
        current = self.root
        while current:
            if price == current.product.price:
                return current.product
            if price < current.product.price:
                current = current.left
            else:
                current = current.right
        return None

    def inorder(self) -> list[Product]:
        result: list[Product] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: BSTNode | None, result: list[Product]) -> None:
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.product)
        self._inorder(node.right, result)


class WeightedGraph:
    def __init__(self) -> None:
        self.graph: dict[str, list[tuple[str, int]]] = {}

    def add_edge(self, source: str, destination: str, weight: int) -> None:
        self.graph.setdefault(source, []).append((destination, weight))
        self.graph.setdefault(destination, []).append((source, weight))

    def dijkstra(self, start: str, end: str) -> tuple[int, list[str]]:
        pq: list[tuple[int, str, list[str]]] = [(0, start, [start])]
        visited: dict[str, int] = {}

        while pq:
            cost, node, path = heapq.heappop(pq)
            if node in visited and visited[node] <= cost:
                continue
            visited[node] = cost
            if node == end:
                return cost, path
            for neighbor, weight in self.graph.get(node, []):
                heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))
        return -1, []


class RecommendationGraph:
    def __init__(self) -> None:
        self.graph: dict[str, list[str]] = {}

    def add_relation(self, product_a: str, product_b: str) -> None:
        self.graph.setdefault(product_a, []).append(product_b)
        self.graph.setdefault(product_b, []).append(product_a)

    def bfs_recommend(self, start: str) -> list[str]:
        if start not in self.graph:
            return []
        visited = {start}
        queue = deque([start])
        recommendations: list[str] = []

        while queue:
            current = queue.popleft()
            for neighbor in self.graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    recommendations.append(neighbor)
                    queue.append(neighbor)
        return recommendations


def bubble_sort_products(products: list[Product], key: str) -> list[Product]:
    items = products[:]
    n = len(items)
    for i in range(n):
        for j in range(0, n - i - 1):
            left = getattr(items[j], key)
            right = getattr(items[j + 1], key)
            if left > right:
                items[j], items[j + 1] = items[j + 1], items[j]
    return items


def quick_sort_products(products: list[Product], key: str) -> list[Product]:
    if len(products) <= 1:
        return products[:]
    pivot = getattr(products[len(products) // 2], key)
    left = [item for item in products if getattr(item, key) < pivot]
    mid = [item for item in products if getattr(item, key) == pivot]
    right = [item for item in products if getattr(item, key) > pivot]
    return quick_sort_products(left, key) + mid + quick_sort_products(right, key)


def binary_search_product(sorted_products: list[Product], target_name: str) -> Product | None:
    low, high = 0, len(sorted_products) - 1
    target_name = target_name.lower()
    while low <= high:
        mid = (low + high) // 2
        current_name = sorted_products[mid].name.lower()
        if current_name == target_name:
            return sorted_products[mid]
        if current_name < target_name:
            low = mid + 1
        else:
            high = mid - 1
    return None


class JilvianXApp:
    def __init__(self) -> None:
        self.products = [
            Product(1, "Air Mineral", 5000, "Minuman"),
            Product(2, "Cola", 8000, "Soda"),
            Product(3, "Keripik Kentang", 12000, "Snack"),
            Product(4, "Roti Cokelat", 10000, "Roti"),
            Product(5, "Kopi Kaleng", 15000, "Kopi"),
            Product(6, "Biskuit", 7000, "Snack"),
            Product(7, "Teh Botol", 6000, "Minuman"),
        ]
        self.history = TransactionHistory()
        self.actions = ActionStack()
        self.customer_queue = deque(["Pelanggan-A", "Pelanggan-B", "Pelanggan-C"])
        self.category_tree = CategoryTree()
        self.product_bst = ProductBST()
        for product in self.products:
            self.product_bst.insert(product)

        self.route_graph = WeightedGraph()
        self._load_routes()

        self.recommendation_graph = RecommendationGraph()
        self._load_recommendations()

    def _load_routes(self) -> None:
        routes = [
            ("Gudang", "Mall A", 4),
            ("Gudang", "Kampus", 6),
            ("Mall A", "Stasiun", 3),
            ("Kampus", "Stasiun", 2),
            ("Kampus", "Apartemen", 5),
            ("Stasiun", "Apartemen", 4),
        ]
        for source, destination, weight in routes:
            self.route_graph.add_edge(source, destination, weight)

    def _load_recommendations(self) -> None:
        pairs = [
            ("Air Mineral", "Keripik Kentang"),
            ("Air Mineral", "Biskuit"),
            ("Cola", "Keripik Kentang"),
            ("Kopi Kaleng", "Roti Cokelat"),
            ("Teh Botol", "Biskuit"),
            ("Roti Cokelat", "Biskuit"),
        ]
        for first, second in pairs:
            self.recommendation_graph.add_relation(first, second)

    def show_products(self, items: list[Product] | None = None) -> None:
        data = items if items is not None else self.products
        print("\nDaftar Produk")
        print("-" * 55)
        for product in data:
            print(product)
        print("-" * 55)

    def sort_products_menu(self) -> None:
        print("\nSort produk:")
        print("1. Bubble Sort by harga")
        print("2. Quick Sort by nama")
        choice = input("Pilih metode: ").strip()
        if choice == "1":
            sorted_products = bubble_sort_products(self.products, "price")
            self.show_products(sorted_products)
        elif choice == "2":
            sorted_products = quick_sort_products(self.products, "name")
            self.show_products(sorted_products)
        else:
            print("Pilihan tidak valid.")

    def search_product_menu(self) -> None:
        sorted_products = quick_sort_products(self.products, "name")
        name = input("Masukkan nama produk yang dicari: ").strip()
        result = binary_search_product(sorted_products, name)
        if result:
            print(f"Produk ditemukan: {result}")
        else:
            print("Produk tidak ditemukan.")

    def buy_product(self) -> None:
        self.show_products()
        try:
            product_id = int(input("Masukkan ID produk yang dibeli: ").strip())
        except ValueError:
            print("ID harus berupa angka.")
            return

        product = next((item for item in self.products if item.product_id == product_id), None)
        if not product:
            print("Produk tidak ditemukan.")
            return

        self.actions.push_action(product)
        self.history.insert_tail(f"Pembelian {product.name} seharga Rp{product.price}")
        print(f"Pesanan {product.name} berhasil ditambahkan.")

    def undo_redo_menu(self) -> None:
        print("\n1. Undo")
        print("2. Redo")
        choice = input("Pilih aksi: ").strip()
        if choice == "1":
            undone = self.actions.undo()
            if undone:
                print(f"Undo berhasil: {undone.name}")
            else:
                print("Tidak ada aksi untuk di-undo.")
        elif choice == "2":
            redone = self.actions.redo()
            if redone:
                print(f"Redo berhasil: {redone.name}")
            else:
                print("Tidak ada aksi untuk di-redo.")
        else:
            print("Pilihan tidak valid.")

        undo_items, redo_items = self.actions.snapshot()
        print("Stack aktif:", [item.name for item in undo_items])
        print("Stack redo:", [item.name for item in redo_items])

    def transaction_history_menu(self) -> None:
        print("\nRiwayat Transaksi")
        print("1. Lihat semua")
        print("2. Tambah manual di head")
        print("3. Hapus transaksi")
        choice = input("Pilih menu: ").strip()

        if choice == "1":
            records = self.history.display()
            if not records:
                print("Riwayat masih kosong.")
                return
            for index, text in enumerate(records, start=1):
                print(f"{index}. {text}")
        elif choice == "2":
            text = input("Masukkan transaksi: ").strip()
            if text:
                self.history.insert_head(text)
                print("Transaksi berhasil ditambah di head.")
        elif choice == "3":
            text = input("Masukkan teks transaksi yang akan dihapus: ").strip()
            if self.history.delete_by_text(text):
                print("Transaksi berhasil dihapus.")
            else:
                print("Transaksi tidak ditemukan.")
        else:
            print("Pilihan tidak valid.")

    def queue_menu(self) -> None:
        print("\nAntrian Pelanggan")
        print("1. Lihat antrian")
        print("2. Tambah pelanggan")
        print("3. Proses pelanggan terdepan")
        choice = input("Pilih menu: ").strip()

        if choice == "1":
            if not self.customer_queue:
                print("Antrian kosong.")
                return
            print(" -> ".join(self.customer_queue))
        elif choice == "2":
            name = input("Nama pelanggan: ").strip()
            if name:
                self.customer_queue.append(name)
                print(f"{name} masuk antrian.")
        elif choice == "3":
            if self.customer_queue:
                current = self.customer_queue.popleft()
                print(f"Memproses {current}.")
            else:
                print("Antrian kosong.")
        else:
            print("Pilihan tidak valid.")

    def category_menu(self) -> None:
        print("\nTraversal Kategori Produk")
        traversals = self.category_tree.traversals()
        for name, values in traversals.items():
            print(f"{name}: {' -> '.join(values)}")

    def bst_menu(self) -> None:
        print("\nBST Produk Berdasarkan Harga")
        print("1. Insert produk baru")
        print("2. Search by harga")
        print("3. Tampilkan sorted (in-order)")
        choice = input("Pilih menu: ").strip()

        if choice == "1":
            try:
                product_id = max(item.product_id for item in self.products) + 1
                name = input("Nama produk: ").strip()
                price = int(input("Harga produk: ").strip())
                category = input("Kategori produk: ").strip() or "Lainnya"
            except ValueError:
                print("Harga harus berupa angka.")
                return

            product = Product(product_id, name, price, category)
            self.products.append(product)
            self.product_bst.insert(product)
            print("Produk berhasil ditambahkan ke BST.")
        elif choice == "2":
            try:
                price = int(input("Masukkan harga: ").strip())
            except ValueError:
                print("Harga harus berupa angka.")
                return
            product = self.product_bst.search_by_price(price)
            if product:
                print(f"Ditemukan: {product}")
            else:
                print("Produk dengan harga tersebut tidak ditemukan.")
        elif choice == "3":
            self.show_products(self.product_bst.inorder())
        else:
            print("Pilihan tidak valid.")

    def restock_route_menu(self) -> None:
        print("\nLokasi tersedia: Gudang, Mall A, Kampus, Stasiun, Apartemen")
        start = input("Mulai dari: ").strip()
        end = input("Tujuan: ").strip()
        distance, path = self.route_graph.dijkstra(start, end)
        if distance == -1:
            print("Rute tidak ditemukan.")
        else:
            print(f"Rute terpendek: {' -> '.join(path)}")
            print(f"Total jarak: {distance} km")

    def recommendation_menu(self) -> None:
        product_name = input("Pilih produk utama: ").strip()
        recommendations = self.recommendation_graph.bfs_recommend(product_name)
        if recommendations:
            print("Rekomendasi BFS:", " -> ".join(recommendations))
        else:
            print("Belum ada rekomendasi untuk produk tersebut.")

    def run(self) -> None:
        while True:
            print("\n=== JilvianX Future Vending Machine ===")
            print("1. Product Catalog")
            print("2. Product Search & Sort")
            print("3. Beli Produk")
            print("4. Transaction History")
            print("5. Undo/Redo Pesanan")
            print("6. Order Queue")
            print("7. Kategori Produk")
            print("8. BST Produk")
            print("9. Restock Route")
            print("10. Rekomendasi Produk")
            print("0. Keluar")
            choice = input("Pilih menu: ").strip()

            if choice == "1":
                self.show_products()
            elif choice == "2":
                print("\n1. Sort")
                print("2. Search")
                sub_choice = input("Pilih menu: ").strip()
                if sub_choice == "1":
                    self.sort_products_menu()
                elif sub_choice == "2":
                    self.search_product_menu()
                else:
                    print("Pilihan tidak valid.")
            elif choice == "3":
                self.buy_product()
            elif choice == "4":
                self.transaction_history_menu()
            elif choice == "5":
                self.undo_redo_menu()
            elif choice == "6":
                self.queue_menu()
            elif choice == "7":
                self.category_menu()
            elif choice == "8":
                self.bst_menu()
            elif choice == "9":
                self.restock_route_menu()
            elif choice == "10":
                self.recommendation_menu()
            elif choice == "0":
                print("Terima kasih telah menggunakan JilvianX.")
                break
            else:
                print("Pilihan tidak valid.")


if __name__ == "__main__":
    JilvianXApp().run()
