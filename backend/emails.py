# email_utils.py
from flask_mail import Message  # type: ignore
# from flask import current_app  # type: ignore
# from email.message import EmailMessage
# import smtplib, ssl, traceback










def send_vl_leave_request_email(
    mail, user, position, dept, leave_number,
    leave_from, leave_to, reason, email, leave_type,
    pdf_file=None
):
    msg = Message(
        subject=f"Approved Leave Request ({leave_type})",
        recipients=[email],
        cc =["bernard.belleza@jewelmer.com"],
        html=f"""
            <p>Approved leave request.</p>
            <b>Employee:</b> {user}<br>
            <b>Leave Type:</b> {leave_type}<br>
            <b>Days:</b> {leave_number}
        """
    )

    if pdf_file:
        msg.attach(
            filename=pdf_file.filename,
            content_type="application/pdf",
            data=pdf_file.read()
        )

    mail.send(msg)





# def _send_via_flask_mail(mail, subject, html, recipients, sender=None):
#     if isinstance(recipients, str):
#         recipients = [recipients]
#     msg = Message(
#         subject=subject,
#         recipients=list(recipients),
#         sender=sender or current_app.config.get('MAIL_DEFAULT_SENDER')
#     )
#     msg.html = html
#     mail.send(msg)

# def _send_via_gmail_smtp(username, password, sender, subject, html, to, cc=None):
#     to_list = [to] if isinstance(to, str) and to else (list(to) if to else [])
#     cc_list = [cc] if isinstance(cc, str) and cc else (list(cc) if cc else [])

#     if not to_list and not cc_list:
#         print("[EMAIL WARN] No recipients (To/CC); skipping send.")
#         return

#     em = EmailMessage()
#     em['Subject'] = subject
#     em['From'] = sender
#     if to_list:
#         em['To'] = ", ".join(to_list)
#     if cc_list:
#         em['Cc'] = ", ".join(cc_list)
#     em.set_content("This email contains HTML content.")
#     em.add_alternative(html or "", subtype='html')

#     recipients = to_list + cc_list
#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#         smtp.login(username, password)
#         smtp.send_message(em, from_addr=sender, to_addrs=recipients)

# def send_vl_leave_request_email(mail,
#         user,
#         position,
#         dept_code,
#         leave_number,
#         leave_from,
#         leave_to,
#         leave_reason,
#         email,
#         leave_type
#     ):

#     html_body = f"""
#         <div style = "max-width: 1100px; margin: 0 auto; background-color: #fff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding: 30px 40px;">
# 	<div style= " text-align: center; background-color : #fb6f92; padding : 10px; border-radius: 8px; color: #fff; font-family: 'Poppins', sans-serif;">
# 		<h2>Vacation Leave Request Form</h2>
# 	</div>
# 		<div style ="margin: 30px 0; font-size: 18px;">
# 			<div style= "margin:20px">I. Requestor Information</div>
# 				<div style ="margin: 20px 50px;">
# 					<table style = "border-collapse: collapse;width: 100%;text-align: center; border : 1px solid black; padding: 12px;">
# 						<tr>
# 							<td style ="padding: 12px 8px 0px 30px; vertical-align: top; font-size: 20px; text-align: left;  border: 1px solid black; border-collapse: collapse;">Employee Name  </td>
# 							<td style ="padding: 12px 8px 0px 30px; vertical-align: top; text-align: left; font-size: 20px; border: 1px solid black; border-collapse: collapse;">{user}</td>
# 						</tr>

# 						<tr>
# 							<td style ="padding: 12px 8px 0px 30px; vertical-align: top; font-size: 20px; text-align: left;  border: 1px solid black; border-collapse: collapse;">Employee Position  </td>
# 							<td style ="padding: 12px 8px 0px 30px; vertical-align: top; text-align: left; font-size: 20px; border: 1px solid black; border-collapse: collapse;">{position}</td>
# 						</tr>

# 						<tr>
# 							<td style ="padding: 12px 8px 0px 30px; vertical-align: top; font-size: 20px; text-align: left;  border: 1px solid black; border-collapse: collapse;">Department </td>
# 							<td style ="padding: 12px 8px 0px 30px; vertical-align: top; text-align: left; font-size: 20px; border: 1px solid black; border-collapse: collapse;">{dept_code}</td>
# 						</tr>	
# 					</table>
# 				</div>
				
# 				<div style= "margin:20px">II. Leave Information</div>
# 				<div style ="margin: 20px 50px;">
# 					<table style = "border-collapse: collapse;width: 100%;text-align: center; border : 1px solid black; padding: 12px;">
# 						<tr>
# 							<td style ="padding: 12px 8px 0px 30px; vertical-align: top; font-size: 20px; text-align: left;  border: 1px solid black; border-collapse: collapse;">Leave From  </td>
# 							<td style ="padding: 12px 8px 0px 30px; vertical-align: top; text-align: left; font-size: 20px; border: 1px solid black; border-collapse: collapse;">{leave_from}</td>
# 						</tr>

# 						<tr>
# 							<td style ="padding: 12px 8px 0px 30px; vertical-align: top; font-size: 20px; text-align: left;  border: 1px solid black; border-collapse: collapse;">Leave To  </td>
# 							<td style ="padding: 12px 8px 0px 30px; vertical-align: top; text-align: left; font-size: 20px; border: 1px solid black; border-collapse: collapse;">{leave_to}</td>
# 						</tr>

# 						<tr>
# 							<td style ="padding: 12px 8px 0px 30px; vertical-align: top; font-size: 20px; text-align: left;  border: 1px solid black; border-collapse: collapse;">Reason of Leave </td>
# 							<td style ="padding: 12px 8px 0px 30px; vertical-align: top; text-align: left; font-size: 20px; border: 1px solid black; border-collapse: collapse;">{leave_reason}</td>
# 						</tr>	

#                         <tr>
# 							<td style ="padding: 12px 8px 0px 30px; vertical-align: top; font-size: 20px; text-align: left;  border: 1px solid black; border-collapse: collapse;">Days of Leave </td>
# 							<td style ="padding: 12px 8px 0px 30px; vertical-align: top; text-align: left; font-size: 20px; border: 1px solid black; border-collapse: collapse;">{leave_number} (days)</td>
# 						</tr>	
# 					</table>
# 				</div>
			
# 		</div>
# </div>
# """
       
# #     html_body = f"""
# #                   <div style="font-family: 'Poppins', sans-serif; color: #333; background-color: #f4f7f6; padding: 20px; border-radius: 8px;">
# #     <!-- Header Section -->
# #     """
# #     if leave_type == 'VL':
# #         html_body += f""" 
# #         <div style="background-color: #fb6f92; padding: 20px; text-align: center; color: #fff; border-radius: 8px 8px 0 0;">
# #         <h2 style="margin: 0; font-size: 26px; font-weight: 600; letter-spacing: 1px;">Vacation Leave Request Form</h2>"""
# #     else:
# #         html_body += f""" 
# #         <div style="background-color: #edc55b; padding: 20px; text-align: center; color: #fff; border-radius: 8px 8px 0 0;">
# #         <h2 style="margin: 0; font-size: 26px; font-weight: 600; letter-spacing: 1px;">Sick Leave Request Form</h2>"""
# #     html_body += f"""
# #     </div>

# #     <!-- Ticket Details Section -->
# #     <div style="padding: 25px; background-color: #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-radius: 0 0 8px 8px;">
# #                <div style="font-size: 16px; margin-bottom: 10px;">
# #             <strong>Hello {user}, </strong>
# #         </div>


# #       <div style="font-size: 18px; margin: 25px 0">
# #             <center>The ticket status for your ticket <strong style="color: #00796b;">{position}</strong> has been updated. Kindly check it in the system for the latest status.</center>
# #         </div>


# #         <!-- Action Button -->
# #       <div style="text-align: center; margin: 25px 0 15px 0;">
# #             <a href="http://192.168.1.31:8080" style="background-color: #38c2ef; color: #fff; padding: 14px 28px; text-decoration: none; font-size: 16px; font-weight: 600;">
# #                ACCESS THE TICKETING SYSTEM
# #             </a>
# #         </div>
# #         <!-- Text indicating action below the button -->
# #         <div style="text-align: center; font-size: 14px; color: #777; margin-top: 10px;">
# #             <p><i>To track the progress of the ticket or add a reply, please click the button above. </i></p>
# #         </div>

# #     </div>

# #     <!-- Footer Section -->
# #     <hr style="margin-top: 30px; border: none; border-top: 1px solid #ddd;">
# #     <div style="text-align: center; font-size: 14px; color: #777;">
# #         <p style="font-size: 12px; color: #999;">This is an automated message. Please do not reply directly to this email.</p>
# #     </div>
# # </div>
# #             """

#     try:
#         msg = Message(
#             subject=f"Ticket Concern - Ticket No",
#             recipients=[email],
#             html=html_body
#         )
#         mail.send(msg)
#         print(f"Email sent successfully for ticket {user}")
#     except Exception as e:
#         print(f"Error sending email: {str(e)}")


        