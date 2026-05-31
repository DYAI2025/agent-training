"""Design Agent - visual design and PDF generation using llama3.2:latest"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import json
import sys

try:
    import ollama
except ImportError:
    ollama = None


@dataclass
class DesignTask:
    """Task for design agent"""
    task_type: str  # "visual_design", "pdf_generation", "accessibility_optimization", "brand_guidelines"
    content: Dict[str, Any]
    requirements: Optional[Dict[str, Any]] = None


@dataclass
class DesignResult:
    """Result from design work"""
    design_system: Dict[str, Any]
    slide_layouts: List[Dict[str, Any]]
    visual_elements: List[str]
    design_recommendations: List[str]


class DesignAgent:
    """Design Agent for visual design and PDF generation"""
    
    def __init__(self, model: str = "llama3.2:latest"):
        self.model = model
        self.ollama = ollama
        
    def create_visual_design(
        self,
        pitch_deck: Dict[str, Any],
        requirements: Dict[str, Any]
    ) -> DesignResult:
        """Create visual design for pitch deck"""
        
        if self.ollama is None:
            return self._fallback_visual_design(pitch_deck, requirements)
        
        prompt = self._build_visual_design_prompt(pitch_deck, requirements)
        
        try:
            response = self.ollama.generate(
                model=self.model,
                prompt=prompt,
                format="json"
            )
            
            result_data = json.loads(response.response)
            return DesignResult(
                design_system=result_data.get("design_system", {}),
                slide_layouts=result_data.get("slide_layouts", []),
                visual_elements=result_data.get("visual_elements", []),
                design_recommendations=result_data.get("design_recommendations", [])
            )
        except Exception as e:
            print(f"Error in visual design: {e}", file=sys.stderr)
            return self._fallback_visual_design(pitch_deck, requirements)
    
    def generate_pdf_structure(
        self,
        pitch_deck: Dict[str, Any],
        export_options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Generate PDF structure for pitch deck"""
        
        if export_options is None:
            export_options = {"quality": "high"}
        
        if self.ollama is None:
            return self._fallback_pdf_structure(pitch_deck)
        
        prompt = self._build_pdf_structure_prompt(pitch_deck, export_options)
        
        try:
            response = self.ollama.generate(
                model=self.model,
                prompt=prompt,
                format="json"
            )
            
            return json.loads(response.response)
        except Exception as e:
            print(f"Error in PDF structure generation: {e}", file=sys.stderr)
            return self._fallback_pdf_structure(pitch_deck)
    
    def optimize_design_for_accessibility(
        self,
        design_content: Dict[str, Any],
        accessibility_standards: str = "WCAG 2.1 AA"
    ) -> Dict[str, Any]:
        """Optimize design for accessibility"""
        
        if self.ollama is None:
            return self._fallback_accessibility_optimization(design_content)
        
        prompt = self._build_accessibility_prompt(design_content, accessibility_standards)
        
        try:
            response = self.ollama.generate(
                model=self.model,
                prompt=prompt,
                format="json"
            )
            
            return json.loads(response.response)
        except Exception as e:
            print(f"Error in accessibility optimization: {e}", file=sys.stderr)
            return self._fallback_accessibility_optimization(design_content)
    
    def create_brand_guidelines(
        self,
        brand_info: Dict[str, Any],
        include_examples: bool = True
    ) -> Dict[str, Any]:
        """Create comprehensive brand guidelines"""
        
        if self.ollama is None:
            return self._fallback_brand_guidelines(brand_info)
        
        prompt = self._build_brand_guidelines_prompt(brand_info, include_examples)
        
        try:
            response = self.ollama.generate(
                model=self.model,
                prompt=prompt,
                format="json"
            )
            
            return json.loads(response.response)
        except Exception as e:
            print(f"Error in brand guidelines creation: {e}", file=sys.stderr)
            return self._fallback_brand_guidelines(brand_info)
    
    def _build_visual_design_prompt(
        self,
        pitch_deck: Dict[str, Any],
        requirements: Dict[str, Any]
    ) -> str:
        """Build prompt for visual design"""
        
        prompt = f"""You are a professional presentation designer. Create a visual design for the following pitch deck.

PITCH DECK:
{json.dumps(pitch_deck, indent=2)}

DESIGN REQUIREMENTS:
{json.dumps(requirements, indent=2)}

Provide design specifications in JSON format:
{{
    "design_system": {{
        "primary_color": "<hex>",
        "secondary_color": "<hex>",
        "accent_color": "<hex>",
        "font_family": "<font>",
        "font_sizes": {{"title": <size>, "body": <size>}}
    }},
    "slide_layouts": [
        {{
            "slide_index": <index>,
            "layout": "<layout_type>",
            "elements": ["<element1>", "<element2>"]
        }}
    ],
    "visual_elements": ["<element1>", "<element2>"],
    "design_recommendations": ["<recommendation1>", "<recommendation2>"]
}}

Focus on modern, professional design that enhances content clarity."""
        
        return prompt
    
    def _build_pdf_structure_prompt(
        self,
        pitch_deck: Dict[str, Any],
        export_options: Dict[str, Any]
    ) -> str:
        """Build prompt for PDF structure"""
        
        prompt = f"""You are a PDF specialist. Create the optimal PDF structure for the following pitch deck.

PITCH DECK:
{json.dumps(pitch_deck, indent=2)}

EXPORT OPTIONS:
{json.dumps(export_options, indent=2)}

Provide PDF structure in JSON format:
{{
    "pdf_structure": {{
        "page_size": "<A4/Letter>",
        "orientation": "<landscape/portrait>",
        "margins": {{"top": <inches>, "bottom": <inches>, "left": <inches>, "right": <inches>}}
    }},
    "page_breaks": [<slide_index1>, <slide_index2>],
    "master_slides": [
        {{"name": "<master_name>", "background": "<color>"}}
    ],
    "export_settings": {{
        "quality": "<high/medium/low>",
        "compression": "<none/low/medium/high>",
        "include_fonts": <boolean>
    }}
}}

Optimize for professional presentation and print quality."""
        
        return prompt
    
    def _build_accessibility_prompt(
        self,
        design_content: Dict[str, Any],
        accessibility_standards: str
    ) -> str:
        """Build prompt for accessibility optimization"""
        
        prompt = f"""You are an accessibility specialist. Optimize the following design for {accessibility_standards} compliance.

DESIGN CONTENT:
{json.dumps(design_content, indent=2)}

Provide accessibility analysis in JSON format:
{{
    "accessibility_score": <float 0-1>,
    "issues": [
        {{"type": "<issue_type>", "severity": "<high/medium/low>", "description": "<description>"}}
    ],
    "recommendations": ["<recommendation1>", "<recommendation2>"],
    "optimized_design": {{
        "colors": ["<color1>", "<color2>"],
        "fonts": ["<font1>", "<font2>"],
        "font_sizes": [<size1>, <size2>]
    }}
}}

Focus on color contrast, font sizes, and screen reader compatibility."""
        
        return prompt
    
    def _build_brand_guidelines_prompt(
        self,
        brand_info: Dict[str, Any],
        include_examples: bool
    ) -> str:
        """Build prompt for brand guidelines"""
        
        prompt = f"""You are a brand specialist. Create comprehensive brand guidelines for the following company.

BRAND INFO:
{json.dumps(brand_info, indent=2)}

INCLUDE EXAMPLES: {include_examples}

Provide brand guidelines in JSON format:
{{
    "brand_identity": {{
        "logo_variations": ["<variation1>", "<variation2>"],
        "color_palette": {{
            "primary": "<hex>",
            "secondary": "<hex>",
            "neutral": "<hex>"
        }},
        "typography": {{
            "headings": "<font>",
            "body": "<font>"
        }}
    }},
    "voice_guidelines": {{
        "tone": "<tone_description>",
        "language_style": "<style>",
        "key_phrases": ["<phrase1>", "<phrase2>"]
    }},
    "usage_rules": ["<rule1>", "<rule2>"]
}}

Create guidelines that ensure consistent brand application."""
        
        return prompt
    
    def _fallback_visual_design(
        self,
        pitch_deck: Dict[str, Any],
        requirements: Dict[str, Any]
    ) -> DesignResult:
        """Fallback visual design when ollama is not available"""
        
        return DesignResult(
            design_system={
                "primary_color": "#0066CC",
                "secondary_color": "#FFFFFF",
                "accent_color": "#FF6B35",
                "font_family": "Inter",
                "font_sizes": {"title": 48, "body": 16}
            },
            slide_layouts=[
                {"slide_index": i, "layout": "standard", "elements": ["title", "content"]}
                for i in range(len(pitch_deck.get("slides", [])))
            ],
            visual_elements=["basic_icons", "text"],
            design_recommendations=["Install ollama for advanced design features"]
        )
    
    def _fallback_pdf_structure(
        self,
        pitch_deck: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Fallback PDF structure when ollama is not available"""
        
        return {
            "pdf_structure": {
                "page_size": "A4",
                "orientation": "landscape",
                "margins": {"top": 0.5, "bottom": 0.5, "left": 0.5, "right": 0.5}
            },
            "page_breaks": [],
            "master_slides": [
                {"name": "standard", "background": "#FFFFFF"}
            ],
            "export_settings": {
                "quality": "medium",
                "compression": "medium",
                "include_fonts": True
            }
        }
    
    def _fallback_accessibility_optimization(
        self,
        design_content: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Fallback accessibility optimization when ollama is not available"""
        
        return {
            "accessibility_score": 0.7,
            "issues": [],
            "recommendations": ["Install ollama for detailed accessibility analysis"],
            "optimized_design": design_content
        }
    
    def _fallback_brand_guidelines(
        self,
        brand_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Fallback brand guidelines when ollama is not available"""
        
        return {
            "brand_identity": {
                "logo_variations": ["primary"],
                "color_palette": {
                    "primary": "#0066CC",
                    "secondary": "#FF6B35",
                    "neutral": "#F5F5F5"
                },
                "typography": {
                    "headings": "Arial",
                    "body": "Arial"
                }
            },
            "voice_guidelines": {
                "tone": "professional",
                "language_style": "clear",
                "key_phrases": []
            },
            "usage_rules": ["Install ollama for detailed brand guidelines"]
        }


if __name__ == "__main__":
    # Quick test
    agent = DesignAgent()
    
    test_pitch_deck = {
        "title": "Test Pitch",
        "slides": [{"title": "Problem", "content": "Test"}]
    }
    
    result = agent.create_visual_design(
        pitch_deck=test_pitch_deck,
        requirements={"style": "modern"}
    )
    
    print(f"Design system: {result.design_system}")
    print(f"Recommendations: {result.design_recommendations}")
