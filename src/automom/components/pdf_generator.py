import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from automom.utils.logger import logger
from automom.utils.exception import AutoMoMException
import sys

class PDFGenerator:
    def __init__(self, output_dir="data/processed/pdfs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_pdf(self, df):
        """
        Generate PDF summaries for each meeting transcript in the DataFrame.
        Each PDF includes region, meeting ID, date, summary, keywords, and intent.
        """
        try:
            logger.info("🧾 Generating PDF reports...")

            for _, row in df.iterrows():
                meeting_id = str(row.get("meeting_id", "UnknownMeeting"))
                region = str(row.get("region", "UnknownRegion"))
                date = str(row.get("meeting_date", "UnknownDate"))
                summary = str(row.get("summary", "No summary available"))
                keywords = str(row.get("keywords", "N/A"))
                intent = str(row.get("intent", "N/A"))

                pdf_path = os.path.join(self.output_dir, f"{meeting_id}_MoM.pdf")

                # Create PDF
                c = canvas.Canvas(pdf_path, pagesize=A4)
                width, height = A4
                c.setFont("Helvetica-Bold", 14)
                c.drawString(100, height - 80, "📄 AutoMoM - Minutes of Meeting")
                c.setFont("Helvetica", 11)

                # Meeting info
                y = height - 120
                c.drawString(100, y, f"Region: {region}")
                y -= 20
                c.drawString(100, y, f"Meeting ID: {meeting_id}")
                y -= 20
                c.drawString(100, y, f"Date: {date}")
                y -= 30

                # Summary
                c.setFont("Helvetica-Bold", 12)
                c.drawString(100, y, "Summary:")
                c.setFont("Helvetica", 10)
                y -= 20
                for line in summary.split(". "):
                    c.drawString(100, y, line.strip() + ".")
                    y -= 15
                    if y < 100:  # new page if content too long
                        c.showPage()
                        y = height - 100
                        c.setFont("Helvetica", 10)

                # Keywords
                y -= 30
                c.setFont("Helvetica-Bold", 12)
                c.drawString(100, y, "Keywords:")
                c.setFont("Helvetica", 10)
                y -= 20
                c.drawString(100, y, keywords)

                # Intent
                y -= 30
                c.setFont("Helvetica-Bold", 12)
                c.drawString(100, y, "Intent:")
                c.setFont("Helvetica", 10)
                y -= 20
                c.drawString(100, y, intent)

                c.save()
                logger.success(f"📄 PDF generated: {pdf_path}")

            logger.success("🎉 All PDFs created successfully!")

        except Exception as e:
            raise AutoMoMException(e, sys)
