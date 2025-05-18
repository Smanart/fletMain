from flet import *
from flet import View
from datetime import datetime
from db import get_professor_classes, get_pending_activities
from db import authenticate_user, register_user
from db import create_class as db_create_class, create_activity as db_create_activity, create_quiz as db_create_quiz
from db import update_class, delete_class, get_class_by_id, get_quiz_by_id, get_quiz_questions, save_student_answer, get_pending_quizzes, get_finished_quizzes, get_finished_activities
from db import get_student_classes, get_student_pending_activities, join_class, get_activities_by_class_id, get_quizzes_by_class_id, upload_student_file
from db import random, string
from urllib.parse import urlparse, parse_qs

def professor_login_view(page: Page):

    back_button = TextButton(
        "Back",
        on_click=lambda _: page.go("/"),
        style = ButtonStyle( color = 'green')
    )

    username_field = TextField(label="Username", width=400)
    password_field = TextField(label="Password", width=400, password=True)

    def handle_submit(e):
        username = username_field.value.strip()
        password = password_field.value.strip()
        user_id = authenticate_user(username, password, "professor")

        if user_id:
            page.session.set("user_id", user_id)
            page.update()
            page.go("/professor_dashboard")

        else:
            page.update()
            page.go("/professor_invalid_credentials")

    return Column(
        controls=[
            Container(
                content=back_button,
                alignment=alignment.top_left
            ),
            Column(
                controls=[
                    Text("Professor Login Page", size=30, color="green"),
                    username_field,
                    password_field,
                    ElevatedButton(
                        "Submit",
                        on_click=handle_submit,
                        height=50,
                        width=150,
                        color="white",
                        bgcolor="green"
                    )
                ]
            ),
        ],
        horizontal_alignment=CrossAxisAlignment.CENTER
    )

def student_login_view(page: Page):

    back_button = TextButton(
        "Back",
        on_click = lambda _: page.go("/"),
        style = ButtonStyle(color = 'green')
    )

    username_field = TextField(label="Username", width=400)
    password_field = TextField(label="Password", width=400, password=True)

    def handle_submit(e):
        username = username_field.value.strip()
        password = password_field.value.strip()
        user_id = authenticate_user(username, password, "student")

        if user_id:
            page.session.set("user_id", user_id)
            page.update()
            page.go("/student_dashboard")

        else:
            page.update()
            page.go("/student_invalid_credentials")

    return Column(
        controls=[
            Container(
                content=back_button,
                alignment=alignment.top_left
            ),
            Column(
                controls=[
                    Text("Student Login Page", size=30, color="green"),
                    username_field,
                    password_field,
                    ElevatedButton(
                        "Submit",
                        on_click=handle_submit,
                        height=50,
                        width=150,
                        color="white",
                        bgcolor="green"
                    )
                ]
            ),
        ],
        horizontal_alignment=CrossAxisAlignment.CENTER
    )

def professor_sign_up_view(page: Page):
    back_button = TextButton(
        "Back",
        on_click=lambda _: page.go("/"),
        style=ButtonStyle(color='green')
    )

    first_name_field = TextField(label="First Name", width=400)
    last_name_field = TextField(label="Last Name", width=400)
    username_field = TextField(label="Username", width=400)
    password_field = TextField(label="Password", width=400, password=True)

    def handle_submit(e):
        first_name = first_name_field.value.strip()
        last_name = last_name_field.value.strip()
        username = username_field.value.strip()
        password = password_field.value.strip()

        if not (first_name and last_name and username and password):
            page.snack_bar = SnackBar(Text("All fields are required."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        if register_user(username, password, "professor", first_name, last_name):
            page.snack_bar = SnackBar(Text("Sign up successful!"), bgcolor="green")
            page.snack_bar.open = True
            page.update()
            page.go("/")
        else:
            page.snack_bar = SnackBar(Text("Sign up failed! Username may already exist."), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    return Column(
        controls=[
            Container(content=back_button, alignment=alignment.top_left),
            Column(
                controls=[
                    Text("Sign up as a Professor", size=30, color="green"),
                    first_name_field,
                    last_name_field,
                    username_field,
                    password_field,
                    ElevatedButton(
                        "Submit",
                        on_click=handle_submit,
                        height=50,
                        width=150,
                        color="white",
                        bgcolor="green"
                    )
                ]
            )
        ],
        horizontal_alignment=CrossAxisAlignment.CENTER
    )

def student_sign_up_view(page: Page):
    back_button = TextButton(
        "Back",
        on_click=lambda _: page.go("/"),
        style=ButtonStyle(color='green')
    )

    first_name_field = TextField(label="First Name", width=400)
    last_name_field = TextField(label="Last Name", width=400)
    username_field = TextField(label="Username", width=400)
    password_field = TextField(label="Password", width=400, password=True)

    def handle_submit(e):
        first_name = first_name_field.value.strip()
        last_name = last_name_field.value.strip()
        username = username_field.value.strip()
        password = password_field.value.strip()

        if not (first_name and last_name and username and password):
            page.snack_bar = SnackBar(Text("All fields are required."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        if register_user(username, password, "student", first_name, last_name):
            page.snack_bar = SnackBar(Text("Sign up successful!"), bgcolor="green")
            page.snack_bar.open = True
            page.update()
            page.go("/")
        else:
            page.snack_bar = SnackBar(Text("Sign up failed! Username may already exist."), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    return Column(
        controls=[
            Container(content=back_button, alignment=alignment.top_left),
            Column(
                controls=[
                    Text("Sign up as a Student", size=30, color="green"),
                    first_name_field,
                    last_name_field,
                    username_field,
                    password_field,
                    ElevatedButton(
                        "Submit",
                        on_click=handle_submit,
                        height=50,
                        width=150,
                        color="white",
                        bgcolor="green"
                    )
                ]
            )
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

def professor_dashboard_view(page: Page):
    def navigate_to(route):
        page.go(route)

    professor_id = page.session.get("user_id")
    if not professor_id:
        page.go("/")
        return

    navbar = Row(
        controls=[
            TextButton("Dashboard", on_click=lambda e: navigate_to("/professor_dashboard"), style=ButtonStyle(bgcolor='green', color='white')),
            TextButton("Log-out", on_click=lambda e: navigate_to("/"), style=ButtonStyle(color='white'))
        ]
    )

    class_container = Row(wrap=True)

    def refresh_classes():
        classes = get_professor_classes(professor_id) or []
        
        class_container.controls.clear()

        for cls in classes:
            print(f"[DEBUG] Class data: {cls}")
            class_container.controls.append(
                Container(
                    content=Column(
                        controls=[
                            Text(f"📚 {cls['subject_name']}", size=18, weight="bold"),
                            Text(f"Class Name: {cls['class_name']}"),
                            Text(f"Subject: {cls['subject_name']}"),
                            Text(f"Class Code: {cls['class_code']}", color="blue"),
                            Row(
                                controls=[
                                    TextButton("View", on_click=lambda e, c=cls: print(f"Viewing: {c}")),
                                    TextButton("Edit", on_click=lambda e, c=cls: open_edit_dialog(c)),
                                    TextButton("Delete", on_click=lambda e, cid=cls['id']: open_delete_dialog(cid)),
                                    TextButton("Create Activity", on_click=lambda e, cid=cls['id']: page.go(f"/create_activity?class_id={cid}")),
                                    TextButton("Create Quiz", on_click=lambda e, cid=cls['id']: page.go(f"/create_quiz?class_id={cid}")),
                                ],
                                spacing=5
                            )
                        ]
                    ),
                    bgcolor="white",
                    padding=15,
                    border_radius=10,
                    shadow=BoxShadow(blur_radius=6, color="grey"),
                    margin=5
                )
            )
        page.update()

    def open_edit_dialog(class_data):
        class_name_field = TextField(label="Class Name", value=class_data['class_name'])
        subject_field = TextField(label="Subject", value=class_data['subject_name'])

        def submit_update(e):
            update_class(class_data['id'], class_name_field.value, subject_field.value)
            page.dialog.open = False
            refresh_classes()

        dialog = AlertDialog(
            title=Text("Edit Class"),
            content=Column([class_name_field, subject_field]),
            actions=[
                TextButton("Cancel", on_click=lambda e: close_dialog()),
                TextButton("Update", on_click=submit_update)
            ]
        )
        page.dialog = dialog
        page.overlay.append(dialog)
        page.dialog.open = True
        page.update()

    def open_delete_dialog(class_id):
        def confirm_delete(e):
            delete_class(class_id)
            page.dialog.open = False
            refresh_classes()

        dialog = AlertDialog(
            title=Text("Confirm Deletion"),
            content=Text("Are you sure you want to delete this class?"),
            actions=[
                TextButton("Cancel", on_click=lambda e: close_dialog()),
                TextButton("Delete", on_click=confirm_delete)
            ]
        )
        page.dialog = dialog
        page.overlay.append(dialog)
        page.dialog.open = True
        page.update()

    def close_dialog():
        page.dialog.open = False
        page.update()

    def open_create_class_dialog(e):
        class_name_field = TextField(label="Class Name")
        subject_field = TextField(label="Subject")

        def generate_class_code(length=6):
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

        def submit_class(ev):
            professor_id = page.session.get("user_id")
            if professor_id is None:
                page.snack_bar = SnackBar(Text("Session expired. Please log in again."))
                page.snack_bar.open = True
                page.update()
                return

            class_name = class_name_field.value
            subject_name = subject_field.value
            class_code = generate_class_code()

            print(f"[DEBUG] Creating class with code: {class_code}")

            db_create_class(professor_id, class_name_field.value, subject_field.value)
            close_dialog()
            refresh_classes()

        dialog = AlertDialog(
            title=Text("Create Class"),
            content=Column([class_name_field, subject_field]),
            actions=[
                TextButton("Cancel", on_click=lambda e: close_dialog()),
                TextButton("Create", on_click=submit_class)
            ]
        )
        page.dialog = dialog
        page.overlay.append(dialog)
        page.dialog.open = True
        page.update()

    # Initial load of classes
    refresh_classes()

    activities = get_pending_activities(professor_id) or []
    activity_list = [
        ListTile(
            title=Text(f"{'📝' if act['type'] == 'activity' else '🧠'} {act['title']}"),
            subtitle=Text(f"Due: {act['due_date'].strftime('%Y-%m-%d') if isinstance(act['due_date'], datetime) else act['due_date']}")
        ) for act in activities
    ]

    return Column(
        controls=[
            Container(Text("Dashboard", size=30, weight='bold', color='green'), alignment=alignment.top_center, padding=10),
            Container(content=navbar, bgcolor='lightgreen', padding=10),
            Divider(),
            Text("Your Classes", size=20, weight="bold"),
            class_container,
            Divider(),
            Text("Pending Activities", size=20, weight="bold"),
            Column(controls=activity_list),
            Container(
                content=FloatingActionButton(
                    text="Create Class",
                    bgcolor="green",
                    on_click=open_create_class_dialog
                ),
                alignment=alignment.bottom_right,
                margin=10,
            )
        ],
        scroll="auto",
        horizontal_alignment=CrossAxisAlignment.CENTER,
        alignment=MainAxisAlignment.START,
        expand=True
    )

def create_activity_view(page: Page):
    query = parse_qs(urlparse(page.route).query)
    class_id = query.get("class_id", [None])[0]
    
    title_field = TextField(label="Activity Title", width=400)
    description_field = TextField(label="Description", multiline=True, min_lines=3, max_lines=5, width=400)
    due_date_picker = DatePicker()
    page.overlay.append(due_date_picker)  # Add to overlay
    
    def open_date_picker(e):
        due_date_picker.open = True
        page.update()

    due_date_button = TextButton("Select Due Date", on_click=open_date_picker)


    def handle_submit(e):
        try:
            title = title_field.value.strip()
            description = description_field.value.strip()
            due_date = due_date_picker.value.strftime("%Y-%m-%d") if due_date_picker.value else None

            if not title or not due_date:
                page.snack_bar = SnackBar(
                    Text("Title and Due Date are required!", color="white"),
                    bgcolor="red"
                )
                page.snack_bar.open = True
                page.update()
                return

            professor_id = page.session.get("user_id")
            db_create_activity(class_id, title, description, due_date)

            page.snack_bar = SnackBar(
                Text("Activity created successfully!", color="white"),
                bgcolor="green"
            )
            page.snack_bar.open = True
            page.update()
            page.go(f"/professor_dashboard")

        except Exception as ex:
            print(f"[ERROR] {ex}")
            page.snack_bar = SnackBar(
                Text("An error occurred while submitting.", color="white"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()

    return Column(
        controls=[
            Text(f"Create Activity for Class ID: {class_id}", size=20, weight="bold"),
            Column([
                Text("Create New Activity", size=24, weight="bold"),
                title_field,
                description_field,
                Row([Text("Due Date:"), due_date_button]),
                ElevatedButton("Submit", on_click=handle_submit, bgcolor="green", color="white"),
            ], spacing=20, alignment=MainAxisAlignment.START, horizontal_alignment=CrossAxisAlignment.CENTER),
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )

def create_quiz_view(page: Page):
    query = parse_qs(urlparse(page.route).query)
    class_id = query.get("class_id", [None])[0]

    page.appbar = AppBar(
        title=Text(f"Create Quiz for Class ID: {class_id}"),
        center_title=True
    )

    title_field = TextField(label="Quiz Title", width=400)
    question_fields = []
    answer_fields = []

    for i in range(5):
        question_fields.append(TextField(label=f"Question {i + 1}", width=400))
        answer_fields.append(TextField(label=f"Correct Answer {i + 1}", width=400))

    due_date_picker = DatePicker()
    page.overlay.append(due_date_picker)

    def open_date_picker(e):
        due_date_picker.open = True
        page.update()

    due_date_button = TextButton("Select Due Date", on_click=open_date_picker)

    def handle_submit(e):
        try:
            title = title_field.value.strip()
            questions = [q.value.strip() for q in question_fields]
            answers = [a.value.strip() for a in answer_fields]
            due_date = due_date_picker.value.strftime("%Y-%m-%d") if due_date_picker.value else None

            if not title or not due_date or any(not q for q in questions) or any(not a for a in answers):
                page.snack_bar = SnackBar(
                    Text("All fields are required!", color="white"),
                    bgcolor="red"
                )
                page.snack_bar.open = True
                page.update()
                return

            professor_id = page.session.get("user_id")
            from db import create_quiz  # or `from db import create_quiz as db_create_quiz`

            # Create quiz
            create_quiz(professor_id, class_id, title, due_date,
                        [{"question": q, "answer": a} for q, a in zip(questions, answers)])

            page.snack_bar = SnackBar(
                Text("Quiz created successfully!", color="white"),
                bgcolor="green"
            )
            page.snack_bar.open = True
            page.update()
            page.go("/professor_dashboard")

        except Exception as ex:
            import traceback
            print("[ERROR] Quiz creation failed:")
            traceback.print_exc()

            page.snack_bar = SnackBar(
                Text("An error occurred while submitting.", color="white"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()

    questions_column = Column([
        Text("Questions & Answers", size=20, weight="bold"),
        *[Row([q, a]) for q, a in zip(question_fields, answer_fields)]
    ])

    return Column(
        controls=[
            Column([
                Text("Create New Quiz", size=24, weight="bold"),
                title_field,
                questions_column,
                Row([Text("Due Date:"), due_date_button]),
                ElevatedButton("Submit", on_click=handle_submit, bgcolor="green", color="white"),
            ],
                spacing=20,
                alignment=MainAxisAlignment.START,
                horizontal_alignment=CrossAxisAlignment.CENTER),
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )

def student_dashboard_view(page: Page):
    from datetime import datetime

    def navigate_to(route):
        page.go(route)

    student_id = page.session.get("user_id")
    print("Current logged in student ID:", student_id)
    if not student_id:
        page.go("/")
        return

    navbar = Row(
        controls=[
            TextButton("Dashboard", on_click=lambda e: navigate_to("/student_dashboard"), style=ButtonStyle(bgcolor='green', color='white')),
            TextButton("Log-out", on_click=lambda e: navigate_to("/"), style=ButtonStyle(color='white'))
        ]
    )

    classes = get_student_classes(student_id) or []
    activities = get_student_pending_activities(student_id) or []
    finished_activities = get_finished_activities(student_id) or []
    finished_activity_list = [
        ListTile(
            title=Text(f"✅ {act['title']}"),
            subtitle=Text(f"Submitted | Due: {act['due_date'].strftime('%Y-%m-%d') if isinstance(act['due_date'], datetime) else act['due_date']}")
        ) for act in finished_activities
    ]


    # 👉 Fetch quizzes
    pending_quizzes = get_pending_quizzes(student_id) or []
    finished_quizzes = get_finished_quizzes(student_id) or []

    def open_join_class_dialog(e):
        class_code_field = TextField(label="Enter Class Code")

        def submit_join(ev):
            class_code = class_code_field.value.strip()
            if not class_code:
                page.snack_bar = SnackBar(Text("Class code cannot be empty."))
                page.snack_bar.open = True
                page.update()
                return

            success = join_class(student_id, class_code)
            if success:
                close_dialog()
                page.snack_bar = SnackBar(Text("Successfully joined class!"))
                page.snack_bar.open = True
                page.views.clear()
                page.views.append(student_dashboard_view(page))
                page.update()
            else:
                page.snack_bar = SnackBar(Text("Failed to join class. Check class code."))
                page.snack_bar.open = True
                page.update()

        dialog = AlertDialog(
            title=Text("Join Class"),
            content=Column([class_code_field]),
            actions=[
                TextButton("Cancel", on_click=lambda e: close_dialog()),
                TextButton("Join", on_click=submit_join)
            ]
        )
        page.dialog = dialog
        page.overlay.append(dialog)
        page.dialog.open = True
        page.update()

    def close_dialog():
        page.dialog.open = False
        page.update()

    class_cards = [
        Container(
            content=Column(
                controls=[
                    Text(f"📚 {cls['subject_name']}", size=18, weight="bold"),
                    Text(f"Class Name: {cls['class_name']}"),
                    Text(f"Instructor: {cls['first_name']} {cls['last_name']}"),
                    Row(
                        controls=[
                            TextButton("Activities", on_click=lambda e, cid=cls['id']: page.go(f"/student_activities?class_id={cid}")),
                            TextButton("Quizzes", on_click=lambda e, cid=cls['id']: page.go(f"/student_quizzes?class_id={cid}")),
                        ],
                        spacing=5
                    )
                ]
            ),
            bgcolor="white",
            padding=15,
            border_radius=10,
            shadow=BoxShadow(blur_radius=6, color="grey"),
            margin=5
        ) for cls in classes
    ]

    activity_list = [
        ListTile(
            title=Text(f"📝 {act['title']}"),
            subtitle=Text(f"Due: {act['due_date'].strftime('%Y-%m-%d') if isinstance(act['due_date'], datetime) else act['due_date']}")
        ) for act in activities
    ]

    pending_quiz_cards = [
        ListTile(
            title=Text(f"🧠 {quiz['title']}"),
            subtitle=Text(f"Deadline: {quiz['due_date']}"),
            trailing=TextButton("Take", on_click=lambda e, qid=quiz['id']: page.go(f"/take_quiz?quiz_id={qid}"))
        ) for quiz in pending_quizzes
    ]

    finished_quiz_cards = [
        ListTile(
            title=Text(f"✅ {quiz['title']}"),
            subtitle=Text("Submitted")
        ) for quiz in finished_quizzes
    ]

    return Column(
        controls=[
            Container(Text("Dashboard", size=30, weight='bold', color='green'), alignment=alignment.top_center, padding=10),
            Container(content=navbar, bgcolor='lightgreen', padding=10),
            Divider(),
            Text("Your Classes", size=20, weight="bold"),
            Row(controls=class_cards, wrap=True),
            Divider(),
            Text("Pending Activities", size=20, weight="bold"),
            Column(controls=activity_list),
            Divider(),
            Text("Finished Activities", size=20, weight="bold"),
            Column(controls=finished_activity_list),
            Container(
                content=FloatingActionButton(
                    text="Join Class",
                    bgcolor="green",
                    on_click=open_join_class_dialog
                ),
                alignment=alignment.bottom_right,
                margin=10
            )
        ],
        scroll="auto",
        horizontal_alignment=CrossAxisAlignment.CENTER,
        alignment=MainAxisAlignment.START,
        expand=True
    )

def student_activities_view(page: Page):
    import urllib.parse
    
    query = urllib.parse.urlparse(page.route).query
    params = urllib.parse.parse_qs(query)
    class_id = params.get("class_id", [None])[0]

    if not class_id:
        return Column([Text("No class ID provided.")])

    print("Student viewing activities for class_id:", class_id)

    activities = get_activities_by_class_id(class_id)  # 👈 You must define this in db.py

    activity_cards = [
        Container(
            content=Column([
                Text(f"📝 {activity['title']}", size=18, weight="bold"),
                Text(f"Due: {activity['due_date']}"),
                TextButton("Submit", on_click=lambda e, aid=activity['id']: page.go(f"/submit_activity?activity_id={aid}"))
            ]),
            padding=10,
            bgcolor="white",
            margin=5,
            border_radius=10
        ) for activity in activities
    ]
    
    back_button = TextButton(
        "Back",
        on_click=lambda _: page.go("/student_dashboard"),
        style = ButtonStyle( color = 'green')
    )

    return Column(
        controls=[
            Container(
                content=back_button,
                alignment=alignment.top_left
            ),
            Container(
                content=Text("Activities", size=30, weight="bold", color="green"),
                alignment=alignment.top_center,
                padding=10
            ),
            Column(
                controls=activity_cards
            )
        ],
        scroll="auto"
    )

def student_quizzes_view(page: Page):
    import urllib.parse

    query = urllib.parse.urlparse(page.route).query
    params = urllib.parse.parse_qs(query)
    class_id = params.get("class_id", [None])[0]

    if not class_id:
        return Column([Text("No class ID provided.")])

    print("Student viewing quizzes for class_id:", class_id)

    quizzes = get_quizzes_by_class_id(class_id)  # 🔧 You’ll add this in db.py

    quiz_cards = [
        Container(
            content=Column([
                Text(f"🧠 {quiz['title']}", size=18, weight="bold"),
                Text(f"Deadline: {quiz['due_date']}"),
                TextButton("Take Quiz", on_click=lambda e, qid=quiz['id']: page.go(f"/take_quiz?quiz_id={qid}"))
            ]),
            padding=10,
            bgcolor="white",
            margin=5,
            border_radius=10
        ) for quiz in quizzes
    ]

    back_button = TextButton(
        "Back",
        on_click=lambda _: page.go("/student_dashboard"),
        style = ButtonStyle( color = 'green')
    )

    return Column(
        controls=[
            Container(
                content=back_button,
                alignment=alignment.top_left
            ),
            Container(
                content=Text("Quizzes", size=30, weight="bold", color="green"),
                alignment=alignment.top_center,
                padding=10
            ),
            Column(
                controls=quiz_cards
            )
        ],
        scroll="auto"
    )

def submit_activity_view(page: Page):
    def on_file_selected(e):
        if not e.files:
            return

        file_path = e.files[0].path

        # Extract student_id and activity_id from URL parameters
        import urllib.parse
        query = urllib.parse.urlparse(page.route).query
        params = urllib.parse.parse_qs(query)

        student_id = params.get("student_id", [""])[0]
        activity_id = params.get("activity_id", [""])[0]

        if not student_id or not activity_id:
            page.snack_bar = SnackBar(Text("❌ Missing student or activity ID."))
            page.snack_bar.open = True
            page.update()
            return

        cloud_path = f"submissions/student_{student_id}/activity_{activity_id}.pdf"
        url = upload_student_file(file_path, cloud_path)

        if url:
            page.snack_bar = SnackBar(Text("✅ Upload successful!"))
        else:
            page.snack_bar = SnackBar(Text("❌ Upload failed."))

        page.snack_bar.open = True
        page.update()

    file_picker = FilePicker(on_result=on_file_selected)
    page.overlay.append(file_picker)

    back_button = TextButton(
        "Back",
        on_click=lambda _: page.go("/student_dashboard"),
        style = ButtonStyle( color = 'green')
    )

    return Column(
        controls=[
            back_button,
            Container(
                content=Text("📄 Submit Activity", size=24, weight="bold"),
                alignment=alignment.top_center,
                padding=10
            ),
            ElevatedButton(
                "Choose File",
                on_click=lambda _: file_picker.pick_files(allowed_extensions=["pdf", "docx"])
            ),
        ]
    )

def take_quiz_view(page: Page):
    import urllib.parse

    # Parse quiz_id from URL
    query = urllib.parse.urlparse(page.route).query
    params = urllib.parse.parse_qs(query)
    quiz_id = params.get("quiz_id", [None])[0]

    if not quiz_id:
        return Column([Text("❌ No quiz ID provided.")])

    print("Taking quiz with quiz_id:", quiz_id)

    questions = get_quiz_questions(quiz_id)
    if not questions:
        return Column([Text("❌ No questions found for this quiz.")])

    responses = {}
    question_controls = []

    for i, question in enumerate(questions):
        answer_field = TextField(label="Your answer", multiline=True)
        responses[question["id"]] = answer_field

        question_controls.append(
            Container(
                content=Column([
                    Text(f"Q{i+1}: {question['question_text']}", size=16, weight="bold"),
                    answer_field
                ]),
                bgcolor="white",
                padding=10,
                margin=5,
                border_radius=8
            )
        )

    def submit_answers(e):
        student_id = page.session.get("user_id")
        if not student_id:
            page.snack_bar = SnackBar(Text("❌ Student not logged in."))
            page.snack_bar.open = True
            page.update()
            return

        for qid, field in responses.items():
            answer_text = field.value.strip()
            save_student_answer(student_id, quiz_id, qid, answer_text)

        page.snack_bar = SnackBar(Text("✅ Quiz submitted!"))
        page.snack_bar.open = True
        page.go("/student_dashboard")

    back_button = TextButton(
        "Back",
        on_click=lambda _: page.go("/student_dashboard"),
        style=ButtonStyle(color="green")
    )

    return Container(
        content=Column(
            controls=[
                Container(back_button, alignment=alignment.top_left),
                Container(
                    content=Text("🧠 Take Quiz", size=28, weight="bold", color="green"),
                    alignment=alignment.top_center,
                    padding=10
                ),
                Column(controls=question_controls),
                ElevatedButton("Submit Quiz", on_click=submit_answers, bgcolor="green", color="white")
            ],
            scroll="auto",
            expand=True
        ),
        expand=True,
        padding=10
    )

def professor_invalid_credentials(page: Page):
    
    back_button = TextButton(
        "Back",
        on_click=lambda _: page.go("/professor_login"),
        style=ButtonStyle(color = 'green')
    )

    return Column(
        controls=[
            Container(
                content=back_button
            ),
            Text("Invalid Credentials", size = 50, color = 'red', weight='bold')
        ]
    )

def student_invalid_credentials(page: Page):
    
    back_button = TextButton(
        "Back",
        on_click=lambda _: page.go("/student_login"),
        style=ButtonStyle(color = 'green')
    )

    return Column(
        controls=[
            Container(
                content=back_button
            ),
            Text("Invalid Credentials", size = 50, color = 'red', weight='bold')
        ]
    )

class_view_dialog = AlertDialog(
    modal=True,
    title=Text("Class Details"),
    content=Column(
        controls=[],
        tight=True,
    ),
    actions=[
        TextButton("Close", on_click=lambda e: close_dialog(e))
    ]
)

def close_dialog(e):
    e.page.dialog.open = False
    e.page.update()


def main(page: Page):
    page.title = "LearnOnGo - Welcome"
    page.theme_mode = ThemeMode.LIGHT

    def route_change(route):
        print("Current route: ", page.route)
        page.views.clear()

        if page.route == "/":
            route = urlparse(page.route)
            query_params = parse_qs(route.query)
            page.views.append(
                View(
                    "/",
                    [   
                    Container(
                        content = Column(
                            controls = [        
                                Text("Welcome to LearnOnGo", size = 50, weight = 'bold', color = 'green'),
                                Text("Learn Anytime, Anywhere.", size = 15, weight = 'bold', color = 'green'),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER
                        ),
                        alignment=alignment.top_center,
                        expand = True
                    ),
                    Container(
                        content = Column(
                            controls = [
                                Text("Log in as", size = 20, weight = 'bold', color = 'green'),
                                ElevatedButton(
                                    "Professor",
                                    color = 'white',
                                    bgcolor = 'green',
                                    height = '70',
                                    width = '500',
                                    on_click = lambda _: page.go("/professor_login"),
                                    style=ButtonStyle(
                                        text_style=TextStyle(size = 30),
                                        shape = RoundedRectangleBorder(radius=15)
                                        ),
                                    elevation=10
                                ),
                                Text("or", size = 20, color = 'green', weight = 'bold'),
                                ElevatedButton(
                                    "Student",
                                    color = 'white',
                                    bgcolor = 'green',
                                    height = 70,
                                    width = 500,
                                    elevation = 10,
                                    on_click = lambda _: page.go("/student_login"),
                                    style = ButtonStyle(
                                        text_style=TextStyle(size = 30),
                                        shape=RoundedRectangleBorder(radius = 15)
                                        ),
                                ),
                            ],

                            horizontal_alignment = CrossAxisAlignment.CENTER
                        ),
                        alignment=alignment.top_center,
                        expand=True
                    ),
                    Container(
                        content=Column(
                            controls=[
                                Text("Don't have an account yet?",size = 20, color = 'green', weight = 'bold'),
                                TextButton(
                                    "Sign up as a Professor",
                                    on_click = lambda _: page.go("/professor_sign_up"),
                                    style = ButtonStyle(color = 'green')
                                ),
                                TextButton(
                                    "Sign up as a Student",
                                    on_click = lambda _: page.go("/student_sign_up"),
                                    style = ButtonStyle(color = 'green')
                                ),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            spacing = 0
                        ),
                        alignment=alignment.center,
                    )
                ],
                padding = padding.all(20),
            ),
        )

        if page.route == "/professor_login":
            page.views.append(
                View(
                    "/professor_login",
                    [professor_login_view(page)],
                    padding = padding.all(20),
                )
            )
        elif page.route == "/student_login":
            page.views.append(
                View(
                    "/student_login",
                    [student_login_view(page)],
                    padding = padding.all(20),
                )
            )
        elif page.route == "/professor_sign_up":
            page.views.append(
                View(
                    "/professor_sign_up",
                    [professor_sign_up_view(page)],
                    padding = padding.all(20),
                )
            )
        elif page.route == "/student_sign_up":
            page.views.append(
                View(
                    "/student_sign_up",
                    [student_sign_up_view(page)],
                    padding = padding.all(20),
                )
            )
        elif page.route == "/professor_dashboard":
            page.views.append(
                View(
                    "/professor_dashboard",
                    [professor_dashboard_view(page)],
                    padding = padding.all(20),
                )
            )
        elif page.route == "/student_dashboard":
            page.views.append(
                View(
                    "/student_dashboard",
                    [student_dashboard_view(page)],
                    padding = padding.all(20),
                )
            )
        elif page.route == "/professor_invalid_credentials":
            page.views.append(
                View(
                    "/professor_invalid_credentials",
                    [professor_invalid_credentials(page)],
                    padding=padding.all(20),
                )
            )
        elif page.route == "/student_invalid_credentials":
            page.views.append(
                View(
                    "/student_invalid_credentials",
                    [student_invalid_credentials(page)],
                    padding=padding.all(20),
                )
            )
        elif page.route.startswith("/create_activity"):
            parsed_url = urlparse(page.route)
            query_params = parse_qs(parsed_url.query)
            class_id = query_params.get("class_id", [None])[0]

            if not class_id:
                page.go("/professor_dashboard")
                return

            page.views.append(
                View(
                    route=page.route,
                    controls=[create_activity_view(page)],
                    padding=padding.all(20),
                )
            )
        elif page.route.startswith("/create_quiz"):
            parsed_url = urlparse(page.route)
            query_params = parse_qs(parsed_url.query)
            class_id = query_params.get("class_id", [None])[0]

            if not class_id:
                page.go("/professor_dashboard")
                return

            page.views.append(
                View(
                    route=page.route,
                    controls=[create_quiz_view(page)],
                    padding=padding.all(20),
                )
            )
        elif page.route.startswith("/student_activities"):
            page.views.append(
                View(
                    "/student_activities",
                    controls=[student_activities_view(page)],
                    padding=padding.all(20)
                )
            )
        elif page.route.startswith("/student_quizzes"):
            page.views.append(
                View(
                    "/student_quizzes",
                    controls=[student_quizzes_view(page)],
                    padding=padding.all(20)
                )
            )
        elif page.route.startswith("/submit_activity"):
            page.views.append(
                View(
                    "/submit_activity",
                    controls=[submit_activity_view(page)],
                    padding=padding.all(20)
                )
            )
        elif page.route.startswith("/take_quiz"):
            page.views.append(
                View(
                    "/take_quiz",
                    controls=[take_quiz_view(page)],
                    padding=padding.all(20)
                )
            )
        page.update()
    page.on_route_change = route_change
    page.go(page.route)

app(target = main, view = WEB_BROWSER)