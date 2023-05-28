import openai

#Chat GPT API를 이용한 응답 프로그램
#함수1. generate(list) : 질문들의 리스트를 파라미터로 담아 각 질문들에대한 답변을 리스트로 리턴한다. 받은 답변들은 self.data에 저장된다.
#함수2. save_to_local(file_path) : self.data를 지정한 로컬 파일에 저장한다.

class GptGenerator():
    def __init__(self):
        openai.api_key = os.environ.get('API_KEY') # API KEY
        self.model_engine = "gpt-3.5-turbo"
        self.data = []
        
    def generate(self, questions, option=[]): #params : list , list  / output : list
        if len(questions) <= 0:
            print("There are no questions")
            return
        answer_list = []
        print("Start generating ...")
        for q in questions:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": q}
                ]
            )
            answer_list.append(completion.choices[0].message.content)
        print("Done!!")
        self.data.extend(answer_list)

        return answer_list
        
    def save_to_local(self, file_path="./output_generator.txt"):
        cnt = 0
        with open(file_path, 'a') as f:
            for item in self.data:
                if len(item) > 0:
                    f.write("%s\n" % item)
                    cnt += 1
                    print(f"saved {cnt} answer")
        print(f"successfully finished to save {cnt} items to {file_path} !!")

if __name__ == "__main__":
  questions = ["내 이름은 김혜성이야"]
  questions1 = ["내 이름이 뭐야?"]
  g = GptGenerator()
  g.generate(questions)
  print(g.data[0])
 
  #g.save_to_local()

