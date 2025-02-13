class ModelListDTO:
    def __init__(self, models=[]):
        self.list = [
            {"name": model["name"], "size": f"{round(model["size"] / (10**9), 2)} GB"}
            for model in models["models"]
        ]

    def __iter__(self):
        return iter(self.list)

    def __len__(self):
        return len(self.list)

    def __getitem__(self, index):
        return self.list[index]
