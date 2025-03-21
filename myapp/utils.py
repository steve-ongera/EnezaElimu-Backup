from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from io import BytesIO
from datetime import datetime
from django.utils.text import slugify

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    """
    # Use the static folder
    static_url = settings.STATIC_URL
    static_root = settings.STATIC_ROOT
    media_url = settings.MEDIA_URL
    media_root = settings.MEDIA_ROOT

    # Make sure that file exists
    if uri.startswith(media_url):
        path = os.path.join(media_root, uri.replace(media_url, ""))
    elif uri.startswith(static_url):
        path = os.path.join(static_root, uri.replace(static_url, ""))
    else:
        return uri

    # Make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (static_url, media_url)
        )
    return path

def render_to_pdf(template_src, context_dict={}):
    """
    Function to generate PDF from HTML template
    """
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, link_callback=link_callback)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def generate_term_report_pdf(student, term_data):
    """
    Generate a PDF report for a specific term
    """
    context = {
        'student': student,
        'term_data': term_data,
        'school_name': settings.SCHOOL_NAME,
        'school_logo': settings.SCHOOL_LOGO_PATH,
        'generated_date': datetime.now().strftime("%d-%m-%Y"),
        'principal_name': settings.PRINCIPAL_NAME,
        'is_term_report': True
    }
    
    pdf = render_to_pdf('marks/pdf_reports/term_report_template.html', context)
    if pdf:
        filename = f"{slugify(student.name)}_{term_data['term'].name}_{term_data['term'].year}_report.pdf"
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    return HttpResponse("Error generating PDF", status=400)

def generate_year_report_pdf(student, year, year_data):
    """
    Generate a PDF report for an entire academic year
    """
    # Calculate yearly averages and summaries
    total_score = 0
    subject_count = 0
    
    # Extract term data for the specified year
    term_data_list = []
    for data in year_data:
        term_data_list.append(data)
        for subject in data['subjects']:
            if subject['average'] != 'N/A' and subject['average'] != 0:
                total_score += subject['average']
                subject_count += 1
    
    # Calculate year average
    year_average = round(total_score / max(1, subject_count), 2)
    
    # Determine year grade and position
    overall_grade = ''
    position = ''
    if year_average >= 80:
        overall_grade = 'A'
        position = 'First Class'
    elif year_average >= 75:
        overall_grade = 'A-'
        position = 'First Class'
    elif year_average >= 70:
        overall_grade = 'B+'
        position = 'First Class'
    elif year_average >= 65:
        overall_grade = 'B'
        position = 'Second Class Upper'
    elif year_average >= 60:
        overall_grade = 'B-'
        position = 'Second Class Upper'
    elif year_average >= 55:
        overall_grade = 'C+'
        position = 'Second Class Lower'
    elif year_average >= 50:
        overall_grade = 'C'
        position = 'Second Class Lower'
    elif year_average >= 40:
        overall_grade = 'D'
        position = 'Pass'
    else:
        overall_grade = 'F'
        position = 'Fail'
    
    context = {
        'student': student,
        'year': year,
        'term_data_list': term_data_list,
        'year_average': year_average,
        'overall_grade': overall_grade,
        'position': position,
        'school_name': settings.SCHOOL_NAME,
        'school_logo': settings.SCHOOL_LOGO_PATH,
        'generated_date': datetime.now().strftime("%d-%m-%Y"),
        'principal_name': settings.PRINCIPAL_NAME,
        'is_year_report': True
    }
    
    pdf = render_to_pdf('marks/pdf_reports/year_report_template.html', context)
    if pdf:
        filename = f"{slugify(student.name)}_{year}_annual_report.pdf"
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    return HttpResponse("Error generating PDF", status=400)

def get_term_data(progress_data, year, term_name):
    """
    Helper function to extract term data for a specific year and term
    """
    for term_data in progress_data:
        if term_data['term'].year == year and term_data['term'].name == term_name:
            return term_data
    return None

def get_year_data(progress_data, year):
    """
    Helper function to extract all term data for a specific year
    """
    year_data = []
    for term_data in progress_data:
        if term_data['term'].year == year:
            year_data.append(term_data)
    return year_data