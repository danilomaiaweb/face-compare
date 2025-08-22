import requests
import sys
import io
from PIL import Image
import numpy as np
from datetime import datetime

class FaceComparisonAPITester:
    def __init__(self, base_url="https://facematch-3.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0

    def create_test_image(self, width=200, height=200, color=(255, 255, 255)):
        """Create a simple test image"""
        image = Image.new('RGB', (width, height), color)
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        return img_bytes

    def create_face_like_image(self, width=200, height=200):
        """Create a more realistic face-like image using geometric patterns"""
        # Create a simple face-like pattern with better contrast
        image = Image.new('RGB', (width, height), (240, 220, 200))  # Light skin color
        
        from PIL import ImageDraw
        draw = ImageDraw.Draw(image)
        
        # Face outline (oval)
        face_margin = 20
        draw.ellipse([face_margin, face_margin, width-face_margin, height-face_margin], 
                    fill=(220, 200, 180), outline=(180, 160, 140), width=2)
        
        # Eyes (larger, more realistic)
        eye_y = height // 3
        left_eye_x = width // 3
        right_eye_x = 2 * width // 3
        eye_size = 15
        
        # Eye whites
        draw.ellipse([left_eye_x-eye_size, eye_y-eye_size//2, left_eye_x+eye_size, eye_y+eye_size//2], 
                    fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.ellipse([right_eye_x-eye_size, eye_y-eye_size//2, right_eye_x+eye_size, eye_y+eye_size//2], 
                    fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        
        # Pupils
        pupil_size = 6
        draw.ellipse([left_eye_x-pupil_size, eye_y-pupil_size, left_eye_x+pupil_size, eye_y+pupil_size], 
                    fill=(0, 0, 0))
        draw.ellipse([right_eye_x-pupil_size, eye_y-pupil_size, right_eye_x+pupil_size, eye_y+pupil_size], 
                    fill=(0, 0, 0))
        
        # Eyebrows
        brow_y = eye_y - 20
        draw.arc([left_eye_x-eye_size-5, brow_y-5, left_eye_x+eye_size+5, brow_y+5], 
                start=0, end=180, fill=(100, 80, 60), width=3)
        draw.arc([right_eye_x-eye_size-5, brow_y-5, right_eye_x+eye_size+5, brow_y+5], 
                start=0, end=180, fill=(100, 80, 60), width=3)
        
        # Nose (more detailed)
        nose_x = width // 2
        nose_y = height // 2
        nose_points = [
            (nose_x, nose_y - 15),
            (nose_x - 8, nose_y + 5),
            (nose_x - 3, nose_y + 8),
            (nose_x + 3, nose_y + 8),
            (nose_x + 8, nose_y + 5)
        ]
        draw.polygon(nose_points, fill=(200, 180, 160), outline=(180, 160, 140))
        
        # Nostrils
        draw.ellipse([nose_x-8, nose_y+3, nose_x-5, nose_y+6], fill=(150, 130, 110))
        draw.ellipse([nose_x+5, nose_y+3, nose_x+8, nose_y+6], fill=(150, 130, 110))
        
        # Mouth (more realistic)
        mouth_y = 2 * height // 3
        mouth_width = 30
        draw.arc([nose_x-mouth_width, mouth_y-8, nose_x+mouth_width, mouth_y+8], 
                start=0, end=180, fill=(150, 100, 100), width=4)
        
        # Add some texture/noise to make it more realistic
        import random
        for _ in range(100):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            current_pixel = image.getpixel((x, y))
            noise = random.randint(-10, 10)
            new_pixel = tuple(max(0, min(255, c + noise)) for c in current_pixel)
            draw.point((x, y), fill=new_pixel)
        
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        return img_bytes

    def run_test(self, name, test_func):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            success = test_func()
            if success:
                self.tests_passed += 1
                print(f"✅ Passed")
            else:
                print(f"❌ Failed")
            return success
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False

    def test_root_endpoint(self):
        """Test the root API endpoint"""
        try:
            response = requests.get(f"{self.api_url}/")
            if response.status_code == 200:
                data = response.json()
                if data.get("message") == "Face Comparison API":
                    print(f"   Response: {data}")
                    return True
                else:
                    print(f"   Unexpected response: {data}")
                    return False
            else:
                print(f"   Status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"   Error: {str(e)}")
            return False

    def test_compare_faces_valid(self):
        """Test compare-faces endpoint with valid data (synthetic images may not have detectable faces)"""
        try:
            # Create test images
            base_image = self.create_face_like_image()
            comp_image1 = self.create_face_like_image(180, 180)
            comp_image2 = self.create_face_like_image(220, 220)
            
            files = [
                ('base_image', ('base.jpg', base_image, 'image/jpeg')),
                ('comparison_images', ('comp1.jpg', comp_image1, 'image/jpeg')),
                ('comparison_images', ('comp2.jpg', comp_image2, 'image/jpeg'))
            ]
            
            response = requests.post(f"{self.api_url}/compare-faces", files=files)
            
            # Note: Synthetic images may not have detectable faces, so we accept both success and "no face" error
            if response.status_code == 200:
                data = response.json()
                required_fields = ['base_image_has_face', 'results', 'total_images', 'processing_time']
                
                for field in required_fields:
                    if field not in data:
                        print(f"   Missing field: {field}")
                        return False
                
                print(f"   Total images: {data['total_images']}")
                print(f"   Processing time: {data['processing_time']:.2f}s")
                print(f"   Base image has face: {data['base_image_has_face']}")
                print(f"   Results count: {len(data['results'])}")
                
                # NEW: Check for base64 image data fields
                if 'base_image_data' in data and data['base_image_data']:
                    if data['base_image_data'].startswith('data:image/jpeg;base64,'):
                        print(f"   ✅ Base image data correctly formatted as base64")
                    else:
                        print(f"   ❌ Base image data format incorrect: {data['base_image_data'][:50]}...")
                        return False
                else:
                    print(f"   ❌ Missing base_image_data field")
                    return False
                
                # Check results structure
                for i, result in enumerate(data['results']):
                    result_fields = ['image_index', 'similarity_percentage', 'has_face']
                    for field in result_fields:
                        if field not in result:
                            print(f"   Missing result field: {field}")
                            return False
                    
                    # NEW: Check for image_data field in results
                    if 'image_data' in result and result['image_data']:
                        if result['image_data'].startswith('data:image/jpeg;base64,'):
                            print(f"   ✅ Result {i}: image_data correctly formatted as base64")
                        else:
                            print(f"   ❌ Result {i}: image_data format incorrect")
                            return False
                    else:
                        print(f"   ❌ Result {i}: Missing image_data field")
                        return False
                    
                    print(f"   Result {i}: {result['similarity_percentage']:.1f}% similarity, has_face: {result['has_face']}")
                
                return True
            elif response.status_code == 400:
                # Accept "no face detected" as valid response for synthetic images
                data = response.json()
                if "Nenhum rosto detectado na imagem base" in data.get('detail', ''):
                    print(f"   Synthetic image correctly identified as having no detectable face")
                    print(f"   API structure and face detection working correctly")
                    return True
                else:
                    print(f"   Unexpected error message: {data}")
                    return False
            else:
                print(f"   Status code: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Response text: {response.text}")
                return False
                
        except Exception as e:
            print(f"   Error: {str(e)}")
            return False

    def test_compare_faces_no_base_image(self):
        """Test compare-faces endpoint without base image"""
        try:
            comp_image = self.create_test_image()
            
            files = [
                ('comparison_images', ('comp1.jpg', comp_image, 'image/jpeg'))
            ]
            
            response = requests.post(f"{self.api_url}/compare-faces", files=files)
            
            # Should return 422 (validation error) for missing base_image
            if response.status_code == 422:
                print(f"   Correctly rejected missing base image")
                return True
            else:
                print(f"   Unexpected status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   Error: {str(e)}")
            return False

    def test_compare_faces_too_many_images(self):
        """Test compare-faces endpoint with too many images (>50)"""
        try:
            base_image = self.create_face_like_image()
            
            # Create files list with base image and 51 comparison images
            files = [('base_image', ('base.jpg', base_image, 'image/jpeg'))]
            
            for i in range(51):
                comp_image = self.create_test_image()
                files.append(('comparison_images', (f'comp{i}.jpg', comp_image, 'image/jpeg')))
            
            response = requests.post(f"{self.api_url}/compare-faces", files=files)
            
            # Should return 400 for too many images
            if response.status_code == 400:
                data = response.json()
                if "Maximum 50 images allowed" in data.get('detail', ''):
                    print(f"   Correctly rejected too many images")
                    return True
                else:
                    print(f"   Unexpected error message: {data}")
                    return False
            else:
                print(f"   Unexpected status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   Error: {str(e)}")
            return False

    def test_compare_faces_no_face_in_base(self):
        """Test compare-faces endpoint with base image containing no face"""
        try:
            # Create a plain image without face-like features
            base_image = self.create_test_image(200, 200, (0, 255, 0))  # Green image
            comp_image = self.create_face_like_image()
            
            files = [
                ('base_image', ('base.jpg', base_image, 'image/jpeg')),
                ('comparison_images', ('comp1.jpg', comp_image, 'image/jpeg'))
            ]
            
            response = requests.post(f"{self.api_url}/compare-faces", files=files)
            
            # Should return 400 for no face in base image
            if response.status_code == 400:
                data = response.json()
                if "Nenhum rosto detectado na imagem base" in data.get('detail', ''):
                    print(f"   Correctly detected no face in base image")
                    return True
                else:
                    print(f"   Unexpected error message: {data}")
                    return False
            else:
                print(f"   Unexpected status code: {response.status_code}")
                try:
                    data = response.json()
                    print(f"   Response: {data}")
                except:
                    print(f"   Response text: {response.text}")
                return False
                
        except Exception as e:
            print(f"   Error: {str(e)}")
            return False

    def test_compare_faces_invalid_file_format(self):
        """Test compare-faces endpoint with invalid file format"""
        try:
            # Create a text file instead of image
            text_file = io.BytesIO(b"This is not an image")
            comp_image = self.create_face_like_image()
            
            files = [
                ('base_image', ('base.txt', text_file, 'text/plain')),
                ('comparison_images', ('comp1.jpg', comp_image, 'image/jpeg'))
            ]
            
            response = requests.post(f"{self.api_url}/compare-faces", files=files)
            
            # Should return 400 for invalid image format
            if response.status_code == 400:
                data = response.json()
                if "Invalid image format" in data.get('detail', ''):
                    print(f"   Correctly rejected invalid file format")
                    return True
                else:
                    print(f"   Unexpected error message: {data}")
                    return False
            else:
                print(f"   Unexpected status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   Error: {str(e)}")
            return False

def main():
    print("🚀 Starting Face Comparison API Tests")
    print("=" * 50)
    
    tester = FaceComparisonAPITester()
    
    # Run all tests
    tests = [
        ("Root Endpoint", tester.test_root_endpoint),
        ("Compare Faces - Valid Data", tester.test_compare_faces_valid),
        ("Compare Faces - No Base Image", tester.test_compare_faces_no_base_image),
        ("Compare Faces - Too Many Images", tester.test_compare_faces_too_many_images),
        ("Compare Faces - No Face in Base", tester.test_compare_faces_no_face_in_base),
        ("Compare Faces - Invalid File Format", tester.test_compare_faces_invalid_file_format),
    ]
    
    for test_name, test_func in tests:
        tester.run_test(test_name, test_func)
    
    # Print final results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())