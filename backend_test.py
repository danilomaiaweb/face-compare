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
        """Create a simple image that might contain face-like features"""
        # Create a simple face-like pattern
        image = Image.new('RGB', (width, height), (255, 220, 177))  # Skin color
        
        # Add some basic shapes that might be detected as face features
        from PIL import ImageDraw
        draw = ImageDraw.Draw(image)
        
        # Eyes (dark circles)
        draw.ellipse([60, 60, 80, 80], fill=(0, 0, 0))  # Left eye
        draw.ellipse([120, 60, 140, 80], fill=(0, 0, 0))  # Right eye
        
        # Nose (small triangle)
        draw.polygon([(100, 90), (95, 110), (105, 110)], fill=(200, 180, 150))
        
        # Mouth (small line)
        draw.rectangle([90, 130, 110, 135], fill=(150, 100, 100))
        
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
        """Test compare-faces endpoint with valid data"""
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
                
                # Check results structure
                for i, result in enumerate(data['results']):
                    result_fields = ['image_index', 'similarity_percentage', 'has_face']
                    for field in result_fields:
                        if field not in result:
                            print(f"   Missing result field: {field}")
                            return False
                    print(f"   Result {i}: {result['similarity_percentage']:.1f}% similarity, has_face: {result['has_face']}")
                
                return True
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
            
            files = {
                'base_image': ('base.jpg', base_image, 'image/jpeg'),
                'comparison_images': [('comp1.jpg', comp_image, 'image/jpeg')]
            }
            
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
            
            files = {
                'base_image': ('base.txt', text_file, 'text/plain'),
                'comparison_images': [('comp1.jpg', comp_image, 'image/jpeg')]
            }
            
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