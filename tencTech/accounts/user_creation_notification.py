from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.template import engines

HTML_CONTENT = """
<!DOCTYPE html>
<html>
  <body style="font-family: Arial, sans-serif; background-color:#f4f6f8; margin:0; padding:20px;">
    <table align="center" width="600" style="background:#ffffff; border-radius:10px; padding:20px; box-shadow:0px 4px 12px rgba(0,0,0,0.1);">
      <tr>
        <td style="text-align:center; padding-bottom:20px;">
          <h2 style="color:#2c3e50;">👋 Welcome to <span style="color:#3498db;">Bhadri Social</span></h2>
        </td>
      </tr>
      <tr>
        <td style="font-size:16px; color:#2c3e50;">
          <p>Hi <b>{{ username }}</b>,</p>
          <p>Your account with username: <b style="color:#3498db;">{{ username }}</b> has been successfully created for 
            <a href="https://bhadrisocial.pythonanywhere.com/" style="color:#e74c3c; text-decoration:none;">Bhadri Social</a>.
          </p>
          <p>Please create your password using the link below:</p>
          <p style="text-align:center; margin:30px 0;">
            <a href="https://bhadrisocial.pythonanywhere.com/accounts/password_reset/" 
               style="background:#3498db; color:#ffffff; padding:12px 25px; border-radius:5px; text-decoration:none; font-weight:bold;">
               🔑 Create Password
            </a>
          </p>
          <p>Once done, you can log in and start exploring posts right away 🚀.</p>
        </td>
      </tr>
      <tr>
        <td style="text-align:center; font-size:14px; color:#7f8c8d; padding-top:20px;">
          <p>Thank you,<br><b>Bhadri Social Team</b></p>
        </td>
      </tr>
    </table>
  </body>
</html>
"""

def render_inline_template(template_string, context):
    django_engine = engines['django']
    template = django_engine.from_string(template_string)
    return template.render(context)

def send_account_created_email(username, recipient_email):
    subject = "🎉 Welcome to Bhadri Social!"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [recipient_email]

    html_content = render_inline_template(HTML_CONTENT, {"username": username})

    msg = EmailMessage(subject, html_content, from_email, to)
    msg.content_subtype = "html"
    msg.send()