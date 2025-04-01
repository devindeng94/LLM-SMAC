# call_llm.py
import config
import logging
import pdb
from logging.handlers import RotatingFileHandler
from openai import OpenAI
from configs.llm_api_config import LLMAPIConfig

def setup_logger(name, log_file, level=logging.INFO):

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


model_info = LLMAPIConfig.get_model_dict()
main_logger = setup_logger('main_logger', '{}#{}#{}#{}.log'.format(model_info['planner'], model_info['coder'], model_info['summarizer'], config.map_name), level=logging.DEBUG)

class BaseChatbot:
    def __init__(self, task):
        model_config = LLMAPIConfig.get_task_model(task)
        if model_config is None:
            raise ValueError(f"No model configured for task: {task}")

        self.client = OpenAI(
            api_key=model_config.api_key,
            base_url=model_config.base_url
        )
        main_logger.debug(f"{task.capitalize()} API client created")

        self.model = LLMAPIConfig.TASK_MODELS[task]
        main_logger.debug(f"Model set to: {self.model}")
        self.conversation_history = []

        self.log_system=False

    def query(self, system_prompt, user_input):
        raise NotImplementedError("Subclasses must implement this method")

    def clear_history(self):
        self.conversation_history = []

class TextChatbot(BaseChatbot):

    

    def query(self, system_prompt, user_input, maintain_history=True):
        try:
            messages = [{"role": "system", "content": system_prompt}]

            if maintain_history:
                messages.extend(self.conversation_history)

            messages.append({"role": "user", "content": user_input})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False
            )
            assistant_response = response.choices[0].message.content

            if maintain_history:
                self.conversation_history.append({"role": "user", "content": user_input})
                self.conversation_history.append({"role": "assistant", "content": assistant_response})

            main_logger.debug(f"Querying model: {self.model}")
            if self.log_system==False:
                main_logger.debug(system_prompt)
                self.log_system = True
            main_logger.debug(user_input)
            main_logger.debug("Query successful")
            main_logger.debug(assistant_response)

            return assistant_response
        except Exception as e:
            main_logger.error(f"An error occurred: {e}", exc_info=True)
            return f"An error occurred: {str(e)}"
