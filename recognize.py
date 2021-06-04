from imageai.Classification.Custom import CustomImageClassification
import os


def recognizing(image):

    image.download('user_photo.jpg')
    model = "model_ex-010_acc-0.836387.h5"

    execution_path = os.getcwd()

    prediction = CustomImageClassification()
    prediction.setModelTypeAsInceptionV3()
    prediction.setModelPath(os.path.join(execution_path, model))
    prediction.setJsonPath(os.path.join(execution_path, "model_class.json"))
    prediction.loadModel(num_objects=5)

    return prediction.classifyImage('user_photo.jpg', result_count=2)
