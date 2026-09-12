import flet as ft
import database


def my_payment_page(page: ft.Page, on_back):

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

    name = tenant[1]
    room_id = tenant[4]

    # =========================
    # GET ROOM
    # =========================

    room = database.get_room_by_id(room_id)

    if room:
        room_number = room[1]
        room_type = room[2]
        room_price = room[3]
    else:
        room_number = "-"
        room_type = "-"
        room_price = 0

    # =========================
    # GET PAYMENTS
    # =========================

    payments = database.get_payments_by_tenant(tenant_id)

    payment_list = ft.Column(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
    )

    if not payments:

        payment_list.controls.append(
            ft.Container(
                padding=25,
                border_radius=18,
                bgcolor="#FFFFFF",
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        ft.Icon(
                            ft.Icons.RECEIPT_LONG_OUTLINED,
                            size=55,
                            color="#A8BBD4",
                        ),
                        ft.Text(
                            "ยังไม่มีรายการชำระเงิน",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="#555555",
                        ),
                        ft.Text(
                            "เมื่อมีการบันทึกการชำระเงิน รายการจะแสดงที่นี่",
                            size=13,
                            color="#888888",
                        ),
                    ],
                ),
            )
        )

    else:

        for payment in payments:

            payment_id = payment[0]
            amount = payment[2] or 0
            payment_date = payment[3] or "-"
            status = payment[4] or "ยังไม่ชำระ"

            if status == "ชำระแล้ว":
                status_color = "#2E8B57"
                status_bg = "#EAF7EF"
                icon = ft.Icons.CHECK_CIRCLE
            else:
                status_color = "#D97706"
                status_bg = "#FFF4E5"
                icon = ft.Icons.PENDING

            payment_card = ft.Container(
                padding=20,
                border_radius=18,
                bgcolor="#FFFFFF",
                content=ft.Column(
                    spacing=12,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    width=50,
                                    height=50,
                                    border_radius=15,
                                    bgcolor="#FFF4DD",
                                    content=ft.Icon(
                                        ft.Icons.PAYMENTS,
                                        color="#D89B24",
                                        size=28,
                                    ),
                                ),

                                ft.Column(
                                    expand=True,
                                    spacing=3,
                                    controls=[
                                        ft.Text(
                                            "ค่าเช่าห้องพัก",
                                            size=17,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            f"รายการที่ {payment_id}",
                                            size=12,
                                            color="#888888",
                                        ),
                                    ],
                                ),

                                ft.Container(
                                    padding=8,
                                    border_radius=20,
                                    bgcolor=status_bg,
                                    content=ft.Row(
                                        spacing=5,
                                        controls=[
                                            ft.Icon(
                                                icon,
                                                size=15,
                                                color=status_color,
                                            ),
                                            ft.Text(
                                                status,
                                                size=12,
                                                color=status_color,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                        ],
                                    ),
                                ),
                            ],
                        ),

                        ft.Divider(height=1),

                        ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.Icons.ATTACH_MONEY,
                                    size=20,
                                    color="#3679D8",
                                ),
                                ft.Text(
                                    f"จำนวนเงิน: {amount:,.0f} บาท",
                                    size=15,
                                ),
                            ],
                        ),

                        ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.Icons.CALENDAR_MONTH_OUTLINED,
                                    size=20,
                                    color="#3679D8",
                                ),
                                ft.Text(
                                    f"วันที่ชำระ: {payment_date}",
                                    size=15,
                                ),
                            ],
                        ),
                    ],
                ),
            )

            payment_list.controls.append(payment_card)

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
                "การชำระเงิน",
                size=26,
                weight=ft.FontWeight.BOLD,
                color="#3679D8",
            ),
        ],
    )

    # =========================
    # SUMMARY CARD
    # =========================

    summary_card = ft.Container(
        padding=25,
        border_radius=22,
        bgcolor="#4385E5",
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    "สรุปค่าเช่าของฉัน",
                    size=15,
                    color="#EAF3FF",
                ),
                ft.Text(
                    name,
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                ),
                ft.Text(
                    f"ห้อง {room_number} • {room_type}",
                    size=14,
                    color="#EAF3FF",
                ),
                ft.Text(
                    f"ค่าเช่าประจำเดือน {room_price:,.0f} บาท",
                    size=17,
                    weight=ft.FontWeight.BOLD,
                    color="white",
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
                summary_card,

                ft.Text(
                    "ประวัติการชำระเงิน",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),

                payment_list,
            ],
        ),
    )