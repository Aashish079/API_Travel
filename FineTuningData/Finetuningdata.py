'''
Enhanced Script for Processing Monument Data for Llama-3.1-8B Fine-tuning
'''

import os
import json
import re
from typing import List, Dict, Any
import random
from tqdm import tqdm

def extract_monument_sections(text: str) -> List[Dict[str, Any]]:
    """Extract individual monument sections from the text document with improved parsing."""
    # Split the text by major monument headings (# Title)
    monuments = re.split(r'(?=^# )', text, flags=re.MULTILINE)
    
    # Filter out any empty sections
    monuments = [m.strip() for m in monuments if m.strip()]
    
    # Process each monument section
    processed_monuments = []
    for monument in monuments:
        # Extract title and content
        title_match = re.match(r'^# (.*?)(:|\n|$)', monument, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
            # Remove the title from the content
            content = re.sub(r'^# .*?$', '', monument, flags=re.MULTILINE).strip()
            
            # Extract subsections more robustly
            sections = {}
            
            # First, find all section headers
            section_headers = re.finditer(r'^## (.*?)$', content, re.MULTILINE)
            header_positions = [(m.group(1).strip(), m.start()) for m in section_headers]
            
            # Then extract content between headers
            for i in range(len(header_positions)):
                section_title = header_positions[i][0]
                start_pos = header_positions[i][1]
                
                # If this is the last section, the end is the end of the content
                if i == len(header_positions) - 1:
                    section_content = content[start_pos:].strip()
                else:
                    end_pos = header_positions[i+1][1]
                    section_content = content[start_pos:end_pos].strip()
                
                # Remove the section header from the content
                section_content = re.sub(r'^## .*?$', '', section_content, flags=re.MULTILINE).strip()
                
                # Clean up common formatting issues
                section_content = section_content.replace('---', '').strip()
                
                sections[section_title] = section_content
            
            # Extract key facts from content
            key_facts = extract_key_facts(content, title)
            
            processed_monuments.append({
                "title": title,
                "content": content,
                "sections": sections,
                "key_facts": key_facts
            })
    
    return processed_monuments

def extract_key_facts(content: str, title: str) -> Dict[str, str]:
    """Extract key facts from monument content using regex patterns."""
    key_facts = {}
    
    # Extract year/date of construction
    date_matches = re.findall(r'built in (\d{3,4}(?: CE)?)', content)
    if date_matches:
        key_facts['construction_date'] = date_matches[0][0]
    
    # Extract location details
    location_matches = re.findall(r'located in ([^.]+)', content)
    if location_matches:
        key_facts['location'] = location_matches[0].strip()
    
    # Extract builder/patron
    patron_matches = re.findall(r'(commissioned|built|constructed) by ([^.,]+)', content)
    if patron_matches:
        key_facts['patron'] = patron_matches[0][1].strip()
    
    # Extract architectural style
    style_matches = re.findall(r'(style|design) (known as|called)? ([^.,]+)', content)
    if style_matches:
        key_facts['architectural_style'] = style_matches[0][2].strip()
    
    # Extract religious significance
    if 'dedicated to' in content.lower():
        dedication_matches = re.findall(r'dedicated to ([^.,]+)', content.lower())
        if dedication_matches:
            key_facts['dedicated_to'] = dedication_matches[0].strip()
    
    return key_facts

def create_instruction_samples(monuments: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Generate comprehensive instruction-output pairs for fine-tuning."""
    samples = []
    
    for monument in tqdm(monuments, desc="Creating instruction samples"):
        title = monument['title']
        
        # 1. General description queries with variations
        description_instructions = [
            f"Provide a detailed description of {title}.",
            f"Tell me about {title} in Patan, Nepal.",
            f"What is {title}? Provide comprehensive information.",
            f"I'm visiting Patan and want to learn about {title}.",
            f"Give me information about {title} in Nepal."
        ]
        for instruction in description_instructions:
            samples.append({
                "instruction": instruction,
                "input": "",
                "output": monument['content']
            })
        
        # 2. Section-specific questions with variations
        for section_title, section_content in monument['sections'].items():
            section_instructions = [
                f"What is the {section_title} of {title}?",
                f"Tell me about the {section_title} of {title}.",
                f"Describe the {section_title} of {title}.",
                f"I'm interested in the {section_title} of {title}. What can you tell me?",
                f"Provide information about the {section_title} of {title}."
            ]
            
            # Only add a random selection of variations to prevent dataset bloat
            for instruction in random.sample(section_instructions, min(3, len(section_instructions))):
                samples.append({
                    "instruction": instruction,
                    "input": "",
                    "output": section_content
                })
        
        # 3. Specific factual questions based on extracted key facts
        if 'key_facts' in monument and monument['key_facts']:
            for fact_type, fact_value in monument['key_facts'].items():
                if fact_type == 'construction_date':
                    samples.append({
                        "instruction": f"When was {title} built?",
                        "input": "",
                        "output": f"{title} was built in {fact_value}."
                    })
                elif fact_type == 'location':
                    samples.append({
                        "instruction": f"Where is {title} located?",
                        "input": "",
                        "output": f"{title} is located in {fact_value}."
                    })
                elif fact_type == 'patron':
                    samples.append({
                        "instruction": f"Who built or commissioned {title}?",
                        "input": "",
                        "output": f"{title} was built by {fact_value}."
                    })
                elif fact_type == 'architectural_style':
                    samples.append({
                        "instruction": f"What architectural style is {title} built in?",
                        "input": "",
                        "output": f"{title} is built in the {fact_value} style."
                    })
                elif fact_type == 'dedicated_to':
                    samples.append({
                        "instruction": f"Which deity or figure is {title} dedicated to?",
                        "input": "",
                        "output": f"{title} is dedicated to {fact_value}."
                    })
        
        # 4. Specialized questions based on monument type
        if "Temple" in title:
            samples.append({
                "instruction": f"What religious ceremonies or festivals are associated with {title}?",
                "input": "",
                "output": extract_festival_info(monument['content'], title)
            })
        
        if "Pillar" in title or "Dhara" in title:
            samples.append({
                "instruction": f"What is the cultural significance of {title} in Nepalese society?",
                "input": "",
                "output": extract_cultural_significance(monument['content'], title)
            })
        
        # 5. Questions about restoration and current status
        samples.append({
            "instruction": f"How was {title} affected by the 2015 earthquake? What restoration efforts have been made?",
            "input": "",
            "output": extract_earthquake_info(monument['content'], title)
        })
    
    # 6. Create comparative questions between monuments
    if len(monuments) > 1:
        # Group monuments by type for more meaningful comparisons
        temples = [m for m in monuments if "Temple" in m['title']]
        pillars = [m for m in monuments if "Pillar" in m['title']]
        other = [m for m in monuments if "Temple" not in m['title'] and "Pillar" not in m['title']]
        
        # Compare similar monument types
        for monument_group in [temples, pillars, other]:
            if len(monument_group) > 1:
                for i in range(len(monument_group) - 1):
                    for j in range(i + 1, min(i + 3, len(monument_group))):  # Limit to reasonable number of comparisons
                        m1, m2 = monument_group[i], monument_group[j]
                        samples.append({
                            "instruction": f"Compare and contrast {m1['title']} and {m2['title']} in terms of architecture and historical significance.",
                            "input": "",
                            "output": generate_comparison(m1, m2)
                        })
        
        # Create thematic comparisons across all monuments
        samples.append({
            "instruction": "What are the common architectural features shared by temples in Patan Durbar Square?",
            "input": "",
            "output": generate_architectural_analysis(temples)
        })
        
        samples.append({
            "instruction": "How do religious structures in Patan reflect the syncretic nature of Nepalese culture?",
            "input": "",
            "output": generate_religious_analysis(monuments)
        })
    
    # 7. Create itinerary and tourist guidance questions
    samples.append({
        "instruction": "I have 3 hours to explore Patan Durbar Square. What monuments should I prioritize?",
        "input": "",
        "output": generate_itinerary(monuments, duration="3 hours")
    })
    
    samples.append({
        "instruction": "What's the best time of year to visit Patan Durbar Square to experience cultural festivals?",
        "input": "",
        "output": generate_festival_calendar(monuments)
    })
    
    return samples

def extract_festival_info(content: str, title: str) -> str:
    """Extract information about festivals and ceremonies associated with the monument."""
    # First look for a Cultural and Religious Significance section
    sections = re.split(r'^## ', content, flags=re.MULTILINE)
    festival_section = ""
    
    for section in sections:
        if "Cultural" in section or "Religious" in section or "Significance" in section:
            festival_section = section
            break
    
    if not festival_section:
        # If no dedicated section, extract paragraphs mentioning festivals
        festival_keywords = ["festival", "ceremony", "ritual", "worship", "devotee", "celebration"]
        paragraphs = content.split("\n\n")
        festival_paragraphs = []
        
        for para in paragraphs:
            if any(keyword in para.lower() for keyword in festival_keywords):
                festival_paragraphs.append(para)
        
        if festival_paragraphs:
            return f"The following festivals and ceremonies are associated with {title}:\n\n" + "\n\n".join(festival_paragraphs)
        else:
            return f"There is limited information available about specific festivals associated with {title}, but as with most religious structures in Nepal, it likely plays a role in local religious observances and may be particularly active during major Hindu festivals like Dashain and Tihar."
    
    else:
        return f"The following festivals and ceremonies are associated with {title}:\n\n{festival_section}"

def extract_cultural_significance(content: str, title: str) -> str:
    """Extract information about the cultural significance of the monument."""
    # Look for cultural significance mentions
    significance_keywords = ["significance", "important", "symbol", "cultural", "heritage", "tradition"]
    paragraphs = content.split("\n\n")
    significance_paragraphs = []
    
    for para in paragraphs:
        if any(keyword in para.lower() for keyword in significance_keywords):
            significance_paragraphs.append(para)
    
    if significance_paragraphs:
        return f"The cultural significance of {title} includes:\n\n" + "\n\n".join(significance_paragraphs)
    else:
        # Fallback response if nothing specific is found
        return f"{title} is an important part of Nepal's cultural heritage, representing the artistic and architectural achievements of the Newar civilization. Such monuments serve as living links to Nepal's past and continue to play a role in local religious and social practices."

def extract_earthquake_info(content: str, title: str) -> str:
    """Extract information about earthquake damage and restoration efforts."""
    # Look for earthquake and restoration mentions
    earthquake_keywords = ["earthquake", "damage", "restoration", "repair", "rebuild", "conservation"]
    paragraphs = content.split("\n\n")
    earthquake_paragraphs = []
    
    for para in paragraphs:
        if any(keyword in para.lower() for keyword in earthquake_keywords):
            earthquake_paragraphs.append(para)
    
    if earthquake_paragraphs:
        return f"Information about earthquake damage and restoration efforts for {title}:\n\n" + "\n\n".join(earthquake_paragraphs)
    else:
        # Fallback response
        return f"While specific information about earthquake damage to {title} is not detailed in the available content, many structures in Patan Durbar Square were affected by the 2015 Gorkha earthquake. Restoration efforts throughout the square have been ongoing, with organizations like the Kathmandu Valley Preservation Trust working to preserve Nepal's architectural heritage using traditional materials and techniques."

def generate_comparison(monument1: Dict[str, Any], monument2: Dict[str, Any]) -> str:
    """Generate a detailed comparison between two monuments."""
    title1, title2 = monument1['title'], monument2['title']
    
    # Extract key comparison points
    comparison_points = []
    
    # Historical era
    date1 = monument1.get('key_facts', {}).get('construction_date', "unknown date")
    date2 = monument2.get('key_facts', {}).get('construction_date', "unknown date")
    comparison_points.append(f"Historical Era: {title1} was built in {date1}, while {title2} was built in {date2}.")
    
    # Architectural style
    style1 = monument1.get('key_facts', {}).get('architectural_style', "its architectural style")
    style2 = monument2.get('key_facts', {}).get('architectural_style', "its architectural style")
    comparison_points.append(f"Architectural Style: {title1} features {style1}, whereas {title2} showcases {style2}.")
    
    # Religious significance
    dedicated1 = monument1.get('key_facts', {}).get('dedicated_to', "religious significance")
    dedicated2 = monument2.get('key_facts', {}).get('dedicated_to', "religious significance")
    comparison_points.append(f"Religious Significance: {title1} is associated with {dedicated1}, while {title2} is connected to {dedicated2}.")
    
    # Generate the full comparison
    comparison = f"Comparison between {title1} and {title2}:\n\n"
    comparison += "\n\n".join(comparison_points) + "\n\n"
    
    # Add monument-specific details
    comparison += f"{title1}:\n{monument1['content'][:300]}...\n\n"
    comparison += f"{title2}:\n{monument2['content'][:300]}...\n\n"
    
    # Add a synthesizing conclusion
    comparison += f"Both {title1} and {title2} represent important elements of Patan's cultural heritage, showcasing the artistic and architectural achievements of the Newar civilization and the religious diversity of Nepal. Visitors to Patan Durbar Square can appreciate these monuments together to gain a more comprehensive understanding of the historical and spiritual significance of this UNESCO World Heritage Site."
    
    return comparison

def generate_architectural_analysis(temples: List[Dict[str, Any]]) -> str:
    """Generate an analysis of common architectural features among temples."""
    if not temples:
        return "There is insufficient data to provide an architectural analysis of temples in Patan."
    
    # Extract temple names for reference
    temple_names = [temple['title'] for temple in temples]
    
    analysis = "Common Architectural Features of Temples in Patan Durbar Square:\n\n"
    
    # Standard features of Newar temple architecture
    analysis += "1. Tiered Pagoda Design: Most temples in Patan feature multiple tiers or levels, typically two or three, with each successive tier being smaller than the one below. The Krishna Mandir and Char Narayan Temple exemplify this design philosophy.\n\n"
    
    analysis += "2. Materials: Traditional construction materials include brick, wood, and stone. While brick forms the core structure, ornately carved wooden elements (struts, beams, and window frames) provide both decoration and structural support.\n\n"
    
    analysis += "3. Roof Structure: Sloping roofs with wide eaves supported by intricately carved wooden struts are characteristic. These roofs are often covered with terracotta tiles or gilded copper sheets.\n\n"
    
    analysis += "4. Carved Elements: Elaborate wood carvings depicting deities, mythological scenes, and erotic motifs adorn many temples. These serve both decorative and educational purposes, illustrating religious narratives for devotees.\n\n"
    
    analysis += "5. Seismic Adaptations: Traditional Newar temples incorporate flexible joints and adaptive foundations that have helped them withstand earthquakes over centuries.\n\n"
    
    analysis += "6. Surrounding Elements: Many temples feature ancillary structures such as stone pillars (often with Garuda statues), water spouts (hiti), and rest houses (pati) that form part of the ritual landscape.\n\n"
    
    # Reference specific examples
    analysis += f"These architectural elements can be observed across the temples of Patan Durbar Square, including {', '.join(temple_names[:-1])} and {temple_names[-1]}. While each temple has unique features reflecting its specific deity and historical context, together they showcase the consistent architectural language that defines Newar religious structures in the Kathmandu Valley."
    
    return analysis

def generate_religious_analysis(monuments: List[Dict[str, Any]]) -> str:
    """Generate an analysis of religious syncretism reflected in Patan's monuments."""
    analysis = "Religious Syncretism in Patan's Sacred Architecture:\n\n"
    
    analysis += "The monuments of Patan Durbar Square vividly illustrate Nepal's unique religious syncretism, where Hindu and Buddhist traditions harmoniously coexist and intermingle. This synthesis is evident in several key aspects:\n\n"
    
    analysis += "1. Hybrid Deities: Structures like the Harishankar Temple venerate composite deities that combine aspects of different gods—in this case, Vishnu (Hari) and Shiva (Shankar). This theological fusion reflects the Newar approach to religion that transcends sectarian boundaries.\n\n"
    
    analysis += "2. Shared Sacred Spaces: While temples like Krishna Mandir are primarily Hindu, they incorporate Buddhist elements and are often visited by Buddhist devotees. Similarly, Buddhist shrines may incorporate Hindu iconography.\n\n"
    
    analysis += "3. Ritual Integration: Festivals often involve both Hindu and Buddhist participants. For example, during certain celebrations, deities may be paraded to both Hindu temples and Buddhist monasteries (viharas).\n\n"
    
    analysis += "4. Artistic Hybridity: Architectural elements and decorative motifs blend both traditions. The lotus (a Buddhist symbol) appears frequently in Hindu temples, while Hindu deities may be depicted in poses reminiscent of Buddhist iconography.\n\n"
    
    analysis += "5. Functional Overlaps: Structures like the Dhunge Dhara (stone water spouts) serve practical needs while incorporating both Hindu elements (makara creatures) and Buddhist purification concepts.\n\n"
    
    analysis += "This religious fluidity in Patan's monuments demonstrates how Nepalese culture has historically emphasized harmony between different spiritual paths rather than rigid separation. The result is a unique sacred landscape where boundaries between traditions become permeable, creating a distinctively Nepalese approach to spirituality that has persisted despite political changes and natural disasters."
    
    return analysis

def generate_itinerary(monuments: List[Dict[str, Any]], duration: str = "3 hours") -> str:
    """Generate a tourist itinerary for visiting monuments in Patan."""
    # Sort monuments by importance (simplified approach)
    key_monuments = [m for m in monuments if "Krishna Mandir" in m['title'] or "Char Narayan" in m['title']]
    secondary_monuments = [m for m in monuments if m not in key_monuments]
    
    itinerary = f"Recommended {duration} Itinerary for Patan Durbar Square:\n\n"
    
    itinerary += "For a {duration} visit to Patan Durbar Square, I recommend prioritizing these monuments:\n\n"
    
    # Add must-see monuments
    itinerary += "Must-See Monuments:\n"
    for monument in key_monuments:
        itinerary += f"1. {monument['title']} - This iconic structure is essential to understanding Patan's cultural heritage.\n"
    
    # Add a few secondary monuments
    itinerary += "\nIf Time Permits:\n"
    for i, monument in enumerate(secondary_monuments[:3], 1):
        itinerary += f"{i}. {monument['title']} - Worth visiting to appreciate the diversity of architectural styles in the square.\n"
    
    # Add practical tips
    itinerary += "\nPractical Tips:\n"
    itinerary += "- Start your visit early in the morning (before 10 AM) to avoid crowds and harsh midday sun.\n"
    itinerary += "- Purchase the Patan Durbar Square entry ticket (NPR 1000 for foreign tourists) at the main entrance.\n"
    itinerary += "- Consider hiring a local guide for deeper insights into the historical and cultural significance.\n"
    itinerary += "- Visit the Patan Museum, located in the former royal palace, which provides excellent context for understanding the monuments.\n"
    itinerary += "- Take breaks at one of the rooftop cafes overlooking the square for refreshments and spectacular views.\n"
    
    return itinerary

def generate_festival_calendar(monuments: List[Dict[str, Any]]) -> str:
    """Generate information about festival timing in Patan."""
    calendar = "Festival Calendar for Patan Durbar Square:\n\n"
    
    calendar += "The best time to visit Patan Durbar Square to experience cultural festivals depends on your interests. Here's a seasonal overview of major celebrations that animate these monuments:\n\n"
    
    calendar += "Spring (March-May):\n"
    calendar += "- Holi (February/March): The festival of colors is celebrated enthusiastically in Patan.\n"
    calendar += "- Chaitra Dashain (March/April): A smaller version of the main Dashain festival.\n"
    calendar += "- Seto Machhendranath Jatra (April): An important chariot procession honoring the White Machhendranath deity.\n\n"
    
    calendar += "Summer (June-August):\n"
    calendar += "- Sithi Nakha (June): An ancient Newar festival marking the beginning of the monsoon, when water sources like the Dhunge Dhara are cleaned and honored.\n"
    calendar += "- Janai Purnima (July/August): Sacred thread ceremony and celebrations at various temples.\n"
    calendar += "- Krishna Janmashtami (August): Birth celebration of Lord Krishna with special ceremonies at Krishna Mandir. Devotees gather for all-night vigils and bhajans (devotional songs).\n\n"
    
    calendar += "Autumn (September-November):\n"
    calendar += "- Indra Jatra (September): The festival honoring Indra features masked dances and processions.\n"
    calendar += "- Dashain (September/October): Nepal's longest and most important festival with ceremonies at various temples.\n"
    calendar += "- Tihar (October/November): The festival of lights beautifies the entire square with oil lamps and marigold decorations.\n\n"
    
    calendar += "Winter (December-February):\n"
    calendar += "- Yomari Punhi (December): A Newar festival celebrating the harvest with special sweets.\n"
    calendar += "- Magh Sankranti (January): Ritual bathing and offerings at temples and water spouts.\n"
    calendar += "- Shivaratri (February/March): Celebrated with special importance at Vishwanath Temple.\n\n"
    
    calendar += "For the most immersive cultural experience, autumn (particularly during Dashain and Tihar) offers the richest festival atmosphere. However, each season presents unique celebrations that showcase different aspects of Nepal's living heritage. Spring and autumn also offer the most pleasant weather for exploring the square comfortably."
    
    return calendar

def format_for_alpaca(samples: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Format the samples to match the Alpaca dataset structure."""
    formatted_samples = []
    
    for sample in samples:
        formatted_samples.append({
            "instruction": sample["instruction"],
            "input": sample["input"],
            "output": sample["output"]
        })
    
    return formatted_samples

def write_dataset_to_file(samples: List[Dict[str, str]], filename: str):
    """Write the dataset to a JSONL file."""
    with open(filename, 'w', encoding='utf-8') as f:
        for sample in samples:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')

def create_modelfile(output_path: str = "Modelfile"):
    """Create an enhanced Modelfile for Ollama with a more detailed system prompt."""
    modelfile_content = '''FROM llama3.1:8b

# Add EOS_TOKEN to the prompt template
TEMPLATE """
### Instruction: {{.Prompt}}

### Response: {{.Response}} </s>
"""

# Set the format for chat completions with adjusted parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER stop "</s>"
PARAMETER stop "<human>"

# Enhanced system prompt for the Nepal monuments travel guide
SYSTEM """
You are TravelGuru, an expert on historical monuments in Nepal, with specialized knowledge of Patan (Lalitpur) and its UNESCO World Heritage Sites. Your expertise covers:

1. HISTORICAL CONTEXT:
   - The evolution of Nepal's dynasties (Licchavi, Malla, Shah) and their architectural contributions
   - Key historical events that shaped Patan's monuments, including earthquakes and restorations
   - Royal patronage and the social/political context of monument construction

2. ARCHITECTURAL KNOWLEDGE:
   - Distinct Newar architectural styles and their evolution over centuries
   - Construction techniques, materials, and artistic elements (woodcarving, metalwork, stone sculpture)
   - Specialized vocabulary for temple components (torana, struts, tympanum, etc.)
   - Seismic adaptation features in traditional Nepali architecture

3. RELIGIOUS AND CULTURAL SIGNIFICANCE:
   - Hindu-Buddhist syncretism in Nepal's religious practices
   - Specific deities, their iconography, and theological importance
   - Annual festivals, rituals, and ceremonies associated with each monument
   - Living heritage aspects and contemporary worship practices

4. VISITOR INFORMATION:
   - Practical advice for visitors exploring Patan Durbar Square
   - Respectful behavior and etiquette at religious sites
   - Recommended viewing sequences and thematic routes
   - Photography tips and best times to visit each monument

You provide detailed, accurate information that balances scholarly depth with accessibility. Your responses incorporate relevant Nepali and Sanskrit terminology (with translations) when appropriate. When discussing damage from the 2015 earthquake, you include updates on restoration efforts. For comparative questions, you highlight both similarities and contrasting features between monuments. Your knowledge encompasses the following monuments in detail: Garuda Pillar, Harishankar Temple, Krishna Mandir, Dhunge Dhara, Bhimsen Temple, Char Narayan Temple, Vishwanath Temple, and Octagonal Chyasing Deval.
"""
'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(modelfile_content)
    
    print(f"Created enhanced Modelfile at {output_path}")

def main():
    # 1. Read the monument data (assuming it's saved as a text file)
    try:
        with open("MonumentsData.txt", "r", encoding="utf-8") as f:
            monuments_text = f.read()
        print("Successfully read monument data from paste.txt")
    except FileNotFoundError:
        print("Error: paste.txt not found. Please ensure the file exists in the current directory.")
        return
    
    # 2. Extract individual monuments
    monuments = extract_monument_sections(monuments_text)
    print(f"Extracted {len(monuments)} monument descriptions")
    
    # 3. Create instruction-based samples
    instruction_samples = create_instruction_samples(monuments)
    print(f"Created {len(instruction_samples)} instruction samples")
    
    # 4. Format for Alpaca structure
    formatted_samples = format_for_alpaca(instruction_samples)
    
    # 5. Save the dataset
    write_dataset_to_file(formatted_samples, "patan_monuments_dataset.jsonl")
    print(f"Saved dataset to patan_monuments_dataset.jsonl")
    
    # 6. Create enhanced Modelfile
    create_modelfile()
    
    # 7. Sample output for verification
    print("\nSample instruction-output pairs:")
    sample_indices = random.sample(range(len(formatted_samples)), min(3, len(formatted_samples)))
    for i in sample_indices:
        print(f"\nInstruction: {formatted_samples[i]['instruction']}")
        print(f"Output (truncated): {formatted_samples[i]['output'][:150]}...")
    
    # 8. Print next steps
    print("\nNEXT STEPS FOR FINE-TUNING:")
    print("1. Modify the original training code:")
    print("   ```python")
    print("   from datasets import load_dataset")
    print("   dataset = load_dataset('json', data_files='patan_monuments_dataset.jsonl', split='train')")
    print("   dataset = dataset.map(formatting_prompts_func, batched=True)")
    print("   ```")
    print("2. Run the fine-tuning process with the dataset")
    print("3. Create your custom Ollama model using the generated Modelfile:")
    print("   ```bash")
    print("   ollama create patan-guide -f Modelfile")
    print("   ```")
    print("4. Test your model:")
    print("   ```bash")
    print("   ollama run patan-guide")
    print("   ```")

if __name__ == "__main__":
    main()