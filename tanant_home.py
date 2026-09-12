import flet as ft
import database


def tenant_home_page(
    page: ft.Page,
    tenant_id,
    on_my_room,
    on_my_payment,
    on_back
):

    # =========================
    # GET TENANT DATA
    # =========================

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
                        size=24,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
            ),
        )

    name = tenant[1]
    phone = tenant[2] or "-"
    email = tenant[3] or "-"
    room_id = tenant[4]
    check_in_date = tenant[5] or "-"

    # =========================
    # GET ROOM DATA
    # =========================

    room = database.get_room_by_id(room_id)

    if room:
        room_number = room[1]
        room_type = room[2]
        price = room[3]
    else:
        room_number = "-"
        room_type = "-"
        price = 0

    # =========================
    # GET PAYMENT DATA
    # =========================

    payments = database.get_payments_by_tenant(tenant_id)

    if payments:
        latest_payment = payments[0]
        latest_amount = latest_payment[2] or 0
        latest_status = latest_payment[4] or "ยังไม่ชำระ"
    else:
        latest_amount = price
        latest_status = "ยังไม่มีข้อมูล"

    # =========================
    # HEADER
    # =========================

    header = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Column(
                spacing=2,
                controls=[
                    ft.Text(
                        "DormEase",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="#3679D8",
                    ),
                    ft.Text(
                        "สำหรับผู้เช่า",
                        size=14,
                        color="#777777",
                    ),
                ],
            ),
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                tooltip="กลับ",
                on_click=on_back,
            ),
        ],
    )

    # =========================
    # WELCOME CARD
    # =========================

    welcome_card = ft.Container(
        width=float("inf"),
        padding=25,
        border_radius=22,
        bgcolor="#4385E5",
        content=ft.Row(
            controls=[
                ft.Column(
                    expand=True,
                    spacing=8,
                    controls=[
                        ft.Text(
                            "ยินดีต้อนรับ 👋",
                            size=16,
                            color="#EAF3FF",
                        ),
                        ft.Text(
                            name,
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color="white",
                        ),
                        ft.Text(
                            f"ห้องพัก {room_number}",
                            size=14,
                            color="#EAF3FF",
                        ),
                    ],
                ),
                ft.Icon(
                    ft.Icons.PERSON,
                    size=65,
                    color="white",
                ),
            ],
        ),
    )

    # =========================
    # ROOM CARD
    # =========================

    room_card = ft.Container(
        width=220,
        padding=20,
        border_radius=18,
        bgcolor="#EAF3FF",
        on_click=on_my_room,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Icon(
                    ft.Icons.HOME,
                    size=32,
                    color="#4285E5",
                ),
                ft.Text(
                    "ห้องของฉัน",
                    size=15,
                    color="#555555",
                ),
                ft.Text(
                    room_number,
                    size=25,
                    weight=ft.FontWeight.BOLD,
                    color="#2167D5",
                ),
                ft.Text(
                    f"ค่าเช่า {price:,.0f} บาท/เดือน",
                    size=12,
                    color="#777777",
                ),
            ],
        ),
    )

    # =========================
    # PAYMENT CARD
    # =========================

    if latest_status == "ชำระแล้ว":
        payment_color = "#2E8B57"
    else:
        payment_color = "#B67B13"

    payment_card = ft.Container(
        width=220,
        padding=20,
        border_radius=18,
        bgcolor="#FFF8E8",
        on_click=on_my_payment,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Icon(
                    ft.Icons.PAYMENTS,
                    size=32,
                    color="#D89B24",
                ),
                ft.Text(
                    "การชำระเงิน",
                    size=15,
                    color="#555555",
                ),
                ft.Text(
                    f"{latest_amount:,.0f} บาท",
                    size=25,
                    weight=ft.FontWeight.BOLD,
                    color="#B67B13",
                ),
                ft.Text(
                    f"สถานะ: {latest_status}",
                    size=12,
                    color=payment_color,
                ),
            ],
        ),
    )

    # =========================
    # MENU
    # =========================

    room_menu = ft.Container(
        width=150,
        padding=18,
        border_radius=16,
        bgcolor="white",
        on_click=on_my_room,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(
                    ft.Icons.HOME_OUTLINED,
                    color="#4385E5",
                    size=30,
                ),
                ft.Text(
                    "ห้องของฉัน",
                    size=14,
                ),
            ],
        ),
    )

    payment_menu = ft.Container(
        width=150,
        padding=18,
        border_radius=16,
        bgcolor="white",
        on_click=on_my_payment,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(
                    ft.Icons.PAYMENTS_OUTLINED,
                    color="#4385E5",
                    size=30,
                ),
                ft.Text(
                    "การชำระเงิน",
                    size=14,
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
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            controls=[
                header,
                welcome_card,

                ft.Text(
                    "ภาพรวมของฉัน",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Row(
                    wrap=True,
                    spacing=15,
                    run_spacing=15,
                    controls=[
                        room_card,
                        payment_card,
                    ],
                ),

                ft.Text(
                    "เมนู",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Row(
                    spacing=15,
                    controls=[
                        room_menu,
                        payment_menu,
                    ],
                ),

                ft.Text(
                    "ข้อมูลการเข้าพัก",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Container(
                    padding=20,
                    border_radius=18,
                    bgcolor="white",
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Text(
                                f"ชื่อผู้เช่า: {name}",
                                size=14,
                            ),
                            ft.Text(
                                f"เบอร์โทร: {phone}",
                                size=14,
                            ),
                            ft.Text(
                                f"ห้องพัก: {room_number}",
                                size=14,
                            ),
                            ft.Text(
                                f"ประเภทห้อง: {room_type}",
                                size=14,
                            ),
                            ft.Text(
                                f"วันที่เข้าพัก: {check_in_date}",
                                size=14,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )