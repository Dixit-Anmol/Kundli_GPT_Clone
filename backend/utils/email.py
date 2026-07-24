import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_subscription_email(user_email: str, user_name: str, tier: str, amount: float, order_id: str, payment_id: str):
    """
    Sends a premium HTML order confirmation email to the user.
    Falls back to rich console logs if SMTP settings are missing from .env.
    """
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = os.environ.get("SMTP_PORT")
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASSWORD")
    smtp_from = os.environ.get("SMTP_FROM", "billing@astrosutra.ai")

    subject = f"🌌 AstroSutra AI — Welcome to the {tier.upper()} Tier!"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Order Confirmation</title>
        <style>
            body {{
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                background-color: #FAF8F5;
                color: #2D2721;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #FFFFFF;
                border-radius: 24px;
                overflow: hidden;
                box-shadow: 0 8px 30px rgba(110, 101, 88, 0.1);
                border: 1px solid #E9DFC8;
            }}
            .header {{
                background: linear-gradient(135deg, #F5E6C8, #FAF8F3);
                padding: 40px 20px;
                text-align: center;
                border-bottom: 1px solid #E9DFC8;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                color: #C89B3C;
                font-weight: 700;
            }}
            .content {{
                padding: 40px 30px;
                line-height: 1.6;
            }}
            .content h2 {{
                margin-top: 0;
                font-size: 20px;
                color: #6E6558;
            }}
            .invoice-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 24px 0;
            }}
            .invoice-table td {{
                padding: 12px 0;
                border-bottom: 1px solid #FAF8F5;
                font-size: 14px;
            }}
            .invoice-table td.label {{
                color: #6E6558;
                font-weight: 600;
            }}
            .invoice-table td.value {{
                text-align: right;
                font-weight: 700;
                color: #2D2721;
            }}
            .total-row td {{
                border-top: 2px solid #E9DFC8;
                font-size: 16px !important;
                padding-top: 18px !important;
            }}
            .footer {{
                background-color: #FAF8F5;
                padding: 24px 30px;
                text-align: center;
                font-size: 12px;
                color: #6E6558;
                border-top: 1px solid #E9DFC8;
            }}
            .btn {{
                display: inline-block;
                background: linear-gradient(135deg, #C89B3C, #A77C2B);
                color: #FFFFFF !important;
                text-decoration: none;
                padding: 14px 28px;
                border-radius: 14px;
                font-weight: 700;
                margin-top: 20px;
                box-shadow: 0 4px 15px rgba(200, 155, 60, 0.25);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌌 ASTROSUTRA AI</h1>
                <p style="margin: 8px 0 0 0; color: #6E6558; font-weight: 500;"> Cosmic Upgrade Successful</p>
            </div>
            <div class="content">
                <h2>Namaste {user_name},</h2>
                <p>Your spiritual journey has ascended. Your subscription to the <strong>AstroSutra AI {tier.capitalize()} Plan</strong> is now active, unlocking premium Vedic chart features, Vimshottari timelines, and RAG-Gita guided AI chats.</p>
                
                <table class="invoice-table">
                    <tr>
                        <td class="label">Tier Upgraded</td>
                        <td class="value">{tier.capitalize()}</td>
                    </tr>
                    <tr>
                        <td class="label">Order ID</td>
                        <td class="value">{order_id}</td>
                    </tr>
                    <tr>
                        <td class="label">Payment ID</td>
                        <td class="value">{payment_id}</td>
                    </tr>
                    <tr class="total-row">
                        <td class="label" style="font-size: 16px; color: #C89B3C;">Amount Charged</td>
                        <td class="value" style="font-size: 16px; color: #C89B3C;">INR {amount:.2f}</td>
                    </tr>
                </table>

                <p>Please refresh your dashboard to access standard/pro features instantly. If you have any questions or require custom rectifications, do not hesitate to contact our team.</p>
                
                <div style="text-align: center;">
                    <a href="https://astrosutraai.onrender.com" class="btn">Go to Dashboard</a>
                </div>
            </div>
            <div class="footer">
                🔒 Secured transaction · Powered by Razorpay · Thank you for trusting AstroSutra AI
            </div>
        </div>
    </body>
    </html>
    """

    if smtp_host and smtp_port and smtp_user and smtp_pass:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = smtp_from
            msg["To"] = user_email
            
            part = MIMEText(html_content, "html")
            msg.attach(part)
            
            # Use SSL/TLS based on port
            port = int(smtp_port)
            if port == 465:
                server = smtplib.SMTP_SSL(smtp_host, port)
            else:
                server = smtplib.SMTP(smtp_host, port)
                server.starttls()
                
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_from, [user_email], msg.as_string())
            server.quit()
            print(f"[Email Service] Transactional receipt email successfully sent to {user_email}.")
        except Exception as smtp_err:
            print(f"[Email Service] SMTP connection failed to send mail: {smtp_err}")
    else:
        print("\n" + "="*80)
        print(f"[EMAIL MOCK - NO SMTP ENVIRONMENT FOUND]")
        print(f"TO: {user_email}")
        print(f"SUBJECT: {subject}")
        print(f"BODY:\n{html_content}")
        print("="*80 + "\n")
