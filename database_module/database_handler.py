from database_module.models import models


class DatabaseHandler:
    @staticmethod
    def save_request(user_id, command):
        # Сохранение запроса в базу данных
        models.History.create(user_id=user_id, command=command)

    @staticmethod
    def get_last_history_records(limit):
        return models.History.select().order_by(models.History.id.desc()).limit(limit)
