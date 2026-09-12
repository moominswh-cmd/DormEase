import flet as ft
import database


def rooms_page(page: ft.Page, on_back):

    room_list = ft.Column(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
    )

    def load_rooms():

        room_list.controls.clear()

        rooms = database.get_all_rooms()

        if not rooms:
            room_list.controls.append(
                ft.Container(
                    padding=30,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                        controls=[
                            ft.Icon(
                                ft.Icons.HOME_OUTLINED,
                                size=60,
                                color="#A8BBD4",
                            ),
                            ft.Text(
                                "ยังไม่มีข้อมูลห้องพัก",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="#555555",
                            ),
                        ],
                    ),
                )
            )

        else:

            for room in rooms:

                room_id = room[0]
                room_number = room[1]
                room_type = room[2]
                price = room[3]
                status = room[4]

                if status == "ว่าง":
                    status_color = "#2E8B57"
                    status_bg = "#EAF7EF"
                else:
                    status_color = "#D97706"
                    status_bg = "#FFF4E5"

                room_card = ft.Container(
                    padding=18,
                    border_radius=16,
                    bgcolor="#FFFFFF",
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                width=55,
                                height=55,
                                border_radius=15,
                                bgcolor="#E8F1FF",
                                content=ft.Icon(
                                    ft.Icons.HOME,
                                    color="#3679D8",
                                    size=30,
                                ),
                            ),

                            ft.Column(
                                expand=True,
                                spacing=5,
                                controls=[
                                    ft.Text(
                                        f"ห้อง {room_number}",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        f"ประเภท: {room_type}",
                                        size=13,
                                        color="#777777",
                                    ),
                                    ft.Text(
                                        f"ค่าเช่า: {price:,.0f} บาท/เดือน",
                                        size=13,
                                        color="#555555",
                                    ),
                                ],
                            ),

                            ft.Container(
                                padding=8,
                                border_radius=20,
                                bgcolor=status_bg,
                                content=ft.Text(
                                    status,
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    color=status_color,
                                ),
                            ),
                        ],
                    ),
                )

                room_list.controls.append(room_card)

        page.update()

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
                "ห้องพัก",
                size=26,
                weight=ft.FontWeight.BOLD,
                color="#3679D8",
            ),
        ],
    )

    # =========================
    # TITLE
    # =========================

    title_section = ft.Column(
        spacing=3,
        controls=[
            ft.Text(
                "รายการห้องพัก",
                size=20,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Text(
                "ดูสถานะและข้อมูลห้องพักในหอพัก",
                size=13,
                color="#888888",
            ),
        ],
    )

    # โหลดข้อมูลห้องพัก
    load_rooms()

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
                title_section,
                ft.Container(
                    expand=True,
                    content=room_list,
                ),
            ],
        ),
    )