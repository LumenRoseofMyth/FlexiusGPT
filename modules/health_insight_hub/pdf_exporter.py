from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os, json

def export_weekly_pdf(input_folder, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    c.setFont("Helvetica", 12)

    y = 800
    for fname in sorted(os.listdir(input_folder)):
        if fname.endswith(".json"):
            with open(os.path.join(input_folder, fname), 'r') as f:
                data = json.load(f)
            c.drawString(50, y, f"{data['date']} - Steps: {data['steps']}, HR: {data['resting_hr']}, Kcal: {data['calories_burned']}")
            y -= 20
            if y < 100:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = 800

    c.save()
    return output_path
