import requests

# 引用config中的方法
from app.core.config import *
# 引用utils中的方法
from app.utils.connect_openai import *

bot_id = Settings.VoceChat['bot_config']["bot1"]["secret"]

command_help = "!help"
command_context_mode = "!context"
command_single_mode = "!single"
command_clean_msg = "!clean"
command_check_msg = "!check"
command_view_system = "!view"

voce_help = {
    command_help: "调出帮助菜单",
    command_context_mode: "设置为上下文聊天模式，默认为单次聊天模式，运行这个命令可以开启上下文聊天，"
                          "上下文聊天会保存聊天记录，若不想影响后续聊天，请手动清除聊天记录",
    command_single_mode: "设置为单次聊天模式",
    command_clean_msg: "清除与AI的聊天记录",
    command_check_msg: "查看与AI的聊天记录",
    command_view_system: "查看如何为AI赋予一个角色"
}

command_show_server_system = "!show"
command_set_system = "!set+"
command_select_system = "!select+"
command_show_me_system = "!me"
command_clean_me_system = "!unset"

voce_ai_system_help = {
    command_show_server_system: f"通过输入 {command_show_server_system} 可以显示已经存储备用的角色",
    command_show_me_system: f"通过输入 {command_show_me_system} 可以查看我已经设置的角色",
    command_set_system: f"通过输入 {command_set_system}内容 来设置行为,例如:{command_set_system}角色描述(描述可以参考系统预制的格式)",
    command_select_system: f"通过输入 {command_select_system}角色 来选择一个角色(必须是系统有的), 例如：!select+程序员",
    command_clean_me_system: f"通过输入 {command_clean_me_system} 可以清除已经设置的行为，清除聊天记录的时候会同时清除角色"
}

# 隐藏命令
# /admin+角色名+角色描述
command_admin_set_system = "!admin+"

chat_mod_descript = {
    "0": "单聊天模式",
    "1": "上下文模式"
}


class MessageHandler:
    def __init__(self, data):
        self.data = data
        self.user_id = str(self.data.from_uid)
        self.created_at = self.data.created_at
        self.target_gid = self.data.target.gid
        self.msg = self.data.detail.content

    def handle(self):
        # 如果是群发消息，不接收
        if self.is_group_message():
            return

        # 不处理bot的msg
        
        if self.is_bot_message():
            return
        # 功能函数
        # 帮助
        if self.is_help_command():
            return self.send_help()
        # 切换聊天模式
        if self.is_switch_context_mode_command():
            return self.switch_chat_mode("1")
        if self.is_switch_single_chat_mode_command():
            return self.switch_chat_mode("0")
        # 聊天记录操作
        if self.is_clear_chat_history_command():
            return self.clear_chat_history()
        if self.is_view_chat_history_command():
            return self.view_chat_history()
        if self.is_view_server_store_ai_system():
            return self.view_server_store_ai_system()

        # system设置操作
        if self.is_view_ai_system_help():
            return self.send_ai_system_help()
        if self.is_clear_user_ai_system():
            return self.clear_user_ai_system()
        if self.is_set_user_ai_system():
            return self.set_user_ai_system()
        if self.is_view_user_current_ai_system():
            return self.view_user_current_ai_system()
        if self.is_select_server_store_ai_system_to_user():
            return self.select_server_store_ai_system_to_user()

        # 隐藏命令
        if self.is_admin_set_ai_system():
            return self.admin_set_ai_system()

        # 是否命令输入错误
        if self.is_command_wrong():
            return self.command_wrong()

        return self.process_user_message()

    def is_group_message(self):
        return self.target_gid is not None

    def send_msg_to_where(self):
        # 如果gid不是None,返回send_to_group/group_id
        if self.target_gid is not None:
            return f"send_to_group/{self.target_gid}"
        # 如果gid是None,send_to_user/user_id
        return f"send_to_user/{self.user_id}"

    def is_bot_message(self):
        return self.user_id == Settings.VoceChat['bot_config']["bot1"]["bot_id"]

    # 帮助
    def is_help_command(self):
        return self.msg == command_help

    def send_help(self):
        chat_mod_id = self.get_user_current_chat_mode()
        chat_mod_id_text = chat_mod_descript[chat_mod_id]
        help_text = f"|命令|功能|\n|-|-|\n |当前模式|你的模式为:{chat_mod_id_text};|"
        for name, descript in voce_help.items():
            help_text += f"|{name}|{descript}|\n"
        return self.send_to_voce_bot(f"### 功能展示\n{help_text}")

    # 切换模式
    def is_switch_context_mode_command(self):
        return self.msg.startswith(command_context_mode)

    def is_switch_single_chat_mode_command(self):
        return command_single_mode in self.msg[:len(command_context_mode) + 1]

    def switch_chat_mode(self, chat_mod):
        return self.send_to_voce_bot(f"不支持该功能")

    # 聊天记录
    def is_clear_chat_history_command(self):
        return command_clean_msg in self.msg[:len(command_context_mode) + 1]

    def clear_chat_history(self):
        return self.send_to_voce_bot(f"不支持该功能")

    def is_view_chat_history_command(self):
        return command_check_msg in self.msg[:len(command_context_mode) + 1]

    def view_chat_history(self):
        history_msg = self.process_user_history_msg()
        return self.send_to_voce_bot(str(history_msg))

    # AI System 设置
    def is_view_ai_system_help(self):
        return command_view_system in self.msg[:len(command_view_system) + 1]

    def send_ai_system_help(self):
        user_ai_system = "未设置"
        if self.get_user_current_ai_system():
            user_ai_system = self.get_user_current_ai_system()
        help_text = f"|命令|功能|\n|-|-|\n |当前模式|你设置的AI角色:{user_ai_system};|\n"
        for name, descript in voce_ai_system_help.items():
            help_text += f"|{name}|{descript}|\n"
        return self.send_to_voce_bot(f"### AI角色设置帮助\n{help_text}")

    def is_clear_user_ai_system(self):
        return command_clean_me_system in self.msg[:len(command_clean_me_system) + 1]

    def clear_user_ai_system(self):
        return self.send_to_voce_bot(f"不支持该功能")

    def is_set_user_ai_system(self):
        return command_set_system in self.msg[:len(command_set_system) + 1]

    def set_user_ai_system(self):
        return self.send_to_voce_bot(f"不支持该功能")

    def is_view_server_store_ai_system(self):
        return command_show_server_system in self.msg[:len(command_show_server_system) + 1]

    def view_server_store_ai_system(self):
        help_text = f"|角色名称|角色描述|\n|-|-|\n"
        if self.get_server_current_ai_system():
            server_store_ai_system = self.get_server_current_ai_system()
            for i in server_store_ai_system:
                help_text += f"|{i['system_name']}|{i['system_descript']}|\n"
            return self.send_to_voce_bot(f"### 系统预设角色\n{help_text}")
        return self.send_to_voce_bot(f"系统无预设角色")

    # 查看我的角色
    def is_view_user_current_ai_system(self):
        return command_show_me_system in self.msg[:len(command_show_me_system) + 1]

    def view_user_current_ai_system(self):
        user_ai_system = "未设置"
        if self.get_user_current_ai_system():
            user_ai_system = self.get_user_current_ai_system()
        return self.send_to_voce_bot(f"### 当前AI角色设置为\n{user_ai_system}")

    # 选择一个服务器预设的角色
    def is_select_server_store_ai_system_to_user(self):
        return command_select_system in self.msg[:len(command_select_system) + 1]

    def select_server_store_ai_system_to_user(self):
        return self.send_to_voce_bot(f"不支持该功能")
    
    # 隐藏命令,用来给服务器插入一个预设角色
    def is_admin_set_ai_system(self):
        return command_admin_set_system in self.msg[:len(command_admin_set_system) + 1]

    def admin_set_ai_system(self):
        return self.send_to_voce_bot(f"不支持该功能")
    
    # 是否输入错误
    def is_command_wrong(self):
        return r"/" in self.msg.replace("\n", "")[:3]

    def command_wrong(self):
        return self.send_to_voce_bot("命令输入错误,请检查!")

    # 开始处理对话
    def process_user_message(self):
        send_msg = []
        ai_mod = self.get_user_current_ai_system()
        if ai_mod:
            send_msg.insert(0, {'role': 'system', 'content': ai_mod})

        if self.get_user_current_chat_mode() == "1":
            history_msg = self.process_user_history_msg()
            if len(history_msg) > 0:
                send_msg += history_msg
            send_msg.append({'role': "user", 'content': self.msg})
            response = send_msg_to_openai(send_msg)
        else:
            send_msg.append({'role': "user", 'content': self.msg})
            response = send_msg_to_openai(send_msg)

        return self.send_to_voce_bot(response)

    # 功能性函数
    # 获取当前用户的聊天模式
    def get_user_current_chat_mode(self):
        return "0"
        
    # 获取当前用户的ai system角色设置
    def get_user_current_ai_system(self):
        return "不支持"

    # 获取当期服务器中的角色情况
    def get_server_current_ai_system(self):
        return "不支持"

    # 处理历史聊天记录
    def process_user_history_msg(self):
        return ""

    # 向voce_chat_bot回传消息
    def send_to_voce_bot(self, message):
        headers = {'content-type': "text/markdown", 'x-api-key': bot_id}
        url = f"{Settings.VoceChat['url']}/api/bot/{self.send_msg_to_where()}"
        requests.post(url=url, headers=headers, data=message.encode('utf-8'))
