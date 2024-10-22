from flask import Flask, jsonify, Response, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import io
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Database Configuration (with your PostgreSQL credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ramukjar@localhost/ezy_metrics_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Your SMTP server
app.config['MAIL_PORT'] = 587  # For starttls
app.config['MAIL_USERNAME'] = 'rajkumarr7102002@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'cysh fffp dued tfti'  # Your email password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db = SQLAlchemy(app)
mail = Mail(app)

# Lead Model
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    campaign_id = db.Column(db.Integer)

# Campaign Model
class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(50))

# Initialize the database
with app.app_context():
    db.create_all()

# Dummy Data for Testing
LEADS = [
    {"id": 1, "name": "Lead 1", "email": "lead1@example.com", "campaign_id": 101},
    {"id": 2, "name": "Lead 2", "email": "lead2@example.com", "campaign_id": 101},
    {"id": 3, "name": "Lead 3", "email": "lead3@example.com", "campaign_id": 102},
    {"id": 4, "name": "Lead 4", "email": "lead4@example.com", "campaign_id": 103},
    {"id": 5, "name": "Lead 5", "email": "lead5@example.com", "campaign_id": 103},
    {"id": 6, "name": "Lead 6", "email": "lead6@example.com", "campaign_id": 104},
    {"id": 7, "name": "Lead 7", "email": "lead7@example.com", "campaign_id": 104},
    {"id": 8, "name": "Lead 8", "email": "lead8@example.com", "campaign_id": 105},
    {"id": 9, "name": "Lead 9", "email": "lead9@example.com", "campaign_id": 105},
    {"id": 10, "name": "Lead 10", "email": "lead10@example.com", "campaign_id": 106},
]

CAMPAIGNS = [
    {"id": 101, "name": "Campaign 1", "status": "Active"},
    {"id": 102, "name": "Campaign 2", "status": "Active"},
    {"id": 103, "name": "Campaign 3", "status": "Completed"},
    {"id": 104, "name": "Campaign 4", "status": "Active"},
    {"id": 105, "name": "Campaign 5", "status": "Paused"},
    {"id": 106, "name": "Campaign 6", "status": "Completed"},
]

# Endpoint to save leads to the database
@app.route('/save_leads', methods=['POST'])
def save_leads():
    for lead in LEADS:
        new_lead = Lead(id=lead['id'], name=lead['name'], email=lead['email'], campaign_id=lead['campaign_id'])
        db.session.add(new_lead)
    db.session.commit()
    return jsonify({"message": "Leads saved successfully!"})

# Endpoint to save campaigns to the database
@app.route('/save_campaigns', methods=['POST'])
def save_campaigns():
    for campaign in CAMPAIGNS:
        new_campaign = Campaign(id=campaign['id'], name=campaign['name'], status=campaign['status'])
        db.session.add(new_campaign)
    db.session.commit()
    return jsonify({"message": "Campaigns saved successfully!"})

# Main route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to EzyMetrics Backend!"})

@app.route('/extract_data', methods=['GET'])
def extract_data():
    leads = Lead.query.all()
    campaigns = Campaign.query.all()

    lead_data = [{"id": lead.id, "name": lead.name, "email": lead.email, "campaign_id": lead.campaign_id} for lead in leads]
    campaign_data = [{"id": campaign.id, "name": campaign.name, "status": campaign.status} for campaign in campaigns]

    return jsonify({"leads": lead_data, "campaigns": campaign_data})

@app.route('/generate_report/csv', methods=['GET'])
def generate_csv_report():
    # Query the total number of leads and active campaigns from the database
    total_leads = Lead.query.count()
    active_campaigns = Campaign.query.filter_by(status='Active').count()
    total_campaigns = Campaign.query.count()

    # Create a response object for CSV
    response = Response()
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=report.csv'

    # Use StringIO to write CSV data
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header row
    writer.writerow(['Metric', 'Value'])
    
    # Write data rows with dynamic data
    writer.writerow(['Total Leads', total_leads])
    writer.writerow(['Active Campaigns', active_campaigns])
    writer.writerow(['Total Campaigns', total_campaigns])

    # Move to the beginning of the StringIO object
    output.seek(0)

    # Set the CSV data in the response
    response.data = output.getvalue()

    return response

@app.route('/generate_pdf_report', methods=['GET'])
def generate_pdf_report():
    # Create a byte stream to hold the PDF data
    pdf_buffer = io.BytesIO()

    # Create the PDF
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    pdf.setTitle("Campaign and Lead Report")

    # Write title
    pdf.drawString(100, 750, "Campaign and Lead Report")

    # Write metrics
    total_leads = Lead.query.count()
    active_campaigns = Campaign.query.filter_by(status='Active').count()
    total_campaigns = Campaign.query.count()

    pdf.drawString(100, 700, f"Total Leads: {total_leads}")
    pdf.drawString(100, 675, f"Active Campaigns: {active_campaigns}")
    pdf.drawString(100, 650, f"Total Campaigns: {total_campaigns}")

    # Save the PDF to the buffer
    pdf.save()

    # Move the buffer position to the beginning
    pdf_buffer.seek(0)

    # Send email with a message (without the PDF)
    send_email_with_message()

    # Return the PDF as a response for direct download
    return send_file(pdf_buffer, as_attachment=True, download_name="report.pdf", mimetype='application/pdf')


def send_email_with_message():
    msg = Message("Your Report Update", sender="prk7102002@gmail.com", recipients=["rajkumarr7102002@gmail.com"])  # Replace with the recipient's email
    msg.body = "Your PDF report has been generated and is ready for download."

    # Send the email without the PDF attachment
    with app.app_context():
        mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)
