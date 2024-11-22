import json

MAX_LEN = 1600

# Transform conversation-based style to document-based style
def conv_to_doc(line):
  idx = line.index(':')
  speaker = line[:idx]
  content = line[idx+1:].strip()

  return f"{speaker} said '{content}'"

# Transform conversation dataset to Python lists(conversation-based and document-based)
dataset_path = 'human_chat.txt'

with open(dataset_path, 'r', encoding='utf-8') as file:
  lines = file.readlines()
  lines = [line.replace('Human 1', 'Tom').replace('Human 2', 'Jerry').strip() for line in lines]

  conversations = []
  documents = []

  for line in lines:
    if not line:
      continue

    if 'a' <= line[-1].lower() <= 'z':
      line += '.'

    if line.lower() == 'tom: hi!' or line.lower() == 'tom: hi.':
      conversations.append(line)
      documents.append(conv_to_doc(line))

    elif len(conversations[-1]) < MAX_LEN:
      conversations[-1] += ' ' + line
      documents[-1] += ' ' + conv_to_doc(line)

# for idx, conv in enumerate(conversations):
#   print(f'대화 내용 {idx}: {conv}\n')

# Transform QA dataset(GPT-generated) to Python lists
qa_path = 'qa.txt'
questions, answers = [], []

with open(qa_path, 'r', encoding='utf-8') as file:
  lines = file.readlines()

  for line in lines:
    idx = line.find(':')
    
    if line[:idx] == 'question':
      questions.append(line[idx+1:].strip())
    elif line[:idx] == 'answer':
      answers.append(line[idx+1:].strip())

# All should be the same
print(f'Conversations: {len(conversations)}')
print(f'Documents: {len(documents)}')
print(f'Questions: {len(questions)}')
print(f'Answers: {len(answers)}')

# Generating conversation-based QA dataset
json_conv = {
  'items': [
    {'conv': conv, 'question': questions[idx], 'answer': answers[idx]} for idx, conv in enumerate(conversations)
  ]
}

path_json_conv = 'conversation_qa.json'

with open(path_json_conv, "w", encoding="utf-8") as file:
  json.dump(json_conv, file, ensure_ascii=False, indent=2)

# Generating document-based QA dataset
json_doc = {
  'items': [
    {'doc': doc, 'question': questions[idx], 'answer': answers[idx]} for idx, doc in enumerate(documents)
  ]
}

path_json_doc = 'document_qa.json'

with open(path_json_doc, "w", encoding="utf-8") as file:
  json.dump(json_doc, file, ensure_ascii=False, indent=2)
