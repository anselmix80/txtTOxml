import xml.etree.ElementTree as ET
import base64
import os


def extract_from_xml(xml_file, output_dir):
  """
  Extracts data from an XML file containing a base64 encoded PDF and creates a directory with the extracted content.

  Args:
      xml_file (str): Path to the XML file.
      output_dir (str): Path to the directory where the extracted files will be saved.
  """

  os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

  tree = ET.parse(xml_file)
  root = tree.getroot()

  # Extract key-value pairs
  data_dict = {}
  for child in root:
    if child.tag != "pdf_content":
      data_dict[child.tag] = child.text

  # Write key-value pairs to a TXT file
  with open(os.path.join(output_dir, "data.txt"), "w") as f:
    for key, value in data_dict.items():
      f.write(f"{key}: {value}\n")

  # Extract and decode base64 encoded PDF
  pdf_base64 = root.find("pdf_content").text
  pdf_data = base64.b64decode(pdf_base64)

  # Write decoded PDF data to a new file
  with open(os.path.join(output_dir, data_dict["file"]), "wb") as f:
    f.write(pdf_data)


# Example usage
xml_file = "output.xml"  # Assuming the output from the previous program
output_dir = "extracted_data"
extract_from_xml(xml_file, output_dir)
