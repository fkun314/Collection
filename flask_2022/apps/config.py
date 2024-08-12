from pathlib import Path

basedir = Path(__file__).parent.parent

# BaseConfigクラスを作る
class BaseConfig:
    SECRET_KEY = "fkdaptjaoiuadk9fdsljge9ht"
    WTF_CSRF_SECRET_KEY = "nidsahrja9gjajszhf9waehtruwaeit39w"
    # 画像アップロード先にapps/imagesを指定する
    UPLOAD_IMG_FOLDER = str(Path(basedir, "apps", "images"))
    UPLOAD_IMG_PREDICTED_FOLDER = str(Path(basedir, "apps", "images", "predicted"))
    UPLOAD_IMG_ANGLE_FOLDER = str(Path(basedir, "apps", "images", "location"))
    UPLOAD_MOVIE_FOLDER = str(Path(basedir, "apps", "movies"))
    UPLOAD_MOVIE_PREDICTED_FOLDER = str(Path(basedir, "apps", "movies", "predicted"))
    # 物体検知に利用するラベル
    LABELS = [
        "unlabeled",
        "person",
        "bicycle",
        "car",
        "motorcycle",
        "airplane",
        "bus",
        "train",
        "truck",
        "boat",
        "traffic light",
        "fire hydrant",
        "street sign",
        "stop sign",
        "parking meter",
        "bench",
        "bird",
        "cat",
        "dog",
        "horse",
        "sheep",
        "cow",
        "elephant",
        "bear",
        "zebra",
        "giraffe",
        "hat",
        "backpack",
        "umbrella",
        "shoe",
        "eye glasses",
        "handbag",
        "tie",
        "suitcase",
        "frisbee",
        "skis",
        "snowboard",
        "sports ball",
        "kite",
        "baseball bat",
        "baseball glove",
        "skateboard",
        "surfboard",
        "tennis racket",
        "bottle",
        "plate",
        "wine glass",
        "cup",
        "fork",
        "knife",
        "spoon",
        "bowl",
        "banana",
        "apple",
        "sandwich",
        "orange",
        "broccoli",
        "carrot",
        "hot dog",
        "pizza",
        "donut",
        "cake",
        "chair",
        "couch",
        "potted plant",
        "bed",
        "mirror",
        "dining table",
        "window",
        "desk",
        "toilet",
        "door",
        "tv",
        "laptop",
        "mouse",
        "remote",
        "keyboard",
        "cell phone",
        "microwave",
        "oven",
        "toaster",
        "sink",
        "refrigerator",
        "blender",
        "book",
        "clock",
        "vase",
        "scissors",
        "teddy bear",
        "hair drier",
        "toothbrush",
    ]


# BaseConfigクラスを継承してLocalConfigクラスを作成する
class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

# BaseConfigクラスを継承してTestingConfigクラスを作成する
class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

# Config辞書にマッピングする
config = {
    "testing": TestingConfig,
    "local": LocalConfig,
}