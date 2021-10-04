from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import csrf
from .models import User
from .serializers import UserSerializer
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.core.files import File
from django.contrib import messages
import cv2
import face_recognition
from rest_framework.parsers import JSONParser



def camera1():
    # Camera 0 is the integrated web cam on my netbook
    camera_port = 0

    # Number of frames to throw away while the camera adjusts to light levels
    ramp_frames = 30
    # global Name
    # Fetching the name of the person
    Dir = 'H:\CodingTask\Facebook\Camera\image.jpg'

    # Now we can initialize the camera capture object with the cv2.VideoCapture class.
    # All it needs is the index to a camera port.
    camera = cv2.VideoCapture(camera_port)

    # Captures a single image from the camera and returns it in PIL format
    def get_image():
        # read is the easiest way to get a full image out of a VideoCapture object.
        retval, im = camera.read()
        return im

    # Ramp the camera - these frames will be discarded and are only used to allow v4l2
    # to adjust light levels, if necessary
    for i in range(ramp_frames):
        temp = get_image()
    print("Taking image...")
    # Take the actual image we want to keep
    camera_capture = get_image()
    file = Dir
    # A nice feature of the imwrite method is that it will automatically choose the
    # correct format based on the file extension you provide. Convenient!
    cv2.imwrite(file, camera_capture)
    # cv2.imwrite(UserProfiles.objects.create(extra_ident=id),camera_capture)

    # You'll want to release the camera, otherwise you won't be able to create a new
    # capture object until your script exits
    del camera
    return file



def facedect(loc):
    cam = cv2.VideoCapture(0)
    s, img = cam.read()
    if s:
        face_1_image = face_recognition.load_image_file(loc)
        try:
            face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]
        except:
            return "Retry"
        # face_1_face_encoding=face_1_face_encoding[0]

        #

        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        
        if len(face_encodings)>0:
            face_encodings = face_encodings[0]
            check = face_recognition.compare_faces([face_1_face_encoding], face_encodings)
            print(check)
            if check[0]:
                return True
            else:
                return False
        else:
            print("No face Found")
            quit()




@csrf_exempt
def signup(request):
    if request.method == 'GET':
        return render(request,'application/signup.html') 
    if request.method == 'POST':
        print("Method is Post")
        # if not request.user.is_authenticated:
        print("User is not authenticated")
        firstname = request.POST['firstname']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        mobile = request.POST['mobile']
        birth_date = request.POST['birth_date']
        gender = request.POST['gender']
        if gender == 'Male':
            profile = "Profile/Deadpool.jpg"
        if gender == "Female":
            profile = "Profile/wonderwoman.jpg"
        file = camera1()
        b = email.replace('gmail.com', '')
        b += "@gmail.com"
        # pydata = JSONParser().parse(request)
        # serialized_data = UserSerializer(data=pydata)
        obj = User(firstname=firstname,surname=surname,email=email,mobile=mobile,birth_date=birth_date,profile=profile,gender=gender)
        obj.set_password(password)
        obj.image.save(b + '.jpg', File(open(file, 'rb')))
        obj.save()
        messages.success(request,"Account created")
        return JsonResponse("Account Created Successfully",safe=False)
        # return render(request,'application/signup.html')
    else:
        messages.error(request,"not Created")
        return JsonResponse("Account not Created ",safe=False)
    #React    
    #return render(request,'application/signup.html')
    # return JsonResponse("Login Successfully",safe=False)        

@csrf_exempt
def signin(request):
    if request.method == 'GET':
        return render(request,'application/signup.html')
    if request.method == 'POST':
        # if not request.user.is_authenticated:
        email = request.POST['email']
        print(email)
        b1 = email.replace("@","")
        password = request.POST['password']
        print(password)
        user = authenticate(request,email=email,password=password)
        if user:
            location = 'H:\Codingtask\Facebook\Camera\DatabaseImage\DatabaseImage\\' + b1 + '.jpg'
            print(location)
            answer = facedect(location)
            if answer=="Retry":
                messages.error(request,"Captured Image is not clear Please be in light")
                #React
                #return render(request,"application/signup.html")
                return JsonResponse("Captured Image is not clear Please be in light",safe=False)

            if answer == True:
                login(request,user)
                messages.success(request,"Account created")
                #React 
                #return redirect('http://localhost:8000/homepage/')
                return JsonResponse("Successfully",safe=False)
            else:
                print("Face Not Found")
                messages.error(request,"Face Not Found")
                #React
                #return render(request, 'Facebook.html')
                return JsonResponse("Face Not Found",safe=True)
        messages.error(request,"Invalid Email or Password")
        #React
        # return render(request,"application/signup.html")
        return JsonResponse("Not a Valid Email Address Or Password",safe=True)


def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse("Successfully Logout",safe="False")
    return JsonResponse("You Need to Login First",safe="False")
    #React
    # return redirect("http://localhost:8000/")

def front(request):
    return render(request,"application/signup.html")

def homepage(request):
    if request.user.is_authenticated:
        return render(request,"application/homepage.html")
    return redirect("http://localhost:8000/")