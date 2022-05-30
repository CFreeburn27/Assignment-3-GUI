# https://www.tensorflow.org/install/pip#windows
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image


class GenreModel:
    class_names = ['Arts & Photography', 'Biographies & Memoirs', 'Business & Money', 'Calendars',
                   "Children's Books",
                   'Comics & Graphic Novels', 'Computers & Technology', 'Cookbooks, Food & Wine',
                   'Crafts, Hobbies & Home', 'Christian Books & Bibles', 'Engineering & Transportation',
                   'Health, Fitness & Dieting', 'History', 'Humor & Entertainment', 'Law', 'Literature & Fiction',
                   'Medical Books', 'Mystery, Thriller & Suspense', 'Parenting & Relationships',
                   'Politics & Social Sciences', 'Reference', 'Religion & Spirituality', 'Romance',
                   'Science & Math',
                   'Science Fiction & Fantasy', 'Self-Help', 'Sports & Outdoors', 'Teen & Young Adult',
                   'Test Preparation', 'Travel']

    def __init__(self, model_path='inception_resnet_genre_model-v2.h5'):
        self.genre_model = tf.keras.models.load_model(model_path)

    def predict_genre(self, img_path):
        """

        Args:
            img_path: path of image to make prediction on

        Returns:
            Genre prediction and confidence/probability

        """

        # Load and preprocess image
        img = image.load_img(img_path, target_size=(224, 224))

        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)

        # Predict genre
        predictions = self.genre_model.predict(img)
        genre_prediction = self.class_names[np.argmax(predictions)]

        # Get probability/confidence
        prob = np.max(predictions, axis=1)[0]

        return genre_prediction, prob


# if __name__ == '__main__':
    # model = GenreModel()

    # genre, confidence = model.predict_genre('static/why_nations_fail.jpg')
    # print(f'Genre: {genre} --- Confidence: {confidence}')
