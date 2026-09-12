import flet as ft 
import database 

from pages.home import home_page
from pages.tenant_form import tenant_form_page
from pages.tenants import tenants_page
from pages.rooms import rooms_page
from pages.payments import payments_page
from pages.tanant_home import tenant_home_page
from pages.my_room import my_room_page
from pages.my_payment import my_payment_page


def main(page: ft.Page):

    page.title = "DormEase"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = "#F5F9FF"

    # =========================
    # OWNER / ADMIN
    # =========================

    def show_home(e=None):
        page.controls.clear()

        page.add(
            home_page(
                page,
                show_add_tenant,
                show_tenants,
                show_rooms,
                show_payments,
                show_tenant_home
            )
        )

        page.update()

    def show_add_tenant(e=None):
        page.controls.clear()

        page.add(
            tenant_form_page(
                page,
                show_home
            )
        )

        page.update()

    def show_tenants(e=None):
        page.controls.clear()

        page.add(
            tenants_page(
                page,
                show_home,
                show_add_tenant
            )
        )

        page.update()

    def show_rooms(e=None):
        page.controls.clear()

        page.add(
            rooms_page(
                page,
                show_home
            )
        )

        page.update()

    def show_payments(e=None):
        page.controls.clear()

        page.add(
            payments_page(
                page,
                show_home
            )
        )

        page.update()

    # =========================
    # TENANT
    # =========================

    def show_tenant_home(e=None):

        # ดึงผู้เช่าคนแรกจากฐานข้อมูล
        tenants = database.get_all_tenants()

        if not tenants:
            page.controls.clear()

            page.add(
                ft.Container(
                    expand=True,
                    padding=30,
                    bgcolor="#F5F9FF",
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                        controls=[
                            ft.Icon(
                                ft.Icons.PEOPLE_OUTLINE,
                                size=60,
                                color="#A8BBD4",
                            ),
                            ft.Text(
                                "ยังไม่มีข้อมูลผู้เช่า",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "กรุณาเพิ่มผู้เช่าก่อนเข้าสู่มุมมองผู้เช่า",
                                size=14,
                                color="#777777",
                            ),
                            ft.ElevatedButton(
                                "กลับหน้า Dashboard",
                                on_click=show_home,
                            ),
                        ],
                    ),
                )
            )

            page.update()
            return

        # get_all_tenants() คืนค่า:
        # id, name, phone, email, room_number, check_in_date
        tenant_id = tenants[0][0]

        page.controls.clear()

        page.add(
            tenant_home_page(
                page,
                tenant_id,
                show_my_room,
                show_my_payment,
                show_home
            )
        )

        page.update()

    def show_my_room(e=None):

        # ผู้เช่าคนแรก
        tenants = database.get_all_tenants()

        if not tenants:
            show_tenant_home()
            return

        tenant_id = tenants[0][0]

        page.controls.clear()

        page.add(
            my_room_page(
                page,
                on_back=show_tenant_home
            )
        )

        page.update()

    def show_my_payment(e=None):

        # ผู้เช่าคนแรก
        tenants = database.get_all_tenants()

        if not tenants:
            show_tenant_home()
            return

        tenant_id = tenants[0][0]

        page.controls.clear()

        page.add(
            my_payment_page(
                page,
                on_back=show_tenant_home
            )
        )

        page.update()

    # =========================
    # START APPLICATION
    # =========================

    show_home()


import os

port = int(os.environ.get("PORT", 8502))
ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)