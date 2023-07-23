from docx import Document
from random import sample

def WordFileHandler(FilePath,Quesno):
    ANS_LIST = []
    PARSE_DICT ={}
    doc = Document(FilePath)
    paraObj = doc.paragraphs
    noPara = len(paraObj)
    actNoPara = (noPara//5)*5
    randomList = sample(range(0,actNoPara,5),Quesno)
    for num in randomList:
        paraText = paraObj[num].text
        optionRandomList=sample(range(1,5),4)
        OPTION_LIST = []
        for opNum in optionRandomList:
            optionObject = paraObj[num+opNum]
            if optionObject.runs[0].bold == True:
                ANS_LIST.append(len(OPTION_LIST))
            OPTION_LIST.append(optionObject.text)
        
        PARSE_DICT[paraText] = OPTION_LIST
    PARSE_DICT["Answers"] = ANS_LIST

    return PARSE_DICT
    
    
WordFileHandler('E:/Django-Questify-Dev/media/WordFiles/MCQ.docx',40)