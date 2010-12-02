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
        
