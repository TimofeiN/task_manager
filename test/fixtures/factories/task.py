from factory import Factory, Faker


class TaskFactory(Factory):
    class Meta:
        model = dict

    title = Faker("text", max_nb_chars=20)
