"""
This module contains the PDF generation code used for Sigmax.
"""
import os
import base64


def _generate_pdf(signal):
    """
    Generate PDF to send to VoegZaakdocumentToe_Lk01
    """
    DIR = os.path.split(__file__)[0]
    with open(os.path.join(DIR, 'testbericht.pdf'), 'rb') as f:
        data = f.read()

    return base64.b64encode(data)
