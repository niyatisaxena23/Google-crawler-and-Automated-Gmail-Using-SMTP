def get_outreach_template(recipient_name, company, sender_name):
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: auto;">

      <div style="background: #0a0a2e; padding: 20px; border-radius: 8px 8px 0 0;">
        <h1 style="color: #fff; margin: 0;">Hackveda</h1>
        <p style="color: #aaa; margin: 4px 0 0;">Digital Growth Solutions</p>
      </div>

      <div style="padding: 30px; border: 1px solid #e0e0e0; border-top: none;">
        <p>Hi <strong>{recipient_name}</strong>,</p>
        <p>
          I came across <strong>{company}</strong> and was impressed by what you're building.
          We help businesses grow their online presence through data-driven digital marketing.
        </p>
        <p><strong>What Hackveda offers:</strong></p>
        <ul>
          <li>🔍 SEO & Content Strategy</li>
          <li>📊 Performance Marketing (Google/Meta Ads)</li>
          <li>📱 Social Media Management</li>
          <li>📧 Email Marketing Automation</li>
        </ul>
        <p>We'd love to offer you a <strong>free 30-minute growth audit</strong>.</p>
        <p>
          Best regards,<br>
          <strong>{sender_name}</strong><br>
          Hackveda | Digital Marketing & Growth
        </p>
      </div>

    </body>
    </html>
    """