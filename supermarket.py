import heapq                         #اكتر المنتجات مبيعا
from collections import deque        #لطوابير الكاشير
from datetime import datetime        #للتعامل مع التاريخ
import tkinter as tk                 #GUI عشان ال 
from tkinter import messagebox, simpledialog   #الرسايل الصغيره

BG      = "#0F172A"             #لون الخلفيه
CARD    = "#A8A8A8"             #لون الكروت والقوائم الجانبيه   
ACCENT  = "#5B6FBB"             #لون الازرار
GREEN   = "#22C55E"             #
RED     = "#0be3ce"
YELLOW  = "#f5a623"
WHITE   = "#121212"
GRAY    = "#6c787b"
FONT    = ("Consolas", 11)
FONT_B  = ("Consolas", 11, "bold")
FONT_T  = ("Consolas", 14, "bold")
FONT_H  = ("Consolas", 18, "bold")

# Product
class Product:
    def __init__(self, barcode, name, price, stock, expiry, sales=0):
        self.barcode = barcode
        self.name = name
        self.price = price
        self.stock = stock
        self.expiry = expiry
        self.sales = sales

    def __str__(self):
        return f"Barcode:{self.barcode} | {self.name} | Price:{self.price} | Expiry:{self.expiry} | Stock:{self.stock}"


# Merge Sort (by expiry)
def merge_sort(products):
    if len(products) <= 1:
        return products
    
    mid = len(products) // 2
    left = merge_sort(products[:mid])   #بنقسم من الاول لحد النص
    right = merge_sort(products[mid:])  #بنقسم من النص لحد الاخر
    
    return merge(left, right)           #بندمجهم بعد م اتفصلو


def merge(left, right):                 #بنعرفها (الدله اللى دمجتهم)
    result = []                         #قايمه فاضيه هنحط فيها النتيجه النهائيه
    i = j = 0 
    
    while i < len(left) and j < len(right):       # طول م لسه فى عناصر ف القايمه
        if datetime.strptime(left[i].expiry, "%d/%m/%Y") <= datetime.strptime(right[j].expiry, "%d/%m/%Y"):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])             #لما بنخلص قايمه بنضيف الباقى ف التانيه
    result.extend(right[j:])
    return result                       #نرجع القايمه مدموجه مرتبه


# Linked List (Cart)
class Node:
    def __init__(self, product, qty):       # النود بتاخد الاسم بتاع البرودكت والكميه  
        self.product = product              #
        self.qty = qty
        self.next = None


class Cart:                        #عربة التسوق
    def __init__(self):            
        self.head = None           #العربيه بتبدا فاضيه

    def add(self, product, qty):        
        new_node = Node(product, qty)
        new_node.next = self.head          #بيخلى الجديد قبل القديم
        self.head = new_node               #بنحرك الhead عشان يشاور على اخر عنصر

    def remove(self):               
        if self.head:                #بنتاكد الاول ان العربيه مش فاضيه
            self.head = self.head.next

    def get_items(self):           #داله بترجع كل عناصر العربيه
        items = []
        temp = self.head
        total = 0
        while temp:
           sub = temp.product.price * temp.qty    #الاجمالى =السعر *الكميه
           total += sub
           items.append((temp.product.name, temp.qty, sub))
           temp = temp.next                          #يحرك المؤشر للعنصر اللى بعده
        return items, total                          #بنرجع القايمه والاجمالى مع بعض


       


# Stack (Undo)
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None


# Cashier
class Cashier:
    def __init__(self, id):
        self.id = id
        self.queue = deque()

    def add_customer(self, name):
        self.queue.append(name)

    def process(self):
        if self.queue:
            return self.queue.popleft()
        return None

# Binary Search
def binary_search(products, target, key):
    left, right = 0, len(products) - 1
    while left <= right:
        mid = (left + right) // 2
        value = getattr(products[mid], key)

        if isinstance(value, str):
            value = value.lower()

        if value == target:
            return products[mid]
        elif value < target:
            left = mid + 1
        else:
            right = mid - 1
    return None


# Top Selling
def top_selling(products):
    heap = [(-p.sales, p.name) for p in products]
    heapq.heapify(heap)

    print("\nTop Selling Products:")
    for _ in range(min(5, len(heap))):
        sales, name = heapq.heappop(heap)
        print(name, "Sold:", -sales)


# Supermarket System
class Supermarket:
    def __init__(self):
        self.products = []
        self.cart = Cart()
        self.undo_stack = Stack()
        self.cashiers = [Cashier(1), Cashier(2), Cashier(3)]

    def add_product(self, p):
        self.products.append(p)

    def show_products(self):
        print("\n--- Products Sorted by Expiry ---")
        for p in merge_sort(self.products):
            print(p)

    def search_by_barcode(self, barcode):
        products_sorted = sorted(self.products, key=lambda x: x.barcode)
        return binary_search(products_sorted, barcode, "barcode")

    def search_by_name(self, name):
        name = name.lower()
        products_sorted = sorted(self.products, key=lambda x: x.name.lower())
        return binary_search(products_sorted, name, "name")

    def add_to_cart(self, barcode, qty):
        p = self.search_by_barcode(barcode)

        if p is None:
            return False, "product not found"
        if qty <= 0:
            return False, "invalid quantity"
        if qty > p.stock:
            return False, "Not enough stock"

        self.cart.add(p, qty)
        self.undo_stack.push(("add", p, qty))
        return True, f"'{p.name}' added successfully"

    def undo(self):
        if self.undo_stack.pop():
            self.cart.remove()
            print("Undo done")

    # cashier selection
    def get_shortest_cashier(self):
        return min(self.cashiers, key=lambda c: len(c.queue))

    def checkout(self, customer_name):
        items, total = self.cart.get_items()
        if not items:
            return False, "Cart is empty"
        temp = self.cart.head
        while temp:
            temp.product.stock -= temp.qty
            temp.product.sales += temp.qty
            temp = temp.next
        cashier = self.get_shortest_cashier()
        cashier.add_customer(customer_name)
        self.cart = Cart()
        return True, f"Bill: {total} EGP\nAssigned to Cashier {cashier.id}"
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Supermarket Management System")
        self.geometry("1100x680")
        self.configure(bg=BG)
        self.market = Supermarket()
        
        self._build_ui()

    def _load_products(self):
        data = [
            (1,"Milk",10,50,"05/04/2026"),
            (2,"Bread",5,30,"02/05/2026"),
            (3,"Eggs",2,100,"01/05/2027"),
            (4,"Cheese",20,10,"10/05/2027"),
            (5,"Juice",8,40,"07/06/2027"),
            (6,"Butter",15,40,"03/03/2026"),
            (7,"Yogurt",7,60,"10/04/2026"),
            (8,"Rice",3,80,"15/08/2027"),
            (9,"Pasta",4,70,"20/09/2027"),
            (10,"Tomato Sauce",6,50,"25/11/2026"),
            (11,"Chocolate",12,35,"14/02/2027"),
            (12,"Water",2,200,"01/01/2028"),
            (13,"Chips",5,90,"30/06/2026"),
            (14,"Sugar",8,45,"12/03/2027"),
            (15,"Coffee",20,25,"05/07/2026"),
        ]
        for d in data:
            self.market.add_product(Product(*d))

    def _build_ui(self):
        header = tk.Frame(self, bg=ACCENT, pady=12)
        header.pack(fill="x")
        tk.Label(header, text="SUPERMARKET MANAGEMENT SYSTEM",
                 font=FONT_H, bg=ACCENT, fg=WHITE).pack()
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True, padx=10, pady=10)
        sidebar = tk.Frame(main, bg=CARD, width=200, padx=10, pady=10)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="MENU", font=FONT_T, bg=CARD, fg=WHITE).pack(pady=(0,10))
        buttons = [
            ("Show Products",    self.show_products),
            ("Add to Cart",      self.add_to_cart),
            ("View Cart",        self.view_cart),
            ("Undo",             self.undo),
            ("Checkout",         self.checkout),
            ("Top Selling",      self.top_selling),
            ("Process Cashiers", self.process_cashiers),
            ("Search Product",   self.search_product),
            ("Add New Product",  self.add_new_product),
        ]
        for text, cmd in buttons:
            tk.Button(sidebar, text=text, font=FONT, bg=ACCENT, fg=WHITE,
                      activebackground=GREEN, activeforeground=BG,
                      bd=0, pady=8, cursor="hand2", command=cmd,
                      anchor="w", padx=10).pack(fill="x", pady=3)
        right = tk.Frame(main, bg=BG)
        right.pack(side="left", fill="both", expand=True, padx=(10,0))
        tk.Label(right, text="OUTPUT", font=FONT_T, bg=BG, fg=WHITE).pack(anchor="w")
        self.output = tk.Text(right, font=FONT, bg=CARD, fg=WHITE,
                              insertbackground=WHITE, bd=0, padx=12, pady=12,
                              state="disabled", wrap="word")
        self.output.pack(fill="both", expand=True)
        self.status = tk.Label(self, text="Ready", font=("Consolas", 9),
                               bg=ACCENT, fg=WHITE, anchor="w", padx=10)
        self.status.pack(fill="x", side="bottom")
        self.show_products()

    def _write(self, text):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", text + "\n")
        self.output.configure(state="disabled")

    def _set_status(self, msg):
        self.status.config(text=f"  {msg}")

    def show_products(self):
        sorted_p = merge_sort(self.market.products)
        lines = ["Products Sorted by Expiry Date\n" + "-"*50]
        for p in sorted_p:
            lines.append(f"  [{p.barcode:02}] {p.name:<16} Price:{p.price:<6} Stock:{p.stock:<5} Expiry:{p.expiry}")
        self._write("\n".join(lines))
        self._set_status(f"Showing {len(sorted_p)} products")

    def add_to_cart(self):
        win = tk.Toplevel(self)
        win.title("Add to Cart")
        win.geometry("320x180")
        win.configure(bg=CARD)
        win.grab_set()
        tk.Label(win, text="Add to Cart", font=FONT_T, bg=CARD, fg=WHITE).pack(pady=10)
        frame = tk.Frame(win, bg=CARD)
        frame.pack()
        tk.Label(frame, text="Barcode:", font=FONT, bg=CARD, fg=WHITE).grid(row=0, column=0, padx=8, pady=6, sticky="e")
        barcode_var = tk.StringVar()
        tk.Entry(frame, textvariable=barcode_var, font=FONT, bg=ACCENT, fg=WHITE, insertbackground=WHITE, width=12).grid(row=0, column=1, padx=8)
        tk.Label(frame, text="Quantity:", font=FONT, bg=CARD, fg=WHITE).grid(row=1, column=0, padx=8, pady=6, sticky="e")
        qty_var = tk.StringVar()
        tk.Entry(frame, textvariable=qty_var, font=FONT, bg=ACCENT, fg=WHITE, insertbackground=WHITE, width=12).grid(row=1, column=1, padx=8)
        def confirm():
            try:
                b = int(barcode_var.get())
                q = int(qty_var.get())
                ok, msg = self.market.add_to_cart(b, q)
                if ok:
                    self._set_status(msg)
                    messagebox.showinfo("Success", msg, parent=win)
                else:
                    messagebox.showerror("Error", msg, parent=win)
                win.destroy()
            except:
                messagebox.showerror("Error", "Invalid input!", parent=win)
        tk.Button(win, text="Add", font=FONT_B, bg=GREEN, fg=BG,
                  bd=0, padx=20, pady=6, cursor="hand2", command=confirm).pack(pady=12)

    def view_cart(self):
        items, total = self.market.cart.get_items()
        if not items:
            self._write("Cart is empty.")
            return
        lines = ["YOUR CART\n" + "-"*40]
        for name, qty, sub in items:
            lines.append(f"  {name:<18} x{qty}  =  {sub:.2f} EGP")
        lines.append("-"*40)
        lines.append(f"  TOTAL:  {total:.2f} EGP")
        self._write("\n".join(lines))

    def undo(self):
        if self.market.undo_stack.pop():
            self.market.cart.remove()
            self._write("Last item removed from cart.")
        else:
            self._write("Nothing to undo.")

    def checkout(self):
        items, total = self.market.cart.get_items()
        if not items:
            messagebox.showwarning("Empty Cart", "Your cart is empty!")
            return
        name = simpledialog.askstring("Checkout", "Enter your name:", parent=self)
        if not name:
            return
        ok, msg = self.market.checkout(name)
        if ok:
            self._write(f"CHECKOUT\n{'-'*40}\n  Customer: {name}\n  {msg}")
            self._set_status(f"Checkout done for {name}")

    def top_selling(self):
        heap = [(-p.sales, p.name) for p in self.market.products]
        heapq.heapify(heap)
        lines = ["TOP 5 SELLING PRODUCTS\n" + "-"*40]
        for i in range(min(5, len(heap))):
            sales, name = heapq.heappop(heap)
            lines.append(f"  {i+1}. {name:<18}  Sold: {-sales}")
        self._write("\n".join(lines))

    def process_cashiers(self):
        lines = ["CASHIER QUEUES\n" + "-"*40]
        for c in self.market.cashiers:
            served = c.process()
            if served:
                lines.append(f"  Cashier {c.id}: Serving '{served}' | Remaining: {len(c.queue)}")
            else:
                lines.append(f"  Cashier {c.id}: No customers in queue")
        self._write("\n".join(lines))

    def search_product(self):
        win = tk.Toplevel(self)
        win.title("Search Product")
        win.geometry("340x200")
        win.configure(bg=CARD)
        win.grab_set()
        tk.Label(win, text="Search Product", font=FONT_T, bg=CARD, fg=WHITE).pack(pady=10)
        choice = tk.IntVar(value=1)
        f = tk.Frame(win, bg=CARD)
        f.pack()
        tk.Radiobutton(f, text="By Barcode", variable=choice, value=1,
                       font=FONT, bg=CARD, fg=WHITE, selectcolor=ACCENT).grid(row=0, column=0, padx=10)
        tk.Radiobutton(f, text="By Name", variable=choice, value=2,
                       font=FONT, bg=CARD, fg=WHITE, selectcolor=ACCENT).grid(row=0, column=1, padx=10)
        tk.Label(win, text="Search:", font=FONT, bg=CARD, fg=WHITE).pack()
        query_var = tk.StringVar()
        tk.Entry(win, textvariable=query_var, font=FONT, bg=ACCENT, fg=WHITE,
                 insertbackground=WHITE, width=20).pack(pady=6)
        def do_search():
            q = query_var.get().strip()
            if not q:
                return
            if choice.get() == 1:
                result = self.market.search_by_barcode(int(q))
            else:
                result = self.market.search_by_name(q)
            if result:
                self._write(f"SEARCH RESULT\n{'-'*40}\n"
                            f"  Name:    {result.name}\n"
                            f"  Barcode: {result.barcode}\n"
                            f"  Price:   {result.price} EGP\n"
                            f"  Stock:   {result.stock}\n"
                            f"  Expiry:  {result.expiry}\n\n  Product Found!")
                self._set_status(f"Found: {result.name}")
            else:
                self._write(f"'{q}' - Product Not Found")
            win.destroy()
        tk.Button(win, text="Search", font=FONT_B, bg=GREEN, fg=BG,
                  bd=0, padx=20, pady=6, cursor="hand2", command=do_search).pack(pady=8)

    def add_new_product(self):
        win = tk.Toplevel(self)
        win.title("Add New Product")
        win.geometry("340x300")
        win.configure(bg=CARD)
        win.grab_set()
        tk.Label(win, text="Add New Product", font=FONT_T, bg=CARD, fg=WHITE).pack(pady=10)
        fields = ["Barcode", "Name", "Price", "Stock", "Expiry (dd/mm/yyyy)"]
        vars_ = []
        frame = tk.Frame(win, bg=CARD)
        frame.pack()
        for i, f in enumerate(fields):
            tk.Label(frame, text=f+":", font=FONT, bg=CARD, fg=WHITE).grid(row=i, column=0, sticky="e", padx=8, pady=4)
            v = tk.StringVar()
            tk.Entry(frame, textvariable=v, font=FONT, bg=ACCENT, fg=WHITE,
                     insertbackground=WHITE, width=16).grid(row=i, column=1, padx=8)
            vars_.append(v)
        def confirm():
            try:
                barcode = int(vars_[0].get())
                name    = vars_[1].get().strip().title()
                price   = float(vars_[2].get())
                stock   = int(vars_[3].get())
                expiry  = vars_[4].get().strip()
                datetime.strptime(expiry, "%d/%m/%Y")
                if self.market.search_by_barcode(barcode):
                    messagebox.showerror("Error", "Product already exists!", parent=win)
                    return
                self.market.add_product(Product(barcode, name, price, stock, expiry))
                messagebox.showinfo("Success", f"'{name}' added!", parent=win)
                win.destroy()
                self.show_products()
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input!\n{e}", parent=win)
        tk.Button(win, text="Add Product", font=FONT_B, bg=GREEN, fg=BG,
                  bd=0, padx=20, pady=6, cursor="hand2", command=confirm).pack(pady=12)


if __name__ == "__main__":
    app = App()
    app.mainloop()
