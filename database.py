import sqlite3
from pathlib import Path


# =========================================================
# DATABASE PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "dormease.db"


# =========================================================
# CONNECTION
# =========================================================

def get_connection():
    return sqlite3.connect(DATABASE_PATH)


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------
    # ROOMS
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT NOT NULL UNIQUE,
            room_type TEXT DEFAULT 'Standard',
            price REAL DEFAULT 0,
            status TEXT DEFAULT 'ว่าง'
        )
    """)

    # -------------------------
    # TENANTS
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tenants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            room_id INTEGER,
            check_in_date TEXT,
            FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
    """)

    # -------------------------
    # PAYMENTS
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id INTEGER,
            amount REAL DEFAULT 0,
            payment_date TEXT,
            status TEXT DEFAULT 'ยังไม่ชำระ',
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# SAMPLE ROOMS
# =========================================================

def add_sample_rooms():

    conn = get_connection()
    cursor = conn.cursor()

    rooms = [
        ("A101", "Standard", 4000),
        ("A102", "Standard", 4000),
        ("A103", "Standard", 4000),
        ("A104", "Standard", 4000),
        ("A105", "Standard", 4000),
        ("A201", "Standard", 4500),
        ("A202", "Standard", 4500),
        ("A203", "Standard", 4500),
        ("A204", "Standard", 4500),
        ("A205", "Standard", 4500),
    ]

    for room in rooms:

        try:

            cursor.execute("""
                INSERT INTO rooms
                (room_number, room_type, price)
                VALUES (?, ?, ?)
            """, room)

        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()


# =========================================================
# ROOMS
# =========================================================

def get_all_rooms():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            room_number,
            room_type,
            price,
            status
        FROM rooms
        ORDER BY room_number
    """)

    rooms = cursor.fetchall()

    conn.close()

    return rooms


def get_room_by_id(room_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            room_number,
            room_type,
            price,
            status
        FROM rooms
        WHERE id = ?
    """, (room_id,))

    room = cursor.fetchone()

    conn.close()

    return room


def get_available_rooms():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            room_number,
            room_type,
            price
        FROM rooms
        WHERE status = 'ว่าง'
        ORDER BY room_number
    """)

    rooms = cursor.fetchall()

    conn.close()

    return rooms


def add_room(room_number, room_type, price):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO rooms
        (room_number, room_type, price, status)
        VALUES (?, ?, ?, 'ว่าง')
    """, (
        room_number,
        room_type,
        price
    ))

    conn.commit()
    conn.close()


def update_room(room_id, room_number, room_type, price, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE rooms
        SET
            room_number = ?,
            room_type = ?,
            price = ?,
            status = ?
        WHERE id = ?
    """, (
        room_number,
        room_type,
        price,
        status,
        room_id
    ))

    conn.commit()
    conn.close()


def delete_room(room_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM rooms
        WHERE id = ?
    """, (room_id,))

    conn.commit()
    conn.close()


# =========================================================
# TENANTS
# =========================================================

def get_all_tenants():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            tenants.id,
            tenants.name,
            tenants.phone,
            tenants.email,
            rooms.room_number,
            tenants.check_in_date
        FROM tenants
        LEFT JOIN rooms
            ON tenants.room_id = rooms.id
        ORDER BY tenants.id DESC
    """)

    tenants = cursor.fetchall()

    conn.close()

    return tenants


def get_tenant_by_id(tenant_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            phone,
            email,
            room_id,
            check_in_date
        FROM tenants
        WHERE id = ?
    """, (tenant_id,))

    tenant = cursor.fetchone()

    conn.close()

    return tenant


def add_tenant(
    name,
    phone,
    email,
    room_id,
    check_in_date
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tenants
        (
            name,
            phone,
            email,
            room_id,
            check_in_date
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        phone,
        email,
        room_id,
        check_in_date
    ))

    # เปลี่ยนสถานะห้องเป็นไม่ว่าง
    cursor.execute("""
        UPDATE rooms
        SET status = 'ไม่ว่าง'
        WHERE id = ?
    """, (room_id,))

    conn.commit()
    conn.close()


def update_tenant(
    tenant_id,
    name,
    phone,
    email,
    room_id,
    check_in_date
):

    conn = get_connection()
    cursor = conn.cursor()

    # หาห้องเดิมก่อน
    cursor.execute("""
        SELECT room_id
        FROM tenants
        WHERE id = ?
    """, (tenant_id,))

    old_data = cursor.fetchone()

    old_room_id = old_data[0] if old_data else None

    # อัปเดตข้อมูลผู้เช่า
    cursor.execute("""
        UPDATE tenants
        SET
            name = ?,
            phone = ?,
            email = ?,
            room_id = ?,
            check_in_date = ?
        WHERE id = ?
    """, (
        name,
        phone,
        email,
        room_id,
        check_in_date,
        tenant_id
    ))

    # ถ้าเปลี่ยนห้อง
    if old_room_id != room_id:

        # ห้องเดิมกลับมาว่าง
        if old_room_id is not None:

            cursor.execute("""
                UPDATE rooms
                SET status = 'ว่าง'
                WHERE id = ?
            """, (old_room_id,))

        # ห้องใหม่ไม่ว่าง
        if room_id is not None:

            cursor.execute("""
                UPDATE rooms
                SET status = 'ไม่ว่าง'
                WHERE id = ?
            """, (room_id,))

    conn.commit()
    conn.close()


def delete_tenant(tenant_id):

    conn = get_connection()
    cursor = conn.cursor()

    # หาห้องของผู้เช่าก่อน
    cursor.execute("""
        SELECT room_id
        FROM tenants
        WHERE id = ?
    """, (tenant_id,))

    tenant = cursor.fetchone()

    room_id = tenant[0] if tenant else None

    # ลบประวัติการชำระเงินของผู้เช่า
    cursor.execute("""
        DELETE FROM payments
        WHERE tenant_id = ?
    """, (tenant_id,))

    # ลบผู้เช่า
    cursor.execute("""
        DELETE FROM tenants
        WHERE id = ?
    """, (tenant_id,))

    # ทำให้ห้องกลับมาว่าง
    if room_id is not None:

        cursor.execute("""
            UPDATE rooms
            SET status = 'ว่าง'
            WHERE id = ?
        """, (room_id,))

    conn.commit()
    conn.close()


# =========================================================
# PAYMENTS
# =========================================================

def get_all_payments():

    conn = get_connection()
    cursor = conn.cursor()

    # สำคัญ:
    # คืนค่าตามลำดับนี้
    #
    # payment_id
    # tenant_name
    # amount
    # payment_date
    # status

    cursor.execute("""
        SELECT
            payments.id,
            tenants.name,
            payments.amount,
            payments.payment_date,
            payments.status
        FROM payments
        LEFT JOIN tenants
            ON payments.tenant_id = tenants.id
        ORDER BY payments.id DESC
    """)

    payments = cursor.fetchall()

    conn.close()

    return payments


def get_payment_by_id(payment_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            payments.id,
            tenants.name,
            payments.amount,
            payments.payment_date,
            payments.status
        FROM payments
        LEFT JOIN tenants
            ON payments.tenant_id = tenants.id
        WHERE payments.id = ?
    """, (payment_id,))

    payment = cursor.fetchone()

    conn.close()

    return payment


def get_payments_by_tenant(tenant_id):

    conn = get_connection()
    cursor = conn.cursor()

    # สำคัญ:
    # คืนค่าตามลำดับเดียวกับ get_all_payments()

    cursor.execute("""
        SELECT
            payments.id,
            tenants.name,
            payments.amount,
            payments.payment_date,
            payments.status
        FROM payments
        LEFT JOIN tenants
            ON payments.tenant_id = tenants.id
        WHERE payments.tenant_id = ?
        ORDER BY payments.id DESC
    """, (tenant_id,))

    payments = cursor.fetchall()

    conn.close()

    return payments


def add_payment(
    tenant_id,
    amount,
    payment_date,
    status
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO payments
        (
            tenant_id,
            amount,
            payment_date,
            status
        )
        VALUES (?, ?, ?, ?)
    """, (
        tenant_id,
        amount,
        payment_date,
        status
    ))

    conn.commit()
    conn.close()


def update_payment(
    payment_id,
    tenant_id,
    amount,
    payment_date,
    status
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE payments
        SET
            tenant_id = ?,
            amount = ?,
            payment_date = ?,
            status = ?
        WHERE id = ?
    """, (
        tenant_id,
        amount,
        payment_date,
        status,
        payment_id
    ))

    conn.commit()
    conn.close()


def delete_payment(payment_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM payments
        WHERE id = ?
    """, (payment_id,))

    conn.commit()
    conn.close()


# =========================================================
# DASHBOARD
# =========================================================

def get_dashboard_stats():

    conn = get_connection()
    cursor = conn.cursor()

    # จำนวนห้องทั้งหมด
    cursor.execute("""
        SELECT COUNT(*)
        FROM rooms
    """)

    total_rooms = cursor.fetchone()[0]

    # จำนวนห้องว่าง
    cursor.execute("""
        SELECT COUNT(*)
        FROM rooms
        WHERE status = 'ว่าง'
    """)

    available_rooms = cursor.fetchone()[0]

    # จำนวนผู้เช่า
    cursor.execute("""
        SELECT COUNT(*)
        FROM tenants
    """)

    total_tenants = cursor.fetchone()[0]

    # รายได้ทั้งหมดจากรายการที่ชำระแล้ว
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM payments
        WHERE status = 'ชำระแล้ว'
    """)

    total_income = cursor.fetchone()[0]

    # จำนวนรายการค้างชำระ
    cursor.execute("""
        SELECT COUNT(*)
        FROM payments
        WHERE status = 'ยังไม่ชำระ'
    """)

    unpaid_count = cursor.fetchone()[0]

    conn.close()

    return {
        "total_rooms": total_rooms,
        "available_rooms": available_rooms,
        "occupied_rooms": total_rooms - available_rooms,
        "total_tenants": total_tenants,
        "total_income": total_income,
        "unpaid_count": unpaid_count,
    }


# =========================================================
# START DATABASE
# =========================================================

init_db()
add_sample_rooms()