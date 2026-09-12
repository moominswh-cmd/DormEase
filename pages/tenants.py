import flet as ft
import database


def tenants_page(page: ft.Page, on_back, on_add_tenant):

    tenant_list = ft.Column(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
    )

    # =====================================================
    # EDIT TENANT
    # =====================================================

    def edit_tenant(tenant_id):

        tenant = database.get_tenant_by_id(tenant_id)

        if tenant is None:
            return

        name_field = ft.TextField(
            label="ชื่อ-นามสกุล",
            value=tenant[1] or "",
            width=500,
        )

        phone_field = ft.TextField(
            label="เบอร์โทรศัพท์",
            value=tenant[2] or "",
            width=500,
        )

        email_field = ft.TextField(
            label="อีเมล",
            value=tenant[3] or "",
            width=500,
        )

        current_room_id = tenant[4]

        rooms = database.get_all_rooms()

        room_options = []

        for room in rooms:

            room_id = room[0]
            room_number = room[1]
            room_type = room[2]
            price = room[3]
            status = room[4]

            # ห้องของผู้เช่าคนนี้สามารถเลือกได้
            # ส่วนห้องอื่นจะเลือกได้เฉพาะห้องว่าง
            if room_id == current_room_id or status == "ว่าง":

                room_options.append(
                    ft.DropdownOption(
                        key=str(room_id),
                        text=f"{room_number} - {room_type} ({price:,.0f} บาท)",
                    )
                )

        room_dropdown = ft.Dropdown(
            label="ห้องพัก",
            width=500,
            options=room_options,
            value=str(current_room_id) if current_room_id else None,
        )

        date_field = ft.TextField(
            label="วันที่เข้าพัก",
            value=tenant[5] or "",
            width=500,
        )

        message = ft.Text(
            "",
            size=14,
        )

        # -------------------------------------------------
        # SAVE EDIT
        # -------------------------------------------------

        def save_edit(e):

            name = (name_field.value or "").strip()
            phone = (phone_field.value or "").strip()
            email = (email_field.value or "").strip()
            check_in_date = (date_field.value or "").strip()

            if not name:

                message.value = "กรุณากรอกชื่อ-นามสกุล"
                message.color = "#D32F2F"
                page.update()
                return

            if not phone:

                message.value = "กรุณากรอกเบอร์โทรศัพท์"
                message.color = "#D32F2F"
                page.update()
                return

            if not room_dropdown.value:

                message.value = "กรุณาเลือกห้องพัก"
                message.color = "#D32F2F"
                page.update()
                return

            if not check_in_date:

                message.value = "กรุณากรอกวันที่เข้าพัก"
                message.color = "#D32F2F"
                page.update()
                return

            try:

                new_room_id = int(room_dropdown.value)

                database.update_tenant(
                    tenant_id,
                    name,
                    phone,
                    email,
                    new_room_id,
                    check_in_date,
                )

                # กลับหน้าผู้เช่า
                show_tenants()

            except Exception as ex:

                message.value = f"เกิดข้อผิดพลาด: {ex}"
                message.color = "#D32F2F"
                page.update()

        # -------------------------------------------------
        # EDIT HEADER
        # -------------------------------------------------

        header = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    tooltip="กลับ",
                    on_click=lambda e: show_tenants(),
                ),

                ft.Text(
                    "แก้ไขข้อมูลผู้เช่า",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color="#3679D8",
                ),
            ],
        )

        # -------------------------------------------------
        # EDIT FORM
        # -------------------------------------------------

        form_card = ft.Container(
            width=550,
            padding=25,
            border_radius=20,
            bgcolor="#FFFFFF",
            content=ft.Column(
                spacing=18,
                controls=[

                    ft.Text(
                        "แก้ไขข้อมูล",
                        size=21,
                        weight=ft.FontWeight.BOLD,
                    ),

                    name_field,
                    phone_field,
                    email_field,
                    room_dropdown,
                    date_field,

                    ft.Divider(),

                    ft.ElevatedButton(
                        "บันทึกการแก้ไข",
                        icon=ft.Icons.SAVE,
                        on_click=save_edit,
                        width=500,
                        height=50,
                    ),

                    message,
                ],
            ),
        )

        page.controls.clear()

        page.add(
            ft.Container(
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
                                form_card,
                            ],
                        ),
                    ],
                ),
            )
        )

        page.update()

    # =====================================================
    # DELETE TENANT
    # =====================================================

    def delete_tenant(tenant_id):

        try:

            database.delete_tenant(tenant_id)

            load_tenants()

        except Exception as ex:

            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    f"เกิดข้อผิดพลาด: {ex}"
                )
            )

            page.snack_bar.open = True

            page.update()

    # =====================================================
    # LOAD TENANTS
    # =====================================================

    def load_tenants():

        tenant_list.controls.clear()

        tenants = database.get_all_tenants()

        if not tenants:

            empty_message = ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Icon(
                        ft.Icons.PEOPLE_OUTLINE,
                        size=60,
                        color="#A8BBD4",
                    ),

                    ft.Text(
                        "ยังไม่มีข้อมูลผู้เช่า",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#555555",
                    ),

                    ft.Text(
                        "กดปุ่มเพิ่มผู้เช่าเพื่อเพิ่มข้อมูล",
                        size=14,
                        color="#888888",
                    ),
                ],
            )

            tenant_list.controls.append(
                ft.Container(
                    padding=30,
                    content=empty_message,
                )
            )

        else:

            for tenant in tenants:

                tenant_id = tenant[0]
                name = tenant[1]
                phone = tenant[2] or "-"
                email = tenant[3] or "-"
                room_number = tenant[4] or "ยังไม่ได้ระบุห้อง"
                check_in_date = tenant[5] or "-"

                # -------------------------------------------------
                # EDIT BUTTON
                # -------------------------------------------------

                edit_button = ft.ElevatedButton(
                    "แก้ไข",
                    icon=ft.Icons.EDIT,
                    on_click=lambda e, tid=tenant_id: edit_tenant(tid),
                    width=110,
                )

                # -------------------------------------------------
                # DELETE BUTTON
                # -------------------------------------------------

                delete_button = ft.ElevatedButton(
                    "ลบ",
                    icon=ft.Icons.DELETE_OUTLINE,
                    on_click=lambda e, tid=tenant_id: delete_tenant(tid),
                    width=110,
                )

                # -------------------------------------------------
                # TENANT CARD
                # -------------------------------------------------

                tenant_card = ft.Container(
                    padding=18,
                    border_radius=16,
                    bgcolor="#FFFFFF",

                    content=ft.Column(
                        spacing=8,
                        controls=[

                            # -----------------------------
                            # NAME
                            # -----------------------------

                            ft.Row(
                                controls=[

                                    ft.Container(
                                        width=45,
                                        height=45,
                                        border_radius=25,
                                        bgcolor="#E8F1FF",

                                        content=ft.Icon(
                                            ft.Icons.PERSON,
                                            color="#3679D8",
                                            size=25,
                                        ),
                                    ),

                                    ft.Column(
                                        spacing=2,
                                        expand=True,

                                        controls=[

                                            ft.Text(
                                                name,
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                            ),

                                            ft.Text(
                                                f"ผู้เช่า ID: {tenant_id}",
                                                size=12,
                                                color="#888888",
                                            ),
                                        ],
                                    ),
                                ],
                            ),

                            ft.Divider(
                                height=1
                            ),

                            # -----------------------------
                            # ROOM
                            # -----------------------------

                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.HOME_OUTLINED,
                                        size=20,
                                        color="#3679D8",
                                    ),

                                    ft.Text(
                                        f"ห้องพัก: {room_number}",
                                        size=14,
                                    ),
                                ],
                            ),

                            # -----------------------------
                            # PHONE
                            # -----------------------------

                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.PHONE_OUTLINED,
                                        size=20,
                                        color="#3679D8",
                                    ),

                                    ft.Text(
                                        f"โทร: {phone}",
                                        size=14,
                                    ),
                                ],
                            ),

                            # -----------------------------
                            # EMAIL
                            # -----------------------------

                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.EMAIL_OUTLINED,
                                        size=20,
                                        color="#3679D8",
                                    ),

                                    ft.Text(
                                        f"อีเมล: {email}",
                                        size=14,
                                    ),
                                ],
                            ),

                            # -----------------------------
                            # CHECK IN DATE
                            # -----------------------------

                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.CALENDAR_MONTH_OUTLINED,
                                        size=20,
                                        color="#3679D8",
                                    ),

                                    ft.Text(
                                        f"วันที่เข้าพัก: {check_in_date}",
                                        size=14,
                                    ),
                                ],
                            ),

                            ft.Divider(
                                height=1
                            ),

                            # -----------------------------
                            # ACTION BUTTONS
                            # -----------------------------

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

                tenant_list.controls.append(
                    tenant_card
                )

        page.update()

    # =====================================================
    # SHOW TENANTS
    # =====================================================

    def show_tenants():

        page.controls.clear()

        page.add(
            tenants_page(
                page,
                on_back,
                on_add_tenant,
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
                "ผู้เช่าทั้งหมด",
                size=26,
                weight=ft.FontWeight.BOLD,
                color="#3679D8",
            ),
        ],
    )

    # =====================================================
    # ADD BUTTON
    # =====================================================

    add_button = ft.ElevatedButton(
        "เพิ่มผู้เช่า",
        icon=ft.Icons.PERSON_ADD,
        on_click=on_add_tenant,
        width=200,
        height=50,
    )

    # =====================================================
    # TITLE
    # =====================================================

    title_section = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[

            ft.Column(
                spacing=3,
                controls=[

                    ft.Text(
                        "รายชื่อผู้เช่า",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),

                    ft.Text(
                        "ข้อมูลผู้เช่าที่บันทึกไว้ในระบบ",
                        size=13,
                        color="#888888",
                    ),
                ],
            ),

            add_button,
        ],
    )

    # =====================================================
    # INITIAL LOAD
    # =====================================================

    load_tenants()

    # =====================================================
    # RETURN PAGE
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

                ft.Container(
                    content=tenant_list,
                    expand=True,
                ),
            ],
        ),
    )