from enum import Enum
import json
import requests
import os
import json

class EntityType(Enum):
    OTHER = 0
    PERSON = 1
    LOCATION = 2
    CONCEPT = 3
    

def make_directory(path):
    """
    Create a directory at the specified path if it doesn't already exist.

    Args:
        path (str): The path of the directory to be created.

    Returns:
        None
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"`{path}` created.")
    else:
        print(f"`{path}` already exists.")


def fetch_page(url, params={}):
    """
    Fetches the content of a web page.

    Args:
        url (str): The URL of the web page to fetch.
        params (dict, optional): The query parameters to include in the request. Defaults to an empty dictionary.

    Returns:
        str: The content of the web page.

    """
    resp = requests.get(url, params=params)
    resp.encoding = 'utf-8'
    return resp.text


## I/O operations
def open_file(path, file_type):
    """
    Opens a file and returns its contents.

    Args:
        path (str): The path to the file.
        file_type (str): The type of the file. Supported types are "json" and any other type.

    Returns:
        The contents of the file as a string if the file type is not "json", or
        the contents of the file as a dictionary if the file type is "json".
    """
    with open(path, 'r', encoding='utf-8') as file:
        if file_type == "json":
            return json.load(file)
        else:
            return file.read()

def save_json(path, data):
    """
    Save data as JSON to the specified file path.

    Args:
        path (str): The file path where the JSON data will be saved.
        data (dict): The data to be saved as JSON.

    Returns:
        None
    """
    with open(path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f"file saved")
    

def viz_data(df, plt):
    """
    Visualizes data from a DataFrame.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the data to be visualized.

    Returns:
    None
    """
    # import matplotlib.pyplot as plt
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Plot 1: Frequency of Classes
    df["label"].value_counts(ascending=True).plot.barh(ax=axs[0])
    axs[0].set_title("Frequency of Classes")

    # Plot 2: Words Per Text Boxplot
    df["Words Per text"] = df["text"].str.split().apply(len)
    df.boxplot("Words Per text", by="label", grid=False, showfliers=False,
                        color="black", ax=axs[1])
    axs[1].set_title("Words Per Text")

    # Adjust layout and remove xlabel from the boxplot
    plt.subplots_adjust(wspace=0.5)
    axs[1].set_xlabel("")

    # Show the plot
    plt.tight_layout()
    plt.show()
