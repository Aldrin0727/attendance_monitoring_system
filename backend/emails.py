# email_utils.py
from flask_mail import Message  # type: ignore
# from flask import current_app  # type: ignore
# from email.message import EmailMessage
# import smtplib, ssl, traceback

def send_leave_for_approval_email(
    mail,
    dept_head_emails,
    employee_name,
    ref_no,
    dept,
    leave_number,
    leave_from,
    leave_to,
    reason,
    leave_type,
):
    header_bg_map = {
        "SL": "#edc55b",
        "VL": "#fb6f92",
        "EL": "rgba(225,131,220,0.50)",
    }

    header_bg = header_bg_map.get(leave_type, "#ffffff")
    header_text = "#111827"

    msg = Message(
        subject=f"Leave Request For Approval [{ref_no}]",
        recipients=dept_head_emails,
        html=f"""
        <div style="margin:0;padding:0;background:#f6f7fb;">
          <div style="max-width:640px;margin:0 auto;padding:24px 14px;font-family:Arial,Helvetica,sans-serif;color:#1f2937;">

            <!-- Header -->
            <div style="background:{header_bg};border:1px solid #e5e7eb;border-radius:12px;padding:18px;">
              <div style="font-size:16px;font-weight:700;letter-spacing:.2px;color:{header_text};">
                Leave Request For Approval
              </div>
              <div style="margin-top:6px;font-size:13px;color:{header_text};opacity:.9;">
                Reference Number: <b style="color:{header_text};">{ref_no}</b>
                <span style="display:inline-block;margin-left:10px;padding:2px 10px;border-radius:999px;background:rgba(255,255,255,.6);border:1px solid rgba(17,24,39,.12);font-size:12px;font-weight:700;color:{header_text};text-transform:uppercase;">
                  {leave_type}
                </span>
              </div>
            </div>

            <!-- Body -->
            <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;padding:18px;margin-top:12px;">
              <p style="margin:0 0 10px;line-height:1.55;">Good day,</p>

              <p style="margin:0 0 12px;line-height:1.55;">
                A leave request has been submitted and requires your approval.
              </p>

              <!-- Details Card -->
              <div style="border:1px solid #e5e7eb;border-radius:10px;background:#fafafa;padding:12px;">
                <table style="width:100%;border-collapse:collapse;font-size:13px;">
                  <tr>
                    <td style="padding:6px 0;color:#6b7280;width:40%;">Employee Name</td>
                    <td style="padding:6px 0;color:#111827;font-weight:600;">{employee_name}</td>
                  </tr>
                  <tr>
                    <td style="padding:6px 0;color:#6b7280;">Department</td>
                    <td style="padding:6px 0;color:#111827;font-weight:600;">{dept}</td>
                  </tr>
                  <tr>
                    <td style="padding:6px 0;color:#6b7280;">No. of Day(s)</td>
                    <td style="padding:6px 0;color:#111827;font-weight:600;">{leave_number}</td>
                  </tr>
                  <tr>
                    <td style="padding:6px 0;color:#6b7280;">Leave Dates</td>
                    <td style="padding:6px 0;color:#111827;font-weight:600;">{leave_from} to {leave_to}</td>
                  </tr>
                  <tr>
                    <td style="padding:6px 0;color:#6b7280;">Reason</td>
                    <td style="padding:6px 0;color:#111827;font-weight:600;">{reason}</td>
                  </tr>
                  <tr>
                    <td style="padding:6px 0;color:#6b7280;">Status</td>
                    <td style="padding:6px 0;color:#111827;font-weight:700;">FOR DEPARTMENT HEAD APPROVAL</td>
                  </tr>
                </table>
              </div>

              <p style="margin:12px 0 0;line-height:1.55;">
                Please log in to AMS to review and approve/deny this request.
              </p>

              <p style="margin:14px 0 0;line-height:1.55;">Thank you.</p>

              <p style="margin:14px 0 0;line-height:1.55;">
                Best Regards,<br>
                <b>AMS Admin</b>
              </p>
            </div>

            <!-- Footer -->
            <div style="margin-top:4px;padding:12px 14px;color:#6b7280;font-size:12px;line-height:1.45;">
              <div style="border-top:1px solid #e5e7eb;padding-top:12px;">
                <i>
                  This is an auto-generated email. Please do not reply.
                </i>
              </div>
            </div>

          </div>
        </div>
        """
    )

    mail.send(msg)


def send_vl_leave_request_email(
    mail, user, ref_no, position, dept, leave_number,
    leave_from, leave_to, reason, email, leave_type,depthead_emails,
    pdf_file=None
):
    header_bg_map = {
        "SL": "#edc55b",
        "VL": "#fb6f92",
        # "80e183dc" -> alpha=0x80 (128/255≈0.50), color=e183dc -> rgb(225,131,220)
        "EL": "rgba(225,131,220,0.50)",
    }

    header_bg = header_bg_map.get(leave_type, "#ffffff")  # fallback if unknown
    header_text = "#111827"  # readable for all above colors

    #RECEPIENT
    cc_emails = [
        "bernard.belleza@jewelmer.com" # as hr
    ]

    if email:
        cc_emails.append(email)

    msg = Message(
        subject=f"Approved Leave Request [{ref_no}]",
        recipients=depthead_emails,
        cc=cc_emails,
        html=f"""
                <div style="margin:0;padding:0;background:#f6f7fb;">
                <div style="max-width:640px;margin:0 auto;padding:24px 14px;font-family:Arial,Helvetica,sans-serif;color:#1f2937;">

                    <!-- Header -->
                     <div style="background:{header_bg};border:1px solid #e5e7eb;border-radius:12px;padding:18px;">
                  <div style="font-size:16px;font-weight:700;letter-spacing:.2px;color:{header_text};">
                    Approved Leave Request
                  </div>
                  <div style="margin-top:6px;font-size:13px;color:{header_text};opacity:.9;">
                    Reference Number: <b style="color:{header_text};">{ref_no}</b>
                    <span style="display:inline-block;margin-left:10px;padding:2px 10px;border-radius:999px;background:rgba(255,255,255,.6);border:1px solid rgba(17,24,39,.12);font-size:12px;font-weight:700;color:{header_text};text-transform:uppercase;">
                      {leave_type}
                    </span>
                  </div>
                </div>

                    <!-- Body -->
                    <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;padding:18px;margin-top:12px;">
                    <p style="margin:0 0 10px;line-height:1.55;">Good day,</p>

                    <p style="margin:0 0 12px;line-height:1.55;">
                        Please be informed that the leave request below has been
                        <b style="color:#16a34a;">APPROVED</b>.
                    </p>

                    <!-- Details Card -->
                    <div style="border:1px solid #e5e7eb;border-radius:10px;background:#fafafa;padding:12px;">
                        <table style="width:100%;border-collapse:collapse;font-size:13px;">
                        <tr>
                            <td style="padding:6px 0;color:#6b7280;width:40%;">Employee Name</td>
                            <td style="padding:6px 0;color:#111827;font-weight:600;">{user}</td>
                        </tr>
                        <tr>
                            <td style="padding:6px 0;color:#6b7280;">Department</td>
                            <td style="padding:6px 0;color:#111827;font-weight:600;">{dept}</td>
                        </tr>
                        <tr>
                            <td style="padding:6px 0;color:#6b7280;">No. of Day(s)</td>
                            <td style="padding:6px 0;color:#111827;font-weight:600;">{leave_number}</td>
                        </tr>
                        <tr>
                            <td style="padding:6px 0;color:#6b7280;">Leave Dates</td>
                            <td style="padding:6px 0;color:#111827;font-weight:600;">{leave_from} to {leave_to}</td>
                        </tr>
                        </table>
                    </div>

                    <p style="margin:12px 0 0;line-height:1.55;">
                        The full details of the approved leave form is attached for your reference.
                    </p>

                    <p style="margin:14px 0 0;line-height:1.55;">Thank you.</p>

                    <p style="margin:14px 0 0;line-height:1.55;">
                        Best Regards,<br>
                        <b>AMS Admin</b>
                    </p>
                    </div>

                    <!-- Footer -->
                    <div style="margin-top:4px;padding:12px 14px;color:#6b7280;font-size:12px;line-height:1.45;">
                    <div style="border-top:1px solid #e5e7eb;padding-top:12px;">
                        <i>
                        This is an auto-generated email. Please do not reply.
                        The attachment in this email serves as an official document of the employee’s leave records.
                        </i>
                    </div>
                    </div>

                </div>
                </div>
                """

    )

    if pdf_file:
        try:
            pdf_file.stream.seek(0)
        except Exception:
            try:
                pdf_file.seek(0)
            except Exception:
                pass

        pdf_bytes = pdf_file.read()
        filename = getattr(pdf_file, "filename", None) or f"{ref_no}.pdf"

        msg.attach(
            filename=filename,
            content_type="application/pdf",
            data=pdf_bytes
        )

    mail.send(msg)

def send_otob_request_email(
    mail, user, ref_no, dept, actual_hrs,
    actual_from, actual_to, email,type,
    pdf_file=None
):
    header_bg_map = {
        "OT": "#fff",
        "OB": "#38c4e0",
       
    }
    if type == "OB":
        types = "Official Business"
    else:
        types = "Overtime"
    header_bg = header_bg_map.get(type, "#ffffff")  # fallback if unknown
    header_text = "#111827"  # readable for all above colors

    msg = Message(
        subject=f"Approved {types} Request [{ref_no}]",
        # recipients=[email],
        # # cc=["bernard.belleza@jewelmer.com"],
        recipients=["aldrin.canarejo@jewelmer.com"],
        cc=["lani.tirao@jewelmer.com"],
        html=f"""
                <div style="margin:0;padding:0;background:#f6f7fb;">
                <div style="max-width:640px;margin:0 auto;padding:24px 14px;font-family:Arial,Helvetica,sans-serif;color:#1f2937;">

                    <!-- Header -->
                     <div style="background:{header_bg};border:1px solid #e5e7eb;border-radius:12px;padding:18px;">
                  <div style="font-size:16px;font-weight:700;letter-spacing:.2px;color:{header_text};">
                    Approved {types} Request
                  </div>
                  <div style="margin-top:6px;font-size:13px;color:{header_text};opacity:.9;">
                    Reference Number: <b style="color:{header_text};">{ref_no}</b>
                    <span style="display:inline-block;margin-left:10px;padding:2px 10px;border-radius:999px;background:rgba(255,255,255,.6);border:1px solid rgba(17,24,39,.12);font-size:12px;font-weight:700;color:{header_text};text-transform:uppercase;">
                      {type}
                    </span>
                  </div>
                </div>

                    <!-- Body -->
                    <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;padding:18px;margin-top:12px;">
                    <p style="margin:0 0 10px;line-height:1.55;">Good day,</p>

                    <p style="margin:0 0 12px;line-height:1.55;">
                        Please be informed that the {type} request below has been
                        <b style="color:#16a34a;">APPROVED</b>.
                    </p>

                    <!-- Details Card -->
                    <div style="border:1px solid #e5e7eb;border-radius:10px;background:#fafafa;padding:12px;">
                        <table style="width:100%;border-collapse:collapse;font-size:13px;">
                        <tr>
                            <td style="padding:6px 0;color:#6b7280;width:40%;">Employee Name</td>
                            <td style="padding:6px 0;color:#111827;font-weight:600;">{user}</td>
                        </tr>
                        <tr>
                            <td style="padding:6px 0;color:#6b7280;">Department</td>
                            <td style="padding:6px 0;color:#111827;font-weight:600;">{dept}</td>
                        </tr>
                        <tr>
                            <td style="padding:6px 0;color:#6b7280;">Actual Hour(s) Rendered</td>
                            <td style="padding:6px 0;color:#111827;font-weight:600;">{actual_hrs}</td>
                        </tr>
                        <tr>
                            <td style="padding:6px 0;color:#6b7280;">Actual Date(s)</td>
                            <td style="padding:6px 0;color:#111827;font-weight:600;">{actual_from} to {actual_to}</td>
                        </tr>
                        </table>
                    </div>

                    <p style="margin:12px 0 0;line-height:1.55;">
                        The full details of the approved {types} form is attached for your reference.
                    </p>

                    <p style="margin:14px 0 0;line-height:1.55;">Thank you.</p>

                    <p style="margin:14px 0 0;line-height:1.55;">
                        Best Regards,<br>
                        <b>AMS Admin</b>
                    </p>
                    </div>

                    <!-- Footer -->
                    <div style="margin-top:4px;padding:12px 14px;color:#6b7280;font-size:12px;line-height:1.45;">
                    <div style="border-top:1px solid #e5e7eb;padding-top:12px;">
                        <i>
                        This is an auto-generated email. Please do not reply.
                        The attachment in this email serves as an official document of the employee’s leave records.
                        </i>
                    </div>
                    </div>

                </div>
                </div>
                """

    )

    if pdf_file:
        try:
            pdf_file.stream.seek(0)
        except Exception:
            try:
                pdf_file.seek(0)
            except Exception:
                pass

        pdf_bytes = pdf_file.read()
        filename = getattr(pdf_file, "filename", None) or f"{ref_no}.pdf"

        msg.attach(
            filename=filename,
            content_type="application/pdf",
            data=pdf_bytes
        )

    mail.send(msg)




        