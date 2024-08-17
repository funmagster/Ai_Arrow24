class Registry:
    _shared_state = {}

    @classmethod
    def set(cls, key, value):
        cls._shared_state[key] = value

    @classmethod
    def get(cls, key):
        return cls._shared_state.get(key)
