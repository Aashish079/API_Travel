import pandas as pd
import re

def split_into_sections(text):
    # Split text into sections by '##' headers
    sections = re.split(r'\n##\s+', text.strip())
    # Remove empty sections
    sections = [s.strip() for s in sections if s.strip()]
    return sections

def extract_title_and_content(section):
    # Split into title and content
    lines = section.split('\n', 1)
    if len(lines) == 2:
        title, content = lines
    else:
        # If there's only one line, it's the title with no content
        title, content = lines[0], ""
    return title.strip(), content.strip()

def create_dataframe(text):
    sections = split_into_sections(text)
    data = []
    
    for i, section in enumerate(sections):
        title, content = extract_title_and_content(section)
        data.append({
            'page_title': title,
            'page_text': content,
            '__index_level_0__': i
        })
    
    return pd.DataFrame(data)

# Your input text
text = """## Garuda Pillar

The Garuda Pillar is an important symbolic structure in Hinduism, representing divine presence and protection. It is often associated with Lord Vishnu, as Garuda is Vishnu's mythical bird mount. In temples, the Garuda Pillar typically stands in front of the main shrine, marking a viewpoint to honor the deity. 

The pillar holds spiritual significance, embodying concepts of devotion and divine connection. In Vaishnavism, it symbolizes the overwhelming love devotees feel for Lord Vishnu or Krishna. Some famous examples include the Garuda Pillar at the Jagannath Temple in Puri.

## Harishankar Temple

Harishankar Temple is an ancient shrine located on the southern slopes of the Gandhamardhan hills in Odisha's Balangir district. Built in the 14th century under the guidance of Queen Durlabha Devi, it is dedicated to a unique form of deity combining aspects of both Vishnu (Hari) and Shiva (Shankar).

The temple is renowned for its picturesque setting amidst lush greenery and cascading streams. A perennial spring flows near the temple, forming beautiful waterfalls over granite rocks. This natural beauty makes Harishankar a popular pilgrimage site as well as a tourist attraction.

Architecturally, the temple showcases a distinctive style that differs from the typical Odishan temple architecture. Its design incorporates intricate carvings and sculptures depicting Hindu deities and mythological scenes.

The site also holds historical significance, with nearby ruins believed to be remnants of the ancient Parimalgiri University. During festivals like Makar Sankranti and Shivratri, the temple comes alive with religious ceremonies and gatherings.

## Krishna Mandir

Krishna Mandir is a remarkable Hindu temple located in Patan Durbar Square, Nepal. Built in 1637 AD by King Siddhinarasimha Malla, it is considered one of the finest examples of stone architecture in Nepal.

The temple is constructed in the Shikhara style, which is unusual for the Kathmandu Valley. It rises three stories high over a three-stage plinth, reaching a total height of 19.67 meters. The structure is entirely made of stone, featuring intricate carvings and sculptures that showcase exceptional craftsmanship.

Each floor of Krishna Mandir is dedicated to different deities:
- Ground floor: Houses a solid core with an circumambulatory path
- First floor: Dedicated to Lord Krishna
- Second floor: Contains a Shiva lingam
- Third floor: Dedicated to Lokeshwor (a form of Avalokiteshvara)

The temple walls are adorned with scenes from the Hindu epics Ramayana and Mahabharata, carved in stone and accompanied by inscriptions in Newari script. This artistic detailing provides a visual narrative of these sacred texts.

Krishna Mandir holds great religious and cultural significance. It is not only a place of worship but also a testament to the rich architectural heritage of Nepal. The temple has withstood several earthquakes over the centuries, including severe damage in 2015, but has been carefully restored to preserve its historical and spiritual value.

For the remaining monuments (Dhungey Dhara, Bhimsen Temple, Narayan Temple, Char Narayan Temple, Octagonal Chyasing Deval, and Vishwanath Temple), I do not have enough reliable information from the provided search results to generate authentic content.

## Dhunge Dhara

Dhunge dhara, also known as hiti, is a traditional stone water spout system found in Nepal, particularly in the Kathmandu Valley. These intricately carved stone fountains have been an integral part of Nepalese culture and daily life for centuries.

The history of dhunge dharas dates back to the Licchavi Kingdom (400-750 AD), with the oldest known working example, Manga Hiti in Patan, built in 570 AD[2][8]. These water spouts are typically adorned with carvings of mythical creatures, most commonly the makara, a hybrid creature with features from various animals.

Dhunge dharas are fed by an elaborate network of underground water channels, often sourcing water from mountain streams or aquifers[8]. The system includes sophisticated filtration methods using materials like gravel, sand, and charcoal[2]. Despite the introduction of modern water systems, many Nepalese still rely on dhunge dharas for their daily water needs, especially in times of water shortages.

## Bhimsen Temple

Bhimsen Temple is a significant religious structure found in various locations across Nepal, dedicated to Bhimsen, one of the five Pandava brothers from the Mahabharata epic. In Nepalese culture, particularly among the Newari people, Bhimsen is revered as the god of trade and commerce.

One notable Bhimsen Temple is located in Patan Durbar Square. This three-storied temple, built in the 18th century by King Srinivasa Malla, features distinctive architecture and intricate wood carvings[9]. The temple's exterior is adorned with erotic carvings, a common feature in many Nepalese temples.

Another prominent Bhimsen Temple can be found in Pokhara. This 200-year-old structure is considered one of the oldest temples in the city and exemplifies the pagoda style of architecture[11]. The temple's walls are decorated with intricate carvings depicting Bhimsen's legendary strength, such as crushing an elephant with his knee or lifting a horse.

## Narayan Temple

Narayan Temple, also known as Vishnu Temple, is dedicated to Lord Vishnu (Narayan) and can be found in various locations throughout Nepal. One significant example is the Changu Narayan Temple, a UNESCO World Heritage Site located east of Kathmandu.

Changu Narayan Temple is renowned for its rich wood and stone carvings, showcasing intricate artwork dating from the 5th to 12th centuries. The temple complex features a two-tiered pagoda structure with a gilded copper roof and pinnacle. The courtyard contains several smaller shrines and idols, including a beautiful bas-relief of Vishnu mounting Garuda from the 12th century.

Another notable Narayan Temple is the Vishnughat Temple in Bode, Madhyapur Thimi Municipality. While less ornate than some other temples, it holds significant historical and cultural value. The temple's name, "Vishnughat," suggests a possible connection to an ancient riverside location, though the area currently shows no signs of a nearby river.

These temples not only serve as important religious sites but also stand as testaments to Nepal's rich architectural heritage and artistic traditions.

## Char Narayan Temple

Char Narayan Temple, also known as Pyamha Narandya or Jagat Narayan, is one of the oldest and most significant temples in Patan's Durbar Square, Nepal. Built in 1566, it was dedicated to Lord Narayan, another name for Vishnu[3]. The temple is renowned for its intricate wood carvings and stunning architecture, showcasing the rich artistic heritage of the Newar community.

Unfortunately, the Char Narayan Temple was completely leveled by the devastating earthquake in April 2015[3]. However, through extensive restoration efforts, the temple was fully reconstructed and reopened to the public in January 2020[3]. The reconstruction process incorporated modern seismic reinforcement techniques, including enhanced timber joints, steel reinforcement, and concealed beams, while maintaining its historical authenticity.

The temple serves as both a place of worship and a popular tourist attraction. During religious festivals, it becomes a hub of activity, with colorful processions and ceremonies that bring the community together.

## Octagonal Chyasing Deval

The Chyasing Deval, also known as Chyasim Deval Krishna Temple or Chassi Deval Krishna temple, is a unique octagonal temple located in Patan Durbar Square, Lalitpur, Nepal. Built between 1685 and 1705, it is believed to have been constructed by Yogamati, the daughter of King Yog Narendra.

This temple stands out due to its distinctive architecture:

- It features an octagonal design, with "Chyasim" meaning "eight-sided" in the local language[4].
- The temple is built in the Shikhara style, which is more commonly found in North India.
- It stands alongside other notable structures in Patan Durbar Square, such as the four-story pagoda-style temple of Degu Tale or Degutale.

The Chyasing Deval Krishna Temple showcases the diverse architectural influences in Nepal's religious structures and serves as an important landmark in the UNESCO World Heritage Site of Patan Durbar Square.

## Vishwanath Temple

The Vishwanath Temple is located in Patan, Nepal. While specific details about this temple are limited in the provided search results, it is known to be one of the many significant religious structures in the Patan area.

Patan, also known as Lalitpur, is renowned for its rich architectural heritage and numerous temples. The city's Durbar Square alone contains 55 major temples and 136 bahals or courtyards, many dating back to the tenth century[4]. These structures showcase traditional Newari architecture, often featuring pagoda-style designs.

Like many other temples in the area, the Vishwanath Temple likely plays a role in the local Hindu religious practices and contributes to the cultural landscape of Patan. However, without more specific information, it's not possible to provide detailed descriptions of its architecture or historical significance.

"""

# Create DataFrame
df = create_dataframe(text)

# Save to CSV
df.to_csv('monuments.csv', index=False)

# Display the first few rows
print(df.head())