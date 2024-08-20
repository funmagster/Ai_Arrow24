class Registry:
    _shared_state = {}

    @classmethod
    def set(cls, key, value):
        cls._shared_state[key] = value

    @classmethod
    def get(cls, key):
        return cls._shared_state.get(key)

    @classmethod
    def set_all(cls, items, value_processor=lambda x: x):
        for key, value in items.items():
            cls.set(key, value_processor(value))
