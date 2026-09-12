import flet as ft
import database


def home_page(
    page: ft.Page,
    on_add_tenant,
    on_tenants,
    on_rooms,
    on_payments,
    on_tenant_view
):

    # =====================================================
    # GET REAL DATA FROM DATABASE
    # =====================================================

    stats = database.get_dashboard_stats()

    total_rooms = stats["total_rooms"]
    occupied_rooms = stats["occupied_rooms"]
    total_tenants = stats["total_tenants"]
    total_income = stats["total_income"]
    unpaid_count = stats["unpaid_count"]

    # =====================================================
    # ROOM CARD
    # =====================================================

    room_card = ft.Container(
        width=220,
        padding=20,
        border_radius=18,
        bgcolor="#EAF3FF",
        content=ft.Column(
            controls=[
                ft.Icon(
                    ft.Icons.HOME,
                    size=32,
                    color="#4285E5",
                ),
                ft.Text(
                    "ห้องพัก",
                    size=15,
                    color="#555555",
                ),
                ft.Text(
                    f"{total_rooms} ห้อง",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#2167D5",
                ),
                ft.Text(
                    f"ไม่ว่าง {occupied_rooms} ห้อง",
                    size=12,
                    color="#777777",
                ),
            ],
        ),
    )

    # =====================================================
    # TENANT CARD
    # =====================================================

    tenant_card = ft.Container(
        width=220,
        padding=20,
        border_radius=18,
        bgcolor="#EEF9F3",
        content=ft.Column(
            controls=[
                ft.Icon(
                    ft.Icons.PEOPLE,
                    size=32,
                    color="#35A66B",
                ),
                ft.Text(
                    "ผู้เช่า",
                    size=15,
                    color="#555555",
                ),
                ft.Text(
                    f"{total_tenants} คน",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#258A56",
                ),
            ],
        ),
    )

    # =====================================================
    # PAYMENT CARD
    # =====================================================

    payment_card = ft.Container(
        width=220,
        padding=20,
        border_radius=18,
        bgcolor="#FFF8E8",
        content=ft.Column(
            controls=[
                ft.Icon(
                    ft.Icons.PAYMENTS,
                    size=32,
                    color="#D89B24",
                ),
                ft.Text(
                    "รายได้",
                    size=15,
                    color="#555555",
                ),
                ft.Text(
                    f"{total_income:,.0f} บาท",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#B67B13",
                ),
                ft.Text(
                    "จากรายการที่ชำระแล้ว",
                    size=12,
                    color="#777777",
                ),
            ],
        ),
    )

    # =====================================================
    # UNPAID CARD
    # =====================================================

    overdue_card = ft.Container(
        width=220,
        padding=20,
        border_radius=18,
        bgcolor="#F5EEFF",
        content=ft.Column(
            controls=[
                ft.Icon(
                    ft.Icons.RECEIPT_LONG,
                    size=32,
                    color="#8B5BD6",
                ),
                ft.Text(
                    "ค้างชำระ",
                    size=15,
                    color="#555555",
                ),
                ft.Text(
                    f"{unpaid_count} รายการ",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#7043B5",
                ),
            ],
        ),
    )

    # =====================================================
    # HEADER
    # =====================================================

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
                        "ระบบจัดการหอพัก",
                        size=14,
                        color="#777777",
                    ),
                ],
            ),
        ],
    )

    # =====================================================
    # WELCOME
    # =====================================================

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
                            "ยินดีต้อนรับกลับ 👋",
                            size=16,
                            color="#EAF3FF",
                        ),
                        ft.Text(
                            "ผู้ดูแลหอพัก",
                            size=25,
                            weight=ft.FontWeight.BOLD,
                            color="white",
                        ),
                        ft.Row(
                            spacing=5,
                            controls=[
                                ft.Icon(
                                    ft.Icons.LOCATION_ON,
                                    size=16,
                                    color="white",
                                ),
                                ft.Text(
                                    "หอพักไพทอนร่วมใจ",
                                    color="white",
                                ),
                            ],
                        ),
                    ],
                ),
                ft.Icon(
                    ft.Icons.APARTMENT,
                    size=70,
                    color="white",
                ),
            ],
        ),
    )

    # =====================================================
    # QUICK MENU
    # =====================================================

    add_tenant_menu = ft.Container(
        width=120,
        padding=15,
        border_radius=16,
        bgcolor="white",
        on_click=on_add_tenant,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    ft.Icons.PERSON_ADD,
                    color="#4385E5",
                    size=30,
                ),
                ft.Text(
                    "เพิ่มผู้เช่า",
                    size=13,
                ),
            ],
        ),
    )

    tenant_menu = ft.Container(
        width=120,
        padding=15,
        border_radius=16,
        bgcolor="white",
        on_click=on_tenants,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    ft.Icons.PEOPLE,
                    color="#4385E5",
                    size=30,
                ),
                ft.Text(
                    "ผู้เช่า",
                    size=13,
                ),
            ],
        ),
    )

    room_menu = ft.Container(
        width=120,
        padding=15,
        border_radius=16,
        bgcolor="white",
        on_click=on_rooms,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    ft.Icons.HOME,
                    color="#4385E5",
                    size=30,
                ),
                ft.Text(
                    "ห้องพัก",
                    size=13,
                ),
            ],
        ),
    )

    payment_menu = ft.Container(
        width=120,
        padding=15,
        border_radius=16,
        bgcolor="white",
        on_click=on_payments,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    ft.Icons.PAYMENTS,
                    color="#4385E5",
                    size=30,
                ),
                ft.Text(
                    "การชำระเงิน",
                    size=13,
                ),
            ],
        ),
    )

    tenant_view_menu = ft.Container(
        width=150,
        padding=15,
        border_radius=16,
        bgcolor="white",
        on_click=on_tenant_view,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    ft.Icons.PERSON_OUTLINE,
                    color="#4385E5",
                    size=30,
                ),
                ft.Text(
                    "มุมมองผู้เช่า",
                    size=13,
                ),
            ],
        ),
    )

    quick_menu = ft.Row(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            add_tenant_menu,
            tenant_menu,
            room_menu,
            payment_menu,
        ],
    )

    # =====================================================
    # RETURN PAGE
    # =====================================================

    return ft.Container(
        expand=True,
        padding=25,
        bgcolor="#F5F9FF",
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            controls=[
                header,

                welcome_card,

                ft.Text(
                    "เมนูด่วน",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),

                quick_menu,

                tenant_view_menu,

                ft.Text(
                    "ภาพรวม",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Row(
                    wrap=True,
                    spacing=15,
                    run_spacing=15,
                    controls=[
                        room_card,
                        tenant_card,
                        payment_card,
                        overdue_card,
                    ],
                ),
            ],
        ),
    )