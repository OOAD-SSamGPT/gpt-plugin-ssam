from open_ai_api import GptGenerator
import re

# GptGenerator을 상속받은 질문 생성 프로그램
# 함수 1. follow_questions(txt, k) : txt와 k를 파라미터로 받아 txt와 관련된 질문 k개를 리스트로 리턴한다.
# 함수 2. what_is_question(txt) : txt와 같은 답변을 얻으려면 무슨 질문을 해야하는지 물어보고 답변을 스트링으로 리턴한다.

class Q_generator_by_GPT(GptGenerator):
    def __init__(self):
        super().__init__()

    def follow_questions(self, txt, k = 5) -> list:
        print(txt)
        base = " 이 글과 관련된 질문" + str(k) + "개 한글로 알려줘"
        question = txt + base
        lst = self.generate([question])[0].split("\n")
        res = []
        for q in lst:
            res.append(re.sub(r'^\d+\.', '', q))
        return res
    
    def what_is_question(self, txt):
        base = " 이 답변을 받으려면 무슨 질문을 해야할까?"
        question = txt + base
        res = self.generate([question])
        return res[0]
    

if __name__ == "__main__":
    txt = """
    Analysis  •emphasizesaninvestigationoftheproblemand  requirements,ratherthanasolution.  •Requirementsanalysis(aninvestigationoftherequirements)  •Objectanalysis(aninvestigationofthedomainobjects).  •Design  •emphasizesaconceptualsolutionthatfulfillsthe  requirements,ratherthanitsimplementation.  •Forexample,adescriptionofadatabaseschemaandsoftware  objects
    """
      
    Q = Q_generator_by_GPT()
    res = Q.follow_questions(txt, 3)
    res2 = Q.what_is_question(txt)
    print("관련된 질문 3개 : ")
    for i in res:
        print(i)
    print()

    print("무슨 글에 대한 답변일까?")    
    print(res2)