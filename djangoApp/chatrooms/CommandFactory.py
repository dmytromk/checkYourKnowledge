from .Command import *

class CommandFactory:
    @staticmethod
    def create_command(consumer, command_name, data):
        if command_name == 'fetch':
            return FetchCommand(consumer, data)
        elif command_name == 'new_message':
            return NewMessageCommand(consumer, data)
        elif command_name == 'new_task':
            return NewTaskCommand(consumer, data)
        elif command_name == 'check_answer':
            return CheckAnswearCommand(consumer, data)
        elif command_name == 'get_task':
            return GetTask(consumer, data)
        elif command_name == 'fetch_task':
            return FetchTasks(consumer, data)
        elif command_name == 'generate_invite':
            return GenerateInviteLink(consumer, data)

        # Handle unknown commands or return a default command
        return None