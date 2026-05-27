#!/usr/bin/env python3
"""
Erstellt ein professionelles Pitch-Deck PDF für CarbonAI Solutions
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.colors import HexColor
import os

# PDF Konfiguration
OUTPUT_PATH = "/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/test_pitch_deck_output/carbonai_pitch_deck_iteration_1.pdf"

# Farben (Corporate Green Theme)
PRIMARY_COLOR = HexColor('#2E7D32')  # Forest Green
SECONDARY_COLOR = HexColor('#4CAF50')  # Light Green
ACCENT_COLOR = HexColor('#FFC107')  # Amber
TEXT_COLOR = HexColor('#333333')
LIGHT_GRAY = HexColor('#F5F5F5')

def create_styles():
    """Erstellt benutzerdefinierte Styles für das PDF"""
    styles = getSampleStyleSheet()
    
    # Title Style
    styles.add(ParagraphStyle(
        name='PitchTitle',
        parent=styles['Title'],
        fontSize=36,
        textColor=PRIMARY_COLOR,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    # Subtitle Style
    styles.add(ParagraphStyle(
        name='PitchSubtitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=SECONDARY_COLOR,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    # Heading Style
    styles.add(ParagraphStyle(
        name='PitchHeading',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=PRIMARY_COLOR,
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    ))
    
    # Body Style
    styles.add(ParagraphStyle(
        name='PitchBody',
        parent=styles['Normal'],
        fontSize=12,
        textColor=TEXT_COLOR,
        spaceAfter=12,
        leading=16,
        fontName='Helvetica'
    ))
    
    # Bullet Style
    styles.add(ParagraphStyle(
        name='PitchBullet',
        parent=styles['Normal'],
        fontSize=11,
        textColor=TEXT_COLOR,
        spaceAfter=8,
        leftIndent=20,
        bulletIndent=10,
        fontName='Helvetica'
    ))
    
    return styles

def create_title_page(canvas, doc):
    """Erstellt die Titelseite"""
    canvas.saveState()
    
    # Background
    canvas.setFillColor(PRIMARY_COLOR)
    canvas.rect(0, 0, doc.width, doc.height, stroke=0, fill=1)
    
    # Logo Placeholder
    canvas.setFillColor(colors.white)
    canvas.drawCentredString(doc.width/2, doc.height - 200, "CarbonAI Solutions")
    
    canvas.setFont('Helvetica-Bold', 48)
    canvas.setFillColor(colors.white)
    canvas.drawCentredString(doc.width/2, doc.height - 300, "Making Net Zero")
    canvas.drawCentredString(doc.width/2, doc.height - 350, "Profitable")
    
    canvas.setFont('Helvetica', 18)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawCentredString(doc.width/2, doc.height - 450, "AI-Powered Carbon Footprint Optimization")
    canvas.drawCentredString(doc.width/2, doc.height - 480, "for Manufacturing")
    
    canvas.restoreState()

def create_pitch_deck():
    """Erstellt das vollständige Pitch-Deck PDF"""
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    styles = create_styles()
    story = []
    
    # Title Page
    story.append(Spacer(1, 2.5*inch))
    
    # Slide 1: Title & Hook
    story.append(Paragraph("The Cost of Carbon:", styles['PitchTitle']))
    story.append(Paragraph("Operationalizing Decarbonization", styles['PitchSubtitle']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("CarbonAI Solutions", styles['PitchBody']))
    story.append(Paragraph("Making Net Zero profitable", styles['PitchBody']))
    story.append(PageBreak())
    
    # Slide 2: Problem
    story.append(Paragraph("The Problem", styles['PitchHeading']))
    story.append(Paragraph("Compliance is a Guessing Game", styles['PitchSubtitle']))
    story.append(Spacer(1, 0.3*inch))
    
    problem_data = [
        ["Complexity", "Scope 3 Emissionen sind ein Daten-Chaos (Lieferkette, Prozesse, Energiequellen)"],
        ["Ineffizienz", "Manuelle oder ERP-basierte Messung ist langsam, teuer und ungenau"],
        ["Wirtschaftlicher Druck", "Mittelständler müssen jetzt handeln, um wettbewerbsfähig zu bleiben (EU CBAM, Lieferkettengesetze)"]
    ]
    
    problem_table = Table(problem_data, colWidths=[2*inch, 4*inch])
    problem_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), LIGHT_GRAY),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray)
    ]))
    story.append(problem_table)
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Der deutsche Mittelstand verliert jährlich geschätzt 2-3 Milliarden Euro an Optimierungspotenzial durch ungenaue CO2-Messung.", styles['PitchBody']))
    story.append(PageBreak())
    
    # Slide 3: Solution
    story.append(Paragraph("The Solution", styles['PitchHeading']))
    story.append(Paragraph("AI-Driven Optimization, Not Just Reporting", styles['PitchSubtitle']))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("CarbonAI ist eine proprietäre, Predictive AI-Engine, die Produktionsdaten (Energieverbrauch, Materialfluss, Prozessparameter) in Echtzeit mit Emissionsfaktoren verknüpft.", styles['PitchBody']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Wir liefern nicht nur einen Fußabdruck (Reporting), sondern aktive, umsetzbare Optimierungsanweisungen (Operation AI).", styles['PitchBody']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Key Feature: Vom Rohdaten-Input zum CO2-reduzierten Produktionsplan – automatisiert.", styles['PitchBody']))
    story.append(PageBreak())
    
    # Slide 4: Product Demo
    story.append(Paragraph("How It Works", styles['PitchHeading']))
    story.append(Paragraph("From Data Chaos to Decarbonization Roadmap", styles['PitchSubtitle']))
    story.append(Spacer(1, 0.3*inch))
    
    workflow_data = [
        ["Step 1: Input", "IoT-Sensordaten, ERP-Daten, Lieferkettendaten (Integration)"],
        ["Step 2: Engine", "CarbonAI AI verarbeitet und simuliert (Predictive Modeling)"],
        ["Step 3: Output", "Dashboard mit 3 KPIs: Reduktionspotenzial (%), Kosteneinsparung (€), Zeitrahmen (Tage)"]
    ]
    
    workflow_table = Table(workflow_data, colWidths=[1.5*inch, 4.5*inch])
    workflow_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), SECONDARY_COLOR),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), LIGHT_GRAY),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray)
    ]))
    story.append(workflow_table)
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("USP: Wir sind operational. Wir zeigen, wo und wie man die Energie sparen kann, nicht nur, wie viel man verbraucht hat.", styles['PitchBody']))
    story.append(PageBreak())
    
    # Slide 5: Market Size
    story.append(Paragraph("Market Size & Opportunity", styles['PitchHeading']))
    story.append(Paragraph("The Global Transition Market", styles['PitchSubtitle']))
    story.append(Spacer(1, 0.3*inch))
    
    market_data = [
        ["TAM (Total Addressable Market)", "$50 Mrd+ - Globales industrielles CO2-Management & Effizienz-SaaS"],
        ["SAM (Serviceable Available Market)", "$3 Mrd - DACH-Mittelstand in produzierenden Gewerben mit Compliance-Druck"],
        ["SOM (Serviceable Obtainable Market)", "50 Kunden in 3 Jahren (5-10% des SAM)"]
    ]
    
    market_table = Table(market_data, colWidths=[2.5*inch, 3.5*inch])
    market_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), LIGHT_GRAY),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray)
    ]))
    story.append(market_table)
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("VC-Takeaway: Wir zielen auf eine massive, regulatorisch getriebene Marktdurchdringung.", styles['PitchBody']))
    story.append(PageBreak())
    
    # Slide 6: Traction
    story.append(Paragraph("Traction & Metrics", styles['PitchHeading']))
    story.append(Paragraph("Proven Impact, Growing Revenue", styles['PitchSubtitle']))
    story.append(Spacer(1, 0.3*inch))
    
    traction_data = [
        ["Pilot-Kunden", "5 Industrie-Pioniere (Automobilzulieferer, Maschinenbau)"],
        ["MRR", "€15,000 (Steigend um 25% QoQ)"],
        ["Impact", "Unsere Piloten haben im Schnitt 120 Tonnen CO2/Jahr reduziert"],
        ["LTV/CAC", "> 5:1 (Zeigt skalierbares Geschäftsmodell)"]
    ]
    
    traction_table = Table(traction_data, colWidths=[2*inch, 4*inch])
    traction_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), SECONDARY_COLOR),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), LIGHT_GRAY),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray)
    ]))
    story.append(traction_table)
    story.append(PageBreak())
    
    # Slide 7: Business Model
    story.append(Paragraph("Business Model & Go-to-Market", styles['PitchHeading']))
    story.append(Paragraph("Subscription SaaS + Performance-Optimierung", styles['PitchSubtitle']))
    story.append(Spacer(1, 0.3*inch))
    
    model_data = [
        ["Core SaaS", "Basis-Abo für die AI-Engine (€2,000-€5,000/Monat) - Recurring Revenue"],
        ["Optimization Fee", "Prozentualer Anteil der durch CarbonAI eingesparten Kosten (Performance-Basis)"],
        ["Enterprise Consulting", "Implementierung bei Großkunden (€50,000-€100,000/Projekt)"]
    ]
    
    model_table = Table(model_data, colWidths=[2*inch, 4*inch])
    model_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), LIGHT_GRAY),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray)
    ]))
    story.append(model_table)
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Go-to-Market: Phase 1 (Berlin/DACH) - Industrie-Cluster-Fokus mit KfW/Deutschlandfonds Förderung. Phase 2 - Globale Skalierung.", styles['PitchBody']))
    story.append(PageBreak())
    
    # Slide 8: Competition
    story.append(Paragraph("Competition & Defensibility", styles['PitchHeading']))
    story.append(Paragraph("We Bridge the Gap between Reporting and Action", styles['PitchSubtitle']))
    story.append(Spacer(1, 0.3*inch))
    
    competition_data = [
        ["Traditionelle Berater", "Reporting, teuer, statisch - Nicht operational"],
        ["Reine SaaS-Tracker", "AI, aber nur Messung, kein Handlungsplan - Keine Optimierung"],
        ["CarbonAI (Sweet Spot)", "Predictive AI + Operational Action Plan - Aktive CO2-Reduktion"]
    ]
    
    competition_table = Table(competition_data, colWidths=[2.5*inch, 3.5*inch])
    competition_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), SECONDARY_COLOR),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), LIGHT_GRAY),
        ('BACKGROUND', (2, 0), (2, -1), ACCENT_COLOR),
        ('TEXTCOLOR', (2, 0), (2, -1), TEXT_COLOR),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray)
    ]))
    story.append(competition_table)
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Defensibility: Proprietäre Datenmodelle (AI-IP), Industriepartner-Netzwerk, Integration in Kernprozesse (Hohe Switching Costs)", styles['PitchBody']))
    story.append(PageBreak())
    
    # Slide 9: Team
    story.append(Paragraph("Team", styles['PitchHeading']))
    story.append(Paragraph("The Perfect Intersection of Tech, Industry, and Scale", styles['PitchSubtitle']))
    story.append(Spacer(1, 0.3*inch))
    
    team_data = [
        ["Gründer 1 (AI Tech Expert)", "Fokus auf das Wie (Deep Learning, Predictive Modeling) - Der Architekt"],
        ["Gründer 2 (Industry Veteran)", "Fokus auf das Wo (Mittelstand-Know-how, regulatorische Tiefe) - Der Brückenbauer"],
        ["Gründer 3 (Business Development)", "Fokus auf das Wer (Vertrieb, Mittelständische Netzwerke) - Der Motor"]
    ]
    
    team_table = Table(team_data, colWidths=[2.5*inch, 3.5*inch])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), LIGHT_GRAY),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray)
    ]))
    story.append(team_table)
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Message: Wir sind kein reines Tech-Startup. Wir sind ein Industrial AI Company.", styles['PitchBody']))
    story.append(PageBreak())
    
    # Slide 10: Financials & Ask
    story.append(Paragraph("Financials & The Ask", styles['PitchHeading']))
    story.append(Paragraph("Seed Round: Scaling the Industrial Footprint", styles['PitchSubtitle']))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("The Ask: €800.000", styles['PitchTitle']))
    story.append(Spacer(1, 0.2*inch))
    
    use_of_funds_data = [
        ["40% - Produktentwicklung", "AI-Features, API-Integration"],
        ["40% - Sales & Marketing", "Aufbau des DACH-Vertriebsteams"],
        ["20% - Operation", "Legal, Overhead"]
    ]
    
    funds_table = Table(use_of_funds_data, colWidths=[2.5*inch, 3.5*inch])
    funds_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), SECONDARY_COLOR),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), LIGHT_GRAY),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray)
    ]))
    story.append(funds_table)
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Milestones: Innerhalb von 18 Monaten - 20 zahlende Enterprise-Kunden, €50,000 MRR, Proof-of-Concept für Series A.", styles['PitchBody']))
    story.append(PageBreak())
    
    # Slide 11: Conclusion
    story.append(Paragraph("Conclusion & Call to Action", styles['PitchHeading']))
    story.append(Paragraph("The Future of Manufacturing is Decarbonized. Join us.", styles['PitchSubtitle']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Investieren Sie nicht in Technologie. Investieren Sie in die notwendige Transformation der globalen Industrie.", styles['PitchBody']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Lassen Sie uns das Klima und die Wirtschaft gemeinsam retten.", styles['PitchBody']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Contact:", styles['PitchHeading']))
    story.append(Paragraph("Benjamin Poersch - ben.poersch@gmail.com", styles['PitchBody']))
    story.append(Paragraph("CarbonAI Solutions - Berlin, Germany", styles['PitchBody']))
    
    # Build PDF
    doc.build(story)
    print(f"✅ PDF erstellt: {OUTPUT_PATH}")

if __name__ == "__main__":
    create_pitch_deck()