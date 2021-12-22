import yaml
from django.conf import settings
from ..models import ChatbotIntent, Sentence

root_path = settings.BASE_DIR
nlu_data_path = '/home/viet/inet/voice/chatbot/data/nlu.yml'


# response_path = '/nlu_inet/domain/yml'


def get_data_yaml(path):
    with open(path) as f:
        data = yaml.safe_load(f)
        return data


def create_intent_yaml(user):
    data = get_data_yaml(nlu_data_path).get('nlu')
    # data_response = get_data_yaml(response_path)
    # for x in data:
    #     if not x.get('intent'):
    #         continue
    #     intent_obj = ChatbotIntent.objects.create(name=x.get('intent'), user_id=user)
    #     sentence_lst = x.get('examples').replace('-', '').strip().split('\n')
    #     res_lst = x.get('response').replace('-', '').strip().split('\n')
    #     [Sentence.objects.create(name=sentence, intent=intent_obj) for sentence in sentence_lst if sentence]
    #     [ChatBotResponse.objects.create(name=res, intent=intent_obj) for res in res_lst if res]

