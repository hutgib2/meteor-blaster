from os.path import join
from os import walk
from game.settings import pygame

def folder_importer(*path):
    surfs = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            surfs[file_name.split('.')[0]] = pygame.image.load(full_path).convert_alpha()
    return surfs

def image_importer(*path, scale_factor=1):
    image = pygame.image.load(join(*path)).convert_alpha()
    width, height = image.get_size()
    surf = pygame.transform.smoothscale(image, (width * scale_factor, height * scale_factor))
    return surf

def folder_importer_list(*path, scale_factor=1):
    surf_list = []
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
            full_path = join(folder_path, file_name)
            image = pygame.image.load(full_path).convert_alpha()
            width, height = image.get_size()
            surf = pygame.transform.smoothscale(image, (width * scale_factor, height * scale_factor))
            surf_list.append(surf)
    return surf_list

def audio_importer(*path):
    audio_dict = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            audio_dict[file_name.split('.')[0]] = pygame.mixer.Sound(join(folder_path, file_name))
    return audio_dict
