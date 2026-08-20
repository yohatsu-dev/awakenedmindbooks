import os
from PIL import Image, ImageDraw, ImageFilter

def create_shadow(image, offset=(10, 20), blur_radius=15, shadow_color=(0, 0, 0, 80)):
    shadow = Image.new('RGBA', image.size, shadow_color)
    
    # Create a padded image to fit the blurred shadow
    padding = blur_radius * 2 + max(abs(offset[0]), abs(offset[1]))
    padded_size = (image.size[0] + padding * 2, image.size[1] + padding * 2)
    
    shadow_img = Image.new('RGBA', padded_size, (0, 0, 0, 0))
    # Paste shadow with offset
    shadow_pos = (padding + offset[0], padding + offset[1])
    shadow_img.paste(shadow, shadow_pos)
    
    # Blur
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # Paste original image
    shadow_img.paste(image, (padding, padding))
    return shadow_img, padding

def main():
    width, height = 1200, 630
    # Background color --bg-alt: #faf9f6
    bg_color = (250, 249, 246)
    
    # Create background
    canvas = Image.new('RGBA', (width, height), bg_color)
    
    # Optional: add a subtle gradient or radial glow in the center
    # For now, just a flat color is clean and elegant.
    
    # Covers
    series_covers = [
        "assets/covers/tara-pt.jpg",
        "assets/covers/avalo-pt.jpg",
        "assets/covers/manjushri-pt.jpg",
        "assets/covers/vajra-pt.jpg",
        "assets/covers/vajrapani-pt.jpg"
    ]
    standalone_covers = [
        "assets/covers/buddha-pt.jpg",
        "assets/covers/karma-pt.jpg"
    ]
    
    target_width = 160
    target_height = int(target_width * 1.5) # 240
    
    # Calculate row 1 positions
    gap1 = 40
    total_w1 = len(series_covers) * target_width + (len(series_covers) - 1) * gap1
    start_x1 = (width - total_w1) // 2
    y1 = 65
    
    # Draw row 1
    for i, path in enumerate(series_covers):
        if not os.path.exists(path):
            print(f"Missing: {path}")
            continue
            
        img = Image.open(path).convert("RGBA")
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # add shadow
        shadowed, padding = create_shadow(img, offset=(0, 12), blur_radius=15, shadow_color=(0, 0, 0, 50))
        
        x = start_x1 + i * (target_width + gap1)
        # We must subtract padding to center the image itself at (x, y1)
        canvas.paste(shadowed, (x - padding, y1 - padding), shadowed)

    # Calculate row 2 positions
    gap2 = 80
    total_w2 = len(standalone_covers) * target_width + (len(standalone_covers) - 1) * gap2
    start_x2 = (width - total_w2) // 2
    y2 = y1 + target_height + 50
    
    # Draw row 2
    for i, path in enumerate(standalone_covers):
        if not os.path.exists(path):
            print(f"Missing: {path}")
            continue
            
        img = Image.open(path).convert("RGBA")
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        shadowed, padding = create_shadow(img, offset=(0, 12), blur_radius=15, shadow_color=(0, 0, 0, 50))
        
        x = start_x2 + i * (target_width + gap2)
        canvas.paste(shadowed, (x - padding, y2 - padding), shadowed)
        
    # Convert to RGB and save
    out_img = canvas.convert('RGB')
    out_img.save("assets/social-share.jpg", quality=90)
    print("Created assets/social-share.jpg successfully.")

if __name__ == '__main__':
    main()
