from sorl.thumbnail.engines.pil_engine import Engine
from PIL import Image


class FixedEngine(Engine):
    def _colorspace(self, image, colorspace, format):
        if colorspace == 'RGB':
            # Pillow JPEG doesn't allow RGBA anymore. It was converted to RGB before.
            if image.mode == 'RGBA' and format != 'JPEG':
                return image  # RGBA is just RGB + Alpha
            if image.mode == 'LA' or (image.mode == 'P' and 'transparency' in image.info):
                if format == 'JPEG':
                    newimage = Image.new('RGB', image.size, 'white')
                    mask = image.convert('RGBA').split()[-1]
                    newimage.paste(image.convert('RGBA'), (0, 0), mask)
                else:
                    newimage = image.convert('RGBA')
                    transparency = image.info.get('transparency')
                    if transparency is not None:
                        mask = image.convert('RGBA').split()[-1]
                        newimage.putalpha(mask)
                return newimage
            return image.convert('RGB')
        if colorspace == 'GRAY':
            return image.convert('L')
        return image
