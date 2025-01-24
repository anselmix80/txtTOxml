import xml.etree.ElementTree as ET
import hashlib
import base64

def create_xml_from_txt(txt_file, xml_file):
    """
    Crea un file XML da un file TXT, incorporando il file PDF come base64.

    Args:
        txt_file (str): Percorso del file TXT.
        xml_file (str): Percorso del file XML da creare.
    """

    root = ET.Element("record")

    with open(txt_file, 'r') as f:
        for line in f:
            key, value = line.strip().split(': ')
            element = ET.SubElement(root, key)
            element.text = value

    # Calcolo dell'hash SHA del file PDF
    with open(root.find('file').text, 'rb') as f:
        pdf_data = f.read()
        hash_value = hashlib.sha256(pdf_data).hexdigest()
    root.find('hash').text = hash_value

    # Codifica del PDF in base64
    pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
    pdf_element = ET.SubElement(root, "pdf_content")
    pdf_element.text = pdf_base64

    tree = ET.ElementTree(root)
    tree.write(xml_file, encoding="utf-8", xml_declaration=True)

# Esempio di utilizzo
txt_file = "input.txt"
xml_file = "output.xml"
create_xml_from_txt(txt_file, xml_file)
