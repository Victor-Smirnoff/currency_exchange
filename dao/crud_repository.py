"""
Здесь описан класс для выполнения основных действий над базой данных:
позволяют создавать (C - create), читать (R - read), редактировать (U - update), удаление (D - delete)
"""


class CrudRepository:
    """
    Класс для выполнения основных действий над базой данных
    Во всех методах вызываем raise NotImplementedError
    Чтобы в дочерних классах переопределить эти методы
    """
    def find_by_id(self, id):
        """
        Метод для нахождения данных по id
        Это метод Read	SELECT
        :param id: id
        :return: объект с данными из БД
        """
        raise NotImplementedError

    def find_all(self):
        """
        Метод для нахождения всех данных записей в БД
        Это метод Read	SELECT
        :return: список с объектами с данными из БД
        """
        raise NotImplementedError

    def save(self):
        """
        Метод для сохранения (добавления) данных в БД
        Это метод Create	INSERT
        :return: объект с данными из БД (данные которые были добавлены в БД)
        """
        raise NotImplementedError

    def update(self):
        """
        Метод для обновления (изменения) данных в БД
        Это метод Update	UPDATE
        :return: объект с данными из БД (данные которые были изменены в БД)
        """
        raise NotImplementedError

    def delete(self):
        """
        Метод для удаления данных в БД
        Это метод Delete	DELETE
        :return: объект с данными из БД (данные которые были удалены из БД)
        """
        raise NotImplementedError