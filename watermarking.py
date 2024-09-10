from PIL import Image,ImageOps

class Watermarking():
    def __init__(self):    
        pass

    def get_watermark_for_blending(self, watermark, opacity):
        watermark = watermark.convert("RGBA")
        red, green, blue, alpha = watermark.split()
    
        #Create a mask with lowered opacity
        opacity_img = Image.new("RGBA", (watermark.size[0], watermark.size[1]), color="#ffffff")
        alpha = ImageOps.invert(alpha).convert("RGBA")
        alpha_blend = Image.blend(alpha,opacity_img, 1-opacity)
        mask = alpha_blend
        mask =  ImageOps.invert(alpha_blend.convert("L"))
        return mask

    
    def resize_watermark(self, watermark_src,watermark_width_percentage,image_width):
        """Resizes the watermark to percentage of the image_width and maintains the aspect ratio"""
        watermark_src_ratio =  watermark_src.size[1]/watermark_src.size[0]
        watermark_width = int(watermark_width_percentage * image_width)
        watermark_new_height = int( watermark_width* watermark_src_ratio)
        return watermark_src.resize(size=(watermark_width, watermark_new_height))  


    def get_watermark_position(self, position_location, image_size, watermark_size):
        """Gets the position of the watermark start draw location based on the position location:
            'br' : bottom right
            'tr' : top right
            'bl' : bottom left
            'bc' : bottom center
            'tc' : top center
            default : top left
        """
        image_width = image_size[0]
        image_height = image_size[1]
        watermark_width = watermark_size[0]
        watermark_height = watermark_size[1]

        position = (0,0)
        if position_location == "br":
            position = (image_width - watermark_width, image_height - watermark_height)
        elif position_location == "tr":
                position = ( image_width - watermark_width, 0)
        elif position_location == "bl":
                position = (0, image_height - watermark_height)
        elif position_location == "bc":
                image_center = int(image_width / 2)
                offset_watermark = int(watermark_width / 2)
                position = (image_center - offset_watermark,  image_height - watermark_height)
        elif position_location == "tc":
                image_center = int(image_width / 2)
                offset_watermark = int(watermark_width / 2)
                position = (image_center - offset_watermark, 0)

        return position

    def expand_canvas(self, watermark, position, image_size):
        watermark_oncanvas = Image.new("RGBA", image_size, color=(0,0,0,0))
        watermark_oncanvas.paste(im = watermark, box=position)  
        return watermark_oncanvas

    def merge_by_percentage(self,image, watermark_src, watermark_width_percentage, placement, opacity):
        """Processes the watermark to be resized, placed, have its opacity faded and composited with the main image:
            1. Resize the watermark based on a percentage of the size of the main image
            2. Calculate the position to place the watermark
            3. Place the watermark on a canvas the same of the main image based on step 2 calcualtion
            4. Generate a mask of the watermark with the specified opacity
            5. Composite the two images together.  
        """ 
        watermark_resized = self.resize_watermark(watermark_src, watermark_width_percentage, image.size[0])
        position = self.get_watermark_position(placement, image.size, watermark_resized.size)
        watermark_expanded_canvas = self.expand_canvas(watermark_resized, position, image.size)
        watermark_mask = self.get_watermark_for_blending(watermark_expanded_canvas, opacity)
        newImage = Image.composite(image1 = watermark_expanded_canvas, image2= image, mask=watermark_mask)
        return newImage 
