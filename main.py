import misc
import openai
import tgbot
import datetime as dt
import os
import threading

openai.api_key = misc.chat_gpt_api2
messages = []
histories = {}


def logwriter(logs):

    print("90% - user data logging, 2nd step")
    with open(os.path.join('[your directory]'), 'r') as log_file:
        log_read = log_file.read()
    if log_read.find(logs) != -1:
        pass
    else:
        with open(os.path.join('[your directory]'), 'a+') as log_file:
            log_file.write('\n' + logs)
            print(logs)


def user_data_logwriter(username, message, chat_response, user_id):

    date = dt.datetime.now().strftime('%d_%m')
    filename = '[your directory]/user_data/'+str(date)+'_'+str(username)+'.txt'
    with open(filename, 'a+') as log_open1:
        log_open1.write('[' + str(username) + ']' + ': '+ str(message) + '\n')
        log_open1.write('[ChatGPT]' + ': ' + chat_response.strip() + '\n\n')

def chatgpt(firstname, username, user_id, message):
    try:
        chat_response = 0
        print("50% - answer build up")
        if user_id not in histories:
            histories[user_id] = []
        data = f'{username} : {firstname} : {user_id}'
        histories[user_id].append({"role": "user", "content": message})
        history = histories[user_id]  # берем только последние 20 сообщений
        relevant_history = [elem["content"] for elem in history if elem["role"] in ["user", "assistant"] and elem["content"].strip()]
        text = "\n".join(relevant_history[-3:])  # берем только последние 3 сообщения
        prompt = f"{username}: {text}\nAI:"

        completion = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=prompt, 
            max_tokens=2000, 
            temperature=0.7
        )


        print("60% - model generated")
        chat_response = completion.choices[0].text
        histories[user_id].append({"role": "assistant", "content": chat_response})
        print("70% - answer generated")
        print(message)
        print(chat_response)
        try:
            def run_user_data_logwriter():
                user_data_logwriter(username, message, chat_response, user_id)

            def run_logwriter():
                logwriter(data)
            user_data_thread = threading.Thread(target=run_user_data_logwriter)
            log_thread = threading.Thread(target=run_logwriter)
            user_data_thread.start()
            log_thread.start()
            user_data_thread.join()
            log_thread.join()

        except UnicodeEncodeError:
            pass

        print("100% - answer has been sent")
        return chat_response

    except Exception as e:
        histories[user_id] = []
        return('Произошла ошибка. История будет стерта, попробуйте написать запрос заново. ' + str(e))


def main():
    print("20% - bot build up")
    tgbot.tgbot()


if __name__ == '__main__':
    print("10% - main start")
    main()
