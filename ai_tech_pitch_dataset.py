#!/usr/bin/env python3
"""
AI/Tech Startup Pitch Deck Dataset (50 Beispiele)
Spezialisiert auf AI/ML, Developer Tools, Data/Analytics, Cloud/Infrastructure, AI SaaS
"""

AI_TECH_PITCH_DECK_DATASET = [
    # PROBLEM SLIDES (10 Beispiele)
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "ai_ml",
        "input": "Erstelle Problem-Slide für AutoML-Startup",
        "output": "Problem: Data Scientists verbringen 80% ihrer Zeit mit Model Engineering statt Business Value. AutoML Tools sind komplex und erfordern ML-Expertise. Kleinere Unternehmen haben keine Ressourcen für ML-Teams. 70% der ML-Projects scheitern an der Deployment-Phase. Zeit-to-Market für AI-Features ist zu lang."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "ai_ml",
        "input": "Erstelle Problem-Slide für Computer Vision Quality Control",
        "output": "Problem: Manuelle Qualitätskontrolle in der Fertigung ist langsam und fehleranfällig. 15% der Defekte werden übersehen. Human Inspectors können nicht 24/7 arbeiten. Konsistenz ist schwer zu gewährleisten. Kosten für manuelle QC sind hoch und skalieren nicht. Schäden durch spät erkannte Defekte sind teuer."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "ai_ml",
        "input": "Erstelle Problem-Slide für LLM Code Assistant",
        "output": "Problem: Entwickler verbringen 30% ihrer Zeit mit Boilerplate-Code. Code-Reviews sind zeitaufwendig und oft inkonsistent. Junior-Entwickler brauchen viel Mentoring. Knowledge-Silos im Team führen zu Code-Duplizierung. Onboarding neuer Entwickler dauert 3+ Monate. Code-Quality variiert stark zwischen Entwicklern."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "developer_tools",
        "input": "Erstelle Problem-Slide für CI/CD Pipeline Automation",
        "output": "Problem: CI/CD Pipelines sind manuell konfiguriert und fehleranfällig. 40% der Deployments scheitern durch Konfigurationsfehler. Environment-Drift zwischen Dev und Prod ist häufig. Rollouts dauern Stunden statt Minuten. Keine standardisierten Best Practices across Teams. Debugging von Pipeline-Fehlern ist zeitraubend."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "developer_tools",
        "input": "Erstelle Problem-Slide für Code Security Scanning",
        "output": "Problem: Sicherheitslücken werden oft zu spät entdeckt (nach Production). 60% der Unternehmen haben keine automatischen Security-Scans. Manual Code-Reviews für Security sind unzuverlässig. Compliance-Requirements (SOC2, GDPR) sind schwer zu gewährleisten. Security-Teams sind überlastet mit False Positives. Zero-Day-Exploits werden oft zu spät erkannt."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "data_analytics",
        "input": "Erstelle Problem-Slide für Real-time Analytics",
        "output": "Problem: Unternehmen haben Daten-Latency von Stunden bis Tagen. Real-time Entscheidungen sind unmöglich. Batch-Processing ist zu langsam für Customer Experience. Data-Silos verhindern ganzheitliche Insights. 50% der Daten werden nie analysiert. Wettbewerbsvorte durch schnelle Insights gehen verloren."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "data_analytics",
        "input": "Erstelle Problem-Slide für Data Quality Automation",
        "output": "Problem: Data Quality-Probleme kosten Unternehmen jährlich €15M. 30% der Daten sind fehlerhaft oder unvollständig. Manuelle Data-Cleaning ist zeitaufwendig und fehleranfällig. Data-Governance ist manuell und nicht skalierbar. Compliance-Risiken durch schlechte Datenqualität. Vertrauen in Analytics-Daten ist gering."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "cloud_infrastructure",
        "input": "Erstelle Problem-Slide für Kubernetes Management",
        "output": "Problem: Kubernetes-Cluster sind komplex zu managen. 70% der Unternehmen haben nicht genug Kubernetes-Expertise. Cluster-Optimierung ist manuell und zeitraubend. Multi-Cluster-Management ist eine Herausforderung. Cost-Overruns durch fehlende Resource-Limits. Troubleshooting von Cluster-Issues erfordert spezialisierte Kenntnisse."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "ai_saas",
        "input": "Erstelle Problem-Slide für AI Sales Assistant",
        "output": "Problem: Sales-Teams verbringen 60% ihrer Zeit mit Admin-Aufgaben statt Selling. Lead-Qualification ist subjektiv und inkonsistent. Follow-up-Timing ist oft suboptimal. CRM-Daten sind unvollständig und veraltet. Sales-Training ist teuer und zeitintensiv. Conversion-Raten sind niedrig durch fehlende Personalisierung."
    },
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "ai_saas",
        "input": "Erstelle Problem-Slide für AI Customer Support Chatbot",
        "output": "Problem: Kundensupport ist 24/7 schwierig zu staffen. 40% der Kundenanfragen kommen außerhalb der Geschäftszeiten. First-Response-Time ist oft zu lang. Support-Agenten sind mit einfachen Fragen ausgelastet. Konsistenz der Antworten variiert stark zwischen Agenten. Kunden-Erfahrung leidet unter langen Wartezeiten."
    },

    # SOLUTION SLIDES (10 Beispiele)
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "ai_ml",
        "input": "Erstelle Solution-Slide für AutoML-Startup",
        "output": "Solution: No-Code AutoML Platform für Business Users. Automatische Model-Auswahl und Hyperparameter-Optimierung. Integration mit bestehenden Data Sources. One-Click Deployment auf Cloud-Infrastruktur. 10x schnellere Time-to-Market für AI-Features. Keine ML-Expertise erforderlich. 80% weniger Aufwand für Model-Engineering."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "ai_ml",
        "input": "Erstelle Solution-Slide für Computer Vision Quality Control",
        "output": "Solution: AI-gestützte visuelle Qualitätskontrolle in Echtzeit. 99.9% Erkennungsrate für Defekte. 24/7 Verfügbarkeit ohne Ermüdung. Konsistente Qualitätsstandards across Schichten. 50% schnellere als manuelle Inspektion. Integration mit bestehenden Produktionslinien. ROI innerhalb 6 Monaten durch reduzierte Ausschussrate."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "ai_ml",
        "input": "Erstelle Solution-Slide für LLM Code Assistant",
        "output": "Solution: LLM-basierter Code-Assistant für Developer-Produktivität. Automatische Boilerplate-Code-Generierung. Intelligente Code-Vervollständigung und Refactoring. Kontext-aware Vorschläge basierend auf Codebase. 40% weniger Zeit für repetitive Coding-Aufgaben. Konsistente Code-Quality across Team. Onboarding-Zeit für neue Entwickler auf 2 Wochen reduziert."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "developer_tools",
        "input": "Erstelle Solution-Slide für CI/CD Pipeline Automation",
        "output": "Solution: GitOps-basierte CI/CD Automation Platform. Visuelle Pipeline-Konfiguration ohne YAML. Automatische Environment-Parity zwischen Dev und Prod. One-Click Rollbacks und Rollforwards. Integrierte Security-Scans und Compliance-Checks. 90% weniger Pipeline-Fehler. Deployment-Zeit von Stunden auf Minuten reduziert."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "developer_tools",
        "input": "Erstelle Solution-Slide für Code Security Scanning",
        "output": "Solution: AI-gestützte Code-Security-Plattform. Echtzeit-Security-Scanning während Development. Automatische Remediation-Vorschläge für Schwachstellen. Integration mit allen major CI/CD-Tools. 95% weniger False Positives durch ML. Compliance-Reporting für SOC2, GDPR, HIPAA. Security-Debt wird proaktiv reduziert statt akkumuliert."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "data_analytics",
        "input": "Erstelle Solution-Slide für Real-time Analytics",
        "output": "Solution: Stream-Processing Platform für sub-second Latency. Unified Data Lake mit automatischem ETL. Real-time Dashboards für alle Stakeholder. Event-driven Architecture für sofortige Updates. 100x schnellere Insights als Batch-Processing. Data-Silos automatisch aufgelöst. Self-Service Analytics für Business-User ohne IT-Abhängigkeit."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "data_analytics",
        "input": "Erstelle Solution-Slide für Data Quality Automation",
        "output": "Solution: Automatisierte Data Quality-Plattform mit ML-Anomalie-Erkennung. Kontinuierliche Data-Profiling und Quality-Scores. Automatische Data-Cleaning und Standardisierung. Data-Lineage-Tracking für Compliance. 80% weniger manuelle Data-Cleaning-Aufwand. Data-Quality-Score in Echtzeit für alle Daten-Assets. Trust-Score für Analytics-Daten erhöht."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "cloud_infrastructure",
        "input": "Erstelle Solution-Slide für Kubernetes Management",
        "output": "Solution: AI-gestützte Kubernetes-Management-Plattform. Automatische Cluster-Optimierung basierend auf Workload-Patternen. Multi-Cluster-Management mit unified Dashboard. Cost-Optimierung durch Rightsizing und Spot-Instance-Nutzung. Self-Healing für Cluster-Issues ohne manuelle Intervention. 50% reduzierte Kubernetes-Operations-Kosten."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "ai_saas",
        "input": "Erstelle Solution-Slide für AI Sales Assistant",
        "output": "Solution: AI-gestützter Sales-Assistant für Lead-Management. Automatische Lead-Scoring basierend auf CRM- und Verhaltensdaten. Optimierte Follow-up-Timing durch Predictive Analytics. Personalisierte Outreach-Nachrichten basierend auf Lead-Profil. 50% mehr Conversion-Rate durch optimiertes Timing. Sales-Admin-Zeit auf 20% reduziert. Konsistente Pipeline-Klarität across Team."
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "ai_saas",
        "input": "Erstelle Solution-Slide für AI Customer Support Chatbot",
        "output": "Solution: AI-Chatbot mit menschlicher Qualität für 24/7 Support. Kontext-aware Antworten basierend auf Knowledge-Base und Chat-History. Seamless Handover an menschliche Agenten bei komplexen Fällen. Multilingual-Support für globale Kundenbasis. 80% der Anfragen automatisch gelöst. First-Response-Time unter 30 Sekunden. Kundenzufriedenheit +40%."
    },

    # MARKET SIZE SLIDES (10 Beispiele)
    {
        "role": "content",
        "slide_type": "market",
        "industry": "ai_ml",
        "input": "Erstelle Market Size Slide für AutoML-Startup",
        "output": "Market Size: Global AutoML Market €8B/year. DACH Market €800M/year. Serviceable Addressable Market €400M/year (SMEs without ML-Teams). Serviceable Obtainable Market €40M/year (10% market share in 5 years). Growth Rate: 35% CAGR driven by AI-Demokratisierung. Total Addressable Market €20B/year (global SMB expansion)."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "ai_ml",
        "input": "Erstelle Market Size Slide für Computer Vision QC",
        "output": "Market Size: Global Computer Vision QC Market €3B/year. DACH Manufacturing Market €300M/year. Serviceable Addressable Market €150M/year (mid-size manufacturers). Serviceable Obtainable Market €15M/year (10% market share). Growth Rate: 25% CAGR driven by Industry 4.0 and Quality Automation. Total Addressable Market €12B/year (global manufacturing)."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "ai_ml",
        "input": "Erstelle Market Size Slide für LLM Code Assistant",
        "output": "Market Size: Global AI Coding Assistant Market €2B/year. DACH Developer Tools Market €400M/year. Serviceable Addressable Market €200M/year (software companies with 50+ developers). Serviceable Obtainable Market €20M/year (10% market share). Growth Rate: 45% CAGR driven by LLM-Adoption and Developer Shortage. Total Addressable Market €15B/year (global developer tools)."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "developer_tools",
        "input": "Erstelle Market Size Slide für CI/CD Automation",
        "output": "Market Size: Global CI/CD Tools Market €5B/year. DACH DevOps Market €500M/year. Serviceable Addressable Market €250M/year (SMEs adopting DevOps). Serviceable Obtainable Market €25M/year (10% market share). Growth Rate: 20% CAGR driven by Digital Transformation and Remote Work. Total Addressable Market €25B/year (global DevOps)."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "developer_tools",
        "input": "Erstelle Market Size Slide für Code Security Scanning",
        "output": "Market Size: Global Application Security Market €7B/year. DACH Security Market €700M/year. Serviceable Addressable Market €350M/year (mid-market companies). Serviceable Obtainable Market €35M/year (10% market share). Growth Rate: 18% CAGR driven by increasing Cybersecurity Threats and Compliance Requirements. Total Addressable Market €35B/year (global application security)."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "data_analytics",
        "input": "Erstelle Market Size Slide für Real-time Analytics",
        "output": "Market Size: Global Real-time Analytics Platform Market €6B/year. DACH Data Analytics Market €600M/year. Serviceable Addressable Market €300M/year (data-driven companies). Serviceable Obtainable Market €30M/year (10% market share). Growth Rate: 22% CAGR driven by Real-time Business Requirements and Streaming Data. Total Addressable Market €30B/year (global real-time analytics)."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "data_analytics",
        "input": "Erstelle Market Size Slide für Data Quality Automation",
        "output": "Market Size: Global Data Quality Tools Market €2.5B/year. DACH Data Governance Market €250M/year. Serviceable Addressable Market €125M/year (regulated industries). Serviceable Obtainable Market €12.5M/year (10% market share). Growth Rate: 20% CAGR driven by Data Volume Growth and Compliance Requirements. Total Addressable Market €12.5B/year (global data quality)."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "cloud_infrastructure",
        "input": "Erstelle Market Size Slide für Kubernetes Management",
        "output": "Market Size: Global Kubernetes Management Market €4B/year. DACH Cloud Infrastructure Market €400M/year. Serviceable Addressable Market €200M/year (companies adopting Kubernetes). Serviceable Obtainable Market €20M/year (10% market share). Growth Rate: 30% CAGR driven by Container-Orchestration Adoption and Cloud-Native Transformation. Total Addressable Market €20B/year (global Kubernetes ecosystem)."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "ai_saas",
        "input": "Erstelle Market Size Slide für AI Sales Assistant",
        "output": "Market Size: Global AI Sales Tools Market €1.5B/year. DACH CRM Market €300M/year. Serviceable Addressable Market €150M/year (B2B SaaS companies). Serviceable Obtainable Market €15M/year (10% market share). Growth Rate: 40% CAGR driven by Sales Automation and AI-Adoption in Sales. Total Addressable Market €7.5B/year (global AI sales technology)."
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "ai_saas",
        "input": "Erstelle Market Size Slide für AI Customer Support Chatbot",
        "output": "Market Size: Global AI Customer Support Market €3B/year. DACH Customer Service Market €300M/year. Serviceable Addressable Market €150M/year (SaaS and E-Commerce companies). Serviceable Obtainable Market €15M/year (10% market share). Growth Rate: 35% CAGR driven by Customer Experience expectations and 24/7 Support Requirements. Total Addressable Market €15B/year (global AI customer service)."
    },

    # BUSINESS MODEL SLIDES (10 Beispiele)
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "ai_ml",
        "input": "Erstelle Business Model Slide für AutoML-Startup",
        "output": "Business Model: SaaS Subscription mit Usage-Based Pricing. Pricing: €499/Month Starter, €1,999/Month Professional, €9,999/Month Enterprise. Target: SMEs ohne ML-Teams. Revenue Streams: Subscription (70%), Training-Credits (20%), Premium-Support (10%). Customer Lifetime: 4 years, LTV €8K. CAC €1.5K, LTV:CAC 5:1. Gross Margin 85%."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "ai_ml",
        "input": "Erstelle Business Model Slide für Computer Vision QC",
        "output": "Business Model: Hardware + Software Subscription. Pricing: Hardware €25K one-time, Software €2,999/Month. Target: Mid-size Manufacturers. Revenue Streams: Hardware (60%), Software (30%), Maintenance (10%). Customer Lifetime: 8 years, LTV €120K. CAC €20K, LTV:CAC 6:1. Gross Margin 75%."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "ai_ml",
        "input": "Erstelle Business Model Slide für LLM Code Assistant",
        "output": "Business Model: Freemium mit Seat-Based Pricing. Pricing: Free for Individual Developers, €29/seat/month for Teams, Enterprise Custom. Target: Software Companies with 10+ developers. Revenue Streams: Subscription (85%), Enterprise Features (10%), API Access (5%). Customer Lifetime: 3 years, LTV €1K. CAC €200, LTV:CAC 5:1. Gross Margin 90%."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "developer_tools",
        "input": "Erstelle Business Model Slide für CI/CD Automation",
        "output": "Business Model: SaaS Subscription per Pipeline. Pricing: €99/pipeline/month Basic, €299/pipeline/month Pro, Enterprise Custom. Target: DevOps Teams und Platform Engineering. Revenue Streams: Subscription (80%), Premium Integrations (15%), Training (5%). Customer Lifetime: 5 years, LTV €15K. CAC €3K, LTV:CAC 5:1. Gross Margin 88%."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "developer_tools",
        "input": "Erstelle Business Model Slide für Code Security Scanning",
        "output": "Business Model: SaaS Subscription per Scan. Pricing: €0.10/scan Basic, €0.50/scan Pro, Enterprise Custom. Target: Software Companies mit CI/CD Pipelines. Revenue Streams: Per-Scan (70%), Subscription (20%), Consulting (10%). Customer Lifetime: 4 years, LTV €25K. CAC €4K, LTV:CAC 6:1. Gross Margin 92%."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "data_analytics",
        "input": "Erstelle Business Model Slide für Real-time Analytics",
        "output": "Business Model: SaaS Subscription per Data Volume. Pricing: €999/Month up to 1M events/day, €4,999/Month up to 10M events/day, Enterprise Custom. Target: Data-Driven Companies. Revenue Streams: Subscription (75%), Premium Features (15%), Professional Services (10%). Customer Lifetime: 6 years, LTV €30K. CAC €5K, LTV:CAC 6:1. Gross Margin 82%."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "data_analytics",
        "input": "Erstelle Business Model Slide für Data Quality Automation",
        "output": "Business Model: SaaS Subscription per Data Source. Pricing: €499/Month per 5 Data Sources, €1,999/Month per 20 Data Sources, Enterprise Custom. Target: Data-Intensive Companies. Revenue Streams: Subscription (70%), Connectors (20%), Advisory Services (10%). Customer Lifetime: 5 years, LTV €10K. CAC €2K, LTV:CAC 5:1. Gross Margin 85%."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "cloud_infrastructure",
        "input": "Erstelle Business Model Slide für Kubernetes Management",
        "output": "Business Model: SaaS Subscription per Cluster. Pricing: €299/cluster/month Basic, €999/cluster/month Pro, Enterprise Custom. Target: Companies with Kubernetes-Clusters. Revenue Streams: Subscription (75%), Premium Features (15%), Managed Services (10%). Customer Lifetime: 4 years, LTV €20K. CAC €3K, LTV:CAC 7:1. Gross Margin 80%."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "ai_saas",
        "input": "Erstelle Business Model Slide für AI Sales Assistant",
        "output": "Business Model: SaaS Subscription per Seat. Pricing: €99/seat/month Basic, €199/seat/month Pro, Enterprise Custom. Target: B2B Sales Teams. Revenue Streams: Subscription (80%), Integrations (15%), Training (5%). Customer Lifetime: 3 years, LTV €5K. CAC €1K, LTV:CAC 5:1. Gross Margin 87%."
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "ai_saas",
        "input": "Erstelle Business Model Slide für AI Customer Support Chatbot",
        "output": "Business Model: SaaS Subscription per Conversation. Pricing: €0.50/conversation Basic, €1.50/conversation Pro, Enterprise Custom. Target: E-Commerce and SaaS Companies. Revenue Streams: Per-Conversation (70%), Subscription (20%), Setup Services (10%). Customer Lifetime: 4 years, LTV €8K. CAC €1.5K, LTV:CAC 5:1. Gross Margin 86%."
    },

    # TRACTION SLIDES (10 Beispiele)
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "ai_ml",
        "input": "Erstelle Traction Slide für AutoML-Startup",
        "output": "Traction: 18 Monate seit Launch. 200+ SMB-Kunden, 50K+ Modelle trainiert. 92% Kundenzufriedenheit, 35% Referral Rate. 5 Cloud-Platform Partnerships. Revenue €400K MRR, +45% QoQ. 25 FTEs, €5M Series A. Nächste Meilensteine: 500 Kunden, €1M MRR, Series B in 12 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "ai_ml",
        "input": "Erstelle Traction Slide für Computer Vision QC",
        "output": "Traction: 24 Monate seit Launch. 50+ Manufacturing-Kunden, 10M+ Produkte inspiziert täglich. 99.9% Erkennungsrate, 50% weniger Ausschuss. 15 Industry-Partners. Revenue €600K MRR, +30% QoQ. 35 FTEs, €8M Series A + €3M Grant. Nächste Meilensteine: 100 Kunden, €1.5M MRR, Series B in 18 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "ai_ml",
        "input": "Erstelle Traction Slide für LLM Code Assistant",
        "output": "Traction: 12 Monate seit Launch. 100K+ Active Developers, 1M+ Code-Suggestions pro Tag. 4.8/5 GitHub Rating, 70% DAU/MAU. 20 IDE-Plugin Integrations. Revenue €200K MRR, +60% QoQ. 18 FTEs, €3M Seed. Nächste Meilensteine: 250K Developers, €500K MRR, Series A in 9 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "developer_tools",
        "input": "Erstelle Traction Slide für CI/CD Automation",
        "output": "Traction: 16 Monate seit Launch. 300+ DevOps-Teams, 50K+ Pipelines automatisiert. 95% Pipeline-Stability, 60% weniger Deployment-Zeit. 10 Platform-Partnerships. Revenue €350K MRR, +35% QoQ. 22 FTEs, €4M Series A. Nächste Meilensteine: 800 Teams, €1M MRR, Series B in 15 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "developer_tools",
        "input": "Erstelle Traction Slide für Code Security Scanning",
        "output": "Traction: 14 Monate seit Launch. 150+ Software-Kunden, 5M+ Code-Scans pro Monat. 98% Vulnerability-Abdeckung, 40% weniger Security-Incidents. 8 Compliance-Certifications. Revenue €180K MRR, +40% QoQ. 15 FTEs, €2.5M Seed. Nächste Meilensteine: 400 Kunden, €500K MRR, Series A in 12 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "data_analytics",
        "input": "Erstelle Traction Slide für Real-time Analytics",
        "output": "Traction: 20 Monate seit Launch. 100+ Data-Driven Companies, 10B+ Events pro Tag verarbeitet. Sub-second Latency für 95% der Queries. 30+ Data-Source-Connectors. Revenue €450K MRR, +30% QoQ. 28 FTEs, €6M Series A. Nächste Meilensteine: 250 Kunden, €1.2M MRR, Series B in 18 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "data_analytics",
        "input": "Erstelle Traction Slide für Data Quality Automation",
        "output": "Traction: 10 Monate seit Launch. 80+ Data-Intensive Companies, 500TB+ Daten überwacht. 85% Data-Quality-Score-Verbesserung. 15 Compliance-Approvals. Revenue €120K MRR, +50% QoQ. 12 FTEs, €1.8M Seed. Nächste Meilensteine: 200 Kunden, €300K MRR, Series A in 9 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "cloud_infrastructure",
        "input": "Erstelle Traction Slide für Kubernetes Management",
        "output": "Traction: 22 Monate seit Launch. 200+ Kubernetes-Adoptionen, 1K+ Cluster verwaltet. 50% Kost-Reduktion für Kunden. 20 Cloud-Provider Partnerships. Revenue €280K MRR, +25% QoQ. 20 FTEs, €3.5M Series A. Nächste Meilensteine: 500 Adoptions, €700K MRR, Series B in 15 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "ai_saas",
        "input": "Erstelle Traction Slide für AI Sales Assistant",
        "output": "Traction: 8 Monate seit Launch. 50+ B2B Sales-Teams, 100K+ Leads analysiert. 50% höhere Conversion-Rate, 30% mehr Sales-Meetings. 12 CRM-Integrations. Revenue €80K MRR, +55% QoQ. 10 FTEs, €1.2M Seed. Nächste Meilensteine: 150 Teams, €250K MRR, Series A in 6 Monaten."
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "ai_saas",
        "input": "Erstelle Traction Slide für AI Customer Support Chatbot",
        "output": "Traction: 14 Monate seit Launch. 100+ E-Commerce/SaaS-Kunden, 2M+ Support-Anfragen pro Monat. 80% automatische Auflösung, 40% höhere CSAT. 25 Platform-Integrations. Revenue €150K MRR, +45% QoQ. 14 FTEs, €2M Seed. Nächste Meilensteine: 300 Kunden, €400K MRR, Series A in 12 Monaten."
    }
]

def create_ai_tech_dataset(output_path="ai_tech_pitch_dataset.jsonl"):
    """Erstelle AI/Tech Pitch Deck Dataset im JSONL-Format"""
    import json
    
    with open(output_path, 'w') as f:
        for item in AI_TECH_PITCH_DECK_DATASET:
            f.write(json.dumps(item) + '\n')
    
    print(f"✅ AI/Tech Pitch Deck Dataset erstellt: {output_path}")
    print(f"📊 Anzahl Beispiele: {len(AI_TECH_PITCH_DECK_DATASET)}")
    
    # Statistiken
    slide_types = {}
    industries = {}
    for item in AI_TECH_PITCH_DECK_DATASET:
        slide_type = item['slide_type']
        industry = item['industry']
        slide_types[slide_type] = slide_types.get(slide_type, 0) + 1
        industries[industry] = industries.get(industry, 0) + 1
    
    print(f"\n📊 Slide Types: {slide_types}")
    print(f"🏭 Industries: {industries}")
    print(f"🎯 Rollen: {set(item['role'] for item in AI_TECH_PITCH_DECK_DATASET)}")

if __name__ == "__main__":
    create_ai_tech_dataset()