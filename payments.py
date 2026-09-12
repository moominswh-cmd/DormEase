import flet as ft
import database


def payments_page(page: ft.Page, on_back):

    payment_list = ft.Column(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
    )

    # =====================================================
    # FORM FIELDS
    # =====================================================

    tenant_dropdown = ft.Dropdown(
        label="ผู้เช่า",
        hint_text="เลือกผู้เช่า",
        width=500,
    )

    amount_field = ft.TextField(
        label="จำนวนเงิน",
        hint_text="เช่น 4000",
        width=500,
    )

    date_field = ft.TextField(
        label="วันที่ชำระ",
        hint_text="เช่น 12/09/2026",
        width=500,
    )

    status_dropdown = ft.Dropdown(
        label="สถานะ",
        width=500,
        options=[
            ft.DropdownOption(
                key="ชำระแล้ว",
                text="ชำระแล้ว",
            ),
            ft.DropdownOption(
                key="ยังไม่ชำระ",
                text="ยังไม่ชำระ",
            ),
        ],
        value="ชำระแล้ว",
    )

    message = ft.Text(
        "",
        size=14,
    )

    # =====================================================
    # LOAD TENANTS
    # =====================================================

    def load_tenant_options():

        tenants = database.get_all_tenants()

        options = []

        for tenant in tenants:

            tenant_id = tenant[0]
            name = tenant[1]
            room_number = tenant[4] or "-"

            options.append(
                ft.DropdownOption(
                    key=str(tenant_id),
                    text=f"{name} - ห้อง {room_number}",
                )
            )

        tenant_dropdown.options = options

    # =====================================================
    # CLEAR FORM
    # =====================================================

    def clear_form():

        tenant_dropdown.value = None
        amount_field.value = ""
        date_field.value = ""
        status_dropdown.value = "ชำระแล้ว"
        message.value = ""

    # =====================================================
    # SAVE NEW PAYMENT
    # =====================================================

    def save_payment(e):

        tenant_value = tenant_dropdown.value
        amount_value = (amount_field.value or "").strip()
        payment_date = (date_field.value or "").strip()
        status = status_dropdown.value

        # -------------------------
        # VALIDATION
        # -------------------------

        if not tenant_value:

            message.value = "กรุณาเลือกผู้เช่า"
            message.color = "#D32F2F"

            page.update()
            return

        if not amount_value:

            message.value = "กรุณากรอกจำนวนเงิน"
            message.color = "#D32F2F"

            page.update()
            return

        try:

            amount = float(
                amount_value.replace(",", "")
            )

        except ValueError:

            message.value = "จำนวนเงินต้องเป็นตัวเลข"
            message.color = "#D32F2F"

            page.update()
            return

        if amount <= 0:

            message.value = "จำนวนเงินต้องมากกว่า 0"
            message.color = "#D32F2F"

            page.update()
            return

        if not payment_date:

            message.value = "กรุณากรอกวันที่ชำระ"
            message.color = "#D32F2F"

            page.update()
            return

        # -------------------------
        # SAVE
        # -------------------------

        try:

            tenant_id = int(tenant_value)

            database.add_payment(
                tenant_id,
                amount,
                payment_date,
                status,
            )

            message.value = "บันทึกการชำระเงินสำเร็จ ✓"
            message.color = "#2E8B57"

            clear_form()

            load_payments()

            page.update()

        except Exception as ex:

            message.value = f"เกิดข้อผิดพลาด: {ex}"
            message.color = "#D32F2F"

            page.update()

    # =====================================================
    # EDIT PAYMENT
    # =====================================================

    def edit_payment(payment_id):

        payment = database.get_payment_by_id(payment_id)

        if payment is None:
            return

        # payment:
        # id
        # tenant_name
        # amount
        # payment_date
        # status

        # -------------------------------------------------
        # หา tenant_id จาก payment
        # -------------------------------------------------

        conn = database.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT tenant_id
            FROM payments
            WHERE id = ?
            """,
            (payment_id,)
        )

        result = cursor.fetchone()

        conn.close()

        if result is None:
            return

        tenant_id = result[0]

        # -------------------------------------------------
        # สร้าง Dropdown ผู้เช่า
        # -------------------------------------------------

        edit_tenant_dropdown = ft.Dropdown(
            label="ผู้เช่า",
            width=500,
            options=[],
            value=str(tenant_id),
        )

        tenants = database.get_all_tenants()

        for tenant in tenants:

            tid = tenant[0]
            name = tenant[1]
            room_number = tenant[4] or "-"

            edit_tenant_dropdown.options.append(
                ft.DropdownOption(
                    key=str(tid),
                    text=f"{name} - ห้อง {room_number}",
                )
            )

        # -------------------------------------------------
        # จำนวนเงิน
        # -------------------------------------------------

        try:
            edit_amount = float(
                str(payment[2] or 0).replace(",", "")
            )
        except ValueError:
            edit_amount = 0

        edit_amount_field = ft.TextField(
            label="จำนวนเงิน",
            value=str(edit_amount),
            width=500,
        )

        # -------------------------------------------------
        # วันที่
        # -------------------------------------------------

        edit_date_field = ft.TextField(
            label="วันที่ชำระ",
            value=payment[3] or "",
            width=500,
        )

        # -------------------------------------------------
        # สถานะ
        # -------------------------------------------------

        edit_status_dropdown = ft.Dropdown(
            label="สถานะ",
            width=500,
            options=[
                ft.DropdownOption(
                    key="ชำระแล้ว",
                    text="ชำระแล้ว",
                ),
                ft.DropdownOption(
                    key="ยังไม่ชำระ",
                    text="ยังไม่ชำระ",
                ),
            ],
            value=payment[4] or "ยังไม่ชำระ",
        )

        edit_message = ft.Text(
            "",
            size=14,
        )

        # -------------------------------------------------
        # SAVE EDIT
        # -------------------------------------------------

        def save_edit(e):

            if not edit_tenant_dropdown.value:

                edit_message.value = "กรุณาเลือกผู้เช่า"
                edit_message.color = "#D32F2F"

                page.update()
                return

            amount_text = (
                edit_amount_field.value or ""
            ).strip()

            try:

                amount = float(
                    amount_text.replace(",", "")
                )

            except ValueError:

                edit_message.value = "จำนวนเงินต้องเป็นตัวเลข"
                edit_message.color = "#D32F2F"

                page.update()
                return

            if amount <= 0:

                edit_message.value = "จำนวนเงินต้องมากกว่า 0"
                edit_message.color = "#D32F2F"

                page.update()
                return

            payment_date = (
                edit_date_field.value or ""
            ).strip()

            if not payment_date:

                edit_message.value = "กรุณากรอกวันที่ชำระ"
                edit_message.color = "#D32F2F"

                page.update()
                return

            try:

                database.update_payment(
                    payment_id,
                    int(edit_tenant_dropdown.value),
                    amount,
                    payment_date,
                    edit_status_dropdown.value,
                )

                show_payment_page()

            except Exception as ex:

                edit_message.value = (
                    f"เกิดข้อผิดพลาด: {ex}"
                )

                edit_message.color = "#D32F2F"

                page.update()

        # -------------------------------------------------
        # EDIT PAGE
        # -------------------------------------------------

        page.controls.clear()

        page.add(
            ft.Container(
                expand=True,
                padding=25,
                bgcolor="#F5F9FF",
                content=ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=20,
                    controls=[

                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="กลับ",
                                    on_click=lambda e: show_payment_page(),
                                ),

                                ft.Text(
                                    "แก้ไขการชำระเงิน",
                                    size=26,
                                    weight=ft.FontWeight.BOLD,
                                    color="#3679D8",
                                ),
                            ],
                        ),

                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    width=550,
                                    padding=25,
                                    border_radius=20,
                                    bgcolor="#FFFFFF",
                                    content=ft.Column(
                                        spacing=18,
                                        controls=[

                                            ft.Text(
                                                "แก้ไขข้อมูลการชำระเงิน",
                                                size=21,
                                                weight=ft.FontWeight.BOLD,
                                            ),

                                            edit_tenant_dropdown,

                                            edit_amount_field,

                                            edit_date_field,

                                            edit_status_dropdown,

                                            ft.Divider(),

                                            ft.ElevatedButton(
                                                "บันทึกการแก้ไข",
                                                icon=ft.Icons.SAVE,
                                                on_click=save_edit,
                                                width=500,
                                                height=50,
                                            ),

                                            edit_message,
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
            )
        )

        page.update()

    # =====================================================
    # DELETE PAYMENT
    # =====================================================

    def delete_payment(payment_id):

        try:

            database.delete_payment(payment_id)

            load_payments()

        except Exception as ex:

            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    f"เกิดข้อผิดพลาด: {ex}"
                )
            )

            page.snack_bar.open = True

            page.update()

    # =====================================================
    # LOAD PAYMENT LIST
    # =====================================================

    def load_payments():

        payment_list.controls.clear()

        payments = database.get_all_payments()

        if not payments:

            payment_list.controls.append(
                ft.Container(
                    padding=30,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                        controls=[

                            ft.Icon(
                                ft.Icons.PAYMENTS_OUTLINED,
                                size=60,
                                color="#A8BBD4",
                            ),

                            ft.Text(
                                "ยังไม่มีข้อมูลการชำระเงิน",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="#555555",
                            ),

                            ft.Text(
                                "เมื่อมีการบันทึกการชำระเงิน ข้อมูลจะแสดงที่นี่",
                                size=14,
                                color="#888888",
                            ),
                        ],
                    ),
                )
            )

        else:

            for payment in payments:

                payment_id = payment[0]
                tenant_name = payment[1] or "-"

                try:

                    amount = float(
                        str(payment[2] or 0).replace(",", "")
                    )

                except ValueError:

                    amount = 0

                payment_date = payment[3] or "-"
                status = payment[4] or "ยังไม่ชำระ"

                if status == "ชำระแล้ว":

                    status_color = "#2E8B57"
                    status_bg = "#EAF7EF"

                else:

                    status_color = "#D97706"
                    status_bg = "#FFF4E5"

                # -----------------------------------------
                # BUTTONS
                # -----------------------------------------

                edit_button = ft.ElevatedButton(
                    "แก้ไข",
                    icon=ft.Icons.EDIT,
                    width=110,
                    on_click=lambda e, pid=payment_id:
                        edit_payment(pid),
                )

                delete_button = ft.ElevatedButton(
                    "ลบ",
                    icon=ft.Icons.DELETE_OUTLINE,
                    width=110,
                    on_click=lambda e, pid=payment_id:
                        delete_payment(pid),
                )

                # -----------------------------------------
                # CARD
                # -----------------------------------------

                payment_card = ft.Container(
                    padding=18,
                    border_radius=16,
                    bgcolor="#FFFFFF",
                    content=ft.Column(
                        spacing=10,
                        controls=[

                            ft.Row(
                                controls=[

                                    ft.Container(
                                        width=48,
                                        height=48,
                                        border_radius=14,
                                        bgcolor="#FFF4DD",
                                        content=ft.Icon(
                                            ft.Icons.PAYMENTS,
                                            color="#D89B24",
                                            size=26,
                                        ),
                                    ),

                                    ft.Column(
                                        expand=True,
                                        spacing=3,
                                        controls=[

                                            ft.Text(
                                                tenant_name,
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                            ),

                                            ft.Text(
                                                f"รายการ ID: {payment_id}",
                                                size=12,
                                                color="#888888",
                                            ),
                                        ],
                                    ),

                                    ft.Container(
                                        padding=8,
                                        border_radius=20,
                                        bgcolor=status_bg,
                                        content=ft.Text(
                                            status,
                                            size=12,
                                            weight=ft.FontWeight.BOLD,
                                            color=status_color,
                                        ),
                                    ),
                                ],
                            ),

                            ft.Divider(
                                height=1
                            ),

                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.ATTACH_MONEY,
                                        size=20,
                                        color="#3679D8",
                                    ),

                                    ft.Text(
                                        f"จำนวนเงิน: {amount:,.0f} บาท",
                                        size=14,
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
                                        size=14,
                                    ),
                                ],
                            ),

                            ft.Row(
                                spacing=10,
                                controls=[
                                    edit_button,
                                    delete_button,
                                ],
                            ),
                        ],
                    ),
                )

                payment_list.controls.append(
                    payment_card
                )

        page.update()

    # =====================================================
    # SHOW PAYMENT PAGE
    # =====================================================

    def show_payment_page(e=None):

        page.controls.clear()

        page.add(
            payments_page(
                page,
                on_back,
            )
        )

        page.update()

    # =====================================================
    # HEADER
    # =====================================================

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

    # =====================================================
    # TITLE
    # =====================================================

    title_section = ft.Column(
        spacing=3,
        controls=[

            ft.Text(
                "จัดการการชำระเงิน",
                size=20,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Text(
                "บันทึกและตรวจสอบการชำระค่าเช่าของผู้เช่า",
                size=13,
                color="#888888",
            ),
        ],
    )

    # =====================================================
    # ADD PAYMENT FORM
    # =====================================================

    form_card = ft.Container(
        padding=22,
        border_radius=18,
        bgcolor="#FFFFFF",
        content=ft.Column(
            spacing=15,
            controls=[

                ft.Text(
                    "บันทึกการชำระเงิน",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),

                tenant_dropdown,

                amount_field,

                date_field,

                status_dropdown,

                ft.ElevatedButton(
                    "บันทึกการชำระเงิน",
                    icon=ft.Icons.SAVE,
                    on_click=save_payment,
                    width=500,
                    height=50,
                ),

                message,
            ],
        ),
    )

    # =====================================================
    # INITIAL LOAD
    # =====================================================

    load_tenant_options()
    load_payments()

    # =====================================================
    # RETURN
    # =====================================================

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

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        form_card,
                    ],
                ),

                ft.Text(
                    "ประวัติการชำระเงิน",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),

                payment_list,
            ],
        ),
    )