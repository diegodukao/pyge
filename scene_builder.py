#! /usr/bin/python

import xml.dom.minidom
import pygame

class SceneBuilder:
    
    def __init__(self, xml_filename="teste.pyge"):
        self.scene_xml = xml.dom.minidom.parse(xml_filename)
        
    def create_screen(self):
        width, height = self.get_screen_size_from_xml()
        screen = pygame.display.set_mode((int(width), int(height)))
        
        return screen
        
    def get_screen_size_from_xml(self):
        scene_node = self.scene_xml.getElementsByTagName("scene")
        screen_width = scene_node[0].getAttribute("width")
        screen_height = scene_node[0].getAttribute("height")
        
        return screen_width, screen_height
        
    def create_bg(self):
        bg_path = self.get_bg_path_from_xml()
        bg = pygame.image.load(bg_path)
        
        return bg, bg.get_rect
        
        
    def get_bg_path_from_xml(self):
        bg_node = self.scene_xml.getElementsByTagName("background")
        bg_path = bg_node[0].childNodes[0].nodeValue
        
        return bg_path
        
    def get_sprites(self):
        sprites_nodes = self.scene_xml.getElementsByTagName("sprite")
        sprites_dict = {}
        for sprite_node in sprites_nodes:
            x = int(sprite_node.getAttribute("x"))
            y = int(sprite_node.getAttribute("y"))
            image_path = sprite_node.getAttribute("filename")
            sprite_image = pygame.image.load(image_path)
            sprite_name = sprite_node.childNodes[0].nodeValue
            
            sprite = SimpleSprite((x, y), sprite_image)
            sprites_dict[sprite_name] = sprite
        
        return sprites_dict
            
        
        
class SimpleSprite(pygame.sprite.Sprite):
    def __init__(self, position, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = position
