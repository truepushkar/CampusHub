# 🎓 CampusHub — Smart Campus Management Platform

CampusHub is a **web-based platform** designed to simplify and centralize campus life management for **students, clubs, and faculty**.
It helps manage events, notices, attendance, complaints, and collaboration — all from one intuitive dashboard.

---

## 🚀 Features

✅ **Centralized Event & Notice Board**
Easily view and manage all campus events and notices in one place.

✅ **Smart Complaint & Request System** *(coming soon)*
Submit, track, and resolve issues related to hostels, academics, or facilities.

✅ **Attendance / Timetable Tracker** *(coming soon)*
Keep track of attendance and daily class schedules.

✅ **Club & Project Collaboration Space** *(coming soon)*
Facilitate communication and task tracking within student clubs and project groups.

✅ **Feedback & Suggestion System** *(coming soon)*
Allow students to share opinions and suggestions anonymously.

---

## 🏗️ Tech Stack

| Layer                      | Technology                           |
| -------------------------- | ------------------------------------ |
| **Frontend**               | HTML5, CSS3, JavaScript, TailwindCSS |
| **Backend**                | Flask (Python)                       |
| **Database**               | MongoDB                              |
| **Environment Management** | python-dotenv                        |
| **Template Engine**        | Jinja2                               |

---

## 📁 Project Structure

```
campushub/
├─ app.py
├─ requirements.txt
├─ .env.example
├─ static/
│  ├─ js/
│  │  ├─ main.js
│  ├─ css/
│  │  ├─ styles.css
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  ├─ events.html
│  ├─ notices.html
│  ├─ complaints.html
│  ├─ clubs.html
│  ├─ attendance.html
│  ├─ feedback.html
│  ├─ components/_event_card.html
│  └─ components/_notice_card.html
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/campushub.git
cd campushub
```

### 2️⃣ Create & Activate a Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
MONGO_URI=mongodb://localhost:27017/campushub
FLASK_ENV=development
```

(You can refer to `.env.example`)

### 5️⃣ Run the Application

```bash
python app.py
```

The app will start at 👉 **[https://campus-hub-eta-eight.vercel.app/](https://campus-hub-eta-eight.vercel.app/)**

---

## 🧩 MongoDB Collections (Optional Seed)

**Database:** `campushub`
You can manually add sample data into `events` and `notices` collections:

### Example Event Document:

```json
{
  "title": "Tech Fest 2025",
  "description": "Annual inter-college technology festival.",
  "date": "2025-11-10"
}
```

### Example Notice Document:

```json
{
  "title": "Semester Registration Deadline",
  "content": "All students must complete registration by Oct 30, 2025.",
  "date": "2025-10-20"
}
```

---

## 🧠 Future Enhancements

* [ ] Complaint tracking dashboard
* [ ] Club & project collaboration tools
* [ ] Attendance visualization
* [ ] Role-based access (student, faculty, admin)
* [ ] Notification & email integration

---

## 🤝 Contributing

Pull requests are welcome!
If you’d like to contribute:

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -m 'Add awesome feature'`)
4. Push to the branch (`git push origin feature/awesome-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 💡 Author

**CampusHub Team**
🧩 Designed for efficient campus communication and collaboration.
📧 Contact: [help.pushkar@gmail.com]()
