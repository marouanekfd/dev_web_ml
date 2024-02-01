import os
import pickle
import uuid
from flask import jsonify


def generate_token():
    # Générer un UUID de version 4
    token = uuid.uuid4()
    return str(token)


def save_model(model, dataset_name, token, additional_info=None):

    model_info = {
        'model': model,
        'dataset_name': dataset_name,
        'token': token,
        'additional_info': additional_info
    }

    # Create 'saved_models' directory if it doesn't exist
    if not os.path.exists('saved_models'):
        os.makedirs('saved_models')

    filename = os.path.join('saved_models', f'model_{token}.pkl')
    with open(filename, 'wb') as file:
        pickle.dump(model_info, file)

    print(f'Model saved to {filename}')


def load_model(token):
    """
    Load a machine learning model from a pickle file in the 'saved_models' directory,
    using the 4-digit code.

    :param code: A 4-digit code associated with the model.
    :return: The loaded model and its metadata.
    """
    filename = os.path.join('saved_models', f'model_{token}.pkl')

    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            model_info = pickle.load(file)
        return jsonify({'model_info':model_info})
    else:
        print(f"No model found with code {token}.")
        return None


def delete_model(token):
    # Assumer que le token est le même que le code utilisé pour enregistrer le modèle
    filename = os.path.join('saved_models', f'model_{token}.pkl')

    # Vérifier si le fichier existe
    if os.path.exists(filename):
        os.remove(filename)
        print(f'Model file {filename} has been deleted.')
        return jsonify({'token':token})
    else:
        print(f'No model file found for the token: {token}')
        return jsonify({'token':token})