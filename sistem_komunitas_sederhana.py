# SISTEM KOMUNITAS - VERSI SEDERHANA
# Struktur Data : Menggunakan Linked List & Hash Map
# Database      : CSV (community.csv)

import csv
import os

FILE_CSV = "community.csv"
FIELDS = ["id", "nama", "umur", "jenis kelamin"]


# STRUKTUR DATA 1: LINKED LIST
# Menyimpan seluruh data anggota komunitas secara berurutan
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        node = Node(data)
        if not self.head:
            self.head = node
            return node
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node
        return node

    def delete(self, member_id):
        cur, prev = self.head, None
        while cur:
            if cur.data["id"] == member_id:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                return True
            prev, cur = cur, cur.next
        return False

    def to_list(self):
        result, cur = [], self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    def clear(self):
        self.head = None


# STRUKTUR DATA 2: HASH MAP

class HashMap:
    def __init__(self):
        self.table = {}

    def put(self, key, node):
        self.table[key] = node

    def get(self, key):
        return self.table.get(key)

    def remove(self, key):
        self.table.pop(key, None)

    def clear(self):
        self.table.clear()


# ALGORITMA SORTING: INSERTION SORT
def insertion_sort(data, key):
    arr = data[:]
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and str(arr[j][key]).lower() > str(current[key]).lower():
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr


# ALGORITMA SEARCHING: BINARY SEARCH (data harus sudah terurut)
def binary_search(sorted_data, key, target):
    lo, hi = 0, len(sorted_data) - 1
    target = str(target).strip().lower()
    while lo <= hi:
        mid = (lo + hi) // 2
        val = str(sorted_data[mid][key]).lower()
        if val == target:
            return sorted_data[mid]
        elif val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


# SISTEM KOMUNITAS: CRUD + CSV, untuk menggabungkan kedua struktur data
class Komunitas:
    def __init__(self):
        self.list = LinkedList()
        self.map = HashMap()
        self.load()

    def load(self):
        self.list.clear()
        self.map.clear()
        if not os.path.exists(FILE_CSV):
            return
        with open(FILE_CSV, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                node = self.list.append(row)
                self.map.put(row["id"], node)

    def save(self):
        with open(FILE_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(self.list.to_list())

    def create(self, data):
        if self.map.get(data["id"]):
            print("[GAGAL] ID sudah dipakai.")
            return
        node = self.list.append(data)
        self.map.put(data["id"], node)
        self.save()
        print(f"[OK] Anggota '{data['nama']}' ditambahkan.")

    def read_all(self):
        return self.list.to_list()

    def find_id(self, member_id):
        node = self.map.get(member_id)
        return node.data if node else None

    def find_nama(self, nama):
        data_terurut = insertion_sort(self.read_all(), "nama")
        return binary_search(data_terurut, "nama", nama)

    def update(self, member_id, new_data):
        node = self.map.get(member_id)
        if not node:
            print("[GAGAL] ID tidak ditemukan.")
            return
        node.data.update(new_data)
        self.save()
        print("[OK] Data anggota diperbarui.")

    def delete(self, member_id):
        if not self.map.get(member_id):
            print("[GAGAL] ID tidak ditemukan.")
            return
        nama = self.map.get(member_id).data["nama"]
        self.list.delete(member_id)
        self.map.remove(member_id)
        self.save()
        print(f"[OK] Anggota '{nama}' dihapus.")

    def sorted_by_nama(self):
        return insertion_sort(self.read_all(), "nama")


# ANTARMUKA CLI
def tampil(data):
    if not data:
        print("Tidak ada data.")
        return
    print(f"{'ID':<6}{'Nama':<18}{'Umur':<6}{'jenis kelamin':<12}")
    print("-" * 42)
    for d in data:
        print(f"{d['id']:<6}{d['nama']:<18}{d['umur']:<6}{d['jenis kelamin']:<12}")


def input_data():
    return {
        "id": input("ID       : ").strip(),
        "nama": input("Nama     : ").strip(),
        "umur": input("Umur     : ").strip(),
        "jenis kelamin": input("jenis kelamin : ").strip(),
    }


def main():
    sistem = Komunitas()
    while True:
        print("\n========== SISTEM KOMUNITAS ==========")
        print("1. Tambah Anggota         (Create)")
        print("2. Lihat Semua Anggota    (Read)")
        print("3. Cari by ID             (Hash Map)")
        print("4. Cari by Nama           (Binary Search)")
        print("5. Ubah Anggota           (Update)")
        print("6. Hapus Anggota          (Delete)")
        print("7. Urutkan Anggota        (Insertion Sort)")
        print("0. Keluar")
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            data = input_data()
            if data["id"] and data["nama"]:
                sistem.create(data)
            else:
                print("[GAGAL] ID dan nama wajib diisi.")
        elif pilih == "2":
            tampil(sistem.read_all())
        elif pilih == "3":
            mid = input("Masukkan ID: ").strip()
            hasil = sistem.find_id(mid)
            tampil([hasil] if hasil else [])
        elif pilih == "4":
            nama = input("Masukkan nama: ").strip()
            hasil = sistem.find_nama(nama)
            tampil([hasil] if hasil else [])
        elif pilih == "5":
            mid = input("ID anggota yang diubah: ").strip()
            if sistem.find_id(mid):
                print("Kosongkan jika tidak ingin diubah:")
                nama = input("Nama baru     : ").strip()
                umur = input("Umur baru     : ").strip()
                kategori = input("jenis kelamin baru : ").strip()
                baru = {}
                if nama: baru["nama"] = nama
                if umur: baru["umur"] = umur
                if kategori: baru["jenis kelamin"] = kategori
                sistem.update(mid, baru)
            else:
                print("[GAGAL] ID tidak ditemukan.")
        elif pilih == "6":
            mid = input("ID anggota yang dihapus: ").strip()
            sistem.delete(mid)
        elif pilih == "7":
            tampil(sistem.sorted_by_nama())
        elif pilih == "0":
            print("Terima kasih.")
            break
        else:
            print("[GAGAL] Pilihan tidak valid.")


if __name__ == "__main__":
    main()
