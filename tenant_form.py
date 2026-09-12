import flet as ft
import database


def tenant_form_page(page: ft.Page, on_back):

    # ==========================================
    # ดึงห้องว่างจากฐานข้อมูล
    # ==========================================

    def get_room_options():
        rooms = database.get_available_rooms()

        options = []

        for room in rooms:
            room_id = room[0]
            room_number = room[1]
            room_type = room[2]
            price = room[3]

            options.append(
                ft.DropdownOption(
                    key=str(room_id),
                    text=f"{room_number} - {room_type} ({price:,.0f} บาท)"
                )
            )

        return options

    # ==========================================
    # ช่องกรอกข้อมูลผู้เช่า
    # ==========================================

    name_field = ft.TextField(
        label="ชื่อ-นามสกุล",
        hint_text="กรอกชื่อและนามสกุลผู้เช่า",
        width=550,
    )

    phone_field = ft.TextField(
        label="เบอร์โทรศัพท์",
        hint_text="กรอกเบอร์โทรศัพท์",
        width=550,
    )

    email_field = ft.TextField(
        label="อีเมล",
        hint_text="กรอกอีเมล (ถ้ามี)",
        width=550,
    )

    room_dropdown = ft.Dropdown(
        label="ห้องพัก",
        hint_text="เลือกห้องพัก",
        options=get_room_options(),
        width=550,
    )

    date_field = ft.TextField(
        label="วันที่เข้าพัก",
        hint_text="เช่น 07/09/2026",
        width=550,
    )

    # ==========================================
    # ข้อความแจ้งเตือน
    # ==========================================

    message = ft.Text(
        "",
        size=14,
    )

    # ==========================================
    # ฟังก์ชันบันทึกข้อมูล
    # ==========================================

    def save_tenant(e):

        name = (name_field.value or "").strip()
        phone = (phone_field.value or "").strip()
        email = (email_field.value or "").strip()
        check_in_date = (date_field.value or "").strip()

        # --------------------------------------
        # ตรวจสอบชื่อ
        # --------------------------------------

        if not name:
            message.value = "กรุณากรอกชื่อ-นามสกุล"
            message.color = "#D32F2F"
            page.update()
            return

        # --------------------------------------
        # ตรวจสอบเบอร์โทรศัพท์
        # --------------------------------------

        if not phone:
            message.value = "กรุณากรอกเบอร์โทรศัพท์"
            message.color = "#D32F2F"
            page.update()
            return

        # --------------------------------------
        # ตรวจสอบห้องพัก
        # --------------------------------------

        if room_dropdown.value is None:
            message.value = "กรุณาเลือกห้องพัก"
            message.color = "#D32F2F"
            page.update()
            return

        # --------------------------------------
        # ตรวจสอบวันที่เข้าพัก
        # --------------------------------------

        if not check_in_date:
            message.value = "กรุณากรอกวันที่เข้าพัก"
            message.color = "#D32F2F"
            page.update()
            return

        # --------------------------------------
        # บันทึกลงฐานข้อมูล
        # --------------------------------------

        try:

            room_id = int(room_dropdown.value)

            database.add_tenant(
                name,
                phone,
                email,
                room_id,
                check_in_date
            )

            # ----------------------------------
            # แสดงข้อความสำเร็จ
            # ----------------------------------

            message.value = "บันทึกข้อมูลผู้เช่าสำเร็จ ✓"
            message.color = "#2E8B57"

            # ----------------------------------
            # ล้างข้อมูลในฟอร์ม
            # ----------------------------------

            name_field.value = ""
            phone_field.value = ""
            email_field.value = ""
            room_dropdown.value = None
            date_field.value = ""

            # ----------------------------------
            # โหลดห้องว่างใหม่
            # ----------------------------------

            room_dropdown.options = get_room_options()

            page.update()

        except Exception as ex:

            message.value = f"เกิดข้อผิดพลาด: {ex}"
            message.color = "#D32F2F"

            page.update()

    # ==========================================
    # ส่วนหัว
    # ==========================================

    header = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                tooltip="กลับ",
                on_click=on_back,
            ),

            ft.Text(
                "เพิ่มผู้เช่า",
                size=26,
                weight=ft.FontWeight.BOLD,
                color="#3679D8",
            ),
        ],
    )

    # ==========================================
    # การ์ดฟอร์ม
    # ==========================================

    form_card = ft.Container(
        width=600,
        padding=25,
        border_radius=20,
        bgcolor="#FFFFFF",

        content=ft.Column(
            spacing=18,

            controls=[

                ft.Text(
                    "ข้อมูลผู้เช่า",
                    size=21,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Text(
                    "กรุณากรอกข้อมูลผู้เช่าให้ครบถ้วน",
                    size=14,
                    color="#777777",
                ),

                name_field,

                phone_field,

                email_field,

                room_dropdown,

                date_field,

                ft.Divider(),

                # ==================================
                # ปุ่มบันทึก
                # ==================================

                ft.ElevatedButton(
                    "บันทึกข้อมูล",
                    icon=ft.Icons.SAVE,
                    on_click=save_tenant,
                    width=550,
                    height=50,
                ),

                message,
            ],
        ),
    )

    # ==========================================
    # หน้าหลักของหน้าเพิ่มผู้เช่า
    # ==========================================

    return ft.Container(
        expand=True,
        padding=25,
        bgcolor="#F5F9FF",

        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,

            controls=[

                header,

                ft.Container(
                    height=10,
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,

                    controls=[
                        form_card
                    ],
                ),
            ],
        ),
    )