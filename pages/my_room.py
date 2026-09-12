import flet as ft
import database


def my_room_page(page: ft.Page, on_back):

    # =========================
    # GET TENANT
    # =========================

    tenants = database.get_all_tenants()

    if not tenants:
        return ft.Container(
            expand=True,
            padding=25,
            bgcolor="#F5F9FF",
            content=ft.Column(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        on_click=on_back,
                    ),
                    ft.Text(
                        "ยังไม่มีข้อมูลผู้เช่า",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
            ),
        )

    # ใช้ผู้เช่าคนแรกสำหรับ MVP
    tenant_id = tenants[0][0]

    tenant = database.get_tenant_by_id(tenant_id)

    if tenant is None:
        return ft.Container(
            expand=True,
            padding=25,
            bgcolor="#F5F9FF",
            content=ft.Column(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        on_click=on_back,
                    ),
                    ft.Text(
                        "ไม่พบข้อมูลผู้เช่า",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
            ),
        )

    # tenant:
    # id, name, phone, email, room_id, check_in_date

    name = tenant[1]
    phone = tenant[2] or "-"
    email = tenant[3] or "-"
    room_id = tenant[4]
    check_in_date = tenant[5] or "-"

    # =========================
    # GET ROOM
    # =========================

    room = database.get_room_by_id(room_id)

    if room:
        room_number = room[1]
        room_type = room[2]
        price = room[3]
        status = room[4]
    else:
        room_number = "-"
        room_type = "-"
        price = 0
        status = "-"

    # =========================
    # HEADER
    # =========================

    header = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                tooltip="กลับ",
                on_click=on_back,
            ),
            ft.Text(
                "ห้องของฉัน",
                size=26,
                weight=ft.FontWeight.BOLD,
                color="#3679D8",
            ),
        ],
    )

    # =========================
    # ROOM HEADER
    # =========================

    room_header = ft.Container(
        padding=25,
        border_radius=22,
        bgcolor="#4385E5",
        content=ft.Row(
            controls=[
                ft.Container(
                    width=65,
                    height=65,
                    border_radius=18,
                    bgcolor="#FFFFFF",
                    content=ft.Icon(
                        ft.Icons.HOME,
                        size=35,
                        color="#4385E5",
                    ),
                ),

                ft.Column(
                    expand=True,
                    spacing=5,
                    controls=[
                        ft.Text(
                            f"ห้อง {room_number}",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color="white",
                        ),
                        ft.Text(
                            f"ห้องพักประเภท {room_type}",
                            size=14,
                            color="#EAF3FF",
                        ),
                    ],
                ),
            ],
        ),
    )

    # =========================
    # ROOM INFORMATION
    # =========================

    room_info = ft.Container(
        padding=22,
        border_radius=18,
        bgcolor="#FFFFFF",
        content=ft.Column(
            spacing=16,
            controls=[
                ft.Text(
                    "รายละเอียดห้องพัก",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.HOME_OUTLINED,
                            color="#3679D8",
                        ),
                        ft.Text(
                            f"หมายเลขห้อง: {room_number}",
                            size=15,
                        ),
                    ],
                ),

                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.CATEGORY_OUTLINED,
                            color="#3679D8",
                        ),
                        ft.Text(
                            f"ประเภทห้อง: {room_type}",
                            size=15,
                        ),
                    ],
                ),

                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.ATTACH_MONEY,
                            color="#3679D8",
                        ),
                        ft.Text(
                            f"ค่าเช่า: {price:,.0f} บาท/เดือน",
                            size=15,
                        ),
                    ],
                ),

                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.CALENDAR_MONTH_OUTLINED,
                            color="#3679D8",
                        ),
                        ft.Text(
                            f"วันที่เข้าพัก: {check_in_date}",
                            size=15,
                        ),
                    ],
                ),

                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.CHECK_CIRCLE_OUTLINE,
                            color="#2E8B57",
                        ),
                        ft.Text(
                            f"สถานะห้อง: {status}",
                            size=15,
                        ),
                    ],
                ),
            ],
        ),
    )

    # =========================
    # TENANT INFORMATION
    # =========================

    tenant_info = ft.Container(
        padding=22,
        border_radius=18,
        bgcolor="#FFFFFF",
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Text(
                    "ข้อมูลผู้เช่า",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.PERSON_OUTLINE,
                            color="#3679D8",
                        ),
                        ft.Text(
                            f"ชื่อ: {name}",
                            size=15,
                        ),
                    ],
                ),

                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.PHONE_OUTLINED,
                            color="#3679D8",
                        ),
                        ft.Text(
                            f"เบอร์โทร: {phone}",
                            size=15,
                        ),
                    ],
                ),

                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.EMAIL_OUTLINED,
                            color="#3679D8",
                        ),
                        ft.Text(
                            f"อีเมล: {email}",
                            size=15,
                        ),
                    ],
                ),
            ],
        ),
    )

    # =========================
    # RETURN PAGE
    # =========================

    return ft.Container(
        expand=True,
        padding=25,
        bgcolor="#F5F9FF",
        content=ft.Column(
            expand=True,
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                header,
                room_header,
                room_info,
                tenant_info,
            ],
        ),
    )