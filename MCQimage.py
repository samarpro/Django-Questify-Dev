from docx import Document


docx = Document("C:\\Users\\LENOVO\\OneDrive\\Desktop\\mcqImages.docx")

# defining the dict for namespaces 
CustomNsmap = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
}

# assuming this paragraphs to be options only
para_list = [0,5,10,15,20,25,30,35,40,45,50,55,60]
for para_num in para_list:
    image_object_blip = docx.paragraphs[para_list].runs[-1]._element.findall(".//a:blip",namespace=CustomNsmap)
    for img_blip in  image_object_blip:
            # getting relationship id
        rId = img_blip.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        if rId:
            image_part= docx.part.rels[rId].target_part
            image_part_binary = image_part.blob


