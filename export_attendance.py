# ===============================
# 📦 Required Libraries
# ===============================
import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from email.message import EmailMessage
import smtplib
import os
from fpdf import FPDF


# ===============================
# 🏫 Attendance Exporter GUI Class
# ===============================
class AttendanceExporter:
    def __init__(self, root):
        # === Basic Window Setup ===
        self.root = root
        self.root.title("Attendance Exporter")
        self.root.geometry("400x350")
        self.root.configure(bg="#f0f0f0")

        # === Subject Dropdown Menu ===
        tk.Label(root, text="Select Subject:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.subject_var = tk.StringVar(root)
        self.subjects = self.load_subjects()

        # Default subject selection
        if self.subjects:
            self.subject_var.set(self.subjects[0])
        else:
            self.subject_var.set("No subjects available")
            self.subjects = ["No subjects available"]

        self.subject_dropdown = ttk.Combobox(
            root, textvariable=self.subject_var, values=self.subjects, state="readonly", font=("Arial", 10)
        )
        self.subject_dropdown.pack(pady=5)
        self.subject_dropdown.bind("<<ComboboxSelected>>", self.update_dates)

        # === Date Dropdown Menu ===
        tk.Label(root, text="Select Date:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.date_var = tk.StringVar(root)
        self.date_dropdown = ttk.Combobox(
            root, textvariable=self.date_var, values=[], state="readonly", font=("Arial", 10)
        )
        self.date_dropdown.pack(pady=5)

        # === Professor Email Label ===
        self.prof_email_label = tk.Label(root, text="", font=("Arial", 10), bg="#f0f0f0", fg="blue")
        self.prof_email_label.pack(pady=5)

        # === Export Format Dropdown ===
        tk.Label(root, text="Select Export Format:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.format_var = tk.StringVar(root)
        self.format_dropdown = ttk.Combobox(
            root, textvariable=self.format_var, values=["Excel", "PDF", "Email"], state="readonly", font=("Arial", 10)
        )
        self.format_dropdown.pack(pady=5)

        # === Export/Send Button ===
        ttk.Button(root, text="Export / Send", command=self.handle_export).pack(pady=20)

    # ===============================
    # 📚 Load Subjects from Database
    # ===============================
    def load_subjects(self):
        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM subjects")
        subjects = [row[0] for row in cursor.fetchall()]
        conn.close()
        return subjects

    # ============================================
    # 🔄 Update Dates and Professor Email on Select
    # ============================================
    def update_dates(self, event=None):
        selected_subject = self.subject_var.get()
        if selected_subject == "No subjects available":
            self.date_dropdown["values"] = []
            self.date_var.set("")
            self.prof_email_label.config(text="")
            return

        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()

        # Get available dates
        cursor.execute("SELECT DISTINCT date FROM attendance WHERE subject = ?", (selected_subject,))
        dates = [row[0] for row in cursor.fetchall()]

        # Get professor email
        cursor.execute("SELECT email FROM subjects WHERE name = ?", (selected_subject,))
        result = cursor.fetchone()
        email_text = f"Professor Email: {result[0]}" if result else "Professor Email: Not found"
        self.prof_email_label.config(text=email_text)

        conn.close()

        # Update date dropdown
        if dates:
            dates.sort()
            self.date_dropdown["values"] = dates
            self.date_var.set(dates[0])
        else:
            self.date_dropdown["values"] = ["No dates available"]
            self.date_var.set("No dates available")

    # ===============================
    # 📥 Fetch Attendance Data
    # ===============================
    def fetch_attendance_data(self, date, subject):
        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, time FROM attendance WHERE date = ? AND subject = ?", (date, subject))
        data = cursor.fetchall()
        conn.close()
        return data

    # =====================================
    # 🚀 Handle Export Based on Format Chosen
    # =====================================
    def handle_export(self):
        subject = self.subject_var.get()
        date = self.date_var.get()
        export_format = self.format_var.get()

        if subject == "No subjects available" or date == "No dates available":
            messagebox.showwarning("Warning", "Please select a valid subject and date.")
            return

        data = self.fetch_attendance_data(date, subject)
        if not data:
            messagebox.showwarning("No Data", f"No attendance data found for {subject} on {date}.")
            return

        df = pd.DataFrame(data, columns=["Name", "Time"])

        # Export according to selected format
        if export_format == "Excel":
            self.export_to_excel(df, subject, date)
        elif export_format == "PDF":
            self.export_to_pdf(df, subject, date)
        elif export_format == "Email":
            self.send_email_with_excel(df, subject, date)

    # ===============================
    # 📤 Export to Excel
    # ===============================
    def export_to_excel(self, df, subject, date):
        default_filename = f"Attendance_{subject}_{date}.xlsx"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", initialfile=default_filename, filetypes=[("Excel files", "*.xlsx")]
        )
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", f"Excel file saved:\n{file_path}")

    # ===============================
    # 📝 Export to PDF
    # ===============================
    def export_to_pdf(self, df, subject, date):
        default_filename = f"Attendance_{subject}_{date}.pdf"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", initialfile=default_filename, filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, f"Attendance - {subject} - {date}", ln=True, align='C')
            pdf.set_font("Arial", "", 12)
            pdf.ln(10)

            # Add each row
            for name, time in df.values:
                pdf.cell(0, 10, f"{name} - {time}", ln=True)

            pdf.output(file_path)
            messagebox.showinfo("Success", f"PDF saved:\n{file_path}")

    # ===============================
    # ✉️ Send Attendance via Email
    # ===============================
    def send_email_with_excel(self, df, subject, date):
        try:
            filename = f"Attendance_{subject}_{date}.xlsx"
            df.to_excel(filename, index=False)

            # Get recipient (professor) email
            conn = sqlite3.connect("attendance.db")
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM subjects WHERE name = ?", (subject,))
            result = cursor.fetchone()
            conn.close()

            if not result:
                messagebox.showerror("Missing Email", f"No professor email found for subject '{subject}'.")
                return

            recipient_email = result[0]

            # Email credentials
            sender_email = "ahmedproject319@gmail.com"
            app_password = "yyyh khnh aqki kvws"  # Gmail App Password

            # Compose and send email
            msg = EmailMessage()
            msg["Subject"] = f"Attendance - {subject} ({date})"
            msg["From"] = sender_email
            msg["To"] = recipient_email
            msg.set_content("Attached is the attendance record.")

            with open(filename, "rb") as f:
                msg.add_attachment(
                    f.read(), maintype="application",
                    subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    filename=filename
                )

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender_email, app_password)
                smtp.send_message(msg)

            os.remove(filename)
            messagebox.showinfo("Success", "📧 Excel email sent successfully.")
        except Exception as e:
            messagebox.showerror("Email Failed", f"Error: {e}")


# ===============================
# 🚪 Start the Application
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceExporter(root)
    root.mainloop()
