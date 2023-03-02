import openai
import os
import time


def create_chat(chat_array):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=chat_array,
        temperature=0.8,
        frequency_penalty=0,
        presence_penalty=0.6,
    )
    return response


def verify() -> str:  # API Key验证以及输入保存

    def key_validity_cheak(key):
        if (key[0:3] != 'sk-'):
            return False
        if len(key) != 51:
            return False
        return True

    if not (os.path.isfile('./key.txt')):
        os.system('type nul > key.txt')
    with open('key.txt', 'r+') as F:
        key = F.readline()
        F.seek(0)  # 指针归位到文件开头
        F.truncate()  # 指针以后的全部删除
        if len(key) == 0:
            key = input('未识别到存在的API key，请手动输入API key\n')
        while (True):
            flag = key_validity_cheak(key)
            if not flag:
                key = input('当前API Key无效，请重新输入API Key\n')
            else:
                F.write(key)
                return key


def create_record_filename():
    time_tuple = time.localtime(time.time())
    # current_year = str(time_tuple[0])
    current_month = str(time_tuple[1])
    current_day = str(time_tuple[2]).zfill(2)
    current_hour = str(time_tuple[3]).zfill(2)
    current_minute = str(time_tuple[4]).zfill(2)
    current_second = str(time_tuple[5]).zfill(2)
    filename = '{}月{}日-{}时{}分{}秒.txt'.format(current_month, current_day, current_hour, current_minute,
                                                  current_second)
    return filename


def record_text(new_message, response_message, filename):
    if not (os.path.isdir('./record')):
        os.mkdir('./record')
    out = '{}: {}\n{}: {}\n'.format(new_message['role'], new_message['content'], response_message['role'],
                                    response_message['content'])
    with open('./record/{}'.format(filename), 'a', encoding='utf-8') as F:
        F.write(out)


if __name__ == '__main__':
    openai.api_key = verify()
    mode_setting = input('请给AI一个合适的人设，字数请勿超过150，这将直接影响到后续对话的质量和内容\n例如：你是我的得力AI助手\n')
    messages = [
        {'role': 'system', 'content': mode_setting},
    ]
    filename = create_record_filename()
    while (True):
        human_input = input('user: ')
        new_message = {
            'role': 'user',
            'content': human_input
        }
        messages.append(new_message)
        response = create_chat(chat_array=messages)
        response_message = response['choices'][0]['message']
        messages.append(response_message)
        print('{}: {}'.format(response_message['role'], response_message['content']))
        record_text(new_message, response_message, filename)
