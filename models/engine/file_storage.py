#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""

import json
import os
import models


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage, filtered by class if provided"""
        if cls is None:
            return self.__objects
        return {key: obj for key, obj in self.__objects.items() if isinstance(obj, cls)}

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        temp = {key: val.to_dict() for key, val in self.__objects.items() if val is not None}
        try:
            with open(self.__file_path, 'w') as f:
                json.dump(temp, f)
        except Exception as e:
            print(f"Error saving to {self.__file_path}: {e}")

    def reload(self):
        """Loads storage dictionary from file."""
        try:
            if os.path.exists(self.__file_path):
                with open(self.__file_path, 'r') as f:
                    temp = json.load(f)
                    for key, val in temp.items():
                        cls_name = key.split('.')[0]
                        module = __import__(f"models.{cls_name.lower()}", fromlist=[cls_name])
                        cls = getattr(module, cls_name)
                        obj = cls(**val)
                        self.__objects[key] = obj
        except Exception as e:
            print(f"Failed to reload objects from {self.__file_path}: {e}")

    def delete(self, obj=None):
        """Deletes an object from the storage dictionary"""
        if obj is None:
            return
        key = f"{obj.__class__.__name__}.{obj.id}"
        if key in self.__objects:
            del self.__objects[key]
            self.save()
            
    def close(self):
        """Call the reload() method for deserializing the JSON file to objects."""
        self.reload()
