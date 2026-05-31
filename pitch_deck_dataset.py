#!/usr/bin/env python3
"""
Pitch Deck Content Dataset (50 Beispiele)
Verschiedene Slide-Typen und Branchen für WUPHF Training
"""

PITCH_DECK_DATASET = [
    # PROBLEM SLIDES (10 Beispiele)
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "fintech",
        "input": "Erstelle Problem-Slide für Kredite-Startup",
        "output": "Problem: Traditionelle Banken sind langsam und bürokratisch. SMEs warten durchschnittlich 6 Wochen auf Kreditentscheidung. 40% der Anträge werden abgelehnt ohne klare Begründung. Zinsen sind oft unverhältnismäßig hoch. Kleine Unternehmen haben keine fairen Finanzierungsoptionen."
    },
    {
        "role": "content",
        "slide_type": "problem", 
        "industry": "healthtech",
        "input": "Erstelle Problem-Slide für Telemedizin-Startup",
        "output": "Problem: Ärzte sind überlastet, durchschnittliche Wartezeit 3 Wochen. Ländliche Gebiete haben Ärztemangel. Patienten postpone notwendige Behandlungen. 30% der Notfälle werden zu spät erkannt. Das Gesundheitssystem ist ineffizient und patientenunfreundlich."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "greentech",
        "input": "Erstelle Problem-Slide für Solar-Startup",
        "output": "Problem: Solarenergie ist unzuverlässig wetterabhängig. Speichertechnologien sind teuer und ineffizient. 60% der Solaranlagen laufen unter Kapazität. Netze sind nicht auf dezentrale Energieerzeugung vorbereitet. Verbraucher zahlen zu viel für unzuverlässige Energie."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "saas",
        "input": "Erstelle Problem-Slide für Project Management Tool",
        "output": "Problem: Teams nutzen 5+ verschiedene Tools für Projektmanagement. Informationen sind fragmentiert und schwer auffindbar. 40% der Arbeitszeit wird mit Koordination verschwendet. Missverständnisse führen zu verzögerten Projekten. Keine klare Verantwortlichkeiten und Deadlines."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "ecommerce",
        "input": "Erstelle Problem-Slide für E-Commerce Analytics",
        "output": "Problem: E-Commerce-Unternehmen haben Daten in 10+ Systemen. Marketing-ROI ist nicht messbar. Kundenverhalten ist nicht verständlich. 70% der Marketing-Budgets werden ineffizient ausgegeben. Keine Echtzeit-Insights für Entscheidungen."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "fintech",
        "input": "Erstelle Problem-Slide für Investment-App",
        "output": "Problem: Normale Menschen haben keinen Zugang zu professionellen Investment-Strategien. Bankgebühren fressen Renditen auf. Finanzielle Bildung ist komplex und unverständlich. 80% der Deutschen investieren nicht in Aktien. Chancengleichheit im Finanzsektor fehlt."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "healthtech",
        "input": "Erstelle Problem-Slide für Mental-Health-App",
        "output": "Problem: Psychologische Hilfe ist stigmatisiert und teuer. Wartezeiten für Therapieplätze sind 6+ Monate. 40% der Menschen mit Depressionen suchen keine Hilfe. Prävention wird vernachlässigt. Unternehmen verlieren jährlich €100M durch psychische Krankheiten."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "greentech",
        "input": "Erstelle Problem-Slide für Recycling-Startup",
        "output": "Problem: Recycling ist kompliziert und undurchsichtig. 70% der recyclbaren Materialien landen im Müll. Verbraucher wissen nicht, was recycelbar ist. Unternehmen haben keine Anreize für nachhaltiges Verpacken. Kreislaufwirtschaft ist ineffizient."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "saas",
        "input": "Erstelle Problem-Slide für HR-Software",
        "output": "Problem: HR-Teams verbringen 60% ihrer Zeit mit Admin-Aufgaben. Recruiting ist ineffizient und biased. Onboarding ist chaotisch und zeitaufwendig. Employee Engagement ist nicht messbar. Fluktuation kostet Unternehmen jährlich €50K+ pro Mitarbeiter."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "ecommerce",
        "input": "Erstelle Problem-Slide für Logistik-Startup",
        "output": "Problem: E-Commerce-Lieferungen sind oft zu spät (30% Fehllieferungen). Kunden sind frustriert und canceln Bestellungen. Retouren kosten Unternehmen 20% des Umsatzes. Logistikkosten sind intransparent und hoch. Keine Echtzeit-Tracking für Kunden."
    },

    # SOLUTION SLIDES (10 Beispiele)
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "fintech",
        "input": "Erstelle Solution-Slide für Kredite-Startup",
        "output": "Solution: KI-gestützte Kreditprüfung in <24h. Automatische Analyse von 500+ Datenpunkten. Faire Zinsen basierend auf echtem Risiko. Transparente Entscheidungsgründe. Integration mit bestehenden Banking-Systemen. 95% Kundenzufriedenheit vs 60% bei Banken."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "healthtech",
        "input": "Erstelle Solution-Slide für Telemedizin-Startup",
        "output": "Solution: 24/7 Telemedizin mit qualifizierten Ärzten. KI-gestützte Erstdiagnose innerhalb 5 Minuten. Video-Konsultationen von zu Hause. Automatische Überweisung an Spezialisten. Integration mit lokalen Apotheken. 80% der Fälle können online gelöst werden."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "greentech",
        "input": "Erstelle Solution-Slide für Solar-Startup",
        "output": "Solution: Intelligente Solar-Speicher mit KI-Optimierung. 50% höhere Effizienz durch Wetter-Vorhersage. Dezentrales Energiemanagement für Wohngebäude. Automatische Netzeinspeisung bei Überschuss. Kosten 40% unter konventionellen Speichern."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "saas",
        "input": "Erstelle Solution-Slide für Project Management Tool",
        "output": "Solution: All-in-one Project Management Platform. Automatische Aufgabenverteilung basierend auf Skills. Echtzeit-Kollaboration mit @Mentions. Integrierte Zeitplanung und Resource-Management. KI-gestützte Risiko-Erkennung. 50% weniger Koordinations-Aufwand."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "ecommerce",
        "input": "Erstelle Solution-Slide für E-Commerce Analytics",
        "output": "Solution: Unified Analytics Dashboard für E-Commerce. Automatische ROI-Berechnung für alle Marketing-Kanäle. KI-gestützte Kunden-Segmentierung. Echtzeit-Personalisierung für Website. Predictive Analytics für Bestellvolumen. 30% höhere Conversion-Rate."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "fintech",
        "input": "Erstelle Solution-Slide für Investment-App",
        "output": "Solution: Robo-Advisor mit professionellen Strategien. Automatische Rebalancing basierend auf Marktlage. Bildungsspiele für finanzielle Literacy. Community für Erfahrungsaustausch. Minimale Gebühren (0.5% vs 2% bei Banken). Reguliert und sicher."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "healthtech",
        "input": "Erstelle Solution-Slide für Mental-Health-App",
        "output": "Solution: Anonyme Mental-Health-Support App. KI-gestützte Ersthilfe bei Krisen. Matching mit qualifizierten Therapeuten. Tägliche Übungen und Meditations-Anleitungen. Progress-Tracking und Insights. 50% günstiger als traditionelle Therapie."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "greentech",
        "input": "Erstelle Solution-Slide für Recycling-Startup",
        "output": "Solution: Smart Recycling mit KI-Bilderkennung. App scannt Produkte und sagt Recyclebarkeit. Gamification für mehr Motivation. Integration mit kommunalen Abfall-Systemen. Unternehmen erhalten Recycling-Score für Produkte. 40% mehr Recycling-Rate."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "saas",
        "input": "Erstelle Solution-Slide für HR-Software",
        "output": "Solution: Automatisierte HR-Plattform für moderne Unternehmen. KI-gestütztes Recruiting ohne Bias. Self-Service Onboarding für neue Mitarbeiter. Pulse-Surveys für Employee Engagement. Automatische Compliance-Checks. 60% weniger Admin-Aufwand."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "ecommerce",
        "input": "Erstelle Solution-Slide für Logistik-Startup",
        "output": "Solution: KI-optimierte Logistik für E-Commerce. Predictive Routing basierend auf Verkehr und Wetter. Echtzeit-Tracking für Kunden. Automatische Retouren-Abwicklung. Integration mit lokalen Kurierdiensten. 95% pünktliche Lieferung vs 70% Branchendurchschnitt."
    },

    # MARKET SIZE SLIDES (10 Beispiele)
    {
        "role": "content",
        "slide_type": "market",
        "industry": "fintech",
        "input": "Erstelle Market Size Slide für Kredite-Startup",
        "output": "Market Size: SME Lending Market €200B/year in DACH. Serviceable Addressable Market €50B/year (SMEs mit 10-100 employees). Serviceable Obtainable Market €2.5B/year (5% market share in 5 years). Growth Rate: 12% CAGR driven by digitalization. Total Addressable Market €500B/year (pan-European expansion)."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "healthtech",
        "input": "Erstelle Market Size Slide für Telemedizin-Startup",
        "output": "Market Size: Global Telemedicine Market €80B/year. DACH Market €8B/year (10% of global). Serviceable Addressable Market €4B/year (digital-savvy patients). Serviceable Obtainable Market €400M/year (10% market share). Growth Rate: 25% CAGR driven by pandemic effects and doctor shortage."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "greentech",
        "input": "Erstelle Market Size Slide für Solar-Startup",
        "output": "Market Size: Global Solar Storage Market €15B/year. DACH Market €2B/year. Serviceable Addressable Market €800M/year (residential segment). Serviceable Obtainable Market €80M/year (10% market share). Growth Rate: 30% CAGR driven by energy transition and government incentives."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "saas",
        "input": "Erstelle Market Size Slide für Project Management Tool",
        "output": "Market Size: Global Project Management Software Market €6B/year. DACH Market €600M/year. Serviceable Addressable Market €300M/year (SME segment). Serviceable Obtainable Market €30M/year (10% market share). Growth Rate: 15% CAGR driven by remote work and digital transformation."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "ecommerce",
        "input": "Erstelle Market Size Slide für E-Commerce Analytics",
        "output": "Market Size: Global E-Commerce Analytics Market €3B/year. DACH Market €300M/year. Serviceable Addressable Market €150M/year (mid-market e-commerce). Serviceable Obtainable Market €15M/year (10% market share). Growth Rate: 20% CAGR driven by e-commerce growth and data-driven marketing."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "fintech",
        "input": "Erstelle Market Size Slide für Investment-App",
        "output": "Market Size: Global Robo-Advisor Market €2.5B/year. DACH Market €250M/year. Serviceable Addressable Market €100M/year (retail investors). Serviceable Obtainable Market €10M/year (10% market share). Growth Rate: 18% CAGR driven by financial literacy and zero-commission trading."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "healthtech",
        "input": "Erstelle Market Size Slide für Mental-Health-App",
        "output": "Market Size: Global Mental Health App Market €4B/year. DACH Market €400M/year. Serviceable Addressable Market €200M/year (digital-savvy demographic). Serviceable Obtainable Market €20M/year (10% market share). Growth Rate: 22% CAGR driven by destigmatization and corporate wellness programs."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "greentech",
        "input": "Erstelle Market Size Slide für Recycling-Startup",
        "output": "Market Size: Global Recycling Technology Market €1.5B/year. DACH Market €150M/year. Serviceable Addressable Market €75M/year (consumer and enterprise). Serviceable Obtainable Market €7.5M/year (10% market share). Growth Rate: 18% CAGR driven by regulations and consumer awareness."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "saas",
        "input": "Erstelle Market Size Slide für HR-Software",
        "output": "Market Size: Global HR Software Market €15B/year. DACH Market €1.5B/year. Serviceable Addressable Market €750M/year (SME segment). Serviceable Obtainable Market €75M/year (10% market share). Growth Rate: 12% CAGR driven by talent shortage and automation trends."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "ecommerce",
        "input": "Erstelle Market Size Slide für Logistik-Startup",
        "output": "Market Size: Global E-Commerce Logistics Market €25B/year. DACH Market €2.5B/year. Serviceable Addressable Market €1.25B/year (mid-market e-commerce). Serviceable Obtainable Market €125M/year (10% market share). Growth Rate: 20% CAGR driven by e-commerce growth and customer expectations."
    },

    # BUSINESS MODEL SLIDES (10 Beispiele)
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "fintech",
        "input": "Erstelle Business Model Slide für Kredite-Startup",
        "output": "Business Model: B2B2C mit Revenue Sharing. Pricing: 1% Vermittlungsgebühr bei erfolgreicher Kreditvergabe. Target: SMEs mit 10-100 employees. Revenue Streams: Vermittlungsgebühr (70%), Premium-Features (20%), Data-Insights (10%). Customer Lifetime: 3 years, LTV €15K. CAC €3K, LTV:CAC 5:1."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "healthtech",
        "input": "Erstelle Business Model Slide für Telemedizin-Startup",
        "output": "Business Model: B2C Subscription + B2B Enterprise. Pricing: €29/Month Basic, €79/Month Premium, Enterprise Custom. Target: Versicherte Patienten und Unternehmen. Revenue Streams: Subscription (60%), Enterprise (30%), Pharma-Partnerships (10%). Customer Lifetime: 4 years, LTV €2.4K. CAC €400, LTV:CAC 6:1."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "greentech",
        "input": "Erstelle Business Model Slide für Solar-Startup",
        "output": "Business Model: Hardware Sales + Software Subscription. Pricing: Hardware €5K one-time, Software €19/Month. Target: Homeowners mit Solaranlagen. Revenue Streams: Hardware (60%), Software (30%), Maintenance (10%). Customer Lifetime: 10 years, LTV €7.3K. CAC €1.5K, LTV:CAC 5:1."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "saas",
        "input": "Erstelle Business Model Slide für Project Management Tool",
        "output": "Business Model: SaaS Subscription mit Tiered Pricing. Pricing: €19/Month Starter, €49/Month Professional, €149/Month Enterprise. Target: SMEs und Mid-Market Companies. Revenue Streams: Subscription (85%), Implementation (10%), Support (5%). Customer Lifetime: 5 years, LTV €2.9K. CAC €500, LTV:CAC 6:1."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "ecommerce",
        "input": "Erstelle Business Model Slide für E-Commerce Analytics",
        "output": "Business Model: SaaS Subscription mit Usage-Based Pricing. Pricing: €99/Month Basic, €299/Month Pro, €899/Month Enterprise. Target: E-Commerce-Unternehmen mit €1M+ Umsatz. Revenue Streams: Subscription (75%), Premium Features (15%), Consulting (10%). Customer Lifetime: 4 years, LTV €12K. CAC €2K, LTV:CAC 6:1."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "fintech",
        "input": "Erstelle Business Model Slide für Investment-App",
        "output": "Business Model: Freemium mit Asset-Under-Management Fees. Pricing: Free Basic, 0.5% AUM Fee ab €10K Portfolio. Target: Retail Investors 25-45 years. Revenue Streams: AUM Fees (80%), Premium Features (15%), Partnerships (5%). Customer Lifetime: 8 years, LTV €4K. CAC €300, LTV:CAC 13:1."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "healthtech",
        "input": "Erstelle Business Model Slide für Mental-Health-App",
        "output": "Business Model: B2C Subscription + B2B Enterprise Wellness. Pricing: €19/Month Self, €49/Month Pro, Enterprise Custom. Target: Individuals und Unternehmen. Revenue Streams: Subscription (70%), Enterprise (20%), Insurance (10%). Customer Lifetime: 3 years, LTV €1.4K. CAC €250, LTV:CAC 6:1."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "greentech",
        "input": "Erstelle Business Model Slide für Recycling-Startup",
        "output": "Business Model: Freemium App + B2B Enterprise Licensing. Pricing: Free App, €99/Month Pro, Enterprise Custom. Target: Verbraucher und FMCG-Unternehmen. Revenue Streams: Enterprise (60%), In-App Purchases (30%), Data (10%). Customer Lifetime: 4 years, LTV €3.6K. CAC €600, LTV:CAC 6:1."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "saas",
        "input": "Erstelle Business Model Slide für HR-Software",
        "output": "Business Model: SaaS Subscription per Employee. Pricing: €5/employee/month Basic, €12/employee/month Pro, €25/employee/month Enterprise. Target: Unternehmen mit 50-500 employees. Revenue Streams: Subscription (80%), Implementation (15%), Support (5%). Customer Lifetime: 6 years, LTV €8.6K. CAC €1.2K, LTV:CAC 7:1."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "ecommerce",
        "input": "Erstelle Business Model Slide für Logistik-Startup",
        "output": "Business Model: Transaction Fees + Subscription. Pricing: €2/package Basic, €1.50/package Pro (€99/Month), Enterprise Custom. Target: E-Commerce-Unternehmen mit 100+ orders/day. Revenue Streams: Transaction Fees (70%), Subscription (20%), Premium Services (10%). Customer Lifetime: 5 years, LTV €25K. CAC €4K, LTV:CAC 6:1."
    },

    # TRACTION/GO-TO-MARKET SLIDES (10 Beispiele)
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "fintech",
        "input": "Erstelle Traction Slide für Kredite-Startup",
        "output": "Traction: 12 Monate seit Launch. 150+ SME-Kunden, €15M Kreditvolumen vermittelt. 95% Kundenzufriedenheit, 40% Referral Rate. 3 Bank-Partnerschaften signed. Revenue €150K MRR, +30% QoQ. 15 FTEs, €2M Seed Funding. Nächste Meilensteine: 500 Kunden, €50M Kreditvolumen, Series A in 6 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "healthtech",
        "input": "Erstelle Traction Slide für Telemedizin-Startup",
        "output": "Traction: 18 Monate seit Launch. 50K+ aktive Nutzer, 200K+ Konsultationen. 4.8/5 App Store Rating. 20 Health-Insurance Partners. Revenue €300K MRR, +50% QoQ. 25 FTEs, €5M Series A. Nächste Meilensteine: 200K Nutzer, Pan-EU Expansion, Series B in 12 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "greentech",
        "input": "Erstelle Traction Slide für Solar-Startup",
        "output": "Traction: 24 Monate seit Launch. 1K+ Solar-Speicher installiert. 500+ Partner-Installateure. 98% Kundenzufriedenheit. €10M Revenue run rate. 40 FTEs, €8M Series A + €5M Grant. Nächste Meilensteine: 5K Installationen, International Expansion, Series B in 18 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "saas",
        "input": "Erstelle Traction Slide für Project Management Tool",
        "output": "Traction: 8 Monate seit Launch. 500+ Paying Customers, 2K+ Free Users. 85% Retention Rate, 30% MoM Growth. 50+ Enterprise Trials. Revenue €80K MRR, +40% QoQ. 12 FTEs, €1.5M Seed. Nächste Meilensteine: 2K Customers, €300K MRR, Series A in 6 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "ecommerce",
        "input": "Erstelle Traction Slide für E-Commerce Analytics",
        "output": "Traction: 12 Monate seit Launch. 200+ E-Commerce-Kunden, €500M+ GMV tracked. 30% Average Revenue Increase per Customer. 10 Platform-Partnerships. Revenue €120K MRR, +35% QoQ. 18 FTEs, €2.5M Seed. Nächste Meilensteine: 500 Customers, €500K MRR, Series A in 9 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "fintech",
        "input": "Erstelle Traction Slide für Investment-App",
        "output": "Traction: 6 Monate seit Launch. 25K+ Registered Users, €50M+ AUM. 4.7/5 App Store Rating. 30% Active User Rate. Revenue €25K MRR, +50% QoQ. 8 FTEs, €500K Pre-Seed. Nächste Meilensteine: 100K Users, €200M AUM, Seed Round in 6 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "healthtech",
        "input": "Erstelle Traction Slide für Mental-Health-App",
        "output": "Traction: 10 Monate seit Launch. 75K+ Downloads, 30K+ Active Users. 4.6/5 App Store Rating. 15 Corporate Wellness Partners. Revenue €40K MRR, +60% QoQ. 10 FTEs, €1M Seed. Nächste Meilensteine: 200K Downloads, €150K MRR, Series A in 12 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "greentech",
        "input": "Erstelle Traction Slide für Recycling-Startup",
        "output": "Traction: 14 Monate seit Launch. 200K+ App Downloads, 50K+ Active Users. 4.5/5 App Store Rating. 25 FMCG-Partners. Revenue €30K MRR, +45% QoQ. 12 FTEs, €1.2M Seed. Nächste Meilensteine: 500K Downloads, €100K MRR, Series A in 9 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "saas",
        "input": "Erstelle Traction Slide für HR-Software",
        "output": "Traction: 16 Monate seit Launch. 300+ Companies, 50K+ Employees managed. 90% Retention Rate. 20+ Industry Awards. Revenue €180K MRR, +25% QoQ. 20 FTEs, €3M Series A. Nächste Meilensteine: 1K Companies, €500K MRR, Series B in 12 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "ecommerce",
        "input": "Erstelle Traction Slide für Logistik-Startup",
        "output": "Traction: 20 Monate seit Launch. 150+ E-Commerce-Clients, 1M+ Shipments/month. 97% On-Time Delivery Rate. 30+ Carrier Partners. Revenue €250K MRR, +30% QoQ. 30 FTEs, €4M Series A. Nächste Meilensteine: 500 Clients, €1M MRR, Series B in 15 Monaten."
    }
]

def create_pitch_deck_dataset(output_path="pitch_deck_dataset.jsonl"):
    """Erstelle Pitch Deck Dataset im JSONL-Format"""
    import json
    
    with open(output_path, 'w') as f:
        for item in PITCH_DECK_DATASET:
            f.write(json.dumps(item) + '\n')
    
    print(f"✅ Pitch Deck Dataset erstellt: {output_path}")
    print(f"📊 Anzahl Beispiele: {len(PITCH_DECK_DATASET)}")
    
    # Statistiken
    slide_types = {}
    industries = {}
    for item in PITCH_DECK_DATASET:
        slide_type = item['slide_type']
        industry = item['industry']
        slide_types[slide_type] = slide_types.get(slide_type, 0) + 1
        industries[industry] = industries.get(industry, 0) + 1
    
    print(f"\n📊 Slide Types: {slide_types}")
    print(f"🏭 Industries: {industries}")
    print(f"🎯 Rollen: {set(item['role'] for item in PITCH_DECK_DATASET)}")

if __name__ == "__main__":
    create_pitch_deck_dataset()